// @ts-check
import fs from 'node:fs';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Old Jekyll permalinks were /:categories/:title/ — keep inbound links alive.
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
  'bigdata',
  'datoscafe',
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
  redirects[`/articulos/${slug}`] = `/blog/${slug}/`;
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
Object.assign(redirects, {
  '/_events': '/media/',
  '/articulos': '/blog/',
  '/year-archive': '/blog/',
  '/articulos/BigData': '/blog/bigdata/',
  '/articulos/datosCafe': '/blog/datoscafe/',
  '/blog/BigData': '/blog/bigdata/',
  '/blog/datosCafe': '/blog/datoscafe/',
});
// Note: /mlclase/ is a separate GitHub Pages project site
// (github.com/leonpalafox/mlclase), so it cannot be redirected from this repo.

// Publication dates from the content frontmatter, used as <lastmod> so crawlers
// can tell new columns from old ones without a full recrawl.
const blogDir = new URL('./src/content/blog/', import.meta.url);
const postDates = new Map();
for (const file of fs.readdirSync(blogDir)) {
  if (!file.endsWith('.md')) continue;
  const source = fs.readFileSync(new URL(file, blogDir), 'utf8');
  const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const published = frontmatter?.[1].match(/^pubDate:\s*['"]?(\d{4}-\d{2}-\d{2})/m);
  if (published) {
    postDates.set(file.replace(/\.md$/, '').toLowerCase(), new Date(`${published[1]}T00:00:00Z`));
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
        if (slug && postDates.has(slug)) {
          item.lastmod = postDates.get(slug).toISOString();
        } else if (latestPostDate && (item.url === 'https://www.leonpalafox.com/' || /\/blog\/$/.test(item.url))) {
          item.lastmod = latestPostDate.toISOString();
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
