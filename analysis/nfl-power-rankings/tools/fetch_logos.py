#!/usr/bin/env python3
"""Download the 32 club marks used by the blog widget.

The widget renders a logo per team, so the assets must exist before the site is
built. They are committed to `public/images/nfl/` rather than fetched at build
time: the marks change once a decade, and a build that depends on a third-party
CDN is a build that can fail for reasons unrelated to this article.

Run this only to refresh the set:

    python3 tools/fetch_logos.py          # skip files already present
    python3 tools/fetch_logos.py --force  # re-download everything

Source: the NFL's own image CDN, which serves each club mark as a 500x500 SVG
at `.../league/api/clubs/logos/{NFL_CODE}`. Codes are not always the standard
abbreviation (Arizona is AZ, the Rams are LA), so they are mapped explicitly
rather than derived.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from pollofpolls.teams import TEAMS  # noqa: E402

CDN = "https://static.www.nfl.com/f_auto,h_96,q_auto,w_96/league/api/clubs/logos/{code}"
DEST = HERE.parent.parent.parent / "public" / "images" / "nfl"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

# NFL.com's club codes, keyed by canonical team name.
NFL_CODES = {
    "Arizona Cardinals": "AZ",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LA",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args()

    missing = set(TEAMS) - set(NFL_CODES)
    if missing:
        print(f"error: no NFL code mapped for {sorted(missing)}", file=sys.stderr)
        return 2

    DEST.mkdir(parents=True, exist_ok=True)
    written = skipped = 0
    for team in sorted(TEAMS):
        abbr = TEAMS[team][0].lower()
        target = DEST / f"{abbr}.svg"
        if target.exists() and not args.force:
            skipped += 1
            continue
        url = CDN.format(code=NFL_CODES[team])
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                body = response.read()
        except Exception as exc:  # noqa: BLE001 - one-off tool, report and continue
            print(f"  {abbr}: FAILED {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        if b"<svg" not in body[:200]:
            print(f"  {abbr}: unexpected payload, skipped", file=sys.stderr)
            continue
        target.write_bytes(body)
        written += 1
        print(f"  {abbr}.svg  {len(body):>6} bytes  {team}")

    print(f"\n{written} written, {skipped} already present, in {DEST}")
    return 0 if written + skipped == len(TEAMS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
