"""Monte Carlo simulation of the NFL playoff bracket.

This answers a different question from the rankings themselves: not "who is
better", but "who is most likely to be in the Super Bowl", given where each team
is currently seeded.

Two inputs, deliberately from different places:

* **Seeding follows the actual standings** -- win-loss record, with the
  consensus score used only to break ties between teams with identical records.
  That is an approximation and it is worth being explicit about: the real NFL
  tiebreaker chain (head-to-head, division record, common games, conference
  record, strength of victory) needs the full game log, which this pipeline does
  not carry. Records first, consensus second, is the honest simplification.

* **Game outcomes follow the consensus strength**, priced with the same fitted
  model the weekly matchups use::

      margin = k * (z_home - z_away) + home_field
      P(home) = Phi(margin / sigma)

  with k, home_field and sigma fitted on 6,719 regular-season games. The Super
  Bowl is played at a neutral site, so the home-field term is dropped there.

The bracket is the current 7-team-per-conference format: one bye, three wild
card games, then reseeding by seed within each round.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from . import headtohead

DEFAULT_SIMS = 50_000
DEFAULT_SEED = 20260101

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


def seed_conference(rows: list[dict]) -> list[SeededTeam]:
    """Seed one conference: four division winners (1-4), then the best of the rest."""
    # Division winners: best record in each division, consensus breaking ties.
    by_division: dict[str, dict] = {}
    for row in sorted(rows, key=lambda r: (-win_pct(r["record"]), -r["score"])):
        by_division.setdefault(row["division"], row)

    winners = sorted(by_division.values(), key=lambda r: (-win_pct(r["record"]), -r["score"]))
    remaining = [r for r in sorted(rows, key=lambda r: (-win_pct(r["record"]), -r["score"]))
                 if r not in winners]

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
        )
        for index, row in enumerate(ordered)
    ]


def _play(home: SeededTeam, away: SeededTeam, rng: random.Random, *, neutral: bool) -> SeededTeam:
    p_home = headtohead.home_win_probability(home.score, away.score, neutral=neutral)
    return home if rng.random() < p_home else away


def simulate(
    rows: list[dict],
    *,
    n_sims: int = DEFAULT_SIMS,
    seed: int = DEFAULT_SEED,
) -> dict:
    """Run the bracket ``n_sims`` times and return seeding plus round-by-round odds."""
    conferences = sorted({row["conference"] for row in rows})
    fields = {
        conf: seed_conference([r for r in rows if r["conference"] == conf])
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
                _play(by_seed[high], by_seed[low], rng, neutral=False)
                for high, low in ((2, 7), (3, 6), (4, 5))
            ]
            for winner in wc_winners:
                reached[winner.team]["divisional"] += 1
            reached[by_seed[1].team]["divisional"] += 1

            # Divisional: the bye faces the lowest surviving seed; the other two
            # meet. Reseeding means the bye always gets the weakest survivor.
            wc_winners.sort(key=lambda t: t.seed)
            bye_game = _play(by_seed[1], wc_winners[-1], rng, neutral=False)
            other_game = _play(wc_winners[0], wc_winners[1], rng, neutral=False)
            for winner in (bye_game, other_game):
                reached[winner.team]["conference"] += 1

            # Conference championship: higher seed hosts.
            finalists = sorted((bye_game, other_game), key=lambda t: t.seed)
            champion = _play(finalists[0], finalists[1], rng, neutral=False)
            reached[champion.team]["superbowl"] += 1
            champions[conf] = champion

        # Super Bowl: neutral site.
        if len(champions) == 2:
            left, right = (champions[c] for c in conferences)
            winner = _play(left, right, rng, neutral=True)
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
            p_home = headtohead.home_win_probability(home.score, away.score)
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
        "tiebreak": "records first, consensus score second",
        "conferences": {
            conf: [
                {
                    "seed": t.seed, "team": t.team, "abbr": t.abbr,
                    "record": t.record, "score": round(t.score, 4),
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
