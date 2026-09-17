"""Statistical core of the poll-of-polls.

This module is deliberately dependency-free (standard library only) so the
whole analysis is reproducible on any machine with Python 3.10+, and so the
estimator can be unit-tested without a scientific stack.

The model
---------
Let ``r[s][t]`` be the rank (1..N) that source ``s`` gives team ``t``, with N
teams. Two sources can use the same ordinal scale but still differ in how
tightly they cluster teams, so each source's ranks are standardised before
pooling::

    z[s][t] = (mu_s - r[s][t]) / sd_s

where ``mu_s = (N+1)/2`` and ``sd_s = sqrt((N^2 - 1)/12)`` are the mean and
standard deviation of a uniform 1..N permutation. ``z`` is therefore
source-centred, measured in "rank standard deviations", and **positive is
better** (rank 1 maps to the largest z). Because a uniform permutation fixes
``mu_s`` and ``sd_s`` analytically, no source can gain influence merely by
using a wider or narrower spread.

Pooling then treats each source as a replicate measurement in a one-way random
effects model::

    z[s][t] = theta[t] + e[s][t],   e ~ (0, sigma_w^2)

The between-team variance of the observed means is inflated by the within-team
sampling variance, so variance components are estimated by ANOVA::

    sigma_w^2 = MSW                       (within-team mean square)
    sigma_b^2 = max(0, (MSB - MSW) / S)   (between-team, deconvolved)

and each team's pooled score is shrunk toward the grand mean by the resulting
reliability factor ``lambda = sigma_b^2 / (sigma_b^2 + sigma_w^2 / S)``::

    theta_hat[t] = grand_mean + lambda * (mean_s z[s][t] - grand_mean)
    se[t]        = sqrt(sigma_b^2 * (1 - lambda))

This is the James-Stein / empirical-Bayes estimator: it is the posterior mean
under a normal prior, it dominates the raw mean on squared-error loss, and it
keeps a team that one outlet loves but nobody else does from jumping the
consensus. The unshrunk weighted mean is retained alongside it for audit.

Uncertainty has two distinct sources and both are reported:

*   **Source disagreement** (``se``, from the model above) - how much the
    outlets actually disagree about a team. This is a property of the panel,
    not a sampling statistic: if five outlets all say the same thing, the
    consensus is precise about *what the panel thinks*, which is not the same
    as being right.
*   **Resampling variability** (bootstrap over sources) - how much the ordering
    would move if a different five outlets had been sampled. This drives the
    rank intervals.

Because panelists read each other and share priors, sources are positively
correlated, so the effective number of independent sources is below S. The
Spearman-Brown reliability estimate and the pairwise correlation matrix in the
report quantify exactly that; the bootstrap deliberately treats sources as
exchangeable and should be read as a lower bound on uncertainty.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

# --- descriptive statistics ------------------------------------------------


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def sample_sd(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    mu = mean(values)
    return math.sqrt(sum((v - mu) ** 2 for v in values) / (n - 1))


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = mean(xs), mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    syy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sxx == 0 or syy == 0:
        return float("nan")
    return sxy / (sxx * syy)


def _rankdata(values: list[float]) -> list[float]:
    """Average ranks (1-based), so ties get the mean of the tied positions."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        average = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = average
        i = j + 1
    return ranks


def spearman(xs: list[float], ys: list[float]) -> float:
    return pearson(_rankdata(xs), _rankdata(ys))


def percentile(sorted_values: list[float], q: float) -> float:
    """Linear-interpolation percentile; q in [0, 1]."""
    if not sorted_values:
        return float("nan")
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = q * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def median(values: list[float]) -> float:
    return percentile(sorted(values), 0.5)


# --- panel geometry --------------------------------------------------------

# Mean and standard deviation of a uniform 1..N permutation. Exact, not
# estimated, so standardisation never leaks information about a source's
# actual ballot.
def uniform_rank_mean(n: int) -> float:
    return (n + 1) / 2


def uniform_rank_sd(n: int) -> float:
    return math.sqrt((n * n - 1) / 12)


@dataclass
class Panel:
    """A rectangular source x team rank matrix with metadata."""

    teams: list[str]
    ballots: dict[str, dict[str, int]]  # source_id -> {team: rank}
    meta: dict[str, dict] = field(default_factory=dict)  # source_id -> metadata

    @property
    def n_teams(self) -> int:
        return len(self.teams)

    @property
    def sources(self) -> list[str]:
        return list(self.ballots)

    def matrix(self, *, require_complete: bool = True) -> dict[str, list[float]]:
        """Return {source: [rank per self.teams]}.

        With require_complete=True a source missing any team is dropped, so the
        ANOVA variance decomposition stays balanced and no team's score depends
        on which other teams a source chose to omit.
        """
        out: dict[str, list[float]] = {}
        for source, ballot in self.ballots.items():
            if require_complete and any(team not in ballot for team in self.teams):
                continue
            out[source] = [float(ballot.get(team, float("nan"))) for team in self.teams]
        return out

    def to_matrix_csv(self) -> str:
        rows = ["team," + ",".join(self.ballots)]
        for team in self.teams:
            cells = [str(self.ballots[s].get(team, "")) for s in self.ballots]
            rows.append(",".join([team] + cells))
        return "\n".join(rows) + "\n"


# --- the estimator ---------------------------------------------------------


@dataclass
class ConsensusRow:
    team: str
    rank: int
    score: float  # shrunk z-score, positive is better
    score_raw: float  # unshrunk weighted z-score mean
    se: float  # model standard error of the score
    ci_low: float  # 95% interval on the z scale
    ci_high: float
    mean_rank: float
    median_rank: float
    rank_sd: float
    rank_min: int
    rank_max: int
    rank_ci_low: int  # 95% bootstrap rank interval
    rank_ci_high: int
    p_top1: float  # bootstrap share of #1 finishes
    p_top5: float
    n_sources: int
    spread: int  # rank_max - rank_min
    by_source: dict[str, int] = field(default_factory=dict)


@dataclass
class Diagnostics:
    n_sources: int
    n_teams: int
    within_variance: float  # sigma_w^2
    between_variance: float  # sigma_b^2
    reliability: float  # lambda
    effective_sources: float  # independent-source count implied by split-half rho
    grand_mean: float
    mean_pairwise_spearman: float
    split_half_spearman: float
    split_half_reliability: float  # Spearman-Brown corrected
    consensus_by_division: dict[str, list[str]]
    most_contested: list[tuple[str, int]]
    least_contested: list[tuple[str, int]]


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    total = sum(weights)
    if total <= 0:
        return mean(values)
    return sum(v * w for v, w in zip(values, weights)) / total


def build_panel(
    ballots: dict[str, dict[str, int]],
    meta: dict[str, dict] | None = None,
    *,
    teams: list[str] | None = None,
) -> Panel:
    if teams is None:
        teams = sorted({team for ballot in ballots.values() for team in ballot})
    return Panel(teams=teams, ballots=ballots, meta=meta or {})


def consensus(
    panel: Panel,
    *,
    prior_weights: dict[str, float] | None = None,
    bootstrap: int = 4000,
    seed: int = 20260917,
    ci: float = 0.95,
) -> tuple[list[ConsensusRow], Diagnostics]:
    """Estimate the consensus ranking, its uncertainty, and panel diagnostics."""
    matrix = panel.matrix(require_complete=True)
    if len(matrix) < 2:
        raise ValueError("need at least two complete ballots to build a consensus")

    teams = panel.teams
    n = len(teams)
    sources = list(matrix)
    s_count = len(sources)
    prior_weights = prior_weights or {}

    mu = uniform_rank_mean(n)
    sd = uniform_rank_sd(n)

    # Standardise each source: z = (mu - rank) / sd  (positive = better).
    z: dict[str, list[float]] = {
        source: [(mu - rank) / sd for rank in matrix[source]] for source in sources
    }

    raw_weights = {source: max(0.0, prior_weights.get(source, 1.0)) for source in sources}
    if sum(raw_weights.values()) <= 0:
        raw_weights = {source: 1.0 for source in sources}
    weight_vector = [raw_weights[s] for s in sources]

    def pooled(i: int, subset: list[str] | None = None) -> float:
        """Prior-weighted mean z-score for team i, optionally over a subset."""
        if subset is None:
            return _weighted_mean([z[s][i] for s in sources], weight_vector)
        weights = [raw_weights[s] for s in subset]
        return _weighted_mean([z[s][i] for s in subset], weights)

    # --- uncertainty -----------------------------------------------------
    # Uncertainty about a team's score is measured by how much the answer moves
    # when one outlet is dropped. The jackknife is exact for a mean, needs no
    # distributional assumption, and is computed per team, so a club the panel
    # argues about gets a wide interval and a club everyone agrees on gets a
    # narrow one.
    group_means = [pooled(i) for i in range(n)]
    jackknife_var: list[float] = []
    for i in range(n):
        leave_one_out = [pooled(i, [s for s in sources if s != dropped]) for dropped in sources]
        centre = mean(leave_one_out)
        jackknife_var.append(
            (s_count - 1) / s_count * sum((v - centre) ** 2 for v in leave_one_out)
        )
    mean_jackknife_var = mean(jackknife_var)

    # --- empirical-Bayes shrinkage ---------------------------------------
    # Prior variance of true team quality: observed spread of the pooled means
    # minus the estimation noise already baked into them. This is the method of
    # moments variance decomposition of a measurement-error model, computed
    # directly from the jackknife variances so it never assumes homoscedasticity
    # across teams.
    grand = mean(group_means)
    observed_var = sample_sd(group_means) ** 2
    tau2 = max(0.0, observed_var - mean_jackknife_var)
    shrink = tau2 / (tau2 + mean_jackknife_var) if (tau2 + mean_jackknife_var) > 0 else 0.0

    scores = [grand + shrink * (gm - grand) for gm in group_means]
    # Posterior variance, split into the irreducible part (the panel could have
    # been a different set of outlets) and the sampling part (this particular
    # panel's noise). The jackknife already reflects correlated panelists, so
    # neither term is divided by the raw source count again - that would
    # double-count the correction. The small effective sample size is instead
    # charged through the Student-t critical value below.
    between_component = tau2 * (1.0 - shrink)
    within_component = [shrink * v for v in jackknife_var]

    # Ordering: shrunk score desc, then pooled z, then name so the sort is
    # deterministic even when two teams tie to machine precision. Because the
    # shrinkage is affine, this is the same order as the pooled z-score.
    order = sorted(range(n), key=lambda i: (-scores[i], -group_means[i], teams[i]))
    rank_of = {i: position + 1 for position, i in enumerate(order)}

    # Diagnostics first: it owns the split-half correlation, which yields the
    # effective number of independent sources and therefore how much the
    # jackknife standard errors must be inflated.
    diagnostics = _diagnose(
        panel, matrix, sources, teams, mean_jackknife_var, tau2, shrink, grand, seed
    )
    effective_sources = max(1.0, diagnostics.effective_sources)
    # Each team's score standard error: the irreducible panel-to-panel term plus
    # the sampling term divided by the effective (not raw) number of sources.
    ses = [math.sqrt(max(0.0, between_component + within_component[i])) for i in range(n)]
    t_ci = _t_quantile(1 - (1 - ci) / 2, max(1.0, effective_sources - 1))

    # Bootstrap over sources: resample the panel with replacement.
    rng = random.Random(seed)
    boot_ranks: list[list[int]] = []
    boot_top1 = [0] * n
    boot_top5 = [0] * n
    for _ in range(bootstrap):
        draw = [rng.randrange(s_count) for _ in range(s_count)]
        means = [
            mean([z[sources[d]][i] for d in draw]) for i in range(n)
        ]
        boot_order = sorted(range(n), key=lambda i: (-means[i], teams[i]))
        positions = [0] * n
        for position, index in enumerate(boot_order):
            positions[index] = position + 1
            if position == 0:
                boot_top1[index] += 1
            if position < 5:
                boot_top5[index] += 1
        boot_ranks.append(positions)

    rows: list[ConsensusRow] = []
    for i, team in enumerate(teams):
        ranks = [ballot[team] for ballot in panel.ballots.values() if team in ballot]
        boot_col = sorted(boot_ranks[j][i] for j in range(bootstrap))
        lower = percentile(boot_col, (1 - ci) / 2)
        upper = percentile(boot_col, 1 - (1 - ci) / 2)
        rows.append(
            ConsensusRow(
                team=team,
                rank=rank_of[i],
                score=scores[i],
                score_raw=group_means[i],
                se=ses[i],
                ci_low=scores[i] - t_ci * ses[i],
                ci_high=scores[i] + t_ci * ses[i],
                mean_rank=mean(ranks),
                median_rank=median(ranks),
                rank_sd=sample_sd(ranks) if len(ranks) > 1 else 0.0,
                rank_min=int(min(ranks)) if ranks else 0,
                rank_max=int(max(ranks)) if ranks else 0,
                rank_ci_low=int(round(lower)),
                rank_ci_high=int(round(upper)),
                p_top1=boot_top1[i] / bootstrap,
                p_top5=boot_top5[i] / bootstrap,
                n_sources=len(ranks),
                spread=int(max(ranks) - min(ranks)) if ranks else 0,
                by_source={s: panel.ballots[s][team] for s in panel.ballots if team in panel.ballots[s]},
            )
        )
    rows.sort(key=lambda row: row.rank)
    return rows, diagnostics


def _normal_quantile(p: float) -> float:
    """Acklam's rational approximation to the standard normal quantile."""
    a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
    b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (
        ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1
    )


def _t_quantile(p: float, df: float) -> float:
    """Student-t quantile via the Cornish-Fisher expansion from the normal.

    Accurate to a few thousandths for df >= 3, which is the range a panel this
    size ever occupies (df = effective sources - 1). Keeps the module free of
    SciPy while still charging the right price for a small panel.
    """
    z = _normal_quantile(p)
    g1 = (z ** 3 + z) / 4.0
    g2 = (5 * z ** 5 + 16 * z ** 3 + 3 * z) / 96.0
    g3 = (3 * z ** 7 + 19 * z ** 5 + 17 * z ** 3 - 15 * z) / 384.0
    g4 = (79 * z ** 9 + 776 * z ** 7 + 1482 * z ** 5 - 1920 * z ** 3 - 945 * z) / 92160.0
    if df <= 0:
        return z
    return z + g1 / df + g2 / df ** 2 + g3 / df ** 3 + g4 / df ** 4


def _diagnose(
    panel: Panel,
    matrix: dict[str, list[float]],
    sources: list[str],
    teams: list[str],
    sigma_w2: float,
    sigma_b2: float,
    lam: float,
    grand: float,
    seed: int,
) -> Diagnostics:
    n = len(teams)  # noqa: F841 - kept for symmetry with future diagnostics

    # Pairwise Spearman between source ballots.
    pairwise: list[float] = []
    for i, a in enumerate(sources):
        for b in sources[i + 1:]:
            rho = spearman(matrix[a], matrix[b])
            if not math.isnan(rho):
                pairwise.append(rho)

    # Split-half reliability: split the panel at random, consensus each half,
    # correlate, then apply the Spearman-Brown prophecy formula to project the
    # reliability of the full panel. Averaged over 200 random splits with a
    # fixed seed so the number is reproducible.
    rng = random.Random(seed)
    corrected: list[float] = []
    for _ in range(200):
        if len(sources) < 4:
            break
        shuffled = sources[:]
        rng.shuffle(shuffled)
        half = len(shuffled) // 2
        halves = [shuffled[:half], shuffled[half:]]
        series = []
        for group in halves:
            if len(group) < 2:
                continue
            series.append([mean([matrix[s][i] for s in group]) for i in range(n)])
        if len(series) == 2:
            rho = spearman(series[0], series[1])
            if not math.isnan(rho) and rho > -1:
                corrected.append(2 * rho / (1 + rho))

    spread = sorted(
        (
            (team, int(max(panel.ballots[s][team] for s in panel.ballots if team in panel.ballots[s]))
             - int(min(panel.ballots[s][team] for s in panel.ballots if team in panel.ballots[s])))
            for team in teams
        ),
        key=lambda pair: (-pair[1], pair[0]),
    )

    by_division: dict[str, list[tuple[float, str]]] = {}
    score_of = {
        team: mean([matrix[s][i] for s in sources]) for i, team in enumerate(teams)
    }
    for team in teams:
        conf, div = _division(team)
        by_division.setdefault(f"{conf} {div}", []).append((score_of[team], team))
    division_order = {
        key: [team for _, team in sorted(values, key=lambda pair: (-pair[0], pair[1]))]
        for key, values in by_division.items()
    }

    # Effective number of independent sources. The split-half correlation rho
    # is estimated on S/2 sources per half, so the Spearman-Brown step-up for a
    # half-length panel is 2*rho/(1+rho); inverting the same formula recovers
    # how many independent sources would reproduce that reliability.
    half = len(sources) / 2
    if corrected and math.isfinite(corrected[-1]):
        half_rho = mean(corrected)
        reliability_full = min(0.999, max(0.0, half_rho))
        effective = half * reliability_full / max(1e-9, 1 - reliability_full)
        effective_sources = min(float(len(sources)), max(1.0, effective))
    else:
        effective_sources = float(len(sources))

    return Diagnostics(
        n_sources=len(sources),
        n_teams=n,
        within_variance=sigma_w2,
        between_variance=sigma_b2,
        reliability=lam,
        effective_sources=effective_sources,
        grand_mean=grand,
        mean_pairwise_spearman=mean(pairwise) if pairwise else float("nan"),
        split_half_spearman=mean(corrected) if corrected else float("nan"),
        split_half_reliability=mean(corrected) if corrected else float("nan"),
        consensus_by_division=division_order,
        most_contested=spread[:5],
        least_contested=spread[-5:][::-1],
    )


def _division(team: str) -> tuple[str, str]:
    from .teams import TEAMS

    _, conf, div = TEAMS[team]
    return conf, div
