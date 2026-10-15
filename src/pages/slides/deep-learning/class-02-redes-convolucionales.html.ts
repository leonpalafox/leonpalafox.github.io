import type { APIRoute } from 'astro';
import { pdfIsCurrent, renderDeck } from '../../../lib/slides.mjs';

const SLUG = 'deep-learning/class-02-redes-convolucionales';

// A standalone deck: src/slides/deep-learning/class-02-redes-convolucionales.html, served as is.
export const GET: APIRoute = () => {
  const { html, hash } = renderDeck(SLUG);
  if (import.meta.env.PROD && !pdfIsCurrent(SLUG, hash)) {
    console.warn(`[slides] ${SLUG}.pdf is older than the slides. Run \`npm run slides:pdf\` and commit the PDF.`);
  }
  return new Response(html, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
};
