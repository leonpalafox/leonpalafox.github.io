// Slide decks whose words live in Markdown (src/slides/**.md) and whose design and
// animation live in an HTML template next to it. The build merges the two; see
// src/pages/slides/ for the routes and scripts/build-slides-pdf.mjs for the PDFs.
// A "standalone" deck is a single self-contained HTML file (src/slides/**.html),
// served as is: its words live in its own script.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { GA_HEAD } from './analytics.mjs';

export const DECKS = [
  {
    slug: 'deep-learning/class-01-introduccion',
    // The template's animations are written for exactly this many slides, in order.
    slides: 45,
  },
  {
    slug: 'deep-learning/class-02-redes-convolucionales',
    standalone: true,
  },
  {
    slug: 'deep-learning/class-03-embeddings-cnn',
    standalone: true,
  },
];

const root = process.cwd();
export const deckPaths = (slug) => ({
  md: join(root, 'src/slides', `${slug}.md`),
  template: join(root, 'src/slides', `${slug}.template.html`),
  html: join(root, 'src/slides', `${slug}.html`),
  pdf: join(root, 'public/slides', `${slug}.pdf`),
  pdfHash: join(root, 'src/slides', `${slug}.pdf-hash`),
});

const KEY = /^([A-Za-z_][\w-]*):\s*(.*)$/;

/*
 * Grammar (one slide per "## Title", grouped by "# Section"):
 *   key: value          one-line text (HTML allowed)
 *   key:                followed by "- item" lines: a list; "a | b | c" splits an item into fields
 *   key:                followed by "> line" lines: multi-line text
 *   key:                followed by a ``` fence: code, kept verbatim
 *   <!-- ... -->        comments are ignored
 */
export function parseDeck(md) {
  const lines = md.replace(/\r\n?/g, '\n').split('\n');
  const deck = { meta: {}, slides: [] };
  let target = null;
  let section = '';
  let i = 0;
  const fail = (msg) => {
    throw new Error(`Slides markdown, line ${i + 1}: ${msg}\n  > ${lines[i]}`);
  };

  const readBlock = (obj, key) => {
    let j = i + 1;
    while (j < lines.length && lines[j].trim() === '') j++;
    const first = lines[j] ?? '';
    if (first.startsWith('```')) {
      const code = [];
      j++;
      while (j < lines.length && !lines[j].startsWith('```')) code.push(lines[j++]);
      if (j >= lines.length) fail(`code block for "${key}" is never closed`);
      obj[key] = code.join('\n');
      i = j + 1;
    } else if (first.startsWith('- ')) {
      const list = [];
      while (j < lines.length && lines[j].startsWith('- ')) {
        const item = lines[j].slice(2);
        list.push(item.includes(' | ') ? item.split(' | ').map((s) => s.trim()) : item.trim());
        j++;
      }
      obj[key] = list;
      i = j;
    } else if (first.startsWith('>')) {
      const text = [];
      while (j < lines.length && lines[j].startsWith('>')) text.push(lines[j++].replace(/^> ?/, ''));
      obj[key] = text.join('\n');
      i = j;
    } else {
      obj[key] = key === 'sources' || key === 'guide' ? [] : '';
      i++;
    }
  };

  // frontmatter
  if (lines[0]?.trim() === '---') {
    i = 1;
    while (i < lines.length && lines[i].trim() !== '---') {
      const line = lines[i];
      const m = line.match(KEY);
      if (m && m[2] !== '') { deck.meta[m[1]] = m[2].trim(); i++; }
      else if (m) readBlock(deck.meta, m[1]);
      else if (line.trim() === '') i++;
      else fail('expected "key: value" in the header');
    }
    i++;
  }

  while (i < lines.length) {
    const line = lines[i];
    const t = line.trim();
    if (t === '') { i++; continue; }
    if (t.startsWith('<!--')) {
      while (i < lines.length && !lines[i].includes('-->')) i++;
      i++;
      continue;
    }
    if (line.startsWith('## ')) {
      target = { section, title: line.slice(3).trim() };
      deck.slides.push(target);
      i++;
      continue;
    }
    if (line.startsWith('# ')) { section = line.slice(2).trim(); i++; continue; }
    if (!target) fail('text before the first "## Slide title"');
    const m = line.match(KEY);
    if (!m) fail('expected "key: value", a list, or a "## Slide title"');
    if (m[2] !== '') { target[m[1]] = m[2].trim(); i++; }
    else readBlock(target, m[1]);
  }
  return deck;
}

export function renderDeck(slug) {
  const spec = DECKS.find((d) => d.slug === slug);
  if (!spec) throw new Error(`Unknown slide deck: ${slug}`);
  const paths = deckPaths(slug);
  if (spec.standalone) {
    const html = readFileSync(paths.html, 'utf8');
    return { html, deck: loadDeck(slug), hash: createHash('sha256').update(html).digest('hex').slice(0, 16) };
  }
  const md = readFileSync(paths.md, 'utf8');
  const template = readFileSync(paths.template, 'utf8');
  const deck = parseDeck(md);
  if (deck.slides.length !== spec.slides) {
    throw new Error(
      `${slug}.md has ${deck.slides.length} slides but the template is animated for ${spec.slides}. ` +
        'Edit the text of existing slides; adding or removing slides needs a template change.',
    );
  }
  const json = JSON.stringify(deck)
    .replace(/</g, '\\u003c')
    .replace(/[\u2028\u2029]/g, (c) => `\\u${c.charCodeAt(0).toString(16)}`);
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const html = template
    .replace('__DECK_TITLE__', () => esc(deck.meta.title ?? ''))
    .replace('__DECK_CONTENT__', () => json);
  return { html, deck, hash: createHash('sha256').update(html).digest('hex').slice(0, 16) };
}

// The deck is served bare for full-screen viewing, but its class page (which
// embeds it in an iframe) is the page meant for search. Keep the bare URL out
// of the index while its slides still count toward the page that embeds them.
// Applied after renderDeck so the PDF freshness hash stays the same.
export function servedDeck(html) {
  return html
    .replace('</title>', '</title><meta name="robots" content="noindex, indexifembedded">')
    .replace('</head>', `${GA_HEAD}</head>`);
}

export function loadDeck(slug) {
  if (DECKS.find((d) => d.slug === slug)?.standalone) return outlineStandalone(slug);
  return parseDeck(readFileSync(deckPaths(slug).md, 'utf8'));
}

// A standalone deck lists its slides in `const SEC = [...]` and `const META = [...]`
// ({title, layout, sec, ...}). Read only the outline fields: speaker notes and
// other unused metadata may reference helper constants defined elsewhere.
function outlineStandalone(slug) {
  const html = readFileSync(deckPaths(slug).html, 'utf8');
  const literal = (name) => {
    const m = html.match(new RegExp(`\\nconst ${name} = (\\[[\\s\\S]*?\\n?\\]);\\n`));
    if (!m) throw new Error(`${slug}.html: could not find "const ${name} = [...]"`);
    return m[1];
  };
  const sections = new Function(`return ${literal('SEC')};`)();
  const metadata = literal('META');
  const entries = [...metadata.matchAll(/\{\s*title:\s*('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")\s*,\s*layout:\s*('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")\s*,\s*sec:\s*SEC\[(\d+)\]/g)];
  if (!entries.length || entries.length !== [...metadata.matchAll(/\{\s*title:/g)].length) {
    throw new Error(`${slug}.html: expected each META entry to start with title, layout, and sec: SEC[n]`);
  }
  const slides = entries.map(([, title, layout, section]) => {
    const [slideTitle, slideLayout] = new Function(`return [${title}, ${layout}];`)();
    if (sections[Number(section)] === undefined) throw new Error(`${slug}.html: unknown section SEC[${section}]`);
    return { title: slideTitle, layout: slideLayout, section: sections[Number(section)] };
  });
  const title = html.match(/<title>([^<]*)<\/title>/)?.[1] ?? '';
  return {
    meta: { title },
    slides,
  };
}

export function pdfIsCurrent(slug, hash) {
  try {
    return readFileSync(deckPaths(slug).pdfHash, 'utf8').trim() === hash;
  } catch {
    return false;
  }
}
