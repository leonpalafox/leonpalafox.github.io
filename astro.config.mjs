// @ts-check
import fs from 'node:fs';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { LEGACY_REFERRER_SCRIPT } from './src/lib/analytics.mjs';

// Old Jekyll permalinks were /:categories/:title/ — keep inbound links alive.
// :title kept the filename's case, so the old URLs are /articulos/BigData/ and
// /articulos/datosCafe/ (confirmed in the Wayback Machine); the posts now live
// at the lower-cased id.
const oldPostSlugs = [
  '2026-cuando-la-ia-dejo-de-hablar-y-se-puso-a-trabajar-manual',
  'es-hora-de-mirar-hacia-adentro-y-garantizar-el-futuro-de-mex',
  'el-fin-del-desarrollo-de-software-tal-como-lo-conocemos',
  'la-carrera-de-la-ia-cambio-por-completo',
  'lecun-apuesta-por-una-ia-mas-alla-de-los-llms-mexico-haria-b',
  'la-generacion-de-video-con-ia-no-esta-lista-ni-de-cerca',
  'la-ia-se-acerca-a-las-afores-de-los-mexicanos',
  'el-asesor-que-nunca-duerme',
  'mexico-tiene-la-costumbre-de-regular-el-futuro-como-si-fuera',
  'world-cup-managers-rank-vs-tenure',
  'mitos',
  'BigData',
  'datosCafe',
  'etica',
  'theranos',
  'banamex',
];
const redirects = {
  '/blog-by-year': '/blog/',
  '/categories': '/blog/',
  '/tags': '/blog/',
  '/conferences/riiaa': '/blog/riiaa/',
  '/conferences/riiaaesp': '/blog/riiaaesp/',
};
for (const slug of oldPostSlugs) {
  redirects[`/articulos/${slug}`] = `/blog/${slug.toLowerCase()}/`;
}

// Stale routes from the Jekyll-era site that still appear in search results.
// The lower-case permalinks redirect above; these keep the case-preserved and
// collection URLs from turning into 404s and losing their inbound links.
const legacyEventSlugs = [
  'algorithia',
  'arizonapst',
  'arizonastaff',
  'banorte',
  'gbm',
  'nii',
  'novartis',
  'panamericana',
  'phd',
  'rassini',
  'richit',
  'todai_monbusho',
  'todaim',
  'ucla',
  'unam',
];
for (const slug of legacyEventSlugs) {
  redirects[`/_events/${slug}`] = '/media/';
}
// Each URL appears in one case only. On a case-insensitive disk (macOS)
// BigData/ and bigdata/ are the same directory, so a second variant overwrites
// the first (a /blog/BigData redirect replaced the post itself) and Astro
// reports a route collision, which later versions turn into a build error.
Object.assign(redirects, {
  '/_events': '/media/',
  '/articulos': '/blog/',
  '/year-archive': '/blog/',
});
// Note: /mlclase/ is a separate GitHub Pages project site
// (github.com/leonpalafox/mlclase), so it cannot be redirected from this repo.

// The redirects above are meta-refresh pages (GitHub Pages has no server 301s),
// so the destination sees the redirect page as its referrer and GA4 records a
// visitor from Google as direct. Hand the original referrer on; Base.astro's
// GA snippet reports it (src/lib/analytics.mjs).
const legacyReferrer = {
  name: 'legacy-referrer',
  hooks: {
    'astro:build:done': ({ dir }) => {
      const tag = `<script>${LEGACY_REFERRER_SCRIPT}</script>`;
      for (const file of fs.readdirSync(dir, { recursive: true })) {
        if (!file.endsWith('.html')) continue;
        const path = new URL(file, dir);
        const html = fs.readFileSync(path, 'utf8');
        if (!html.includes('http-equiv="refresh"') || html.includes(tag)) continue;
        fs.writeFileSync(path, html.replace('</title>', `</title>${tag}`));
      }
    },
  },
};

// Publication dates from the content frontmatter, used as <lastmod> so crawlers
// can tell new columns from old ones without a full recrawl. A post revised
// after publication reports its `updatedDate` instead.
const blogDir = new URL('./src/content/blog/', import.meta.url);
const postDates = new Map();
const postModified = new Map();
const frontmatterDate = (frontmatter, key) => {
  const match = frontmatter.match(new RegExp(`^${key}:\\s*['"]?(\\d{4}-\\d{2}-\\d{2})`, 'm'));
  return match ? new Date(`${match[1]}T00:00:00Z`) : undefined;
};
for (const file of fs.readdirSync(blogDir)) {
  if (!file.endsWith('.md')) continue;
  const source = fs.readFileSync(new URL(file, blogDir), 'utf8');
  const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1] ?? '';
  const published = frontmatterDate(frontmatter, 'pubDate');
  if (published) {
    const slug = file.replace(/\.md$/, '').toLowerCase();
    const updated = frontmatterDate(frontmatter, 'updatedDate');
    postDates.set(slug, published);
    postModified.set(slug, updated && updated > published ? updated : published);
  }
}
const latestPostDate = postDates.size
  ? new Date(Math.max(...[...postDates.values()].map((date) => date.getTime())))
  : undefined;

export default defineConfig({
  site: 'https://www.leonpalafox.com',
  redirects,
  integrations: [
    sitemap({
      customPages: ['https://www.leonpalafox.com/pisa_results/'],
      serialize(item) {
        const post = item.url.match(/\/blog\/([^/]+)\/$/);
        const slug = post?.[1].toLowerCase();
        if (slug && postModified.has(slug)) {
          item.lastmod = postModified.get(slug).toISOString();
        } else if (latestPostDate && (item.url === 'https://www.leonpalafox.com/' || /\/blog\/$/.test(item.url))) {
          item.lastmod = latestPostDate.toISOString();
        }
        return item;
      },
    }),
    legacyReferrer,
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
