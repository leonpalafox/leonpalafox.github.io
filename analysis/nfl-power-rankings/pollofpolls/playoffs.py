"""Monte Carlo simulation of the NFL playoff bracket.

This answers a different question from the rankings themselves: not "who is
better", but "who is most likely to be in the Super Bowl", given where each team
is currently seeded.

Both the seeding and the game outcomes use a **blend of the power rankings and
each team's record**, so the bracket reflects what the panel thinks and what the
standings say rather than either one alone::

    strength   = w * k_rank * z + (1 - w) * k_rec * win_pct
    margin     = strength_home - strength_away + home_field_blend
    P(home)    = Phi(margin / sigma_blend)

``w`` is the weight on the power rankings. ``k_rank = 4.59`` points per consensus
unit and ``k_rec = 11.01`` points per unit of win-percentage difference are each
fitted on 6,719 regular-season games, so the two signals enter on a common points
scale; ``home_field_blend`` is the same mixture of the two home-field estimates.
The Super Bowl is played at a neutral site, so the home-field term is dropped
there.

Note what the blend does to the standings. With ``w`` below 1 a team's record is
no longer decisive: a 5-0 team the panel distrusts can be seeded below a 3-2 team
it rates highly. That is deliberate. It also means the real NFL tiebreaker chain
(head-to-head, division record, common games, conference record, strength of
victory) is not reproduced -- those need a resolved schedule graph this pipeline
does not carry, and the blended strength ordering replaces them.

The bracket is the current 7-team-per-conference format: one bye, three wild
card games, then reseeding by seed within each round.
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass

from . import headtohead, weighted

DEFAULT_SIMS = 50_000
DEFAULT_SEED = 20260101

# Weight on the power rankings when blending with records. 1.0 would ignore the
# record entirely and 0.0 would ignore the rankings; the fitted value comes from
# weighted.fit_blend and is passed in by the caller.
DEFAULT_WEIGHT = 1.0

# Fallback slope for the record half of the blend, used only when the caller
# does not supply a fitted record model. weighted.fit_record_model returns the
# real value (11.01 on the 2000-2025 window).
DEFAULT_RECORD_K = 11.01

PLAYOFF_FIELD = 7


@dataclass(frozen=True)
class SeededTeam:
    team: str
    abbr: str
    seed: int
    record: str
    score: float
    win_pct: float
    division_winner: bool
    strength: float = 0.0   # blended points above an arbitrary origin


def win_pct(record: str) -> float:
    """Winning percentage from a ``W-L`` or ``W-L-T`` record. Ties count as half."""
    parts = [int(p) for p in record.split("-") if p != ""]
    if len(parts) == 2:
        wins, losses = parts
        ties = 0
    elif len(parts) == 3:
        wins, losses, ties = parts
    else:
        return 0.0
    played = wins + losses + ties
    if played == 0:
        return 0.0
    return (wins + 0.5 * ties) / played


def strength_table(
    rows: list[dict],
    *,
    weight: float = DEFAULT_WEIGHT,
    rank_model=headtohead.DEFAULT_MODEL,
    record_model: dict | None = None,
) -> dict[str, float]:
    """Blended team strength in points, one entry per team.

    Each signal is **standardised across the supplied teams before mixing**. That
    matters more than it sounds. Mixing raw margins gives the record far more
    say than the weight suggests, because a unit of win-percentage difference is
    worth ``k_rec = 11.01`` points against ``k_rank = 4.59`` for a unit of
    consensus: measured against the actual bracket, every weight up to about
    0.55 produced the *records-only* seeding, so "46% on the rankings" behaved
    like none at all.

    Standardising first makes the weight a genuine share of influence -- at 0.5
    each signal contributes half the spread -- and the blend is then converted
    back to points at the matchup model's own rate so the home-field and sigma
    constants keep their meaning.
    """
    if record_model is None:
        record_model = {"k": DEFAULT_RECORD_K}

    rank_pts = [rank_model.k * row["score"] for row in rows]
    rec_pts = [record_model["k"] * win_pct(row["record"]) for row in rows]
    sd_rank = statistics.pstdev(rank_pts) or 1.0
    sd_rec = statistics.pstdev(rec_pts) or 1.0

    return {
        row["team"]: rank_model.k
        * (weight * (rank_pts[i] / sd_rank) + (1.0 - weight) * (rec_pts[i] / sd_rec))
        for i, row in enumerate(rows)
    }


def blended_strength(
    score_z: float,
    pct: float,
    *,
    weight: float = DEFAULT_WEIGHT,
    rank_model=headtohead.DEFAULT_MODEL,
    record_model: dict | None = None,
) -> float:
    """Single-team form of :func:`strength_table`, kept for tests and callers."""
    if record_model is None:
        record_model = {"k": DEFAULT_RECORD_K}
    return weight * rank_model.k * score_z + (1.0 - weight) * record_model["k"] * pct


def seed_conference(
    rows: list[dict],
    *,
    weight: float = DEFAULT_WEIGHT,
    rank_model=headtohead.DEFAULT_MODEL,
    record_model: dict | None = None,
) -> list[SeededTeam]:
    """Seed one conference by blended strength: winners 1-4, then the best rest.

    Ordering is by strength, not by record, so a division winner the panel rates
    highly can outrank one with a better record -- and a wild card can outrank a
    division winner from a weak division.
    """
    if record_model is None:
        record_model = {"k": DEFAULT_RECORD_K}

    strengths = strength_table(
        rows, weight=weight, rank_model=rank_model, record_model=record_model
    )

    def strength_of(row: dict) -> float:
        return strengths[row["team"]]

    decorated = sorted(rows, key=lambda r: -strength_of(r))

    # Division winners: the strongest team in each division.
    by_division: dict[str, dict] = {}
    for row in decorated:
        by_division.setdefault(row["division"], row)
    winners = sorted(by_division.values(), key=lambda r: -strength_of(r))
    remaining = [r for r in decorated if r not in winners]

    ordered = winners + remaining[: PLAYOFF_FIELD - len(winners)]
    return [
        SeededTeam(
            team=row["team"],
            abbr=row["abbr"],
            seed=index + 1,
            record=row["record"],
            score=row["score"],
            win_pct=win_pct(row["record"]),
            division_winner=row in winners,
            strength=strength_of(row),
        )
        for index, row in enumerate(ordered)
    ]


def home_win_probability(
    home: SeededTeam,
    away: SeededTeam,
    *,
    home_field: float,
    sigma: float,
    neutral: bool = False,
) -> float:
    """P(home) from the two blended strengths.

    ``strength`` is already in points above a common origin, so the margin is
    just the difference plus the (blended) home-field term.
    """
    margin = (home.strength - away.strength) + (0.0 if neutral else home_field)
    return headtohead.normal_cdf(margin / sigma)


def _play(
    home: SeededTeam,
    away: SeededTeam,
    rng: random.Random,
    *,
    neutral: bool,
    home_field: float,
    sigma: float,
) -> SeededTeam:
    p_home = home_win_probability(home, away, home_field=home_field, sigma=sigma, neutral=neutral)
    return home if rng.random() < p_home else away


def simulate(
    rows: list[dict],
    *,
    n_sims: int = DEFAULT_SIMS,
    seed: int = DEFAULT_SEED,
    weight: float = DEFAULT_WEIGHT,
    sigma: float | None = None,
    record_model: dict | None = None,
    rank_model=headtohead.DEFAULT_MODEL,
) -> dict:
    """Run the bracket ``n_sims`` times and return seeding plus round-by-round odds.

    ``weight`` is the share given to the power rankings, so ``1.0`` reproduces a
    rankings-only bracket and ``0.0`` a records-only one. ``sigma`` defaults to
    the rank model's own dispersion, which is right for weights near 1 and too
    tight for a blend; the caller should pass the fitted value when it has one.
    """
    if record_model is None:
        record_model = {"k": DEFAULT_RECORD_K, "homeField": rank_model.home_field}
    if sigma is None:
        sigma = rank_model.sigma

    # The home-field term is mixed on the same weights as the strengths.
    home_field = weight * rank_model.home_field + (1.0 - weight) * record_model.get(
        "homeField", rank_model.home_field
    )

    conferences = sorted({row["conference"] for row in rows})
    fields = {
        conf: seed_conference(
            [r for r in rows if r["conference"] == conf],
            weight=weight, rank_model=rank_model, record_model=record_model,
        )
        for conf in conferences
    }

    rng = random.Random(seed)
    reached = {
        t.team: {"divisional": 0, "conference": 0, "superbowl": 0, "champion": 0}
        for field in fields.values()
        for t in field
    }
    matchups: dict[tuple[str, str], int] = {}

    for _ in range(n_sims):
        champions: dict[str, SeededTeam] = {}
        for conf, field in fields.items():
            by_seed = {t.seed: t for t in field}

            # Wild card: 2v7, 3v6, 4v5, higher seed at home.
            wc_winners = [
                _play(by_seed[high], by_seed[low], rng, neutral=False,
                      home_field=home_field, sigma=sigma)
                for high, low in ((2, 7), (3, 6), (4, 5))
            ]
            for winner in wc_winners:
                reached[winner.team]["divisional"] += 1
            reached[by_seed[1].team]["divisional"] += 1

            # Divisional: the bye faces the lowest surviving seed; the other two
            # meet. Reseeding means the bye always gets the weakest survivor.
            wc_winners.sort(key=lambda t: t.seed)
            bye_game = _play(by_seed[1], wc_winners[-1], rng, neutral=False,
                             home_field=home_field, sigma=sigma)
            other_game = _play(wc_winners[0], wc_winners[1], rng, neutral=False,
                               home_field=home_field, sigma=sigma)
            for winner in (bye_game, other_game):
                reached[winner.team]["conference"] += 1

            # Conference championship: higher seed hosts.
            finalists = sorted((bye_game, other_game), key=lambda t: t.seed)
            champion = _play(finalists[0], finalists[1], rng, neutral=False,
                             home_field=home_field, sigma=sigma)
            reached[champion.team]["superbowl"] += 1
            champions[conf] = champion

        # Super Bowl: neutral site.
        if len(champions) == 2:
            left, right = (champions[c] for c in conferences)
            winner = _play(left, right, rng, neutral=True,
                           home_field=home_field, sigma=sigma)
            reached[winner.team]["champion"] += 1
            key = tuple(sorted((left.team, right.team)))
            matchups[key] = matchups.get(key, 0) + 1

    def p(team: str, stage: str) -> float:
        return reached[team][stage] / n_sims

    team_rows = []
    for conf, field in fields.items():
        for t in field:
            team_rows.append({
                "team": t.team,
                "abbr": t.abbr,
                "conference": conf,
                "seed": t.seed,
                "record": t.record,
                "score": round(t.score, 4),
                "strength": round(t.strength, 3),
                "divisionWinner": t.division_winner,
                "pDivisional": p(t.team, "divisional"),
                "pConference": p(t.team, "conference"),
                "pSuperBowl": p(t.team, "superbowl"),
                "pChampion": p(t.team, "champion"),
            })
    team_rows.sort(key=lambda r: (-r["pSuperBowl"], r["conference"], r["seed"]))

    # The wild card round is fixed by seeding, so its prices are exact rather
    # than simulated. Showing both makes it obvious which numbers are which.
    wild_card = {}
    for conf, field in fields.items():
        by_seed = {t.seed: t for t in field}
        wild_card[conf] = []
        for high, low in ((2, 7), (3, 6), (4, 5)):
            home, away = by_seed[high], by_seed[low]
            p_home = home_win_probability(home, away, home_field=home_field, sigma=sigma)
            wild_card[conf].append({
                "home": home.team, "homeAbbr": home.abbr, "homeSeed": high,
                "homeRecord": home.record,
                "away": away.team, "awayAbbr": away.abbr, "awaySeed": low,
                "awayRecord": away.record,
                "pHome": p_home, "pAway": 1.0 - p_home,
            })

    top_matchups = sorted(matchups.items(), key=lambda kv: -kv[1])[:6]

    return {
        "nSims": n_sims,
        "seed": seed,
        "weight": weight,
        "weightOnRankings": weight,
        "weightOnRecords": 1.0 - weight,
        "rankK": rank_model.k,
        "recordK": record_model["k"],
        "homeField": home_field,
        "sigma": sigma,
        "seedingRule": "blended strength (power rankings + win-loss record)",
        "conferences": {
            conf: [
                {
                    "seed": t.seed, "team": t.team, "abbr": t.abbr,
                    "record": t.record, "score": round(t.score, 4),
                    "strength": round(t.strength, 3),
                    "divisionWinner": t.division_winner,
                }
                for t in field
            ]
            for conf, field in fields.items()
        },
        "wildCard": wild_card,
        "teams": team_rows,
        "superBowlMatchups": [
            {"a": key[0], "b": key[1], "probability": count / n_sims}
            for key, count in top_matchups
        ],
        "byConference": {
            conf: {
                "pSuperBowl": sum(p(t.team, "superbowl") for t in field),
                "pChampion": sum(p(t.team, "champion") for t in field),
            }
            for conf, field in fields.items()
        },
    }
