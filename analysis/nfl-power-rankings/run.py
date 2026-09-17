#!/usr/bin/env python3
"""Run the NFL power-rankings poll-of-polls for one week.

Usage
-----
    python3 run.py                     # current week from sources.json
    python3 run.py --week 3            # a different week
    python3 run.py --offline           # use only the on-disk HTML cache
    python3 run.py --validate          # parse + validate, do not write output
    python3 run.py --from-dir /tmp/x   # parse local HTML files instead of HTTP
    python3 run.py --no-site           # do not refresh the Astro data bundle

Outputs (in this directory):
    out/report.md              human-readable audit trail
    out/consensus.json         full machine-readable payload
    out/site-data.json         bundle copied into the site
    out/ballots.json           raw per-source ballots, for replication
    cache/<season>-wk<week>/   raw HTML, one file per source
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pollofpolls import fetch, games, headtohead, report, sources, stats, teams, validate  # noqa: E402

METHOD_NOTE = (
    "Each source's 1-32 ballot is standardised to rank-standard-deviation units, "
    "pooled in a one-way random-effects model, and shrunk toward the panel mean "
    "(empirical Bayes), with uncertainty from both the residual disagreement and a "
    "bootstrap over sources. Full derivation in the post."
)

H2H_METHOD_NOTE = (
    "Win probability comes from the consensus score alone: the projected margin is "
    "k * (score difference) + home field, treated as normal with standard deviation "
    "sigma, so P(home) = Phi(margin / sigma). The three constants are fitted by least "
    "squares on 6,719 completed regular-season games (2000-2025); see model.json and "
    "tools/calibrate.py."
)


def load_registry(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_url(entry: dict, week: int, season: int) -> str:
    template = entry.get("url_tpl") or ""
    if template:
        return template.format(week=week, season=season)
    urls = entry.get("urls") or []
    return urls[0] if urls else ""


def candidate_urls(entry: dict, week: int, season: int) -> list[str]:
    out = []
    template = entry.get("url_tpl") or ""
    if template:
        out.append(template.format(week=week, season=season))
    for url in entry.get("urls") or []:
        if url not in out:
            out.append(url)
    return out


def from_dir_lookup(directory: pathlib.Path, source_id: str) -> str | None:
    """Find a cached fixture for a source in --from-dir mode."""
    for pattern in (f"{source_id}.html", f"*{source_id}*.html", f"*{source_id}*"):
        for candidate in sorted(directory.glob(pattern)):
            if candidate.is_file():
                return candidate.read_text(encoding="utf-8", errors="ignore")
    return None


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def collect_ballots(
    registry: dict,
    week: int,
    season: int,
    *,
    cache_dir: pathlib.Path,
    from_dir: pathlib.Path | None,
    offline: bool,
    verbose: bool,
) -> tuple[dict[str, dict[str, int]], dict[str, dict], list[str]]:
    ballots: dict[str, dict[str, int]] = {}
    meta: dict[str, dict] = {}
    failures: list[str] = []

    for entry in registry["sources"]:
        source_id = entry["id"]
        raw: str | None = None
        resolved_url = resolve_url(entry, week, season)
        provenance = "-"

        if from_dir is not None:
            raw = from_dir_lookup(from_dir, source_id)
            provenance = "from-dir"
            if raw is None:
                failures.append(f"{source_id}: no fixture in {from_dir}")
                if verbose:
                    print(f"  {source_id:22} MISSING FIXTURE")
                continue
        else:
            for candidate in candidate_urls(entry, week, season):
                try:
                    raw, provenance = fetch.fetch(
                        candidate,
                        source_id,
                        cache_dir,
                        offline=offline,
                    )
                    resolved_url = candidate
                    break
                except fetch.FetchError as exc:
                    if verbose:
                        print(f"  {source_id:22} try failed: {exc}")
            if raw is None:
                failures.append(f"{source_id}: unreachable ({resolved_url})")
                if verbose:
                    print(f"  {source_id:22} UNREACHABLE")
                continue

        ballot = sources.extract(entry["extract"], raw)
        entry_meta = dict(entry)
        entry_meta["url"] = resolved_url
        entry_meta["provenance"] = provenance
        entry_meta["content_sha256"] = fetch.sha256(raw)

        issues = validate.validate_ballot(source_id, ballot)
        if issues:
            failures.append(
                f"{source_id}: {len(ballot)} teams parsed; "
                + "; ".join(issue.message for issue in issues)
            )
            if verbose:
                print(f"  {source_id:22} INVALID ({len(ballot)}/32) via {provenance}")
            continue

        ballots[source_id] = ballot
        meta[source_id] = entry_meta
        if verbose:
            print(f"  {source_id:22} ok 32/32  ({provenance}, {len(raw) // 1024} KB)")

    return ballots, meta, failures


def write_matchups_csv(path: pathlib.Path, matchups: list[dict], model) -> None:
    """One row per game, so a week's predictions can be archived and graded."""
    if not matchups:
        return
    import csv as _csv

    columns = [
        "gameday", "kickoff", "away", "home", "neutral",
        "away_score", "home_score", "expected_margin", "home_win_probability",
        "away_win_probability", "pick", "market_spread",
        "model_k", "model_home_field", "model_sigma",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = _csv.writer(handle)
        writer.writerow(columns)
        for record in matchups:
            writer.writerow([
                record.get("gameday", ""), record.get("kickoff", ""),
                record["awayAbbr"], record["homeAbbr"], record.get("neutral", False),
                "", "",  # scores are filled in after the games are played
                round(record["expectedMargin"], 3),
                round(record["homeWinProbability"], 4),
                round(record["awayWinProbability"], 4),
                record["pick"],
                "" if record.get("marketSpread") is None else record["marketSpread"],
                model.k, model.home_field, model.sigma,
            ])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--week", type=int, default=None, help="NFL week (default: sources.json)")
    parser.add_argument("--season", type=int, default=None, help="NFL season (default: sources.json)")
    parser.add_argument("--registry", type=pathlib.Path, default=HERE / "sources.json")
    parser.add_argument("--offline", action="store_true", help="never touch the network")
    parser.add_argument("--from-dir", type=pathlib.Path, default=None, help="parse local HTML fixtures")
    parser.add_argument("--validate", action="store_true", help="parse and validate only")
    parser.add_argument("--no-site", action="store_true", help="skip refreshing the site bundle")
    parser.add_argument("--no-schedule", action="store_true", help="skip the head-to-head slate")
    parser.add_argument("--bootstrap", type=int, default=4000, help="bootstrap resamples (default 4000)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    verbose = not args.quiet
    started = time.time()
    registry = load_registry(args.registry)
    week = args.week or int(registry.get("week", 0))
    season = args.season or int(registry.get("season", 0))
    if not week or not season:
        print("error: week/season must be set in sources.json or passed explicitly", file=sys.stderr)
        return 2

    cache_dir = HERE / "cache" / f"{season}-wk{week:02d}"
    out_dir = HERE / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"NFL poll-of-polls — {season} season, Week {week}")
    print(f"registry: {args.registry}")
    print(f"mode: {'offline' if args.offline else 'network'} "
          f"{'from ' + str(args.from_dir) if args.from_dir else ''}")
    print()

    ballots, meta, failures = collect_ballots(
        registry,
        week,
        season,
        cache_dir=cache_dir,
        from_dir=args.from_dir,
        offline=args.offline,
        verbose=verbose,
    )

    if failures:
        print("\nUnusable sources:")
        for failure in failures:
            print(f"  - {failure}")

    panel_report = validate.validate_panel(ballots)
    if not panel_report.ok:
        print("\nValidation failed:")
        print(panel_report.render())
        return 1

    print(f"\n{len(ballots)} complete ballots passed validation")
    if panel_report.warnings:
        print(panel_report.render())

    prior_weights = {source: meta[source].get("prior_weight", 1.0) for source in ballots}
    panel = stats.build_panel(ballots, meta=meta, teams=sorted(teams.TEAMS))
    rows, diagnostics = stats.consensus(
        panel, prior_weights=prior_weights, bootstrap=args.bootstrap
    )

    print(
        f"agreement: mean pairwise rho {diagnostics.mean_pairwise_spearman:.3f}, "
        f"split-half reliability {diagnostics.split_half_reliability:.3f}, "
        f"shrinkage lambda {diagnostics.reliability:.3f}"
    )
    print()
    print(f"{'#':>2}  {'Team':24} {'score':>7} {'mean':>5} {'range':>6}  P(#1)")
    for row in rows[:12]:
        print(
            f"{row.rank:>2}  {row.team:24} {row.score:>+7.3f} {row.mean_rank:>5.2f} "
            f"{row.rank_min:>2}-{row.rank_max:<2}  {row.p_top1 * 100:>4.0f}%"
        )
    print("...")

    # --- head to head for this week's slate -------------------------------
    model = headtohead.load_model(HERE / "model.json")
    scores = {row.team: row.score for row in rows}
    schedule: list[games.Game] = []
    schedule_source = "none"
    if not args.no_schedule:
        slate_cache = HERE / "cache" / "schedule" / f"nflverse-games.csv"
        slate_cache.parent.mkdir(parents=True, exist_ok=True)
        csv_text = None
        if args.offline and slate_cache.exists():
            csv_text = slate_cache.read_text(encoding="utf-8")
            schedule_source = "cache"
        else:
            try:
                csv_text = games.fetch_nflverse_games()
                slate_cache.write_text(csv_text, encoding="utf-8")
                schedule_source = "nflverse"
            except Exception as exc:  # noqa: BLE001 - fall back to the site parser
                if slate_cache.exists():
                    csv_text = slate_cache.read_text(encoding="utf-8")
                    schedule_source = "stale-cache"
                else:
                    print(f"\nschedule unavailable ({type(exc).__name__}: {exc})")
        if csv_text:
            schedule = games.parse_nflverse_games(csv_text, season=season, week=week)
            if not schedule and args.offline is False:
                try:
                    html = fetch.fetch(
                        games.NFLCOM_SCHEDULE.format(season=season, week=week),
                        f"schedule-wk{week:02d}",
                        HERE / "cache" / f"{season}-wk{week:02d}",
                    )[0]
                    schedule = games.parse_nflcom_schedule(html, season=season, week=week)
                    schedule_source = "nfl.com"
                except Exception:  # noqa: BLE001 - schedule is optional
                    pass

    matchups = [
        headtohead.predict(game.home, game.away, scores, model, neutral=game.neutral)
        for game in schedule
    ]
    for record, game in zip(matchups, schedule):
        record["gameday"] = game.gameday
        record["kickoff"] = game.kickoff
        record["venue"] = game.venue
        record["neutral"] = game.neutral
        record["marketSpread"] = game.spread

    if matchups:
        print(f"\nWeek {week} head to head ({len(matchups)} games, schedule: {schedule_source})")
        print(f"model: k={model.k} pts/z, home field {model.home_field} pts, sigma {model.sigma} pts")
        print(f"{'away':>4} @ {'home':<4} {'proj':>7} {'P(home)':>8}  {'market':>7}")
        for record in matchups:
            market = f"{record['marketSpread']:+.1f}" if record["marketSpread"] is not None else "  n/a"
            print(
                f"{record['awayAbbr']:>4} @ {record['homeAbbr']:<4} "
                f"{record['expectedMargin']:>+7.1f} {record['homeWinProbability']:>7.1%}  {market:>7}"
            )
        bye = games.remaining_bye_teams(sorted(teams.TEAMS), schedule)
        if bye:
            print("no game: " + ", ".join(teams.TEAMS[t][0] for t in bye))

    if args.validate:
        print("\n--validate: no output written")
        return 0

    generated = report.utcnow()
    consensus_payload = {
        "week": week,
        "season": season,
        "generated": generated.replace(microsecond=0).isoformat(),
        "sources": [
            {
                "id": source,
                "outlet": meta[source].get("outlet"),
                "analyst": meta[source].get("analyst"),
                "kind": meta[source].get("kind"),
                "url": meta[source].get("url"),
                "extract": meta[source].get("extract"),
                "prior_weight": meta[source].get("prior_weight"),
                "tier": meta[source].get("tier"),
                "provenance": meta[source].get("provenance"),
                "content_sha256": meta[source].get("content_sha256"),
            }
            for source in ballots
        ],
        "diagnostics": {
            "n_sources": diagnostics.n_sources,
            "n_teams": diagnostics.n_teams,
            "within_variance": diagnostics.within_variance,
            "between_variance": diagnostics.between_variance,
            "reliability": diagnostics.reliability,
            "mean_pairwise_spearman": diagnostics.mean_pairwise_spearman,
            "split_half_reliability": diagnostics.split_half_reliability,
        },
        "teams": [
            {
                "team": row.team,
                "rank": row.rank,
                "score": row.score,
                "score_raw": row.score_raw,
                "se": row.se,
                "ci_low": row.ci_low,
                "ci_high": row.ci_high,
                "mean_rank": row.mean_rank,
                "median_rank": row.median_rank,
                "rank_sd": row.rank_sd,
                "rank_min": row.rank_min,
                "rank_max": row.rank_max,
                "rank_ci_low": row.rank_ci_low,
                "rank_ci_high": row.rank_ci_high,
                "p_top1": row.p_top1,
                "p_top5": row.p_top5,
                "spread": row.spread,
                "by_source": row.by_source,
            }
            for row in rows
        ],
    }

    report.write_json(out_dir / "consensus.json", consensus_payload)
    report.write_json(out_dir / "ballots.json", {source: ballots[source] for source in ballots})
    write_matchups_csv(out_dir / "matchups.csv", matchups, model)

    markdown = report.render_markdown(
        week=week,
        season=season,
        rows=rows,
        diagnostics=diagnostics,
        panel=panel,
        source_notes=meta,
        generated=generated,
        matchups=matchups,
        model=model,
        schedule_source=schedule_source,
    )
    (out_dir / "report.md").write_text(markdown + "\n", encoding="utf-8")

    site_bundle = report.build_site_bundle(
        week=week,
        season=season,
        rows=rows,
        diagnostics=diagnostics,
        panel=panel,
        source_meta=meta,
        generated=generated,
        method_note=METHOD_NOTE,
        matchups=matchups,
        model=model,
        h2h_method_note=H2H_METHOD_NOTE,
        schedule_source=schedule_source,
    )
    report.write_json(out_dir / "site-data.json", site_bundle)

    if not args.no_site:
        target = HERE.parent.parent / "src" / "data" / f"nfl-power-rankings-{season}-wk{week:02d}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        report.write_json(target, site_bundle)
        latest = HERE.parent.parent / "src" / "data" / "nfl-power-rankings-latest.json"
        report.write_json(latest, site_bundle)
        print(f"\nwrote {target.relative_to(HERE.parent.parent)}")
        print(f"wrote {latest.relative_to(HERE.parent.parent)}")

    print(f"wrote out/report.md, out/consensus.json, out/site-data.json")
    print(f"done in {time.time() - started:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
