"""Per-source parsers.

Each parser takes the raw HTML of one weekly ranking page and returns a dict
mapping canonical team name -> ordinal rank (1..32, lower is better).

Design rules, learned the hard way from these pages:

1.  All rank extraction is **ordinal, never positional**. A parser must find
    the rank number that the publication itself printed; it may not infer rank
    from the order in which a team appears in the document. This is what keeps
    the pipeline honest: several of these pages are written in reverse sidebars,
    photo galleries, or index pages where a team's markup order means nothing.

2.  Every result is validated by the caller (see validate.py): exactly one
    occurrence of each of the 32 canonical teams, ranks forming 1..32. A parser
    that returns a partial or duplicated table fails the build instead of
    quietly contributing bad data.

3.  Parsers deliberately discard prose. Only the rank marker and the team name
    cross the boundary; record, previous rank, and commentary are dropped.
"""

from __future__ import annotations

import html
import json
import re

from . import teams

# --- text normalisation ----------------------------------------------------


def to_text(html_source: str) -> str:
    """Strip tags while preserving block boundaries as newlines.

    Newlines are the unit the numbered-table parser works in, and dropping
    scripts/styles first is what keeps inline JS from impersonating a table.
    Both opening and closing block tags emit a newline: some of these pages
    (USA Today) close paragraphs implicitly, so only reacting to ``</p>`` would
    glue consecutive ranking entries onto one line.
    """
    text = re.sub(
        r"<(script|style|noscript|svg|template)\b[^>]*>.*?</\1>",
        " ",
        html_source,
        flags=re.S | re.I,
    )
    text = re.sub(r"<(br|hr)\s*/?>", "\n", text, flags=re.I)
    text = re.sub(
        r"</?(p|div|li|tr|h[1-6]|section|article|figcaption|aside|blockquote)\b[^>]*>",
        "\n",
        text,
        flags=re.I,
    )
    text = re.sub(r"<[^>]+>", "|", text)
    text = html.unescape(text)
    text = text.replace("\u00a0", " ").replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    # A bare "|" is a tag boundary; collapse runs of them plus spaces. Newlines
    # are preserved because they delimit list entries after block tags.
    text = re.sub(r"[ \t]*\|[ \t|]*", "|", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def _clean(line: str) -> str:
    """Collapse a line to a single-line probe with no tag boundaries left."""
    cleaned = line.replace("|", " ").replace("*", " ").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", cleaned).strip()


# --- generic numbered table ------------------------------------------------

_NUMBERED = re.compile(r"^\s*(\d{1,2})[.\u2013\u2014)-]\s*\|?\s*([A-Za-z][^|(]{2,40})")


def _strip_tags(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment)).replace("\u00a0", " ")


def numbered_table(raw: str, *, max_rank: int = 32) -> dict[str, int]:
    """Extract 'N. Team Name' headings, resolving names via teams.normalize.

    Works for Sports Illustrated, USA Today, theScore and Sporting News, which
    all print the rank next to the club name in the article body. Each physical
    line is collapsed to a single probe string first, so markup that wraps the
    rank and the club in separate inline spans still parses. False positives
    are rejected by the resolver: a line whose "name" is not a real club is
    dropped, and the first rank seen for a club wins.
    """
    text = to_text(raw)
    found: dict[str, int] = {}
    for line in text.splitlines():
        probe = _clean(line)
        match = _NUMBERED.match(probe)
        if not match:
            continue
        rank = int(match.group(1))
        if not 1 <= rank <= max_rank:
            continue
        name = re.split(r"\s+[(\u2013\u2014-]", match.group(2), maxsplit=1)[0]
        canonical = teams.normalize(name)
        if canonical and canonical not in found:
            found[canonical] = rank
    return found


# --- NFL.com ---------------------------------------------------------------


def nflcom_rank_marker(raw: str) -> dict[str, int]:
    """NFL.com marks each entry with ``aria-label="Rank N"``.

    The accessible label is the sturdiest hook on the page: it is repeated on
    all 32 cards, it is stable across cosmetic redesigns, and it means the rank
    is read straight out of the markup instead of inferred from layout. Within
    each card the club name is the last resolvable team token before the W-L
    record, so we read the two independently and cross-check the rank set
    downstream.
    """
    blocks = re.findall(
        r'aria-label="Rank (\d{1,2})"[^>]*>(.*?)(?=aria-label="Rank \d{1,2}"|$)',
        raw,
        re.S | re.I,
    )
    found: dict[str, int] = {}
    for rank_text, block in blocks:
        rank = int(rank_text)
        record = re.search(r"\b(\d{1,2}-\d{1,2}(?:-\d{1,2})?)\b", to_text(block))
        if not record:
            continue
        before = to_text(block)[: record.start()]
        for token in reversed([t.strip() for t in before.split("|") if t.strip()]):
            canonical = teams.normalize(token)
            if canonical:
                found.setdefault(canonical, rank)
                break
    return found


def nflcom_reynolds(raw: str) -> dict[str, int]:
    """Neil Reynolds' column splits the list across ``<ol start="N">`` blocks.

    Each entry is ``<ol start="23"><li><strong>Indianapolis Colts -5</strong>``
    so the list attribute carries the rank and the strong tag carries the club
    plus a signed movement value. The first list has no ``start`` attribute and
    implicitly begins at 1. We read the rank directly rather than trusting
    document order, which a sidebar could otherwise poison.
    """
    ordered: dict[str, int] = {}
    implicit = 0
    for match in re.finditer(r"<ol\b([^>]*)>(.*?)</ol>", raw, re.S | re.I):
        attributes, body = match.group(1), match.group(2)
        start = re.search(r"\bstart=[\"']?(\d{1,2})", attributes, re.I)
        implicit = int(start.group(1)) if start else implicit + 1
        strong = re.search(r"<strong>(.*?)</strong>", body, re.S | re.I)
        if not strong:
            continue
        label = _strip_tags(strong.group(1))
        label = re.sub(r"[\s\u00a0]*[+-]?\d{1,2}\s*$", "", label)
        canonical = teams.normalize(label)
        if canonical and canonical not in ordered:
            ordered[canonical] = implicit
    if len(ordered) != 32:
        # Layout changed: fall back to the generic "N. Team" scan.
        return numbered_table(raw)
    return ordered


# --- CBS Sports ------------------------------------------------------------

_CBS_ROW = re.compile(
    r'<tr[^>]*class="[^"]*team-rankings-stats[^"]*"[^>]*>(.*?)</tr>', re.S | re.I
)
_CBS_RANK = re.compile(r'class="rank"[^>]*>\s*(\d{1,2})\s*<', re.I)
_CBS_TEAM = re.compile(r'class="team-name"[^>]*>\s*([^<]+?)\s*<', re.I)


def cbs_table(raw: str) -> dict[str, int]:
    """CBS renders the full ranking as a real ``<table>`` with a .rank cell.

    During the season the hub page (/nfl/powerrankings/) carries the current
    table; the per-week column page is a superset. Parsing the table means a
    layout change in the article prose cannot corrupt the data.
    """
    found: dict[str, int] = {}
    for row in _CBS_ROW.findall(raw):
        rank_match = _CBS_RANK.search(row)
        team_match = _CBS_TEAM.search(row)
        if not rank_match or not team_match:
            continue
        canonical = teams.normalize(team_match.group(1))
        if canonical:
            found.setdefault(canonical, int(rank_match.group(1)))
    return found


# --- FOX Sports ------------------------------------------------------------

# FOX labels every card anchor with the class "entity-title" and prints the
# rank inside the anchor text ("#7 San Francisco 49ers"), so the anchor is both
# the rank marker and the name marker. The name pattern allows a leading digit
# because "49ers" would otherwise be dropped.
_FOX = re.compile(
    r'class="[^"]*entity-title[^"]*"[^>]*>\s*#(\d{1,2})\s+([^<]{2,40}?)\s*<',
    re.I,
)


def fox_hash(raw: str) -> dict[str, int]:
    """FOX prints ``#12 Seattle Seahawks`` and runs the list 32 -> 1."""
    found: dict[str, int] = {}
    for match in _FOX.finditer(raw):
        canonical = teams.normalize(_strip_tags(match.group(2)))
        if canonical:
            found.setdefault(canonical, int(match.group(1)))
    return found


# --- Sharp Football Analysis ----------------------------------------------

_SHARP_ARRAY = re.compile(
    r'\[\s*\[\s*"Power Rank"\s*,\s*"Team"\s*,\s*"Change"\s*\].*?\]\s*\]', re.S
)


def sharp_embedded_table(raw: str) -> dict[str, int]:
    """Sharp's hub page embeds its ranks as a JSON array of 3-element rows."""
    match = _SHARP_ARRAY.search(raw)
    if not match:
        return {}
    try:
        rows = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
    found: dict[str, int] = {}
    for row in rows[1:]:
        if not isinstance(row, list) or len(row) < 2:
            continue
        try:
            rank = int(str(row[0]).strip())
        except ValueError:
            continue
        canonical = teams.normalize(str(row[1]))
        if canonical:
            found.setdefault(canonical, rank)
    return found


# --- dispatch --------------------------------------------------------------

EXTRACTORS = {
    "nflcom_rank_marker": nflcom_rank_marker,
    "nflcom_reynolds": nflcom_reynolds,
    "cbs_table": cbs_table,
    "fox_hash": fox_hash,
    "sharp_embedded_table": sharp_embedded_table,
    "si_numbered": numbered_table,
    "usatoday_numbered": numbered_table,
    "thescore_numbered": numbered_table,
    "sportingnews_numbered": numbered_table,
}


def extract(extractor: str, raw: str) -> dict[str, int]:
    if extractor not in EXTRACTORS:
        raise KeyError(f"unknown extractor {extractor!r}")
    return EXTRACTORS[extractor](raw)
