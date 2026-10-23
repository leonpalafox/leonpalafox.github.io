// Google Analytics 4, shared by Base.astro, the slide decks and the build check
// (scripts/check-ga.mjs). public/pisa_results/build/template.html is static and
// carries a copy of GA_SCRIPT; the build check keeps it in step.
export const GA_ID = 'G-M9BV46V3PD';
export const PRODUCTION_HOST = 'www.leonpalafox.com';
// Set by the legacy redirect pages (see LEGACY_REFERRER_SCRIPT) and consumed here.
const REFERRER_KEY = 'lp_referrer';

// Loads gtag only on the production host, so `astro dev`, `astro preview` and
// local servers never send hits to the property. A visitor who arrived through
// a legacy redirect page keeps the referrer that page saw (usually Google),
// instead of the redirect page itself, which GA4 would count as direct.
export const GA_SCRIPT = `if (location.hostname === '${PRODUCTION_HOST}') {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  let referrer = null;
  try { referrer = sessionStorage.getItem('${REFERRER_KEY}'); sessionStorage.removeItem('${REFERRER_KEY}'); } catch (e) {}
  gtag('js', new Date());
  gtag('config', '${GA_ID}', referrer ? { page_referrer: referrer } : {});
  const tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=${GA_ID}';
  document.head.appendChild(tag);
}`;

// Runs on the meta-refresh pages Astro writes for `redirects`. GitHub Pages
// cannot send real 301s, so the destination would otherwise see the redirect
// page as its referrer. Only an outside referrer is kept.
export const LEGACY_REFERRER_SCRIPT = `try { if (document.referrer && new URL(document.referrer).hostname !== location.hostname) sessionStorage.setItem('${REFERRER_KEY}', document.referrer); } catch (e) {}`;

export const GA_HEAD = `<link rel="preconnect" href="https://www.googletagmanager.com"><link rel="preconnect" href="https://www.google-analytics.com"><script>${GA_SCRIPT}</script>`;
