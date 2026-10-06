// Prints every Markdown-driven slide deck to public/slides/**.pdf with headless Chrome,
// driven over the DevTools protocol so the deck's own 1600×900 @page size is used.
// Usage: npm run slides:pdf   (set CHROME_PATH if Chrome is not in the default place)
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';
import { pathToFileURL } from 'node:url';
import { DECKS, deckPaths, renderDeck } from '../src/lib/slides.mjs';

const chromePath = [
  process.env.CHROME_PATH,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].find((p) => p && existsSync(p));
if (!chromePath) throw new Error('Chrome not found; set CHROME_PATH.');

const work = mkdtempSync(join(tmpdir(), 'slides-pdf-'));
const profile = join(work, 'profile');
const chrome = spawn(chromePath, [
  '--headless=new',
  '--disable-gpu',
  '--no-first-run',
  '--remote-debugging-port=0',
  `--user-data-dir=${profile}`,
  'about:blank',
], { stdio: 'ignore' });

try {
  // Chrome writes the port it picked to DevToolsActivePort.
  let port;
  for (let i = 0; i < 100 && !port; i++) {
    try { port = readFileSync(join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0]; } catch { await sleep(100); }
  }
  if (!port) throw new Error('Chrome did not start.');
  const [target] = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).filter((t) => t.type === 'page');
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  let id = 0;
  const waiting = new Map();
  const events = [];
  ws.onmessage = ({ data }) => {
    const msg = JSON.parse(data);
    if (msg.id && waiting.has(msg.id)) {
      const { ok, fail } = waiting.get(msg.id);
      waiting.delete(msg.id);
      msg.error ? fail(new Error(msg.error.message)) : ok(msg.result);
    } else if (msg.method) events.push(msg.method);
  };
  const send = (method, params = {}) => new Promise((ok, fail) => {
    waiting.set(++id, { ok, fail });
    ws.send(JSON.stringify({ id, method, params }));
  });

  await send('Page.enable');
  for (const { slug } of DECKS) {
    const { html, hash } = renderDeck(slug);
    const page = join(work, 'deck.html');
    writeFileSync(page, html);
    events.length = 0;
    await send('Page.navigate', { url: `${pathToFileURL(page).href}#print` });
    for (let i = 0; i < 200 && !events.includes('Page.loadEventFired'); i++) await sleep(50);
    await sleep(500); // let images decode
    const { data } = await send('Page.printToPDF', { preferCSSPageSize: true, printBackground: true });
    const { pdf, pdfHash } = deckPaths(slug);
    mkdirSync(dirname(pdf), { recursive: true });
    writeFileSync(pdf, Buffer.from(data, 'base64'));
    writeFileSync(pdfHash, hash + '\n');
    console.log(`slides: wrote ${pdf}`);
  }
  ws.close();
} finally {
  chrome.kill();
  await sleep(200);
  rmSync(work, { recursive: true, force: true });
}
