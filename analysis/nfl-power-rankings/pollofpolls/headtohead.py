"""Head-to-head win probability from the panel consensus.

The model
---------
The poll-of-polls publishes each team's score ``z`` in rank-standard-deviation
units (see ``stats.py``). That score is the only strength input here, so the
model is deliberately small and fully specified by three constants:

    margin(away @ home) = k * (z_home - z_away) + H
    margin              ~ Normal(mean = margin, sd = sigma)
    P(home wins)        = Phi(margin / sigma)

``k``      points of expected margin per unit of consensus-score difference
``H``      home-field advantage in points
``sigma``  standard deviation of the actual margin around its expectation

Why a normal margin rather than a logistic on ratings: it keeps the quantity
the reader can check (a projected score) separate from the probability, and it
makes ``sigma`` do honest work. Every source of error lands in ``sigma`` — the
consensus being a noisy proxy for true strength, week-to-week form, injuries,
weather, turnovers — so the constants are estimated from realised margins
rather than assumed. ``tools/calibrate.py`` fits all three by minimising
log-loss on completed seasons, which is the quantity the model is used for.

What this is not
----------------
This is **not** a betting model. It prices a matchup using only what the nine
rankings say, with no injury reports, rest, travel, weather or market
information. Market closing lines are used *only* as an independent benchmark
in ``tools/calibrate.py``; they are never an input to a published number.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .teams import TEAMS


@dataclass(frozen=True)
class Model:
    """Fitted constants.

    Defaults are the pooled medians over the 2000-2025 regular seasons
    (6,719 games), written by ``tools/calibrate.py --write`` into
    ``model.json``. On those games the model's median log-loss is 0.6124
    against 0.6085 for closing lines and 0.6931 for a coin flip.
    """

    k: float = 4.59
    home_field: float = 2.56
    sigma: float = 13.16
    source: str = "median of per-season least-squares fits, 2000-2025"
    n_games: int = 6719

    def as_dict(self) -> dict:
        return {
            "k": self.k,
            "homeField": self.home_field,
            "sigma": self.sigma,
            "source": self.source,
            "nGames": self.n_games,
        }


DEFAULT_MODEL = Model()


def load_model(path) -> Model:
    """Read calibrated constants from ``model.json``, falling back to defaults."""
    import json
    import pathlib

    path = pathlib.Path(path)
    if not path.exists():
        return DEFAULT_MODEL
    payload = json.loads(path.read_text(encoding="utf-8"))
    return Model(
        k=float(payload.get("k", DEFAULT_MODEL.k)),
        home_field=float(payload.get("homeField", DEFAULT_MODEL.home_field)),
        sigma=float(payload.get("sigma", DEFAULT_MODEL.sigma)),
        source=str(payload.get("source", DEFAULT_MODEL.source)),
        n_games=int(payload.get("nGames", 0)),
    )


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def expected_margin(
    home_score: float, away_score: float, model: Model = DEFAULT_MODEL, *, neutral: bool = False
) -> float:
    """Projected home margin in points (negative means the away team wins)."""
    edge = 0.0 if neutral else model.home_field
    return model.k * (home_score - away_score) + edge


def home_win_probability(
    home_score: float, away_score: float, model: Model = DEFAULT_MODEL, *, neutral: bool = False
) -> float:
    margin = expected_margin(home_score, away_score, model, neutral=neutral)
    return normal_cdf(margin / model.sigma)


def predict(
    home: str,
    away: str,
    scores: dict[str, float],
    model: Model = DEFAULT_MODEL,
    *,
    neutral: bool = False,
) -> dict:
    """A complete head-to-head record for one matchup."""
    for team in (home, away):
        if team not in scores:
            raise KeyError(f"no consensus score for {team!r}")
    margin = expected_margin(scores[home], scores[away], model, neutral=neutral)
    p_home = normal_cdf(margin / model.sigma)
    favourite = home if p_home >= 0.5 else away
    return {
        "home": home,
        "away": away,
        "homeAbbr": TEAMS[home][0],
        "awayAbbr": TEAMS[away][0],
        "homeScore": scores[home],
        "awayScore": scores[away],
        "expectedMargin": margin,
        "homeWinProbability": p_home,
        "awayWinProbability": 1.0 - p_home,
        "favourite": favourite,
        "favouriteProbability": max(p_home, 1.0 - p_home),
        "pick": (
            f"{TEAMS[home][0]} by {abs(margin):.1f}"
            if margin >= 0
            else f"{TEAMS[away][0]} by {abs(margin):.1f}"
        ),
    }


# --- scoring rules used to grade the model ---------------------------------


def log_loss(probability: float, outcome: bool) -> float:
    p = min(max(probability, 1e-12), 1 - 1e-12)
    return -math.log(p if outcome else 1 - p)


def brier_score(probability: float, outcome: bool) -> float:
    return (probability - (1.0 if outcome else 0.0)) ** 2


def calibration_table(records: list[tuple[float, bool]], buckets: int = 5) -> list[dict]:
    """Reliability curve: for each predicted-probability band, how often it hit.

    ``records`` is a list of (predicted probability for the side actually
    picked, that side won). A well-calibrated model has hit rate ≈ band centre.
    """
    table = []
    for index in range(buckets):
        low = 0.5 + index * (0.5 / buckets)
        high = 0.5 + (index + 1) * (0.5 / buckets)
        subset = [
            won
            for probability, won in records
            if (low <= probability < high) or (index == buckets - 1 and probability >= high)
        ]
        if subset:
            table.append(
                {
                    "low": round(low, 3),
                    "high": round(high, 3),
                    "n": len(subset),
                    "predicted": round((low + high) / 2, 3),
                    "observed": round(sum(subset) / len(subset), 3),
                }
            )
    return table
