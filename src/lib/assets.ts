// Asset manager for blog imagery.
//
// Drop a file in `src/assets/blog/` and it is picked up automatically — the id is
// the path under that folder without the extension (`mercado-de-inteligencia`,
// or `2026/foo` if you nest it). Register alt text / caption / credit here once
// and every post that uses the asset inherits them, so the same image reused
// across posts never loses its description.
//
// Posts opt in through frontmatter:
//
//   cover: mercado-de-inteligencia
//   coverAlt: "…"        # optional, overrides the entry below
//   coverCaption: "…"    # optional, overrides the entry below

const files = import.meta.glob<ImageMetadata>('../assets/blog/**/*.{png,jpg,jpeg,webp,avif}', {
  eager: true,
  import: 'default',
});

const PREFIX = '../assets/blog/';

/** id -> imported image, keyed by path under src/assets/blog/ minus the extension. */
const sources: Record<string, ImageMetadata> = Object.fromEntries(
  Object.entries(files).map(([path, src]) => [path.slice(PREFIX.length).replace(/\.[^.]+$/, ''), src]),
);

export interface AssetEntry {
  /** Describes the image for screen readers. Empty string marks it purely decorative. */
  alt: string;
  /** Shown under the image. Keep it short — it renders in the mono micro-label style. */
  caption?: string;
  /** Photographer / illustrator / outlet, appended after the caption. */
  credit?: string;
}

/** Metadata for the images in src/assets/blog/. Keys must match an id from that folder. */
const registry: Record<string, AssetEntry> = {
  'mexico-industria-frente-a-pemex': {
    alt: 'Una balanza enfrenta una plataforma petrolera deteriorada con una fábrica automatizada de robots y servidores, frente a la silueta del mapa de México.',
  },
  'mercado-de-inteligencia': {
    alt: 'Portada de El Financiero: León Palafox frente a un pasillo de puestos que anuncian Kimi, GPT, Claude, Grok, Gemini y modelos abiertos, bajo el titular “Quién decide qué inteligencia compra su empresa”.',
    caption: 'El Financiero · 23 de julio de 2026',
  },
  riiaa: {
    alt: 'Conferencia RIIAA en el museo Universum, Ciudad de México',
  },
};

export interface BlogAsset extends AssetEntry {
  id: string;
  src: ImageMetadata;
}

/** All registered ids, sorted — handy for error messages and for listing what exists. */
export function listAssets(): string[] {
  return Object.keys(sources).sort();
}

/**
 * Resolve an asset id to its image plus metadata. Throws at build time on a typo
 * or an unregistered file, so a broken cover never ships silently.
 */
export function getAsset(id: string, overrides: Partial<AssetEntry> = {}): BlogAsset {
  const src = sources[id];
  if (!src) {
    throw new Error(
      `Unknown blog asset "${id}". Add the file to src/assets/blog/ or fix the id. Available: ${listAssets().join(', ')}`,
    );
  }
  const entry = registry[id];
  if (!entry && overrides.alt === undefined) {
    throw new Error(
      `Blog asset "${id}" has no alt text. Add an entry to the registry in src/lib/assets.ts, or set coverAlt in the post frontmatter.`,
    );
  }
  return {
    id,
    src,
    alt: overrides.alt ?? entry.alt,
    caption: overrides.caption ?? entry?.caption,
    credit: overrides.credit ?? entry?.credit,
  };
}
