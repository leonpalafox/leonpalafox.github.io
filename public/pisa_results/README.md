# PISA 2025 score-change map

The site presents the geographic gradient of **changes in system mean scores**:
2025 minus 2022, or OECD fitted decennial trends within the 2015–2025 window.
It does not measure a socioeconomic gradient or individual students' learning gains.
Current mean score levels appear in the table.

Open `index.html`, or serve this directory with `python3 -m http.server 4322`.
The visualization and data are embedded in the page; optional fonts come from Google.
Keep `build/` and `audit/` available if publishing the source and audit download links.

## Rebuild and verify

Requires Python 3 and `openpyxl==3.1.5` (see `build/requirements.txt`).

```sh
python3 build/build_data.py
python3 build/assemble.py
python3 build/validate_data.py
python3 -m unittest discover -s tests
```

Commands work from any directory when given the appropriate script path.
`assemble.py` validates source checksums and numeric evidence before producing HTML.
The source snapshots are included in `build/sources/`; no download is needed to rebuild.
`manifest.json` records retrieval dates, official URLs and SHA-256 checksums.
The source PDF's text was generated with `pdftotext -layout report.pdf pisa.txt`.
Do not update a checksum merely to silence an error: review OECD revisions, re-extract
PDF text when applicable, and rerun the audit.

## Data lineage

- OECD annex workbook, https://stat.link/mrq53f: means and standard errors in Tables
  I.B1.2a.1–4; short-term changes and fitted trends in I.B1.2a.36–38.
- Chapter workbook, https://stat.link/xgs41b: independent cross-check of every
  comparison and significance flag in Tables I.2.6 and I.2.9.
- Report Table I.1: independent check of the 91-system roster, rounded means and
  missing values. Reader's Guide: sampling cautions and reporting restrictions.
- OECD trend tiles use **OECD average-35**, directly from the annex.
- Short-term significance uses a two-sided normal test with the published difference
  standard error (including linking uncertainty); decennial significance uses published
  p-values. All overlapping flags match the chapter workbook.
- Each numeric observation in `pisa_data.json` includes a source sheet, cell, unrounded
  estimate and standard error. Display is rounded; map bands and rankings use raw values.
- Albania's trends are deliberately suppressed per the Reader's Guide even where
  numerical annex cells exist. Other missing/suppressed values are never zero-filled.
- Geography: Natural Earth through pinned world-atlas 2.0.2. Regional samples use
  approximate locator circles, not whole-country fills.

See [the audit](audit/AUDIT.md) for corrected errors, verification scope and limitations.
This validates fidelity to the published OECD estimates, not the underlying student
microdata or freedom from sampling/non-response bias.

## Browser audit

`audit/browser-check.mjs` uses Node 22+ and an existing headless Chrome debugging
session at port 9223, with the site served at port 4322. Set `AXE_PATH` to a local
axe-core browser bundle. It checks all 12 subject/period/highlight combinations,
sorting, tooltips, zoom/reset, and light/dark WCAG A/AA rules. Results and screenshots
are retained in `audit/`. Automated accessibility checks are not a full conformance audit.
