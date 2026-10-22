import type { APIRoute } from 'astro';
import { pdfIsCurrent, renderDeck, servedDeck } from '../../../lib/slides.mjs';

const SLUG = 'deep-learning/class-03-embeddings-cnn';

// A standalone deck: src/slides/deep-learning/class-03-embeddings-cnn.html, served as is.
export const GET: APIRoute = () => {
  const { html, hash } = renderDeck(SLUG);
  if (import.meta.env.PROD && !pdfIsCurrent(SLUG, hash)) {
    console.warn(`[slides] ${SLUG}.pdf is older than the slides. Run \`npm run slides:pdf\` and commit the PDF.`);
  }
  return new Response(servedDeck(html), { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
};
