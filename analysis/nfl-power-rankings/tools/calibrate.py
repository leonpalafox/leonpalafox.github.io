#!/usr/bin/env python3
"""Fit the head-to-head model's constants from completed NFL seasons.

The fitting problem, and why it is done in two stages
-----------------------------------------------------
The model has three constants::

    margin(away @ home) = k * (z_home - z_away) + H
    P(home wins)        = Phi(margin / sigma)

The tempting approach is to grid-search all three by minimising log-loss on
completed games. That works, but it is **not identifiable**: only the ratios
``k/sigma`` and ``H/sigma`` affect the win/loss likelihood, so the search slides
along a flat ridge and returns whatever corner the grid happens to favour. Run
with a narrow grid it reported ``k = 5.7, sigma = 15.5``; widen the grid and the
same data gave ``k = 8.25, sigma = 21.1`` — with identical log-loss. The
probabilities are fine either way, but ``k = 8.25`` would publish absurd
projected margins, because the score spread of real teams is nowhere near 21
points.

So the two quantities the model publishes are pinned by the two things that can
identify them:

1.  **``k`` and ``H`` by least squares on realised margins.** Points are
    measured in points, so regressing the actual margin on the rating difference
    fixes the scale directly. This is what makes a projected margin real.
2.  **``sigma`` by the residual standard deviation** of that same regression:
    the spread of an actual margin around its expectation, which is exactly what
    the probability step needs.

Log-loss is then reported as a *validation* metric rather than an objective —
alongside the same metric computed from closing lines, which is the benchmark.

Ratings use leave-one-out season point differentials. Leave-one-out matters: a
game must not contribute to the ratings that predict it, or the slope comes out
too steep. The first prototype skipped this and reported ``k = 5.66`` where the
honest number is ``4.78``.

Usage
-----
    python3 tools/calibrate.py                      # every season, pooled summary
    python3 tools/calibrate.py --season 2025        # one season in detail
    python3 tools/calibrate.py --write              # refresh model.json defaults
    python3 tools/calibrate.py --csv PATH           # use a local games CSV
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from pollofpolls import games as games_mod  # noqa: E402
from pollofpolls.headtohead import normal_cdf  # noqa: E402

MODEL_PATH = HERE.parent / "model.json"
FIRST_SEASON = 2000


def load_rows(csv_text: str) -> dict[int, list[dict]]:
    by_season: dict[int, list[dict]] = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        if row.get("game_type") != "REG":
            continue
        if not row.get("home_score") or not row.get("away_score"):
            continue
        try:
            season = int(row["season"])
        except (KeyError, ValueError, TypeError):
            continue
        by_season.setdefault(season, []).append(row)
    return by_season


def season_games(rows: list[dict]) -> list[tuple[str, str, int, float | None]]:
    out = []
    for row in rows:
        try:
            margin = int(row["home_score"]) - int(row["away_score"])
        except (KeyError, ValueError, TypeError):
            continue
        raw_spread = (row.get("spread_line") or "").strip()
        try:
            spread = float(raw_spread)
        except ValueError:
            spread = None
        out.append((row["home_team"], row["away_team"], margin, spread))
    return out


def leave_one_out_ratings(
    played: list[tuple[str, str, int, float | None]], exclude: tuple[str, str] | None
) -> dict[str, float]:
    """Standardised point differential with one game optionally removed."""
    totals: dict[str, float] = {}
    for home, away, margin, _ in played:
        if exclude is not None and (home, away) == exclude:
            continue
        totals[home] = totals.get(home, 0.0) + margin
        totals[away] = totals.get(away, 0.0) - margin
    if not totals:
        return {}
    mean = sum(totals.values()) / len(totals)
    spread = statistics.pstdev(list(totals.values())) or 1.0
    return {team: (value - mean) / spread for team, value in totals.items()}


def observations(
    played: list[tuple[str, str, int, float | None]]
) -> list[tuple[float, int, float | None]]:
    """(rating edge, realised margin, closing spread) per game, leave-one-out."""
    cache: dict[tuple[str, str], dict[str, float]] = {}
    out = []
    for home, away, margin, spread in played:
        key = (home, away)
        if key not in cache:
            cache[key] = leave_one_out_ratings(played, key)
        table = cache[key]
        if home not in table or away not in table:
            continue
        out.append((table[home] - table[away], margin, spread))
    return out


def fit(played: list[tuple[str, str, int, float | None]], *, min_games: int = 100) -> dict:
    obs = observations(played)
    if len(obs) < min_games:
        return {}

    # Stage 1: least squares of realised margin on the rating edge.
    mean_x = sum(o[0] for o in obs) / len(obs)
    mean_y = sum(o[1] for o in obs) / len(obs)
    sxx = sum((o[0] - mean_x) ** 2 for o in obs)
    sxy = sum((o[0] - mean_x) * (o[1] - mean_y) for o in obs)
    if sxx == 0:
        return {}
    k = sxy / sxx
    home_field = mean_y - k * mean_x

    # Stage 2: residual spread is the model's sigma.
    residuals = [o[1] - (k * o[0] + home_field) for o in obs]
    sigma = math.sqrt(sum(e * e for e in residuals) / (len(residuals) - 1))

    def loss(probability: float, margin: int) -> float:
        p = min(max(probability, 1e-12), 1 - 1e-12)
        return -math.log(p if margin > 0 else 1 - p)

    logloss = sum(loss(normal_cdf((k * o[0] + home_field) / sigma), o[1]) for o in obs) / len(obs)
    accuracy = sum(1 for o in obs if ((k * o[0] + home_field) > 0) == (o[1] > 0)) / len(obs)

    # Benchmark: the same probability map driven by the closing line instead.
    with_spread = [o for o in obs if o[2] is not None]
    market = {}
    if len(with_spread) > 50:
        candidates = []
        for step in range(80, 301, 5):
            s = step / 10
            candidates.append(
                (sum(loss(normal_cdf(o[2] / s), o[1]) for o in with_spread) / len(with_spread), s)
            )
        best = min(candidates)
        market = {
            "logLoss": round(best[0], 4),
            "sigma": best[1],
            "n": len(with_spread),
            "accuracy": round(
                sum(1 for o in with_spread if (o[2] > 0) == (o[1] > 0)) / len(with_spread), 4
            ),
        }

    return {
        "n": len(obs),
        "k": round(k, 2),
        "homeField": round(home_field, 2),
        "sigma": round(sigma, 2),
        "logLoss": round(logloss, 4),
        "accuracy": round(accuracy, 4),
        "homeWinRate": round(sum(1 for o in obs if o[1] > 0) / len(obs), 4),
        "coinFlipLogLoss": round(math.log(2), 4),
        "market": market,
        "residualR2": round(
            1 - sum(e * e for e in residuals) / sum((o[1] - mean_y) ** 2 for o in obs), 4
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season", type=int, default=None, help="fit one season in detail")
    parser.add_argument("--csv", type=pathlib.Path, default=None, help="local games CSV")
    parser.add_argument("--write", action="store_true", help="write model.json defaults")
    parser.add_argument("--first-season", type=int, default=FIRST_SEASON)
    args = parser.parse_args()

    if args.csv:
        csv_text = args.csv.read_text(encoding="utf-8")
        source = str(args.csv)
    else:
        print(f"downloading {games_mod.NFLVERSE_GAMES}")
        csv_text = games_mod.fetch_nflverse_games()
        source = games_mod.NFLVERSE_GAMES

    by_season = load_rows(csv_text)
    seasons = sorted(s for s in by_season if s >= args.first_season)
    if not seasons:
        print("error: no usable seasons in the CSV", file=sys.stderr)
        return 2

    if args.season:
        if args.season not in by_season:
            print(f"error: season {args.season} not in the dataset", file=sys.stderr)
            return 2
        print(json.dumps({str(args.season): fit(season_games(by_season[args.season]))}, indent=2))
        return 0

    print(
        f"{'season':>6} {'games':>6} {'k':>6} {'H':>6} {'sigma':>6} "
        f"{'logloss':>8} {'acc':>6} {'R2':>6} {'market':>8}"
    )
    fits: list[tuple[int, dict]] = []
    for season in seasons:
        result = fit(season_games(by_season[season]))
        if not result:
            continue
        fits.append((season, result))
        market = f"{result['market']['logLoss']:.4f}" if result["market"] else "n/a"
        print(
            f"{season:>6} {result['n']:>6} {result['k']:>6.2f} {result['homeField']:>6.2f} "
            f"{result['sigma']:>6.2f} {result['logLoss']:>8.4f} {result['accuracy']:>6.1%} "
            f"{result['residualR2']:>6.3f} {market:>8}"
        )

    def med(key: str) -> float:
        return round(statistics.median([r[key] for _, r in fits]), 2)

    losses = [r["logLoss"] for _, r in fits]
    markets = [r["market"]["logLoss"] for _, r in fits if r["market"]]
    accuracies = [r["accuracy"] for _, r in fits]
    print()
    print(
        f"pooled over {len(fits)} seasons "
        f"({fits[0][0]}-{fits[-1][0]}, {sum(r['n'] for _, r in fits)} games)"
    )
    print(
        f"  k          median {med('k'):.2f}   "
        f"range {min(r['k'] for _, r in fits):.2f}-{max(r['k'] for _, r in fits):.2f}"
    )
    print(
        f"  homeField  median {med('homeField'):.2f}   "
        f"range {min(r['homeField'] for _, r in fits):.2f}-{max(r['homeField'] for _, r in fits):.2f}"
    )
    print(
        f"  sigma      median {med('sigma'):.2f}   "
        f"range {min(r['sigma'] for _, r in fits):.2f}-{max(r['sigma'] for _, r in fits):.2f}"
    )
    print(f"  accuracy   median {statistics.median(accuracies):.1%}")
    print(f"  log-loss   median {statistics.median(losses):.4f}   (coin flip {math.log(2):.4f})")
    if markets:
        print(
            f"  market     median {statistics.median(markets):.4f}   "
            f"(closing lines, {len(markets)} seasons)"
        )

    if args.write:
        payload = {
            "k": med("k"),
            "homeField": med("homeField"),
            "sigma": med("sigma"),
            "source": f"median of per-season least-squares fits, {fits[0][0]}-{fits[-1][0]}",
            "nGames": sum(r["n"] for _, r in fits),
            "pooledLogLoss": round(statistics.median(losses), 4),
            "pooledMarketLogLoss": round(statistics.median(markets), 4) if markets else None,
            "sourceUrl": source,
            "seasons": [{"season": season, **result} for season, result in fits],
        }
        MODEL_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote {MODEL_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
