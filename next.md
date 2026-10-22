# Front Page (Portada) — Tuning Brief for a Stronger Model

> Replaces the previous `next.md` (the SEO & Landing audit). Most of that SEO work is
> already implemented on the live branch; this file is now the handoff brief for the next
> design pass on the homepage's newspaper section.

## Objective

Refine the homepage's newspaper-style **"Portada"** section (the block below the hero) so it
reads as genuinely *elegant* and publishable. The current draft is structurally complete and
builds cleanly, but the typography and overall "look" need a more refined pass. Use a stronger,
design-capable model to do that pass — this doc is the brief.

## Current state (what already exists)

- **`src/pages/index.astro`** — homepage. Hero section (unchanged) followed by `<Portada />`.
  The old three-column band (Focus areas / Selected work / Latest writing) was removed.
- **`src/components/Portada.astro`** — the newspaper section, entirely new.
  - **Masthead**: "León Palafox" (serif, `font-medium`, `uppercase`, `tracking-[0.14em]`),
    a serif-italic tagline, a hairline divider with a single signal dot, and a dateline row
    (Ciudad de México · date · 新聞 Edición digital).
  - **Lead story** (most recent post): mono kicker, large serif headline, italic serif deck,
    mono byline, and the opening paragraph with an **ink** serif drop cap.
  - Horizontal hairline rule.
  - **5 secondary stories** in a 3-column grid (2 on tablet, 1 on mobile): kicker + headline + deck.
  - Footer rule with "Fin de la edición" and "Todas las columnas →" (→ `/blog/`).
- **Data**: last 6 posts via `getCollection('blog')`, sorted by `pubDate` desc (`lead` = 1st,
  `rest` = other 5). Uses `post.data.title/description/pubDate/lang` and `post.body` for the lede
  (via `firstParagraph()` + `stripMarkdown()`).
- **Git state**: NOT committed, NOT pushed. `src/pages/index.astro` modified, `src/components/Portada.astro`
  new, both uncommitted.

## Design constraints (must preserve)

- **Tokens** (from `src/styles/global.css`): `paper #efede7`, `sheet #f5f3ee`, `ink #141412`,
  `muted #6f6a61`, `hairline #dcd7cc`, `signal #e2371b`, `signal-deep #c22c13`.
- **Fonts**: `Archivo Variable` (sans), `Source Serif 4 Variable` (serif), `IBM Plex Mono` (mono).
  Utilities: `micro-label` (mono, uppercase, tracked), `vertical-text`.
- **Identity**: Japanese-minimal / print-editorial. Subtle Japanese glosses are on-brand (`新聞`,
  `上昇する信号`, `改善`). Keep the warm paper background and hairline structure.
- **Keep**: hero untouched; exactly 6 items (1 lead + 5); newspaper feel; no navigation/footer changes.

## Directions to tune (priority order)

1. **Masthead typography** — the highest-impact lever. Explore a more *distinctive yet refined*
   lockup: varied weight (e.g. `font-medium`/`font-semibold`), letter-spacing, casing, or a
   two-line treatment. Avoid heavy/black weights and excessive size.
2. **Headline hierarchy** — make the lead unmistakably primary vs the five secondary stories;
   refine sizes, weights, and leading.
3. **Rules & borders** — decide on weight and count (subtle hairline vs a single thin ink rule).
   Less is more here; resist heavy black bars.
4. **Drop cap** — keep (ink, subtle) or remove; if kept, make sure it's elegant and doesn't clip.
   Consider a bold/no-drop-cap alternative opening.
5. **Spacing & rhythm** — tighten or open padding; ensure even vertical rhythm between masthead,
   lead, rule, grid, and footer.
6. **Cover images (optional)** — wire up `post.data.cover` via `getAsset()` (`src/lib/assets.ts`)
   for the lead and/or secondary stories, with proper `alt` text and a grid-aware image treatment.
7. **Responsive** — verify mobile (1-col), tablet (2-col), desktop (3-col); masthead should wrap
   without overflow at each breakpoint (`sm` 640 / `lg` 1024 / `xl` 1280 / `2xl` 1536).
8. **Accessibility** — contrast (muted-on-sheet is borderline; check), semantic heading order,
   `aria-label` on the section, `prefers-reduced-motion`, visible `:focus-visible`, descriptive
   link text.
9. **Refined details** — category/kicker from `post.data.tags`, consistent byline styling,
   hover affordances, and a clean "read more" path to `/blog/`.

## How to test while tuning

- `npm run build`, then `npm run preview` → open **http://localhost:4321/** and scroll down.
- Screenshot with headless Chrome at desktop (1440×3400) and a mobile width to compare. **Chrome
  may hang after capturing** — screenshot to a file, then `pkill -f "chrome-"`; the PNG is written
  before the hang.
- Quick DOM smoke test on `dist/index.html`: masthead present, lead title present, exactly 6
  `/blog/<slug>/` links, and no unintended `font-black` (unless intentionally reintroduced).

## Out of scope this round

- Navigation/footer changes (unless explicitly requested).
- Moving the newspaper to its own route (user decided to keep it on the homepage).
- Editing post content/cover copy itself.

## Commit hygiene when happy

- Commit **only** `src/pages/index.astro` and `src/components/Portada.astro` (plus any new asset
  you add). Leave `next.md` (this brief), `assets/ChatGPT Image….png`, and unrelated `public/`
  changes out of the commit unless intended. Push after the user approves the visual.
