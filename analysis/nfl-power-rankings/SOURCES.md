# Source reference — how to rebuild one week's poll of polls

This is the operating manual. It documents every outlet in the panel, exactly
where its weekly ranking lives, how the pipeline reads it, what can go wrong,
and the checks that must pass before the numbers are published.

Everything here is written so that one person can reproduce a week's consensus
from scratch in about ten minutes, and so that a reader six months from now can
tell whether a source changed its format or its methodology.

**Panel week documented here:** 2026 season, Week 2 (published 2026-09-15/16).
**Sources in panel:** 9. **Teams per ballot:** 32. **Minimum accepted:** 5.

---

## 1. Why these nine

Three rules decided inclusion:

1. **Full ballots only.** A source must publish an explicit 1-through-32
   ranking. Roundups that only cover one team, or partial lists, are excluded
   because they cannot be validated as a permutation.
2. **One voice per desk.** NFL.com contributes twice (Nick Shook and Neil
   Reynolds). That is deliberate: they are separate writers with separate
   columns. Two URLs that resolve to the same syndicated copy are rejected
   automatically by `validate.validate_panel`.
3. **Reproducible retrieval.** If a page cannot be fetched with a plain HTTP
   GET, or requires a logged-in browser, it is out of the panel — the pipeline
   has to run unattended every week. This is why ESPN is documented in
   [§6](#6-excluded-sources-and-why) rather than included.

The panel deliberately mixes league-owned editorial (NFL.com), national
newspapers (USA Today), legacy sports desks (CBS, SI, FOX, Sporting News),
analytics shops (Sharp Football) and youth-facing digital desks (theScore).
The agreement matrix in `out/report.md` shows the payoff: correlations run
0.86–0.97, so the panel is not nine copies of one opinion.

---

## 2. Inventory

| id | Outlet | Analyst | Retrieval | URL pattern | Parser | Prior weight |
|----|--------|---------|-----------|-------------|--------|--------------|
| `nflcom-shook` | NFL.com | Nick Shook | **templated** | `nfl.com/news/nfl-power-rankings-week-{week}-{season}-nfl-season` | `nflcom_rank_marker` | 1.00 |
| `nflcom-reynolds` | NFL.com UK | Neil Reynolds | **templated** | `nfl.com/news/neil-reynolds-week-{week}-power-rankings-{season}` | `nflcom_reynolds` | 0.85 |
| `cbs-prisco` | CBS Sports | Pete Prisco | templated + hub fallback | `cbssports.com/nfl/news/priscos-nfl-week-{week}-power-rankings/` → `/nfl/powerrankings/` | `cbs_table` | 1.00 |
| `si-orr` | Sports Illustrated | Conor Orr | URL discovery | `si.com/nfl/conor-orr-week-{week}-nfl-power-rankings-{slug}` | `si_numbered` | 0.90 |
| `usatoday-davis` | USA Today | Nate Davis | URL discovery | `/story/sports/nfl/columnist/nate-davis/{Y}/{M}/{D}/nfl-power-rankings-…` | `usatoday_numbered` | 0.90 |
| `fox-vacchiano` | FOX Sports | Ralph Vacchiano | templated | `foxsports.com/stories/nfl/{season}-nfl-power-rankings-week-{week}-{slug}` | `fox_hash` | 0.90 |
| `sharp-summerlin` | Sharp Football Analysis | Raymond Summerlin | **fixed hub** | `sharpfootballanalysis.com/analysis/nfl-power-rankings/` | `sharp_embedded_table` | 0.75 |
| `thescore-staff` | theScore | theScore NFL desk | URL discovery | `thescore.com/nfl/news/{id}/{slug}` | `thescore_numbered` | 0.80 |
| `sportingnews-iyer` | Sporting News | Vinnie Iyer | URL discovery | `sportingnews.com/us/nfl/news/{slug}/{hash}` | `sportingnews_numbered` | 0.85 |

`prior_weight` is a credibility prior on [0, 1] used in the weighted pooled
mean. It is **not** a claim about who is right — no source's rankings are
graded against game outcomes here. It encodes a small, explicitly chosen
tiebreak between desks that publish a weekly column with a named analyst and
desks that publish a group product, and it is deliberately compressed into
0.75–1.00 so that no single source can swing the consensus. Changing a weight
is a one-line edit in `sources.json`, and the report prints the weights used.

---

## 3. Per-source reference

### 3.1 NFL.com — Nick Shook · `nflcom-shook`

- **URL:** `https://www.nfl.com/news/nfl-power-rankings-week-2-2026-nfl-season`
- **Cadence:** weekly, Tuesday/Wednesday during the season.
- **Slug:** the only fully templatable pattern in the panel. Verified 200 for
  `week-1-2026`, `week-2-2026` and `week-18-2025`; `week-3-2026` correctly 404s
  before publication.
- **Structure:** 32 cards, each carrying `aria-label="Rank N"` on its rank
  column. Inside a card the club name is the last team token before the `W-L`
  record.
- **Parser:** `nflcom_rank_marker` reads the accessible label directly, then
  resolves the club name from the record's neighbourhood.
- **Failure mode:** if NFL.com ever drops the `aria-label`, the parser returns
  fewer than 32 teams and the run fails validation rather than guessing.
- **Watch for:** the movement widget prints "Rank increased by 2" immediately
  after the rank; a naive `N. Team` scan would read that `2` as a rank.

### 3.2 NFL.com UK — Neil Reynolds · `nflcom-reynolds`

- **URL:** `https://www.nfl.com/news/neil-reynolds-week-2-power-rankings-2026`
- **Cadence:** weekly during the season, but the slug is not reliable for every
  week (`week-1` and `week-3` 404 for 2026). Treat it as a discovery source and
  fall back to the NFL.com power-rankings hub if the template 404s.
- **Structure:** the list is broken into 32 separate `<ol>` blocks. The first
  has no `start` attribute (it is rank 1); every later block carries
  `<ol start="N">` and a `<strong>Team +3</strong>` label.
- **Parser:** `nflcom_reynolds` reads the `start` attribute (defaulting to a
  running counter for the un-numbered first item) and strips the signed
  movement value from the club label.
- **Watch for:** the movement suffix uses `--` when a team is unchanged, and
  the wide layout uses `&nbsp;` padding between club and number.

### 3.3 CBS Sports — Pete Prisco · `cbs-prisco`

- **URL:** `https://www.cbssports.com/nfl/news/priscos-nfl-week-2-power-rankings/`
- **Fallback URL:** `https://www.cbssports.com/nfl/powerrankings/` — the hub
  page renders the current week's table in static HTML and is the more stable
  of the two. The per-week column URL gets headline suffixes in some weeks, so
  the hub is the primary discovery fallback.
- **Structure:** a real `<table>`. Each ranking row has
  `class="team-rankings-stats"` containing `<span class="rank">N</span>` and
  `<span class="team-name">Club</span>`.
- **Parser:** `cbs_table` parses the table rows; prose changes cannot corrupt it.
- **Watch for:** the hub page also embeds the same club names in navigation
  menus. Parsing the table rather than the text is what keeps those out.

### 3.4 Sports Illustrated — Conor Orr · `si-orr`

- **2026 Week 2 URL:**
  `https://www.si.com/nfl/conor-orr-week-2-nfl-power-rankings-high-flying-bears-surge`
- **Cadence:** weekly, Tuesday. **No derivable pattern** — the slug is
  headline-derived, so a new URL must be located each week (SI's NFL index,
  its sitemap, or a search for `site:si.com conor orr power rankings week N`).
- **Structure:** explicit `1. Seattle Seahawks (1–0)` headings followed by
  `Last week's ranking: No. 2` metadata.
- **Parser:** `si_numbered` (generic numbered-table scan).
- **Watch for:** the record uses an en dash; the parser splits the club name at
  the first parenthesis or dash-shaped separator, so the record never leaks
  into the name.

### 3.5 USA Today — Nate Davis · `usatoday-davis`

- **2026 Week 2 URL:**
  `https://www.usatoday.com/story/sports/nfl/columnist/nate-davis/2026/09/15/nfl-power-rankings-week-1-rams-seahawks-bills-bears-49ers/91758615007/`
- **Cadence:** weekly, Monday/Tuesday, sometimes updated the following morning.
- **Structure:** `1. Seattle Seahawks (2):` inside a `<strong>`; the rank and
  the club are wrapped in separate inline elements and paragraphs are closed
  implicitly.
- **Parser:** `usatoday_numbered` (generic numbered-table scan, which collapses
  each line to a single probe before matching).
- **⚠️ Trap:** the Week 2 slug literally reads `week-1`. **The edition number in
  the URL lags the edition.** Always confirm the week from the article `<title>`
  ("NFL power rankings Week 2: …") and never from the slug.
- **Watch for:** links to related stories appear immediately after an entry and
  begin with numbers ("32 things we learned…"). The generic parser ignores
  lines whose leading "name" is not a real club.

### 3.6 FOX Sports — Ralph Vacchiano · `fox-vacchiano`

- **URL:**
  `https://www.foxsports.com/stories/nfl/2026-nfl-power-rankings-week-2-which-teams-suffered-worst-opening-losses`
- **Cadence:** weekly, Tuesday. The `{season}-nfl-power-rankings-week-{week}-`
  prefix is templatable but the trailing headline slug is not, so discovery is
  needed unless the headline is known.
- **Structure:** 32 cards, each with an anchor carrying `class="entity-title"`
  whose text is `#7 San Francisco 49ers`. The list reads **32 → 1**.
- **Parser:** `fox_hash` reads the printed `#N` from the anchor text.
- **Watch for:** the club `49ers` starts with a digit. Any name pattern that
  requires a leading letter silently drops San Francisco. There is a regression
  test for this (`test_fox_hash_allows_digit_leading_names`).
- **Never** infer rank from card order: the page is reversed.

### 3.7 Sharp Football Analysis — Raymond Summerlin · `sharp-summerlin`

- **URL:** `https://www.sharpfootballanalysis.com/analysis/nfl-power-rankings/`
- **Cadence:** updated weekly in place; the page states "Updated: <date>" and
  the title carries "Updated Weekly". Because the URL is fixed, record the
  `Updated:` date in the week's notes.
- **Structure:** an embedded JavaScript array literally headed
  `["Power Rank","Team","Change"]` followed by 32 `[rank, team, change]` rows.
- **Parser:** `sharp_embedded_table` extracts and `json.loads` that array.
- **Watch for:** the hub must genuinely have been refreshed for the week you
  think it has. The consensus pipeline trusts the page, so verify the date.
  This is the one source whose freshness is not visible in its URL.

### 3.8 theScore — theScore NFL desk · `thescore-staff`

- **2026 Week 2 URL:**
  `https://www.thescore.com/nfl/news/3454493/nfl-power-rankings-week-2-early-overreactions-for-every-team`
- **Cadence:** weekly, Tuesday. Opaque numeric article id, so discovery is
  required.
- **Structure:** `1. Buffalo Bills (1-0)` immediately followed by
  `Previous rank: 4`.
- **Parser:** `thescore_numbered` (generic numbered-table scan).
- **Watch for:** one entry in the 2026 Week 2 page broke the pattern
  ("…Chargers 0-1) …" followed by an image on the same line). Because the parser
  collapses each line before matching, the entry still resolved; if a future
  edit hides one, validation fails loudly.

### 3.9 Sporting News — Vinnie Iyer · `sportingnews-iyer`

- **2026 Week 2 URL:**
  `https://www.sportingnews.com/us/nfl/news/nfl-power-rankings-bills-49ers-steelers-rams-chargers-week-2/c66ef9551cbc48cdb0a11d75`
- **Cadence:** weekly. Hash-suffixed slug, so discovery is required.
- **Structure:** `1. Buffalo Bills (previous ranking: 2)` headings.
- **Parser:** `sportingnews_numbered` (generic numbered-table scan).
- **Watch for:** Sporting News ran an agency-wide `403` for automated requests
  from some IP ranges during research. If it 403s persistently, drop it from the
  week and note the panel size — the consensus is designed to survive one
  missing source.

---

## 4. Weekly replication checklist

Run these steps in order every week. Steps 1–3 should take a few minutes; step
5 is the only judgement call.

1. **Resolve the week.** Confirm the current NFL week and that rankings have
   actually been published (most outlets publish Tuesday).
2. **Update `sources.json`.** Set `week` and `season`. For discovery sources
   (SI, USA Today, theScore, Sporting News, FOX), replace the `urls` entry with
   the new week's URL. Do not touch `url_tpl`, `extract`, or `prior_weight`
   unless the outlet changed its format or you are deliberately re-weighting.
3. **Fetch and parse.** From `analysis/nfl-power-rankings/`:

   ```bash
   python3 run.py --validate
   ```

   Every source must report `ok 32/32`. Anything less is a hard failure: fix
   the URL, or fix the parser, or drop the source and say so.
4. **Check freshness.** Open the cached HTML in `cache/<season>-wk<NN>/` for
   any source whose URL is not week-numbered (Sharp, and any hub fallback) and
   confirm the page is dated to this week.
5. **Read the diagnostics before publishing.** The run prints mean pairwise
   ρ, split-half reliability, and shrinkage λ. Sanity bands from the 2026 Week 2
   panel: ρ between 0.85 and 0.97, reliability above 0.90, λ above 0.95. A
   sudden drop means either a source changed its methodology or a parser is
   quietly reading the wrong table — investigate before shipping.
6. **Publish.**

   ```bash
   python3 run.py            # writes src/data/nfl-power-rankings-<season>-wk<NN>.json
   ```

   Then point the blog post at the new week (see `README.md`) and rebuild the
   site.
7. **Archive.** Commit `sources.json`, the new `src/data/*.json`, and
   `out/report.md`. The raw HTML cache is regenerable; commit it only if you
   want a byte-exact archive of what was read.

---

## 5. Adding a tenth source

1. Append an entry to `sources.json` with a unique `id`, the outlet and analyst
   names, `url_tpl` (or `urls`), `prior_weight`, and the `extract` key you are
   about to implement.
2. Implement the parser in `pollofpolls/sources.py`. Two rules are
   non-negotiable:
   - **Read the rank the publication printed.** Never use document position.
   - **Return `{canonical team: rank}` only.** Strip records, movement values
     and prose.
3. Register it in the `EXTRACTORS` dispatch table at the bottom of the file.
4. Add a test in `tests/test_pollofpolls.py` using a minimal inline sample of
   the markup, including any naming trap the site has (digit-leading names,
   reverse ordering, movement widgets).
5. Add a section here following the template in §3: URL, cadence, structure,
   parser, failure modes, traps.
6. Run `python3 -m unittest discover -s tests` and then
   `python3 run.py --validate`.

A source that cannot pass validation is worse than no source: it either
contributes a wrong ballot or inflates the apparent panel size. When in doubt,
leave it out and note the reduced panel in the post.

---

## 5b. Data sources beyond the panel

Two datasets feed the pipeline that are not ranking outlets, and neither is a
voice in the consensus:

| Source | What it provides | Role |
|--------|------------------|------|
| `nflverse` games CSV (`nfldata/data/games.csv`) | Every NFL game with final scores, closing spreads, venue and kickoff | The week's schedule for head-to-head; historical margins for calibration; closing lines as a benchmark only |
| nfl.com schedules page | The same slate as server-rendered markup | Documented fallback when the CSV is unavailable (`pollofpolls/games.py`) |

Both are cached under `cache/`. The schedule is verified against three sources
each week in practice: nflverse, nfl.com's score strip, and — during research —
TheSportsDB, which agreed on the games it carried. TheSportsDB's free tier caps
at five events per season, so it is a spot-check rather than a dependency.

Closing lines never enter a published probability. They exist so the model can
be graded against the market (`METHODOLOGY.md` §9.2), and so a reader can see
where the panel disagrees with it.

## 6. Excluded sources, and why

| Outlet | Status | Reason |
|--------|--------|--------|
| ESPN | **Blocked** | Every URL — including the homepage — returns `HTTP 202` with a zero-byte body, and `site.api.espn.com` returns `403`. This is bot detection, not a bad URL. Requires a headless browser or a different egress IP. |
| The Athletic | Paywalled | `/nfl/power-rankings/` returns 404 to unauthenticated requests. |
| Washington Post | Unreachable | Connection failure from this environment. |
| Yahoo Sports | Not a ballot | Its "power rankings" pieces for 2026 Week 2 were team-specific roundups (one had 5 of 32 clubs). Roundups are useful for context, not for a ballot. |
| RotoWire | Partial | Returned 24 of 32 clubs; the page is a fantasy hub. Cannot be validated as a permutation. |
| Bleacher Report | Not used | A full 32-team panel product is available, but it is a staff aggregate rather than a single analyst's ranking, and its page is ~2.3 MB. Held in reserve as a replacement if a primary source drops. |

If ESPN becomes reachable (or a headless renderer is added), it belongs in the
panel: it is a high-quality weekly ballot. Until then it is documented here so
that the omission is a decision, not an accident.

---

## 7. Known traps, collected

- **USA Today slug weeks lag the edition.** Parse the `<title>`, not the URL.
- **FOX writes the list backwards**, 32 → 1, and has a digit-leading club name.
- **NFL.com's movement widget prints numbers** right after the rank.
- **CBS's hub page embeds club names in navigation**, so parse the table.
- **theScore sometimes folds an entry into the previous line** via an image.
- **Sharp's URL never changes**, so freshness has to be checked by hand.
- **Yahoo-style roundups look like rankings** in search results but are not.
- **Bleacher Report and USA Today syndicate widely** across `*wire.usatoday.com`
  and regional subdomains; two URLs can be one voice. The duplicate-ballot
  check in `validate.validate_panel` exists precisely for this.
