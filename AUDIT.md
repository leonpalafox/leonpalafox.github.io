# Website audit — 7 September 2026

Audited the local Astro production build. Corrections are in the working tree; nothing was deployed.

## Corrections

| Finding | Correction |
| --- | --- |
| Regression demo threw an uncaught exception and left a blank panel when WebGL was unavailable. | Added an explanatory fallback, hid the failed stage, and disabled unavailable controls. Verified both WebGL and failure paths. |
| About-page expanded content required desktop hover and was hidden from assistive technology. | Replaced the overlay with native expandable details, available on touch screens and through keyboard activation. Preserved the information. |
| Segregation labels failed automated contrast checks. | Applied the existing darker muted text token to credits, metric labels, and slider scales. |
| Article source links relied only on color. | Added persistent underlines. |
| Segregation metrics announced changes every 85 milliseconds. | Removed the rapidly updating live region; retained the simulation status announcements. |
| Segregation controls used a nested complementary landmark. | Changed their wrapper to a regular container within the main content. |
| Segregation had no JavaScript-disabled explanation. | Added a noscript explanation. |
| Regression parallax ignored reduced motion. | Disabled pointer-driven parallax when reduced motion is requested. |
| Blog social metadata described articles as websites. | Added article type, publication timestamp, and language locale. |
| Error page could be indexed. | Added `noindex, follow` to the 404 page. |
| Spanish posts inherited English navigation/footer text without language markup. | Marked shared navigation and footer as English and translated the skip link. Made its target programmatically focusable. |
| Course routes did not highlight Teaching. | Included course paths in the navigation active state; normalized trailing slashes. |
| Year labels used local time while the other dates used UTC. | Made Japanese year labels use UTC consistently. |
| Three older posts had duplicate top-level headings or skipped heading levels. | Corrected section heading levels and one heading typo. |
| Course pages showed empty fields and an internal drafting instruction. | Replaced them with clear availability notes and an existing instructor email link. No schedule or grading details were invented. |

## Verification

- `npm run build`: passed, 33 content pages plus legacy redirects.
- Static HTML audit: 54 generated HTML files and 647 local references; no missing local targets, broken fragment links, or duplicate IDs. Content pages have one H1, descriptions, and canonical links. Article metadata and 404 indexing directives passed.
- Chrome: 11 representative routes at widths of 320, 390, 768, and 1440 pixels (44 checks); no horizontal overflow, broken loaded images, or uncaught exceptions after fixes.
- axe-core 4.10.3: WCAG A/AA and best-practice scans passed on 11 representative pages and all 22 articles after corrections. Additional desktop checks passed on the expanded About details, segregation demo, and corrected older articles. Automated scans do not establish full accessibility conformance.
- Working WebGL path: add, undo, reset, stiffness, and play controls passed. Unavailable-WebGL path: fallback visible, stage hidden, controls disabled, no uncaught exception.
- Segregation: step, reshuffle, and threshold controls passed. Both demos start paused with reduced motion enabled.
- About details open through Enter-key activation. Course navigation highlights Teaching.
- `git diff --check`: passed.

## Remaining limits

- The regression page still has a roughly 548 kB minified Three.js bundle (138 kB gzip). It is confined to that demo; no library rewrite was attempted during this audit.
- No production Core Web Vitals, Lighthouse score, deployment headers, dependency vulnerability scan, or external-link availability results are claimed. The web-perf skill's trace workflow requires a Chrome DevTools MCP connection, which is not configured; browser checks used local Chrome instead.
- Lecture schedules, office hours, assessment weights, and unpublished course materials still need the instructor's actual information.
