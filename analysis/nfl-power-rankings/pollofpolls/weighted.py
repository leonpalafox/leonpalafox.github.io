"""A second opinion on each game that blends power rankings with records.

The head-to-head model in :mod:`pollofpolls.headtohead` prices a game from the
consensus score alone. That score is an opinion about quality, and it
deliberately discounts raw results -- which is why a 5-0 Minnesota can sit sixth.
This module asks what happens if you weight the two signals together, and how
much weight the record deserves.

Three models, all on the same margin scale in points:

* ``rank``  -- ``k * (z_home - z_away) + home_field``, the fitted constants from
  §9 of METHODOLOGY.md.
* ``rec``   -- ``k_rec * (win_pct_home - win_pct_away) + home_field_rec``, fitted
  here on the same historical game log, so the record carries its own weight
  rather than an assumed one.
* ``blend`` -- ``w * rank + (1 - w) * rec``, with ``w`` **fitted by out-of-sample
  log-loss**, not chosen.

The evaluation is genuinely ex-ante. Each weekly consensus bundle is published
before that week's games are played, and the record it carries is the standing
entering the week, so every prediction below was made with only pre-game
information. The weight is fitted on the weeks that have been played and applied
to the coming week.
"""

from __future__ import annotations

import csv
import io
import math
import statistics

from . import games, headtohead

# Weeks whose games are complete and for which an ex-ante bundle exists.
EVAL_WEEKS = (3, 4, 5)


def _normal_cdf(x: float) -> float:
    return headtohead.normal_cdf(x)


def win_pct(record: str) -> float:
    """Winning percentage, ties counting as half a win."""
    parts = [int(p) for p in record.split("-") if p != ""]
    if len(parts) == 2:
        wins, losses, ties = parts[0], parts[1], 0
    elif len(parts) == 3:
        wins, losses, ties = parts
    else:
        return 0.5
    played = wins + losses + ties
    return 0.5 if played == 0 else (wins + 0.5 * ties) / played


# The head-to-head constants were fitted on 2000-2025. The record model is
# fitted on the same window so the two log-losses are comparable rather than
# being measured on different eras.
FIT_SEASONS = tuple(range(2000, 2026))


def _pct_from_state(state: list[int]) -> float:
    """Winning percentage from a running [wins, losses, ties] tally.

    A team that has not played is 0.500, not 0.000. Scoring it 0.000 would make
    an opening-week win look like a full game's worth of edge over a team that
    had not played, and it disagreed with :func:`win_pct` on the same input.
    """
    wins, losses, ties = state
    played = wins + losses + ties
    return 0.5 if played == 0 else (wins + 0.5 * ties) / played


def _canonical(raw: str) -> str:
    """Canonical team name when the code is current, otherwise the raw code.

    Historical codes for relocated franchises (OAK, SD, STL) are not in the
    current team map. Resolving is only needed to match a name against a
    consensus bundle, so an unresolvable code falls back to itself rather than
    dropping the game -- dropping them cost 805 of 6,719 observations when this
    keyed on resolved names.
    """
    try:
        return games._resolve(raw)
    except Exception:
        return raw


def _running_records(csv_text: str) -> list[dict]:
    """Every completed regular-season game with each side's record *entering* it.

    The walking state is keyed on (season, raw team code), so a record never
    leaks across seasons or from the game being predicted, and a relocated
    franchise is tracked under the code it played under.
    """
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    rows.sort(key=lambda r: (r.get("season", ""), int(r.get("week") or 0), r.get("gameday", "")))

    state: dict[tuple[str, str], list[int]] = {}
    out: list[dict] = []
    for row in rows:
        if row.get("game_type") != "REG":
            continue
        home_score, away_score = games._to_int(row.get("home_score")), games._to_int(row.get("away_score"))
        if home_score is None or away_score is None:
            continue
        season = row.get("season", "")
        raw_home, raw_away = row["home_team"], row["away_team"]

        h_state = state.setdefault((season, raw_home), [0, 0, 0])
        a_state = state.setdefault((season, raw_away), [0, 0, 0])
        h_pct = _pct_from_state(h_state)
        a_pct = _pct_from_state(a_state)

        out.append({
            "season": season,
            "week": int(row.get("week") or 0),
            "home": _canonical(raw_home), "away": _canonical(raw_away),
            "homeScore": home_score, "awayScore": away_score,
            "margin": home_score - away_score,
            "homePct": h_pct, "awayPct": a_pct,
        })

        if home_score > away_score:
            h_state[0] += 1; a_state[1] += 1
        elif away_score > home_score:
            a_state[0] += 1; h_state[1] += 1
        else:
            h_state[2] += 1; a_state[2] += 1
    return out


def fit_record_model(csv_text: str, *, seasons: tuple[int, ...] | None = FIT_SEASONS) -> dict:
    """Least-squares fit of margin on the difference in winning percentage.

    One predictor plus an intercept, so the closed form is exact rather than
    iterated:  margin = k * (pct_home - pct_away) + home_field.
    """
    obs = _running_records(csv_text)
    if seasons is not None:
        wanted = {str(y) for y in seasons}
        obs = [o for o in obs if o["season"] in wanted]
    xs = [o["homePct"] - o["awayPct"] for o in obs]
    ys = [float(o["margin"]) for o in obs]
    n = len(xs)
    mean_x, mean_y = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mean_x) ** 2 for x in xs)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    k = sxy / sxx
    home_field = mean_y - k * mean_x

    residuals = [y - (k * x + home_field) for x, y in zip(xs, ys)]
    sigma = math.sqrt(sum(r * r for r in residuals) / (n - 2))

    losses = []
    for obs_row, x, y in zip(obs, xs, ys):
        p_home = _normal_cdf((k * x + home_field) / sigma)
        p = min(max(p_home, 1e-9), 1 - 1e-9)
        losses.append(-math.log(p if y > 0 else 1 - p))
    # Ties are vanishingly rare; score them as half a win to each side.
    log_loss = sum(losses) / n

    return {
        "k": k, "homeField": home_field, "sigma": sigma,
        "nGames": n, "logLoss": log_loss,
        "source": "least squares on the same game log as the head-to-head fit",
    }


def _bundle_probs(bundle: dict) -> dict[str, dict]:
    """Per-team score and win percentage from one weekly consensus bundle."""
    out = {}
    for team in bundle["teams"]:
        out[team["team"]] = {"score": team["score"], "pct": win_pct(team.get("record") or "0-0")}
    return out


def _weekly_games(csv_text: str, season: int, week: int) -> list[dict]:
    obs = _running_records(csv_text)
    return [o for o in obs if o["season"] == str(season) and o["week"] == week]


def _margins_for(obs, ranks, rec_model, rank_model):
    """(rank margin, record margin) or None when a team is missing."""
    h, a = ranks.get(obs["home"]), ranks.get(obs["away"])
    if h is None or a is None:
        return None
    return (
        rank_model.k * (h["score"] - a["score"]) + rank_model.home_field,
        rec_model["k"] * (obs["homePct"] - obs["awayPct"]) + rec_model["homeField"],
    )


def standardisers(margins_rank: list[float], margins_rec: list[float]) -> tuple[float, float]:
    """Per-signal spreads used to put both on the same footing before mixing.

    The blend mixes *standardised* margins. Mixing raw ones gives the record far
    more influence than the weight implies, because k_rec is more than twice
    k_rank; measured against the real bracket, every weight below about 0.55
    reproduced the records-only seeding.
    """
    sd_rank = statistics.pstdev(margins_rank) or 1.0
    sd_rec = statistics.pstdev(margins_rec) or 1.0
    return sd_rank, sd_rec


def blend_margin(
    margin_rank: float,
    margin_rec: float,
    weight: float,
    *,
    scale: float,
    sd_rank: float,
    sd_rec: float,
) -> float:
    """The blended margin in points, standardising each signal first."""
    return scale * (
        weight * (margin_rank / sd_rank) + (1.0 - weight) * (margin_rec / sd_rec)
    )


def _log_loss(pairs) -> float:
    """Mean log-loss over (probability, actual home win) pairs."""
    total = 0.0
    for p, won in pairs:
        p = min(max(p, 1e-9), 1 - 1e-9)
        total += -math.log(p if won else 1 - p)
    return total / len(pairs)


def evaluate(
    *,
    csv_text: str,
    season: int,
    bundles: dict[int, dict],
    weeks: tuple[int, ...] = EVAL_WEEKS,
    weight: float = 0.5,
    sigma: float = headtohead.DEFAULT_MODEL.sigma,
) -> dict:
    """Score all three models on the completed weeks that have ex-ante bundles."""
    rec_model = fit_record_model(csv_text)
    rank_model = headtohead.DEFAULT_MODEL

    graded = []
    for week in weeks:
        bundle = bundles.get(week)
        if bundle is None:
            continue
        ranks = _bundle_probs(bundle)
        for obs in _weekly_games(csv_text, season, week):
            margins = _margins_for(obs, ranks, rec_model, rank_model)
            if margins is None:
                continue
            graded.append({**obs, "marginRank": margins[0], "marginRec": margins[1]})

    if not graded:
        return {"nEval": 0, "recordModel": rec_model}

    sd_rank, sd_rec = standardisers(
        [g["marginRank"] for g in graded], [g["marginRec"] for g in graded]
    )
    for g in graded:
        g["marginBlend"] = blend_margin(
            g["marginRank"], g["marginRec"], weight,
            scale=rank_model.k, sd_rank=sd_rank, sd_rec=sd_rec,
        )
        g["pRank"] = _normal_cdf(g["marginRank"] / rank_model.sigma)
        g["pRec"] = _normal_cdf(g["marginRec"] / rec_model["sigma"])
        g["pBlend"] = _normal_cdf(g["marginBlend"] / sigma)

    pairs_rank = [(g["pRank"], g["margin"] > 0) for g in graded]
    pairs_rec = [(g["pRec"], g["margin"] > 0) for g in graded]
    pairs_blend = [(g["pBlend"], g["margin"] > 0) for g in graded]

    return {
        "nEval": len(graded),
        "weeks": list(weeks),
        "recordModel": rec_model,
        "logLoss": {
            "rankingsOnly": _log_loss(pairs_rank),
            "recordsOnly": _log_loss(pairs_rec),
            "blend": _log_loss(pairs_blend),
            "coinFlip": math.log(2),
        },
        "games": graded,
    }


def fit_blend(
    *,
    csv_text: str,
    season: int,
    bundles: dict[int, dict],
    weeks: tuple[int, ...] = EVAL_WEEKS,
    sigma: float = headtohead.DEFAULT_MODEL.sigma,
) -> dict:
    """Find the weight on the rankings that minimises out-of-sample log-loss.

    ``w = 1`` is rankings-only and ``w = 0`` is records-only, so the fitted value
    is directly interpretable and the endpoints double as the two baselines.
    """
    rec_model = fit_record_model(csv_text)
    rank_model = headtohead.DEFAULT_MODEL

    # Assemble the outcome and each model's margin once.
    frames = []
    for week in weeks:
        bundle = bundles.get(week)
        if bundle is None:
            continue
        ranks = _bundle_probs(bundle)
        for obs in _weekly_games(csv_text, season, week):
            h, a = ranks.get(obs["home"]), ranks.get(obs["away"])
            if h is None or a is None:
                continue
            frames.append({
                "marginRank": rank_model.k * (h["score"] - a["score"]) + rank_model.home_field,
                "marginRec": rec_model["k"] * (obs["homePct"] - obs["awayPct"]) + rec_model["homeField"],
                "homeWon": obs["margin"] > 0,
            })
    if not frames:
        return {"weight": None, "nEval": 0}

    # One definition of the blend, shared with evaluate() and the simulation.
    sd_rank, sd_rec = standardisers(
        [f["marginRank"] for f in frames], [f["marginRec"] for f in frames]
    )

    def blended_margin(f, w):
        return blend_margin(
            f["marginRank"], f["marginRec"], w,
            scale=rank_model.k, sd_rank=sd_rank, sd_rec=sd_rec,
        )

    curve = []
    best = None          # unregularised argmin, kept only for reporting
    best_map = None      # what the pipeline actually uses
    # A 2-D sweep: the weight on the rankings, and the margin dispersion, since a
    # blended margin has its own spread and the rank model's sigma need not suit it.
    sigmas = [9.0 + 0.25 * i for i in range(0, 37)]          # 9.0 .. 18.0
    for w_int in range(0, 101):
        w = w_int / 100.0
        margins = [blended_margin(f, w) for f in frames]
        # A weak Beta(2,2) prior on the weight, centred at an even split. With ~45
        # games the likelihood is flat enough that the unregularised argmin jumps
        # between the two boundaries from week to week -- it gave 0.51 on weeks
        # 3-5 and 1.00 on weeks 4-6 -- and a boundary value silently discards one
        # of the two signals the model exists to combine. The prior is worth one
        # pseudo-observation per side, so it regularises without overruling data
        # that actually discriminates.
        prior = math.log(w) + math.log(1.0 - w) if 0.0 < w < 1.0 else -math.inf
        for s in sigmas:
            pairs = [(_normal_cdf(m / s), f["homeWon"]) for m, f in zip(margins, frames)]
            loss = _log_loss(pairs)
            if best is None or loss < best["logLoss"]:
                best = {"weight": w, "sigma": s, "logLoss": loss}
            penalised = loss - prior / len(frames)
            if best_map is None or penalised < best_map["penalised"]:
                best_map = {"weight": w, "sigma": s, "logLoss": loss, "penalised": penalised}
        # record the curve at the rank model's own sigma so the x-axis is honest
        pairs = [(_normal_cdf(m / sigma), f["homeWon"]) for m, f in zip(margins, frames)]
        curve.append({"weight": w, "logLoss": _log_loss(pairs)})

    # How well does 47 games actually pin the weight down? A 95% profile
    # interval comes from the deviance: 2n(loss - loss_min) ~ chi2(1), so accept
    # every weight whose loss is within 1.92/n of the best on the curve. If that
    # spans [0, 1], the data cannot distinguish the two signals at all, which is
    # the honest headline for a single season.
    min_curve = min(point["logLoss"] for point in curve)
    threshold = min_curve + 1.92 / len(frames)
    accepted = [point["weight"] for point in curve if point["logLoss"] <= threshold]
    weight_interval = [min(accepted), max(accepted)]

    # Baselines at the fitted sigma, for a like-for-like comparison.
    def loss_at(w, s):
        margins = [blended_margin(f, w) for f in frames]
        pairs = [(_normal_cdf(m / s), f["homeWon"]) for m, f in zip(margins, frames)]
        return _log_loss(pairs)

    # Cross-check the fitted weight against precision weighting: if the two
    # models' errors were independent, the optimal weight on each is proportional
    # to the inverse of its residual variance. They are not independent -- both
    # read the same teams -- so this is a sanity check, not a second estimator.
    rank_var = rank_model.sigma ** 2
    rec_var = rec_model["sigma"] ** 2
    precision_weight = (1.0 / rank_var) / ((1.0 / rank_var) + (1.0 / rec_var))

    return {
        "weight": best_map["weight"],
        "weightUnregularised": best["weight"],
        "precisionWeight": precision_weight,
        "sigma": best_map["sigma"],
        "logLoss": best_map["logLoss"],
        "logLossUnregularised": best["logLoss"],
        "prior": "Beta(2,2) on the weight, centred at an even split",
        "nEval": len(frames),
        "weeks": list(weeks),
        "recordModel": rec_model,
        "rankModel": {
            "k": rank_model.k, "homeField": rank_model.home_field,
            "sigma": rank_model.sigma, "nGames": rank_model.n_games,
        },
        "curve": curve,
        "weightInterval": weight_interval,
        "weightUndetermined": weight_interval[0] <= 0.0 and weight_interval[1] >= 1.0,
        "atFittedSigma": {
            "rankingsOnly": loss_at(1.0, best["sigma"]),
            "recordsOnly": loss_at(0.0, best["sigma"]),
            "blend": best["logLoss"],
            "coinFlip": math.log(2),
        },
    }


def predict_games(
    *,
    csv_text: str,
    season: int,
    week: int,
    bundle: dict,
    weight: float,
    sigma: float,
    record_model: dict,
) -> list[dict]:
    """Price one week's slate under both the rankings and the blend."""
    rank_model = headtohead.DEFAULT_MODEL
    ranks = _bundle_probs(bundle)
    slate = [g for g in games.parse_nflverse_games(csv_text, season=season, week=week)
             if g.home_score is None]
    if not slate:
        # Nothing scheduled (or all played): fall back to the raw week slice.
        return []

    out = []
    for game in slate:
        h, a = ranks.get(game.home), ranks.get(game.away)
        if h is None or a is None:
            continue
        h_pct = win_pct(bundle_team(bundle, game.home))
        a_pct = win_pct(bundle_team(bundle, game.away))
        m_rank = rank_model.k * (h["score"] - a["score"]) + rank_model.home_field
        m_rec = record_model["k"] * (h_pct - a_pct) + record_model["homeField"]
        m_blend = weight * m_rank + (1 - weight) * m_rec
        p_rank = _normal_cdf(m_rank / rank_model.sigma)
        p_blend = _normal_cdf(m_blend / sigma)
        out.append({
            "week": week,
            "home": game.home, "away": game.away,
            "homePct": h_pct, "awayPct": a_pct,
            "marginRank": m_rank, "marginRec": m_rec, "marginBlend": m_blend,
            "pRank": p_rank, "pBlend": p_blend,
            "pickRank": game.home if p_rank >= 0.5 else game.away,
            "pickBlend": game.home if p_blend >= 0.5 else game.away,
            "agrees": (p_rank >= 0.5) == (p_blend >= 0.5),
            "flip": abs(p_blend - p_rank),
        })
    return out


def bundle_team(bundle: dict, team: str) -> str:
    """The record string a bundle holds for a team (empty when absent)."""
    for entry in bundle["teams"]:
        if entry["team"] == team:
            return entry.get("record") or "0-0"
    return "0-0"
