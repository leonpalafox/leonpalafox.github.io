# NFL poll of polls

A reproducible, statistically explicit consensus NFL power ranking built from
multiple public weekly rankings. Pure Python standard library — no `numpy`,
`pandas`, or `requests` — so a fresh clone can re-run any archived week on any
machine with Python 3.10+.

The published write-up lives in the blog:
`src/content/blog/nfl-power-rankings-poll-of-polls.md`.

## Gotcha: the post body styles the widget

The blog widget is embedded in a post, so it renders inside `.prose-post`
(`src/styles/global.css`). Those article styles are unscoped and apply to
everything nested in the post, including the widget's internals. Two of them
caused visible defects that took a while to trace:

*   `prose-post img` draws a `1px` frame and `margin-block: 1.8em` around every
    image. It framed each logo `<img>` inside its circular badge, which read as
    a stray square outline on every team.
*   `prose-post th/td` draw full cell borders and a tinted header, and
    `prose-post table` adds margins — turning the widget's deliberately minimal
    table into a boxed grid.

The post's `<style>` block therefore opens with an explicit reset for `img`,
`table`, `th` and `td` inside `.pop-root`, and the widget styles paint from
there. Anything else added to the widget should assume the prose styles are in
play and reset what it does not want.

## Quick start

```bash
cd analysis/nfl-power-rankings

python3 -m unittest discover -s tests     # 28 tests, no network needed
python3 run.py --validate                 # fetch, parse, validate; write nothing
python3 run.py                            # full run, writes site data too
python3 run.py --offline                  # re-analyse from the HTML cache
python3 run.py --from-dir /path/to/html   # parse local fixtures instead of HTTP
```

There are no dependencies to install. `run.py` is the only entry point you
need.

## What a run produces

| Path | Contents |
|------|----------|
| `out/report.md` | Human-readable audit trail: consensus table, every ballot, the agreement matrix, variance components, source diagnostics, contested teams |
| `out/consensus.json` | The full machine-readable payload (same numbers, plus per-team source detail) |
| `out/ballots.json` | Raw per-source ballots — the input, archived next to the output |
| `out/matchups.csv` | One row per game for the week: projected margin, win probability, pick, closing line, with score columns left empty for grading |
| `out/site-data.json` | Compact bundle for the blog widget |
| `src/data/nfl-power-rankings-<season>-wk<NN>.json` | Week-stamped copy consumed by the Astro post |
| `src/data/nfl-power-rankings-latest.json` | Same bundle, stable filename |
| `public/images/nfl/<abbr>.svg` | The 32 club marks used by the widget (see below) |
| `cache/<season>-wk<NN>/<source>.html` | Raw HTML per source, so a run can be replayed offline |

### Club marks

The widget renders one logo per team from `public/images/nfl/`. Those files are
committed static assets, not fetched during a run or a site build, because the
marks change roughly once a decade and a build that depends on a third-party
CDN can fail for reasons unrelated to this article. Refresh the set on demand:

```bash
python3 tools/fetch_logos.py          # fetch anything missing
python3 tools/fetch_logos.py --force  # re-download all 32
```

Logos come from the NFL's own image CDN as vector marks and are used for
identification only. If an asset is ever missing the widget hides the broken
image and falls back to a text-only row.

The downloaded marks all claim a 500x500 canvas but use between 72% and 96% of
it, so sizing them with one CSS value would leave some touching the rim of the
circular badge and others floating in the middle. `tools/normalize_logos.py`
rewrites each `viewBox` to that mark's ink bounds plus a 4% margin, which leaves
the artwork untouched and makes every mark fill the same fraction of its canvas:

```bash
# 1. render each SVG to a 500x500 PNG (any headless browser, one file per mark)
# 2. measure the renders and rewrite the viewBoxes
python3 tools/normalize_logos.py --png-dir /tmp/ink --check   # report only
python3 tools/normalize_logos.py --png-dir /tmp/ink
```

It measures ink from **rendered pixels**, not from path data: cubic Bezier
control points sit outside the curves they steer, so a geometry-based bounding
box is far too large, and these files use implicit command repetition besides.
It also removes the full-canvas background plate that eleven of the marks carry
(`<path d="M0 0h500v500H0z"/>`), which paints nothing useful on the widget's own
disc.

Two rules matter, and both were learned from visible artifacts on the published
page:

*   **The frame must not hug the artwork.** If ink reaches the image edge the
    browser anti-aliases that boundary, and white parts of a mark then show a
    square seam against the badge behind them. Each mark is framed in a square
    at least as large as the original 500-unit canvas, so the ink stays interior.
*   **The badge must not stack circular treatments.** A radial gradient plus an
    inset ring plus multiple halos each draw a circle in the same few pixels and
    dither into visible concentric rings at 30px. The widget uses a flat white
    disc, one hairline ring and one halo.

Only re-run the tool if the marks are replaced.

## Pipeline shape

```
sources.json ──▶ fetch ──▶ sources.extract ──▶ validate ──▶ stats.consensus ──▶ report
   registry      cache      per-outlet parser     gate       standardise,        md + json
                                                             shrink, bootstrap
```

- `pollofpolls/teams.py` — canonical club identity; resolves "49ers",
  "L.A. Rams", "Jags", "SEA" to one key and rejects prose.
- `pollofpolls/fetch.py` — per-source HTTP with an on-disk cache, retries, and
  an explicit offline mode.
- `pollofpolls/sources.py` — one parser per outlet. All ordinal: every parser
  reads the rank the publication printed and never document position.
- `pollofpolls/validate.py` — hard gate: 32 distinct clubs, ranks a permutation
  of 1..32, at least 5 complete ballots, no two identical ballots.
- `pollofpolls/stats.py` — standardisation, jackknife uncertainty,
  empirical-Bayes shrinkage, bootstrap rank intervals. See `METHODOLOGY.md`.
- `pollofpolls/report.py` — Markdown audit trail and the site data bundle.

## Head to head

The blog's win probabilities come from the consensus score plus three fitted
constants (`model.json`):

```
margin = k * (score_home - score_away) + H        k = 4.59, H = 2.56
P(home wins) = Phi(margin / sigma)                sigma = 13.16
```

Refit them from completed seasons at any time:

```bash
python3 tools/calibrate.py                    # download nflverse and fit every season
python3 tools/calibrate.py --season 2025     # inspect one season
python3 tools/calibrate.py --csv games.csv --write   # offline, refresh model.json
```

`calibrate.py` fits `k` and `H` by least squares on realised margins (leave-one-out
ratings) and takes `sigma` from the residual spread. It deliberately does **not**
tune the constants by minimising log-loss: only the ratios `k/sigma` and
`H/sigma` affect the win/loss likelihood, so that objective has a flat ridge and
returns an arbitrary scale. `METHODOLOGY.md` §9.1 shows the two grids that
produced identical log-loss with `k` of 5.7 and 8.25 respectively.

The week's schedule comes from the nflverse games CSV (`pollofpolls/games.py`),
which also carries closing spreads used only as a benchmark. There is a
documented fallback parser for nfl.com's score strip if the CSV is unavailable.

## What the reader-facing bundle contains

`build_site_bundle` in `pollofpolls/report.py` emits everything the post needs,
so the page stays static and no Python runs at build time:

- **`teams`** — consensus scores, intervals, bootstrap rank ranges, and every
  source's ballot per team. Each entry carries `conference` and `division`,
  which is what the widget's AFC / NFC filters and division grouping read.
- **`sources`** — outlet, analyst, URL and agreement metrics.
- **`agreement`** — the pairwise Spearman matrix.
- **`headToHead`** — the week's schedule, the model constants, and a priced
  record per game (`expectedMargin`, `homeWinProbability`, `pick`,
  `marketSpread`).

The post renders two widgets from it. The consensus table has a table of
contents above it and filter chips for conference, playoff picture and
contested teams; a conference filter regroups the rows by division and
renumbers them within the filtered set, keeping the league-wide rank in a
separate `Panel` column so the anchor is never lost. The head-to-head widget
lists the week's slate and lets a reader build any matchup.

## Adding or changing sources

`SOURCES.md` is the operating manual: the full inventory, per-source structure
and failure modes, a weekly replication checklist, the excluded-source list,
and the exact steps for adding a tenth source.

## Determinism

Every random draw is seeded from the registry week (`seed=20260917` in
`run.py`). Two runs over the same cached HTML produce byte-identical
`consensus.json`, apart from the `generated` timestamp. Each cached page's
SHA-256 prefix is recorded in `consensus.json` so a reader can confirm which
bytes produced the published numbers.

## Week-to-week use

1. Update `week` and the discovery-source URLs in `sources.json` (see the
   checklist in `SOURCES.md`).
2. `python3 run.py`
3. Point the blog post at the new week's bundle and rebuild the site.

The post imports `src/data/nfl-power-rankings-latest.json`, so step 3 is a
one-line edit at most.
