// Fails the build when a published page is not measured the way the rest of
// the site is. Runs after `astro build` (see package.json), so a deploy cannot
// ship an untagged page — /pisa_results/ went live untagged on 2026-09-08 and
// its first five days of search traffic were never recorded.
//
// Every HTML page in dist/ must carry the exact GA_SCRIPT from
// src/lib/analytics.mjs once (static copies such as the PISA template included),
// and no other measurement ID. Redirect pages must instead hand the referrer on.
import fs from 'node:fs';
import { GA_ID, GA_SCRIPT, LEGACY_REFERRER_SCRIPT } from '../src/lib/analytics.mjs';

const dist = new URL('../dist/', import.meta.url);
const count = (text, needle) => text.split(needle).length - 1;
const failures = [];
let pages = 0;
let redirects = 0;

for (const file of fs.readdirSync(dist, { recursive: true })) {
  if (!file.endsWith('.html')) continue;
  const html = fs.readFileSync(new URL(file, dist), 'utf8');
  if (html.includes('http-equiv="refresh"')) {
    redirects++;
    if (!html.includes(LEGACY_REFERRER_SCRIPT)) failures.push(`${file}: redirect page does not pass the referrer on`);
    continue;
  }
  pages++;
  const snippets = count(html, GA_SCRIPT);
  if (snippets !== 1) failures.push(`${file}: GA snippet found ${snippets} times, expected 1`);
  const otherIds = new Set((html.match(/\bG-[A-Z0-9]{10}\b/g) ?? []).filter((id) => id !== GA_ID));
  if (otherIds.size) failures.push(`${file}: unexpected measurement ID ${[...otherIds].join(', ')}`);
}

if (failures.length) {
  console.error(`[check-ga] ${failures.length} problem(s):\n  ${failures.join('\n  ')}`);
  process.exit(1);
}
console.log(`[check-ga] ${pages} pages tagged once with ${GA_ID}; ${redirects} redirect pages pass the referrer on.`);
