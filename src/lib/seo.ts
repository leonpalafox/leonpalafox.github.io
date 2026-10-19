// Small helpers for search-result metadata.
//
// Titles and descriptions are shown truncated in search results (roughly 60
// characters for a title and 155–160 for a description), so keep the brand
// suffix only when it still fits and trim descriptions on a word boundary.

const BRAND = 'León Palafox';

/**
 * Append the site name only when the combined title fits in a search result.
 * Long editorial titles stay untouched instead of losing their tail to the
 * brand suffix.
 */
export function seoTitle(title: string, brand = BRAND, max = 60): string {
  const clean = title.trim();
  const suffix = ` — ${brand}`;
  return clean.length + suffix.length <= max ? `${clean}${suffix}` : clean;
}

/** Collapse whitespace and cap a description at `max` characters, on a word boundary. */
export function clampDescription(text: string, max = 158): string {
  const clean = text.replace(/\s+/g, ' ').trim();
  if (clean.length <= max) return clean;
  const cut = clean.slice(0, max - 1);
  const lastSpace = cut.lastIndexOf(' ');
  const body = (lastSpace > max * 0.6 ? cut.slice(0, lastSpace) : cut).replace(/[.,;:…]+$/, '');
  return `${body}…`;
}
