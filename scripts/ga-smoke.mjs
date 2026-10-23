// GA4 smoke test in headless Chrome. Every hit to /g/collect is captured and
// answered locally, so a run never reaches the property.
//
//   node scripts/ga-smoke.mjs          test the live site
//   node scripts/ga-smoke.mjs --dist   test ./dist served under the production
//                                      hostname (run `npm run build` first)
//
// Checks: one page_view per page load with the right ID, URL and Google
// referrer; internal navigation; legacy redirect pages keeping the Google
// referrer; mobile; and no hits at all from localhost.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { GA_ID, PRODUCTION_HOST } from '../src/lib/analytics.mjs';

const CHROME = process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const SITE = `https://${PRODUCTION_HOST}`;
const GOOGLE = 'https://www.google.com/';
const LOCAL = process.argv.includes('--dist');
const dist = new URL('../dist/', import.meta.url);
const TYPES = { html: 'text/html; charset=utf-8', js: 'text/javascript', css: 'text/css', svg: 'image/svg+xml', json: 'application/json', xml: 'application/xml', webp: 'image/webp', jpg: 'image/jpeg', png: 'image/png', woff2: 'font/woff2', pdf: 'application/pdf' };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Serve a request for the site (or localhost) from dist/, as GitHub Pages would.
function fromDist(url) {
  let file = decodeURIComponent(new URL(url).pathname).slice(1);
  if (file === '' || file.endsWith('/')) file += 'index.html';
  let target = new URL(file, dist);
  if (!fs.existsSync(target) && fs.existsSync(new URL(`${file}/index.html`, dist))) {
    return { responseCode: 301, responseHeaders: [{ name: 'Location', value: `${url}/` }] };
  }
  if (!fs.existsSync(target) || fs.statSync(target).isDirectory()) target = new URL('404.html', dist);
  const type = TYPES[target.pathname.split('.').pop()] ?? 'application/octet-stream';
  const body = fs.readFileSync(target).toString('base64');
  return { responseCode: target.pathname.endsWith('/404.html') ? 404 : 200, responseHeaders: [{ name: 'Content-Type', value: type }], body };
}

async function session() {
  const target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0;
  const pending = new Map();
  const hits = [];
  const send = (method, params = {}) => new Promise((res, rej) => { pending.set(++id, { res, rej }); ws.send(JSON.stringify({ id, method, params })); });
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(m.error) : p.res(m.result); return; }
    if (m.method !== 'Fetch.requestPaused') return;
    const { requestId, request } = m.params;
    if (/\/g\/collect/.test(request.url)) {
      const shared = Object.fromEntries(new URL(request.url).searchParams);
      const bodies = (request.postData ?? '').split('\n').filter(Boolean);
      for (const body of bodies.length ? bodies : ['']) hits.push({ ...shared, ...Object.fromEntries(new URLSearchParams(body)) });
      send('Fetch.fulfillRequest', { requestId, responseCode: 204, responseHeaders: [{ name: 'Access-Control-Allow-Origin', value: '*' }] }).catch(() => {});
    } else {
      send('Fetch.fulfillRequest', { requestId, ...fromDist(request.url) }).catch(() => {});
    }
  };
  const patterns = [{ urlPattern: '*google-analytics.com/g/collect*' }, { urlPattern: '*analytics.google.com/g/collect*' }];
  if (LOCAL) patterns.push({ urlPattern: `${SITE}/*` }, { urlPattern: 'http://localhost:4321/*' });
  await send('Page.enable');
  await send('Network.enable');
  await send('Network.clearBrowserCookies');
  await send('Fetch.enable', { patterns });
  return {
    hits, send,
    pageViews: () => hits.filter((h) => h.en === 'page_view'),
    go: (url, referrer) => send('Page.navigate', referrer ? { url, referrer } : { url }),
    eval: async (expression) => (await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })).result.value,
    close: () => ws.close(),
  };
}

const results = [];
function check(name, ok, detail) {
  results.push(ok);
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : `\n      ${detail}`}`);
}
const describe = (hits) => JSON.stringify(hits.map((h) => ({ en: h.en, tid: h.tid, dl: h.dl, dr: h.dr })));

const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'ga-smoke-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
try {
  for (let i = 0; i < 50; i++) { try { await fetch(`http://127.0.0.1:${PORT}/json/version`); break; } catch { await sleep(200); } }
  console.log(`GA4 smoke test against ${LOCAL ? 'dist/ (served as the production host)' : 'the live site'}\n`);

  const pages = ['/', '/pisa_results/', '/about/', '/blog/', '/media/', '/publications/', '/teaching/', '/courses/deep-learning/', '/slides/deep-learning/class-01-introduccion.html'];
  for (const page of pages) {
    const s = await session();
    await s.go(SITE + page, GOOGLE); await sleep(4000);
    const views = s.pageViews();
    check(`landing ${page}`, views.length === 1 && views[0].tid === GA_ID && views[0].dl === SITE + page && views[0].dr === GOOGLE, describe(views));
    s.close();
  }

  {
    const s = await session();
    await s.go(`${SITE}/`, GOOGLE); await sleep(4000);
    // Within a session GA4 holds later page_views for ~5 s and flushes them on pagehide.
    await s.eval(`document.querySelector('a[href="/about/"]').click()`); await sleep(7000);
    const views = s.pageViews();
    check('internal navigation / -> /about/', views.length === 2 && views[1].dl === `${SITE}/about/` && views[1].dr === `${SITE}/` && views[0].sid === views[1].sid, describe(views));
    s.close();
  }

  {
    const s = await session();
    await s.go(`${SITE}/`, GOOGLE); await sleep(4000);
    await s.eval(`document.querySelector('a[href="/about/"]').click()`); await sleep(1000);
    await s.eval(`document.querySelector('a[href="/blog/"]').click()`); await sleep(7000);
    const views = s.pageViews().map((h) => h.dl);
    check('quick internal exit still records the page', views.join() === [`${SITE}/`, `${SITE}/about/`, `${SITE}/blog/`].join(), JSON.stringify(views));
    s.close();
  }

  for (const [legacy, destination] of [['/articulos/BigData/', '/blog/bigdata/'], ['/_events/gbm/', '/media/']]) {
    const s = await session();
    await s.go(SITE + legacy, GOOGLE); await sleep(5000);
    const views = s.pageViews();
    check(`legacy redirect ${legacy} keeps the Google referrer`, views.length === 1 && views[0].dl === SITE + destination && views[0].dr === GOOGLE, describe(views));
    s.close();
  }

  {
    const s = await session();
    await s.send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 3, mobile: true });
    await s.send('Emulation.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
    await s.go(`${SITE}/pisa_results/`, GOOGLE); await sleep(4000);
    const views = s.pageViews();
    check('mobile /pisa_results/', views.length === 1 && views[0].dl === `${SITE}/pisa_results/`, describe(views));
    s.close();
  }

  if (LOCAL) {
    const s = await session();
    for (const page of ['/', '/pisa_results/', '/slides/deep-learning/class-01-introduccion.html']) { await s.go(`http://localhost:4321${page}`); await sleep(2500); }
    const tagged = await s.eval('typeof window.gtag');
    check('localhost sends no hits', s.hits.length === 0 && tagged === 'undefined', `${s.hits.length} hits, gtag ${tagged}`);
    s.close();
  }
} finally {
  chrome.kill();
}

const failed = results.filter((ok) => !ok).length;
console.log(`\n${results.length - failed}/${results.length} checks passed`);
process.exit(failed ? 1 : 0);
