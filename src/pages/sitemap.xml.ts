import type { APIContext } from 'astro';

// The Jekyll site published /sitemap.xml. Serve a valid sitemap index there so
// old Search Console submissions and external references still resolve.
export function GET({ site }: APIContext) {
  const base = site ?? new URL('https://www.leonpalafox.com');
  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    `<sitemap><loc>${new URL('sitemap-0.xml', base).href}</loc></sitemap>`,
    '</sitemapindex>',
  ].join('');
  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
