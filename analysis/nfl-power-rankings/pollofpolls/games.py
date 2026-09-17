"""The week's schedule: which teams play, where, and when.

Source
------
`nflverse` publishes the NFL's own schedule and results as a single open CSV
(`nfldata/data/games.csv`). It is the primary source here because it is
machine-readable, covers every season, and carries closing spreads, which
`tools/calibrate.py` uses as an independent benchmark.

`parse_nflcom_schedule` is the documented fallback: it reads the score-strip
markup on nfl.com's schedules page, which is enough to reconstruct a slate
without any third-party dataset. It is used when the CSV is unavailable and is
covered by tests, but it does not carry times as richly nor any market data.

Team identity runs through `teams.normalize`, so nflverse's abbreviations
(`LA`, `WAS`), nfl.com's nicknames (`Rams`, `Commanders`) and full names all
resolve to the same canonical keys used everywhere else in the pipeline.
"""

from __future__ import annotations

import csv
import io
import re
import urllib.request
from dataclasses import dataclass, field
from datetime import date

from .teams import normalize
from .fetch import USER_AGENT, FetchError

NFLVERSE_GAMES = "https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv"
NFLCOM_SCHEDULE = "https://www.nfl.com/schedules/{season}/REG{week}/"


@dataclass
class Game:
    away: str
    home: str
    season: int
    week: int
    gameday: str = ""
    kickoff: str = ""
    venue: str = ""
    neutral: bool = False
    spread: float | None = None  # closing line, home perspective, if published
    away_score: int | None = None
    home_score: int | None = None

    @property
    def played(self) -> bool:
        return self.home_score is not None and self.away_score is not None

    @property
    def margin(self) -> int | None:
        if not self.played:
            return None
        return int(self.home_score) - int(self.away_score)  # type: ignore[arg-type]


def _resolve(raw: str) -> str:
    canonical = normalize(raw)
    if canonical is None:
        raise FetchError(f"schedule: cannot resolve team {raw!r}")
    return canonical


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if value in ("", "NA", "NaN"):
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value in ("", "NA", "NaN"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_nflverse_games(csv_text: str, *, season: int, week: int) -> list[Game]:
    """Filter the nflverse games CSV down to one regular-season week."""
    games: list[Game] = []
    for row in csv.DictReader(io.StringIO(csv_text)):
        if row.get("season") != str(season) or row.get("week") != str(week):
            continue
        if row.get("game_type") != "REG":
            continue
        try:
            away, home = _resolve(row["away_team"]), _resolve(row["home_team"])
        except (KeyError, FetchError):
            continue
        location = (row.get("location") or "").strip().lower()
        games.append(
            Game(
                away=away,
                home=home,
                season=season,
                week=week,
                gameday=(row.get("gameday") or "").strip(),
                kickoff=(row.get("gametime") or "").strip(),
                venue=(row.get("stadium") or "").strip(),
                # nflverse marks international/neutral-site games explicitly.
                neutral=location in ("neutral", "international"),
                spread=_to_float(row.get("spread_line")),
                away_score=_to_int(row.get("away_score")),
                home_score=_to_int(row.get("home_score")),
            )
        )
    games.sort(key=lambda g: (g.gameday, g.kickoff, g.away))
    return games


_GAME_LINK = re.compile(
    r"linkName&quot;:&quot;"
    r"(?P<away>[A-Za-z0-9 .'\-]+?) at (?P<home>[A-Za-z0-9 .'\-]+?), "
    r"(?P<weekday>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), "
    r"(?P<day>[A-Z][a-z]+ \d{1,2}(?:st|nd|rd|th)), "
    r"(?P<time>\d{1,2}:\d{2} [AP]M), "
    r"(?P<network>[A-Za-z0-9+ ]+?)&quot;"
)

_MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
}


def parse_nflcom_schedule(html: str, *, season: int, week: int) -> list[Game]:
    """Fallback parser for the nfl.com score-strip markup.

    Each card emits an analytics label of the form
    ``"<Away> at <Home>, <Weekday>, <Month> <D>, <time>, <network>"``. The team
    pattern deliberately allows a leading digit: "49ers" would otherwise be
    dropped, exactly as it was from the logo set.
    """
    games: list[Game] = []
    seen: set[tuple[str, str]] = set()
    for match in _GAME_LINK.finditer(html):
        try:
            away, home = _resolve(match.group("away")), _resolve(match.group("home"))
        except FetchError:
            continue
        if (away, home) in seen:
            continue
        seen.add((away, home))
        day = match.group("day")
        month_name, _, day_number = day.partition(" ")
        digits = re.sub(r"\D", "", day_number)
        gameday = ""
        if month_name in _MONTHS and digits:
            try:
                gameday = date(season, _MONTHS[month_name], int(digits)).isoformat()
            except ValueError:
                gameday = ""
        games.append(
            Game(
                away=away,
                home=home,
                season=season,
                week=week,
                gameday=gameday,
                kickoff=match.group("time"),
            )
        )
    games.sort(key=lambda g: (g.gameday, g.kickoff, g.away))
    return games


def fetch_nflverse_games(timeout: float = 40.0) -> str:
    request = urllib.request.Request(NFLVERSE_GAMES, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_nflcom_schedule(season: int, week: int, timeout: float = 30.0) -> str:
    url = NFLCOM_SCHEDULE.format(season=season, week=week)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def remaining_bye_teams(all_teams: list[str], games: list[Game]) -> list[str]:
    """Teams with no game this week (byes, or a schedule gap)."""
    playing = {team for game in games for team in (game.home, game.away)}
    return sorted(team for team in all_teams if team not in playing)
