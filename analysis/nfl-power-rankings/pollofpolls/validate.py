"""Validation gate.

Nothing reaches the statistics unless it passes here. A parser that grabs a
sidebar, drops a team, or double-counts a club must fail loudly: silent partial
data is the failure mode that would make the whole exercise untrustworthy.

Checks per ballot:
  * exactly one entry for each of the 32 canonical teams,
  * ranks form exactly the set {1, ..., 32},
  * every rank is an integer in range.

Checks per panel:
  * at least MIN_SOURCES complete ballots,
  * no two sources are byte-identical (a scraper that resolves two different
    URLs to the same syndicated copy would otherwise double-count one voice).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .teams import TEAMS

MIN_SOURCES = 5
N_TEAMS = len(TEAMS)


@dataclass
class BallotIssue:
    source: str
    severity: str  # "error" | "warning"
    message: str


@dataclass
class ValidationReport:
    issues: list[BallotIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[BallotIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[BallotIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self) -> str:
        lines = []
        for issue in self.issues:
            lines.append(f"[{issue.severity.upper():7}] {issue.source}: {issue.message}")
        return "\n".join(lines) if lines else "all ballots valid"


def validate_ballot(source: str, ballot: dict[str, int]) -> list[BallotIssue]:
    issues: list[BallotIssue] = []

    unknown = [team for team in ballot if team not in TEAMS]
    if unknown:
        issues.append(BallotIssue(source, "error", f"unknown team keys: {unknown[:5]}"))

    missing = [team for team in TEAMS if team not in ballot]
    if missing:
        issues.append(
            BallotIssue(
                source,
                "error",
                f"{len(missing)} of {N_TEAMS} teams missing: {missing[:6]}",
            )
        )

    if ballot:
        ranks = list(ballot.values())
        if not all(isinstance(rank, int) for rank in ranks):
            issues.append(BallotIssue(source, "error", "non-integer rank present"))
        expected = set(range(1, N_TEAMS + 1))
        actual = set(ranks)
        duplicated = sorted(rank for rank in actual if ranks.count(rank) > 1)
        if duplicated:
            issues.append(BallotIssue(source, "error", f"duplicate ranks: {duplicated}"))
        if actual != expected:
            extra = sorted(actual - expected)
            gap = sorted(expected - actual)
            issues.append(
                BallotIssue(
                    source,
                    "error",
                    f"ranks are not a permutation of 1..{N_TEAMS} (extra={extra[:5]}, missing={gap[:5]})",
                )
            )
    return issues


def validate_panel(ballots: dict[str, dict[str, int]]) -> ValidationReport:
    report = ValidationReport()

    for source, ballot in ballots.items():
        report.issues.extend(validate_ballot(source, ballot))

    complete = [
        source
        for source, ballot in ballots.items()
        if len(ballot) == N_TEAMS and set(ballot.values()) == set(range(1, N_TEAMS + 1))
    ]
    if len(complete) < MIN_SOURCES:
        report.issues.append(
            BallotIssue(
                "<panel>",
                "error",
                f"only {len(complete)} complete ballots; need at least {MIN_SOURCES}",
            )
        )

    # Duplicate-source detection: compare ballots after removing the source id.
    seen: dict[tuple[tuple[str, int], ...], str] = {}
    for source in complete:
        signature = tuple(sorted(ballots[source].items()))
        if signature in seen:
            report.issues.append(
                BallotIssue(
                    source,
                    "error",
                    f"identical to {seen[signature]}; likely the same syndicated copy",
                )
            )
        else:
            seen[signature] = source

    return report
