"""Report rendering: a Markdown audit trail and the site data bundle.

Two consumers, two formats:

*   ``report.md`` is for a human re-running the pipeline. It shows every
    intermediate number - each ballot, the agreement matrix, the variance
    components, the bootstrap intervals - so a reader can check the work.
*   ``site-data.json`` is for the Astro blog post. It carries only what the
    widget needs, plus provenance for every source so the post can document
    itself without a second lookup.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone

from .stats import Diagnostics, Panel, ConsensusRow, mean, spearman
from .teams import TEAMS


def source_diagnostics(panel: Panel, rows: list[ConsensusRow]) -> list[dict]:
    """Per-source agreement with the consensus and with the rest of the panel.

    ``mean_abs_dev`` is the mean over teams of |ballot rank - consensus rank|,
    in rank positions: a compact statement of how far off a source typically
    is. ``rho_consensus`` is the Spearman correlation between the source's
    ballot and the final consensus order.
    """
    matrix = panel.matrix(require_complete=True)
    consensus_order = [row.team for row in rows]
    consensus_rank = {row.team: row.rank for row in rows}
    out = []
    for source in panel.ballots:
        ballot = panel.ballots[source]
        deviations = [abs(ballot[team] - consensus_rank[team]) for team in consensus_order]
        own = [ballot[team] for team in consensus_order]
        consensus_vector = [consensus_rank[team] for team in consensus_order]
        rho = spearman(own, consensus_vector)
        others = []
        for other in matrix:
            if other == source:
                continue
            rho_other = spearman(
                [ballot[team] for team in consensus_order],
                [panel.ballots[other][team] for team in consensus_order],
            )
            if not math.isnan(rho_other):
                others.append(rho_other)
        out.append(
            {
                "source": source,
                "outlet": panel.meta.get(source, {}).get("outlet", source),
                "analyst": panel.meta.get(source, {}).get("analyst", ""),
                "kind": panel.meta.get(source, {}).get("kind", "analyst"),
                "prior_weight": panel.meta.get(source, {}).get("prior_weight", 1.0),
                "mean_abs_dev": mean(deviations),
                "max_abs_dev": max(deviations),
                "rho_consensus": rho,
                "mean_rho_peers": mean(others) if others else float("nan"),
            }
        )
    out.sort(key=lambda row: row["mean_abs_dev"])
    return out


def agreement_matrix(panel: Panel) -> tuple[list[str], list[list[float]]]:
    sources = list(panel.ballots)
    matrix = panel.matrix(require_complete=True)
    size = len(panel.teams)
    grid = []
    for a in sources:
        row = []
        for b in sources:
            row.append(
                spearman(
                    [matrix[a][i] for i in range(size)],
                    [matrix[b][i] for i in range(size)],
                )
            )
        grid.append(row)
    return sources, grid


def render_markdown(
    *,
    week: int,
    season: int,
    rows: list[ConsensusRow],
    diagnostics: Diagnostics,
    panel: Panel,
    source_notes: dict[str, dict],
    generated: datetime,
    matchups: list[dict] | None = None,
    model=None,
    schedule_source: str = "",
) -> str:
    sources = list(panel.ballots)
    lines: list[str] = []
    add = lines.append

    add(f"# NFL Poll of Polls — {season} season, Week {week}")
    add("")
    add(f"Generated {generated.strftime('%Y-%m-%d %H:%M UTC')} from {len(sources)} source ballots.")
    add("")
    add("## Consensus table")
    add("")
    add("| # | Team | Score (z) | 95% CI | Mean rank | Rank range | 95% rank CI | P(#1) |")
    add("|---|------|-----------|--------|-----------|------------|-------------|-------|")
    for row in rows:
        add(
            f"| {row.rank} | {row.team} | {row.score:+.3f} | "
            f"[{row.ci_low:+.3f}, {row.ci_high:+.3f}] | {row.mean_rank:.2f} | "
            f"{row.rank_min}–{row.rank_max} | {row.rank_ci_low}–{row.rank_ci_high} | "
            f"{row.p_top1 * 100:.0f}% |"
        )
    add("")

    add("## Ballots")
    add("")
    header = "| Team | " + " | ".join(sources) + " |"
    add(header)
    add("|" + "---|" * (len(sources) + 1))
    for row in rows:
        cells = [str(row.by_source.get(source, "")) for source in sources]
        add(f"| {row.team} | " + " | ".join(cells) + " |")
    add("")

    add("## Pairwise Spearman agreement")
    add("")
    add("| | " + " | ".join(sources) + " |")
    add("|" + "---|" * (len(sources) + 1))
    _, grid = agreement_matrix(panel)
    for i, source in enumerate(sources):
        cells = [f"{grid[i][j]:.2f}" for j in range(len(sources))]
        add(f"| {source} | " + " | ".join(cells) + " |")
    add("")

    add("## Source diagnostics")
    add("")
    add("| Source | Analyst | Mean deviation (positions) | Max deviation | ρ vs peers |")
    add("|--------|---------|----------------------------|---------------|------------|")
    for row in source_diagnostics(panel, rows):
        add(
            f"| {row['outlet']} | {row['analyst']} | {row['mean_abs_dev']:.2f} | "
            f"{row['max_abs_dev']} | {row['mean_rho_peers']:.2f} |"
        )
    add("")

    add("## Variance components")
    add("")
    add(f"- Sources in panel: **{diagnostics.n_sources}**")
    add(f"- Teams: **{diagnostics.n_teams}**")
    add(f"- Within-team variance (σ_w²): **{diagnostics.within_variance:.4f}**")
    add(f"- Between-team variance (σ_b²): **{diagnostics.between_variance:.4f}**")
    add(f"- Shrinkage reliability λ: **{diagnostics.reliability:.3f}**")
    add(f"- Effective independent sources (from split-half ρ): **{diagnostics.effective_sources:.2f}**")
    add(f"- Mean pairwise Spearman: **{diagnostics.mean_pairwise_spearman:.3f}**")
    add(f"- Split-half ρ → Spearman-Brown reliability: **{diagnostics.split_half_reliability:.3f}**")
    add("")

    add("## Most contested teams (rank range across sources)")
    add("")
    for team, spread in diagnostics.most_contested:
        add(f"- {team}: {spread} positions")
    add("")

    if matchups:
        add("## Head to head")
        add("")
        if model is not None:
            add(
                f"Model: {model.source}. "
                f"k = {model.k} pts per z, home field {model.home_field} pts, "
                f"sigma = {model.sigma} pts."
            )
            add("")
        if schedule_source:
            add(f"Schedule: {schedule_source}")
            add("")
        add("| Away | Home | Projected margin | P(home) | Pick | Market | Model − market |")
        add("|------|------|------------------|---------|------|--------|----------------|")
        for record in matchups:
            market = record.get("marketSpread")
            delta = ""
            if market is not None:
                delta = f"{record['expectedMargin'] - market:+.1f}"
                market = f"{market:+.1f}"
            else:
                market = "n/a"
            add(
                f"| {record['awayAbbr']} | {record['homeAbbr']} | "
                f"{record['expectedMargin']:+.1f} | {record['homeWinProbability']:.1%} | "
                f"{record['pick']} | {market} | {delta} |"
            )
        add("")

    add("## Source notes")
    add("")
    for source, note in source_notes.items():
        add(f"- **{note.get('outlet', source)}** ({note.get('analyst', '')}) — {note.get('tier', '')}")
        add(f"  - URL: {note.get('url', 'n/a')}")
        add(f"  - Parser: `{note.get('extract', '')}`")
    add("")
    return "\n".join(lines)


def build_site_bundle(
    *,
    week: int,
    season: int,
    rows: list[ConsensusRow],
    diagnostics: Diagnostics,
    panel: Panel,
    source_meta: dict[str, dict],
    generated: datetime,
    method_note: str,
    matchups: list[dict] | None = None,
    model=None,
    h2h_method_note: str = "",
    schedule_source: str = "",
) -> dict:
    sources = list(panel.ballots)
    source_diag = {row["source"]: row for row in source_diagnostics(panel, rows)}

    source_list = []
    for source in sources:
        meta = source_meta.get(source, {})
        diag = source_diag.get(source, {})
        source_list.append(
            {
                "id": source,
                "outlet": meta.get("outlet", source),
                "analyst": meta.get("analyst", ""),
                "kind": meta.get("kind", "analyst"),
                "tier": meta.get("tier", ""),
                "url": meta.get("url", ""),
                "prior_weight": meta.get("prior_weight", 1.0),
                "mean_abs_dev": round(diag.get("mean_abs_dev", float("nan")), 2),
                "rho_consensus": round(diag.get("rho_consensus", float("nan")), 3),
                "mean_rho_peers": round(diag.get("mean_rho_peers", float("nan")), 3),
            }
        )

    teams_payload = []
    for row in rows:
        conf, div = TEAMS[row.team][1], TEAMS[row.team][2]
        teams_payload.append(
            {
                "team": row.team,
                "abbr": TEAMS[row.team][0],
                "conference": conf,
                "division": div,
                "rank": row.rank,
                "score": round(row.score, 4),
                "scoreRaw": round(row.score_raw, 4),
                "se": round(row.se, 4),
                "ciLow": round(row.ci_low, 4),
                "ciHigh": round(row.ci_high, 4),
                "meanRank": round(row.mean_rank, 2),
                "medianRank": round(row.median_rank, 2),
                "rankSd": round(row.rank_sd, 2),
                "rankMin": row.rank_min,
                "rankMax": row.rank_max,
                "rankCiLow": row.rank_ci_low,
                "rankCiHigh": row.rank_ci_high,
                "pTop1": round(row.p_top1, 4),
                "pTop5": round(row.p_top5, 4),
                "spread": row.spread,
                "bySource": row.by_source,
            }
        )

    _, grid = agreement_matrix(panel)
    agreement = [
        {"source": source, "values": [round(value, 3) for value in grid[i]]}
        for i, source in enumerate(sources)
    ]

    head_to_head = None
    if matchups:
        head_to_head = {
            "method": h2h_method_note,
            "scheduleSource": schedule_source,
            "model": model.as_dict() if model is not None else None,
            "games": [
                {
                    "away": record["away"],
                    "home": record["home"],
                    "awayAbbr": record["awayAbbr"],
                    "homeAbbr": record["homeAbbr"],
                    "awayScore": round(record["awayScore"], 4),
                    "homeScore": round(record["homeScore"], 4),
                    "expectedMargin": round(record["expectedMargin"], 2),
                    "homeWinProbability": round(record["homeWinProbability"], 4),
                    "awayWinProbability": round(record["awayWinProbability"], 4),
                    "pick": record["pick"],
                    "gameday": record.get("gameday", ""),
                    "kickoff": record.get("kickoff", ""),
                    "neutral": bool(record.get("neutral", False)),
                    "marketSpread": record.get("marketSpread"),
                }
                for record in matchups
            ],
        }

    return {
        "week": week,
        "season": season,
        "generated": generated.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "method": method_note,
        "headToHead": head_to_head,
        "diagnostics": {
            "sources": diagnostics.n_sources,
            "teams": diagnostics.n_teams,
            "withinVariance": round(diagnostics.within_variance, 4),
            "betweenVariance": round(diagnostics.between_variance, 4),
            "reliability": round(diagnostics.reliability, 4),
            "meanPairwiseSpearman": round(diagnostics.mean_pairwise_spearman, 4),
            "splitHalfReliability": round(diagnostics.split_half_reliability, 4),
            "effectiveSources": round(diagnostics.effective_sources, 3),
        },
        "sources": source_list,
        "teams": teams_payload,
        "agreement": agreement,
        "mostContested": [
            {"team": team, "spread": spread} for team, spread in diagnostics.most_contested
        ],
        "byDivision": diagnostics.consensus_by_division,
    }


def write_json(path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
