// @ts-check
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

export default defineConfig({
  site: 'https://www.leonpalafox.com',
  redirects,
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
