# PISA visual and data audit — 8 September 2026

**Result:** corrected material numeric and presentation errors. The rebuilt site is
traceable to the archived OECD publication and workbooks. No claim of error-free
underlying survey data is made; reported uncertainty and reporting restrictions remain.

## Numeric findings

| Finding | Original | Corrected |
| --- | --- | --- |
| OECD science change, 2022–2025 | −3.0, marked significant | −2.8, **not significant** |
| OECD reading change, 2022–2025 | −14.0 | −14.3 |
| OECD mathematics change, 2022–2025 | −9.0 | −9.4 |
| OECD science fitted decade trend | −7.0 | −6.7 |
| OECD reading fitted decade trend | −28.0 | −27.0 |
| OECD mathematics fitted decade trend | −22.0 | −23.9 |
| Uzbekistan science change | Missing | +82.7, significant |
| Cyprus comparisons | Missing | All three subjects, both periods included |
| Jordan mathematics decade trend | Missing | −7.0, not significant |
| Country/economy mean scores | Existing values | All retained; matched annex at displayed precision |

The original OECD decade figures were endpoint differences from the preface,
although the UI described a fitted regression. The corrected values use
**OECD average-35** from the same trend tables as the country estimates.

The original chapter comparison tables omit some valid subject-specific results.
Using the detailed annex increases short-term coverage from 74 in each subject to
76 science / 75 reading / 75 mathematics, and decennial coverage from 71 each to
72 science / 72 reading / 73 mathematics. Coverage is shown dynamically.

Uzbekistan's +82.73341 comes from Table I.B1.2a.36, cell Z102. The +82.94308 in
Figure I.2.5 is a **median** change (the figure's note identifies median performance).
That is a different statistic, not a source inconsistency; the site uses mean changes.

Albania remains excluded from trends even though some numeric annex cells exist:
the Reader's Guide expressly limits its reporting. Viet Nam has no reportable trends.
Uzbekistan's reading and mathematics remain missing. Guatemala and Paraguay now
carry notes about uncertainty from changing assessment mode. US and Albanian
sampling cautions explicitly note limited reporting.

## Visual and interpretation fixes

- Added HTML doctype, document language, charset and viewport. Before: quirks mode;
  a mobile browser used a 980px layout. After: standards mode and responsive layout.
- Preserved the red/neutral/blue change scale; documented every bin boundary and
  open-ended tail. Color and ranking use unrounded estimates, display uses one decimal.
- Replaced whole-parent-country shading for regional samples with locator circles.
- Replaced “held steady” and “shown as no change” with accurate non-significance
  language. Added visible NS labels, missing-comparison counts and approximate 95%
  intervals in change-cell descriptions and map tooltips.
- Restricted gain lists to positive values and loss lists to negative values. Highlight
  mode now restricts the ranking lists to significant estimates. Rankings are explicitly
  descriptive point-estimate orderings, not tests of differences between systems.
- Corrected missing-value sorting so unavailable results stay last in both directions.
- Increased text contrast and control sizes; preserved mobile page scrolling over the
  map at default zoom. Added tap/focus tooltip access and Escape dismissal.
- Corrected tiny-marker hatching order and combined coverage, sampling and methodological
  notes rather than dropping one when another was present.
- Clarified score-point units versus points per decade in the table, and removed the
  unqualified conversion of score changes into years of schooling.

## Verification performed

- Archived official report PDF, derived text, chapter workbook, annex workbook and
  pinned geography file. SHA-256 checks run before rebuilding.
- Independently checked all 91 participants against the report snapshot, including
  suppressed/missing means. No integer fallback invents decimal precision.
- Validated **360 numeric means** (including four OECD means), **449 changes/trends**
  (including six OECD comparisons), and **8 missing means** against source cells.
- Cross-checked every overlapping chapter-table comparison and its significant /
  non-significant split against annex estimates and uncertainty calculations.
- Verified all source-cell entity names and that embedded HTML data equals generated JSON.
- Browser assertions passed for all **12 subject × period × highlight states**, including
  statistic counts, ranking membership/order, 91 table rows and regional neutral fills.
- Verified null-last sorting, zoom/reset, keyboard tooltip access and Escape dismissal.
- Inspected desktop, mobile and dark-mode screenshots. Layout checks at 320, 390, 768
  and 1440px found no horizontal page overflow. No JavaScript runtime exceptions.
- axe-core WCAG 2 A/AA and 2.1 AA checks reported **zero automated violations** in
  light and dark desktop modes. This does not establish complete accessibility conformance.

Evidence: [browser results](browser-checks.json), [mobile](after-390.png),
[desktop light](light-1440.png), [desktop dark](dark-1440.png).

## Limits and maintenance

The audit establishes agreement with the published aggregate estimates, not an
independent recalculation from student microdata, plausible values and survey weights.
PISA estimates retain sampling, linking, measurement, coverage and non-response
uncertainty. Approximate confidence intervals do not capture every systematic bias.
Statistical significance does not establish causality or the practical importance of
a change. Country means do not describe every student or within-country inequality.

The decade window can use different available cycles across systems; OECD requires
at least three comparable assessments. These are fitted points per ten years, not
necessarily observed endpoint differences. Cross-cycle comparisons use different
student cohorts. The map uses simplified outlines and approximate markers; it does
not depict exact sampling boundaries or a geopolitical position.

Sources are a snapshot retrieved 8 September 2026. OECD revisions require explicit
review, updated source files/checksums, regeneration and rerunning verification.

## Primary sources

- [OECD report](https://www.oecd.org/en/publications/pisa-2025-results-volume-i_73451bc5-en.html)
- [Official PDF, including Reader's Guide and Table I.1](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/09/pisa-2025-results-volume-i_5265bfb1/73451bc5-en.pdf)
- [Annex workbook](https://stat.link/mrq53f)
- [Chapter 2 workbook](https://stat.link/xgs41b)
- [Local source manifest](../build/sources/manifest.json)
