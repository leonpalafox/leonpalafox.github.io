# Methodology

The estimator behind the NFL poll of polls. Written to be read alongside
`pollofpolls/stats.py`, which implements exactly this and nothing else.

The short version: **standardise each ballot, pool the panel in a
measurement-error model, shrink toward the panel mean, and report two different
kinds of uncertainty honestly.** The rest of this document is why each of those
choices was made and what it costs.

---

## 1. The problem with averaging ranks

Suppose five outlets rank 32 teams. The obvious move is to average each team's
five ranks and sort. It is also wrong in three specific ways.

1. **Ranks are not interval-scaled.** The gap between #1 and #2 is not the same
   thing as the gap between #20 and #21, and averaging ordinals assumes it is.
2. **Raw means ignore spread.** A team ranked 1, 1, 1, 16, 16 and a team ranked
   6, 6, 7, 7, 8 both average 7. The first is a genuine argument; the second is
   a consensus. A bare average cannot tell them apart.
3. **A mean has no error bar, and the error bar is the interesting part.**

The method below fixes each. It does not pretend a power ranking is a physical
measurement — a ballot is an opinion, and opinions are correlated with each
other by construction. That correlation is measured and reported rather than
assumed away.

---

## 2. Standardising a ballot

Let `r[s][t]` be the rank source `s` gives team `t`, with `N = 32` teams. Each
ballot is a permutation of `1..N`, so its mean and variance are known exactly
rather than estimated from the data:

```
mu_s = (N + 1) / 2            = 16.5
sd_s = sqrt((N^2 - 1) / 12)   = 9.30
```

Each ballot is converted to rank-standard-deviation units:

```
z[s][t] = (mu_s - r[s][t]) / sd_s
```

which is the usual z-score with the sign flipped so that **positive is better**
and rank 1 maps to the largest value. Properties that matter:

- **Comparable across outlets.** A source that clusters the top teams tightly
  and one that spreads them out produce the same scale once standardised, so
  neither gains influence from its stylistic spread.
- **No leakage.** `mu_s` and `sd_s` are analytic constants, not computed from
  the ballot, so standardising reveals nothing about a source's actual choices.
- **Interpretable.** One unit is one rank standard deviation; on a 32-team
  ballot, going from a score of +1.5 to +0.9 is roughly half a rank spread.

The pipeline also carries the raw mean rank for every team, because "mean rank
2.11" is what a reader wants to see even though the ordering is computed on the
z-scale.

---

## 3. Pooling the panel

Treat each source as a replicate measurement of an unknown quantity `theta[t]`,
the panel's latent view of team `t`:

```
z[s][t] = theta[t] + e[s][t]
```

Pooling uses a **prior-weighted mean** over sources. Weights come from
`sources.json` and are confined to `0.75–1.00`, so they are a tiebreak between
desks rather than a lever. With the variance components estimated separately
(below), the pooled estimate is:

```
zbar[t] = sum_s w[s] * z[s][t] / sum_s w[s]
```

At this point `zbar` is an unbiased summary of what the panel thinks, and it is
already a defensible ranking. Everything after this is about honesty regarding
its precision.

---

## 4. Uncertainty, part 1: how much would the answer move?

Two questions get conflated constantly, so they are separated here.

**(a) Sampling variability — "what if the panel were different outlets?"**
This is answered with a **jackknife**. For each source `s`, recompute the pooled
mean with `s` removed, giving leave-one-out values `zbar_(s)[t]`. The estimated
variance of the pooled mean is:

```
Var_jack[t] = (S - 1) / S * sum_s ( zbar_(s)[t] - mean_s zbar_(s)[t] )^2
```

The jackknife is exact for a mean, needs no distributional assumption, and is
computed **per team**, so a club the panel argues about gets a wide interval
and a club everyone agrees on gets a narrow one. For 2026 Week 2 that range is
real: the jackknife variance runs from 0.0004 for the most agreed-upon club to
0.022 for the Pittsburgh Steelers, whose ranks span 13–27 across nine outlets.

**(b) The effective number of sources.** Panelists are not independent. They
watch the same games, share the same priors, and read each other. The panel
therefore carries less information than its raw count suggests. This is
measured with **split-half reliability**:

- split the panel into two random halves, 200 times with a fixed seed;
- compute the consensus in each half;
- correlate the two half-consensuses (Spearman);
- step the result up to full-panel length with the **Spearman-Brown** formula
  `2ρ / (1 + ρ)`.

For 2026 Week 2 the split-half correlation is 0.983 and the stepped-up
reliability is **0.991**. Inverting the same formula gives the effective number
of independent sources, which lands at 9.0 — meaning this particular panel of
nine behaves like nine independent voices, because their agreement is high and
uniform. When it does not (a panel with heavy syndication or two desks from one
outlet), the effective count drops and the intervals widen accordingly.

---

## 5. Uncertainty, part 2: empirical-Bayes shrinkage

A team that one outlet ranks 2nd and eight others rank 20th has a pooled mean
that is dragged around by a single voice. Shrinking the estimates is the
standard fix, and it is what makes the consensus robust rather than merely
averaged.

The model is a measurement-error / normal-normal hierarchy. Prior variance of
true team quality is estimated by method of moments:

```
tau^2 = max(0, Var(zbar) - mean_t Var_jack[t])
```

The observed spread of pooled means is inflated by the noise already inside
them, so subtracting the average jackknife variance recovers the spread of the
underlying signal. The reliability factor is:

```
lambda = tau^2 / (tau^2 + mean_t Var_jack[t])
```

and the shrunk score is:

```
theta_hat[t] = grand_mean + lambda * (zbar[t] - grand_mean)
```

For 2026 Week 2, `tau^2 = 0.955`, `lambda = 0.991`. A λ near 1 is the correct
answer for a league where the best and worst teams are separated by far more
than the panel's disagreement: it says the between-team differences are real
and the shrinkage has almost nothing to do. In a week where outlets genuinely
scatter — early season, or after a chaotic Sunday — λ falls and the consensus
visibly compresses toward the middle. **The pipeline reports λ every week
precisely so that this is visible rather than hidden.**

Two consequences worth stating plainly:

- Because shrinkage is affine in `zbar`, it cannot reorder teams. The published
  order is the pooled order, and the shrunk score is what carries the error bar.
- Shrinking toward the *panel* mean is not shrinking toward truth. If every
  outlet is wrong about the same team in the same way, this method inherits the
  error. That is a fundamental limit of a poll of polls, not a bug, and §7 is
  about measuring the part of it that can be measured.

Standard error and interval:

```
se[t] = sqrt( lambda * Var_jack[t] + tau^2 * (1 - lambda) )
CI[t] = theta_hat[t] +/- t_(0.975, S_eff - 1) * se[t]
```

The two terms are the sampling part and the irreducible "the panel could have
been different outlets" part. The Student-t critical value charges the correct
price for a small panel; a normal quantile would be overconfident at S ≈ 9.
Note that the jackknife already reflects correlated panelists, so neither term
is divided by the raw source count again — doing so would double-count the
correction.

---

## 6. Rank uncertainty, and the bootstrap

The score interval answers "how precisely do we know this team's quality?"
The published table answers a different question: "how stable is this team's
*position*?" Position depends on every other team, so it is estimated by
resampling the panel:

- draw `S` sources with replacement, 4,000 times, from a fixed seed;
- recompute the pooled ranking in each draw;
- report the 2.5th and 97.5th percentiles of each team's rank, plus `P(#1)`
  and `P(top 5)`.

2026 Week 2 illustrates why this matters. Seattle and Buffalo are separated by
**0.002 z-units** — a statistical dead heat — so the bootstrap gives Buffalo a
59% chance at #1 and Seattle 39%. Reporting "1. Seattle, 2. Buffalo" as if that
were a finding would be a mistake; reporting the 59/39 split is the finding.

The bootstrap treats sources as exchangeable. Combined with the
correlation-adjusted standard errors above, it brackets the true uncertainty:
the bootstrap is the optimistic view (it pretends a re-drawn panel is
independent), the effective-sample correction is the conservative one. Both are
published.

---

## 7. Source diagnostics, and what is *not* claimed

Every source's ballot is compared to the consensus by mean absolute rank
deviation and by Spearman correlation, and every pair of sources is correlated
against every other (the full matrix is in `out/report.md`). For 2026 Week 2:

- mean pairwise ρ = **0.926** (range 0.86–0.97);
- the most central source is Neil Reynolds (mean deviation 1.12 positions);
- the most divergent is Vinnie Iyer (2.44 positions, ρ = 0.947).

These numbers diagnose the panel. They do **not** establish who is right, and
this pipeline deliberately does not grade sources against game outcomes. Doing
that properly requires backtesting each outlet's weekly ballot against
end-of-season results across multiple seasons — a different and much larger
project. Until it exists, the credibility weights in `sources.json` are stated
priors, published in the report, and kept inside a narrow range so the result
never hinges on them.

What the method *can* claim:

- the consensus is a faithful, weighted summary of nine documented ballots;
- the uncertainty is measured under two explicit models and both are reported;
- the process is reproducible byte-for-byte from archived HTML;
- nothing is silently imputed — an incomplete ballot is dropped, not filled in.

What it cannot claim:

- that the consensus is *correct*, only that it is what the panel implies;
- independence of the sources, only an estimate of their effective number;
- that a rank interval is a predictive interval for future games.

---

## 8. Failure modes, and how the pipeline handles them

| Failure | Handling |
|---------|----------|
| A source publishes fewer than 32 teams | Ballot rejected by `validate`; panel proceeds with the rest; run reports the drop |
| Two sources are the same syndicated copy | Identical-ballot check rejects the duplicate |
| A parser grabs a sidebar or nav menu | Ranks fail the permutation check; run fails loudly |
| A source's URL changes | Falls back to `urls` list; if still unreachable, the source is dropped and reported |
| A source goes stale on a fixed URL | Documented manual freshness check (`SOURCES.md` §4) |
| Fewer than 5 usable ballots | Hard failure; no consensus is published |
| Ranking set has ties after pooling | Ordering falls back to pooled z-score, then club name, so output is deterministic |
| A week's schedule has not been published | Head-to-head section is skipped; the consensus still publishes |

---

## 9. Head to head: from consensus score to win probability

The consensus publishes a score per team in rank-standard-deviation units. To
price a matchup that score has to be given a scale in points, and that is the
whole model:

```
margin(away @ home) = k * (z_home - z_away) + H
margin              ~ Normal(mean = margin, sd = sigma)
P(home wins)        = Phi(margin / sigma)
```

| constant | meaning | fitted value |
|----------|---------|--------------|
| `k` | points of expected margin per unit of score difference | 4.59 |
| `H` | home-field advantage, in points | 2.56 |
| `sigma` | standard deviation of the realised margin | 13.16 |

A normal margin rather than a logistic link on ratings is used deliberately: it
keeps the checkable quantity (a projected score) separate from the probability,
and it forces every source of error into `sigma` — the consensus being a noisy
proxy for true strength, week-to-week form, injuries, weather, turnovers. A
probability is therefore only as confident as the observed scatter of NFL
results allows, which is the honest ceiling for a model built on rankings alone.

### 9.1 Fitting, and an identifiability trap

The obvious procedure — grid-search all three constants by minimising log-loss
on completed games — produces good probabilities and a meaningless scale. The
win/loss likelihood depends only on the **ratios** `k/sigma` and `H/sigma`, so
the optimum is a flat ridge rather than a point, and the search returns whichever
ridge point the grid happens to favour. Observed directly on the 2025 season:

| grid | k | sigma | log-loss |
|------|---|-------|----------|
| narrow | 5.70 | 15.50 | 0.6098 |
| widened | 8.25 | 21.12 | 0.6098 |

Identical log-loss — and the second would project 21-point margins between teams
separated by one score unit, which is implausible on its face. The scale has to
come from a quantity that carries units, so the fit is staged
(`tools/calibrate.py`):

1.  **Ratings.** Each season's team strength is its final point differential,
    standardised, computed **leave-one-out** per game. Without that step a game
    helps set its own ratings and the slope inflates: 2025 fits `k = 4.78` with
    leave-one-out and `k = 5.66` without it.
2.  **`k` and `H`** by ordinary least squares of the realised margin on the
    rating difference. Points regressed on points fixes the scale.
3.  **`sigma`** as the residual standard deviation of that regression, which is
    exactly the spread the probability step needs.

Log-loss then serves as *validation*, not as the objective.

### 9.2 What the fit is worth

Fitted per season and pooled over **6,719 regular-season games, 2000–2025**
(medians reported):

| metric | model | benchmark |
|--------|-------|-----------|
| log-loss | **0.6124** | closing lines 0.6085; coin flip 0.6931 |
| accuracy | 66.8% | home teams win 53.7% |
| `k` across seasons | 3.27 – 5.90 | |
| `sigma` across seasons | 11.52 – 14.61 | |

Calibration on the 2025 season, by predicted-probability band:

| band | games | hit rate |
|------|-------|----------|
| 70–80% | 101 | 56% |
| 80–90% | 122 | 67% |
| 90–100% | 49 | 92% |

The 70–80% band under-delivers, which is the expected shape: near-coin-flip
games are the ones the rankings cannot separate. The bands a reader will act on
are close to nominal.

### 9.3 What the model is not

It is **not** a betting model. Only the nine ballots enter a published number.
Injury reports, rest, travel, weather and market information are all excluded;
closing lines appear in the pipeline solely as the independent benchmark in
§9.2. It also inherits the panel's blind spots: a team all nine outlets misjudge
is a team the probability is confidently wrong about, which is why `sigma` is
sized to keep a decent edge from becoming a near-certainty.

### 9.4 Grading a published week

`run.py` writes `out/matchups.csv` with one row per game — projected margin,
win probability, pick and the closing line — leaving the score columns empty on
purpose. Once the games are played, filling them in lets the metrics in §9.2 be
recomputed on the current season, which is how a drift in `k` or a widening gap
to the market would be detected rather than assumed away.

## 10. Path to the Super Bowl: simulating the bracket

§9 prices a single game. This section prices a tournament: given where each team
is seeded today, how often does it reach the Super Bowl? It answers a different
question from the rankings, and mixes two inputs on purpose.

### 10.1 Seeding comes from records, not from the rankings

The bracket is seeded by **win-loss record** -- the actual standings -- not by
consensus score. That matters, because they disagree: Minnesota is 5-0 and ranked
sixth, so the Vikings take the NFC's second seed while Seattle, rated higher by
the panel, enters as a wild card.

Ties between identical records are broken by consensus score. This is an
approximation and should be labelled as one. The real NFL tiebreaker chain is
head-to-head, then division record, then common games, then conference record,
then strength of victory -- all of which need the full game log with opponents
resolved. The pipeline carries results, not a resolved schedule graph, so it
cannot compute them. Records first, consensus second, is the honest stand-in.

Within a conference: the four division winners are seeded 1-4 in record order,
then the three best remaining teams are seeded 5-7.

### 10.2 Games are priced by §9

A playoff game uses the same fitted model as any other:

```
margin    = k * (z_home - z_away) + home_field
P(home)   = Phi(margin / sigma)
```

with `k = 4.59` points per consensus unit, `home_field = 2.56` points and
`sigma = 13.16`, all from §9. The Super Bowl drops the home-field term, since it
is played at a neutral site.

One caveat worth stating: the coefficients were fitted on **regular-season**
games. Playoff home-field advantage is often argued to be larger, and playoff
teams are a selected, better-matched sample, so this likely understates the
home edge slightly and overstates blowout probabilities. Re-fitting on playoff
games alone would require more post-season history than is worth the variance.

### 10.3 The bracket, and why it is a simulation

The format is the current one: seven teams per conference, one bye, three wild
card games (2v7, 3v6, 4v5), then reseeding -- the top seed always faces the
lowest surviving seed -- with the better seed hosting throughout.

That structure is a tree of conditional probabilities with no closed form, so it
is evaluated by Monte Carlo: the bracket is played out 50,000 times and the
round-by-round frequencies are the reported probabilities. The run is seeded
(`season * 10000 + week`) so the output is reproducible; a different seed moves
the numbers by less than a tenth of a point at this sample size.

Two checks that the simulation is wired correctly:

- The probabilities of reaching the Super Bowl sum to exactly 2.0 (one per
  conference) and the championship probabilities sum to 1.0.
- Top seeds have `P(reach divisional) = 1.0`, and every other seed's
  `P(reach divisional)` equals its own wild card win probability.

The wild card matchups are also reported directly from §10.2 rather than from
the simulation, because seeding fixes them, so those six numbers are exact.
Reporting both makes it visible which figures are prices and which are
simulated frequencies.

### 10.4 What this is not

It is not a prediction of the actual playoff field, which is mostly not yet
determined -- 14 of 32 teams would make it if the season ended today, and most
of the other 18 still can. It is a statement about *this panel's current opinion*
of team strength, propagated through the bracket as it stands. If the rankings
are wrong, the bracket odds are wrong in the same direction, and they inherit
every limitation in §7 and §9.3.

## 11. Blending the power rankings with records

Section 10 seeds the bracket on a blend of the power rankings and each team's
record rather than on either alone. This section is how that blend is built and
what the weight is worth.

### 11.1 Each signal is fitted, then standardised

The two signals do not arrive on the same scale, so each is fitted on its own
terms first, on the same 6,719 games and the same 2000-2025 window as the
head-to-head constants:

```
rank  points = k_rank * z            k_rank = 4.59
record points = k_rec  * win_pct     k_rec  = 11.01
```

with win percentage counting a tie as half a win, and a team that has not played
yet scored 0.500 rather than 0.000. The record fit gives a home-field term of
2.36 and a residual `sigma_rec` of 14.08, log-loss **0.6589**; the strength
signal the matchup model was fitted on reaches **0.6124** on the same games.
Record is the weaker predictor, which is what you would expect: it discards
margin of victory, and a 3-2 team that has won by a combined 40 points is not the
same as one that has won three one-score games.

Each signal is then **standardised across the 32 teams before mixing**. That step
matters more than it looks. Mixing raw margins gives the record far more say than
the weight suggests, because `k_rec` is over twice `k_rank`: measured against the
actual bracket, every weight below about 0.55 reproduced the *records-only*
seeding, so "46% on the rankings" behaved like none at all. Standardising first
makes the weight a genuine share of influence, and the blend is converted back to
points at the matchup model's rate so the home-field and sigma constants keep
their meaning.

```
strength   = k_rank * (w * z_rank_std + (1 - w) * z_rec_std)
margin     = strength_home - strength_away + home_field_blend
P(home)    = Phi(margin / sigma)
```

The same blended strength drives both the *seeding* and the *game outcomes*, so a
division winner the panel rates highly can outrank one with a better record.

### 11.2 The weight is fitted on games that had not been played

`w` is fitted by minimising log-loss on genuinely ex-ante games. Each weekly
consensus bundle is published *before* that week's slate, and the record it
carries is the standing entering the week, so grading a bundle against that
week's results involves no future information. Weeks 3, 4 and 5 of 2026 are
complete and have such bundles: **47 games**.

Fitted on those 47 games: **`w = 0.51`** on the power rankings, log-loss
**0.6465**, against 0.6496 for rankings-only and 0.6499 for records-only.

### 11.3 The weight is weakly determined, and is reported that way

A 95% profile interval comes from the deviance, `2n(loss - loss_min) ~ chi2(1)`,
so every weight whose loss is within `1.92/n` of the best is accepted. On 47
games that interval runs from **0.00 to 1.00** -- the entire range. The likelihood
is nearly flat and this season cannot yet distinguish the two signals.

**The weight is therefore fitted with a weak prior, and that is not cosmetic.**
An unregularised minimisation of a flat likelihood lands on whichever boundary is
luckier, and the boundary moves from week to week: on weeks 3-5 it gave 0.51, and
on weeks 4-6 it gave **exactly 1.00** -- which silently discards the record, the
opposite of what the blend exists to do. The published weight is the maximum a
posteriori under a `Beta(2, 2)` prior centred on an even split, worth one
pseudo-observation per side:

```
maximise   -n * log_loss(w)  +  log(w)  +  log(1 - w)
```

That regularises the estimate to **0.50** and **0.55** on the same two windows --
stable, and still driven by the data wherever the data discriminates. The
unregularised argmin is reported alongside it rather than hidden, because the gap
between the two *is* the evidence that the weight is not identified.

Three views, which agree more than the interval suggests:

* **The fitted weight**, 0.51, on the standardised blend.
* **Precision weighting.** If the two models erred independently the optimal
  weight would be proportional to the inverse of each residual variance, giving
  **0.53** on the rankings. They do not err independently -- both read the same
  teams -- so this is a sanity check rather than a second estimator.
* **The longer history.** Over 6,719 games the strength signal beats win-loss
  record by a wide margin (0.6124 against 0.6589), which argues for weighting the
  rankings above half.

All three land near one half, so the published 51/49 is defensible; the honest
caveat is that it is closer to "roughly half each" than to a measurement.

### 11.4 Sigma comes from the long run, not from these 47 games

The blend's own best-fit `sigma` on 47 games is 11.50. The simulation uses
**13.16**, the value fitted on 6,719 games, and the reason is that the choice is
nearly free on the evidence but not on the output. Log-loss differs by 0.0006
across the plausible range, yet `sigma` is the term that compounds over six
rounds: at 11.50 the favourite reaches the Super Bowl in 55% of simulated
brackets, at 13.16 in 52%. A dispersion estimated from 47 games would overstate
confidence throughout the bracket, so the better-estimated constant wins.

### 11.5 What the blend does and does not change

It is not demonstrably a better forecast than the rankings alone, and a 0.004
log-loss margin on 47 games does not support that claim. Because the record model
is the weaker of the two, mixing it in at half weight also pulls confident
predictions toward 50%: the blend is systematically closer to a coin flip than
the rankings alone would be.

In Week 6 it moved the *strengths* and the *probabilities* but not the *field*:
the same fourteen teams qualified in the same seeds as a records-only bracket
would have produced, because the panel and the standings agreed on that week's
seven per conference.

In Week 7 it changed the field. The fourteen teams were the same, but the last
wild card in each conference was not: Seattle and Cincinnati took the seventh
seed, displacing Detroit and Pittsburgh, who a standings-only bracket would have
included. The panel rated the Seahawks and Bengals above their records, and the
blend followed them about halfway. That is the blend doing what it is for, and it
depends on a weight the data cannot pin down -- which is why the weight is stated
on the page rather than buried here.

## 12. References

- Efron, B. & Stein, C. (1981). *The Jackknife Estimate of Variance.* Annals of
  Statistics 9(3) — the leave-one-out variance used in §4.
- James, W. & Stein, C. (1961). *Estimation with Quadratic Loss.* — the
  shrinkage estimator in §5.
- Spearman, C. (1910); Brown, W. (1910). — the split-half step-up formula in §4.
- Efron, B. (1979). *Bootstrap Methods: Another Look at the Jackknife.* — the
  resampling in §6.
