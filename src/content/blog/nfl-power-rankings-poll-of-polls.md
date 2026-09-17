---
title: "The NFL Power Rankings Poll of Polls"
description: "Nine outlets, one consensus: a statistically explicit poll of polls for the 2026 season, with the full Python pipeline and every source documented for weekly replication."
pubDate: 2026-09-17
lang: en
tags: ["data-viz", "nfl", "statistics", "python"]
---

Every Tuesday of the NFL season, a dozen outlets publish a power ranking. They disagree, usually in ways that feel arbitrary. So I did what you do with any panel of noisy opinions: I built a poll of polls, wrote it in Python, and made the disagreement the point.

Nine ballots, 32 teams, Week 2 of the 2026 season. Seattle and Buffalo are separated by **0.002 rank standard deviations** — a statistical tie at the top. Pittsburgh is ranked as high as 13th and as low as 27th. That is not noise to be averaged away; it is the story.

<nav class="toc" aria-label="Contents">
  <details open>
    <summary>
      <span class="toc-kicker">Contents</span>
      <span class="toc-count">9 sections</span>
    </summary>
    <ol>
      <li><a href="#consensus"><span class="toc-n">01</span><span class="toc-t">The consensus</span><span class="toc-d">All 32 teams, filterable by conference</span></a></li>
      <li><a href="#h2h"><span class="toc-n">02</span><span class="toc-t">This week's matchups, priced</span><span class="toc-d">All 16 games priced, plus any matchup you build</span></a></li>
      <li><a href="#top"><span class="toc-n">03</span><span class="toc-t">A tie at the top</span><span class="toc-d">Seattle, Buffalo and a 0.002-point gap</span></a></li>
      <li><a href="#argument"><span class="toc-n">04</span><span class="toc-t">Where the argument is</span><span class="toc-d">The teams nobody can place</span></a></li>
      <li><a href="#panel"><span class="toc-n">05</span><span class="toc-t">The panel</span><span class="toc-d">Nine outlets and how they agree</span></a></li>
      <li><a href="#pricing"><span class="toc-n">06</span><span class="toc-t">How matchups and rankings are priced</span><span class="toc-d">Win probabilities, the calibration, then the estimator</span></a></li>
      <li><a href="#method"><span class="toc-n">07</span><span class="toc-t">How the rankings are made</span><span class="toc-d">Standardise, pool, measure, shrink</span></a></li>
      <li><a href="#reproduce"><span class="toc-n">08</span><span class="toc-t">Reproduce it every week</span><span class="toc-d">The pipeline, the gate, the source manual</span></a></li>
      <li><a href="#honest"><span class="toc-n">09</span><span class="toc-t">Keeping this honest</span><span class="toc-d">How the calibration gets graded as the season runs</span></a></li>
    </ol>
  </details>
</nav>

<style>
  .toc {
    margin: 32px 0;
    border: 1px solid #e0dcd4; border-radius: 2px;
    background: #fbfaf7; padding: 4px 22px 14px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  .toc summary {
    display: flex; align-items: baseline; gap: 12px;
    padding: 12px 0 10px; cursor: pointer; list-style: none;
    border-bottom: 1px solid #e0dcd4;
  }
  .toc summary::-webkit-details-marker { display: none; }
  .toc summary::after {
    content: "\25BE"; font-size: 10px; color: #6b6b6b; margin-left: 6px;
    transition: transform 160ms ease-out;
  }
  .toc details:not([open]) summary::after { transform: rotate(-90deg); }
  .toc-kicker { font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: #0a0a0a; font-weight: 600; }
  .toc-count { font-size: 11px; color: #6b6b6b; margin-left: auto; }
  .toc ol { list-style: none; margin: 4px 0 0; padding: 0; }
  .toc li { margin: 0; border-bottom: 1px solid #ece8e0; }
  .toc li:last-child { border-bottom: 0; }
  .toc a {
    display: grid; grid-template-columns: 32px 1fr; gap: 0 10px;
    padding: 10px 0; text-decoration: none; color: #0a0a0a;
  }
  .toc a:hover { color: #c2472f; }
  .toc a:hover .toc-t { text-decoration: underline; text-underline-offset: 3px; }
  .toc-n {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px; color: #6b6b6b; padding-top: 3px;
  }
  .toc-t { font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
  .toc-d { grid-column: 2; font-size: 12.5px; color: #6b6b6b; margin-top: 2px; }
  @media (max-width: 560px) {
    .toc { padding: 4px 16px 12px; }
    .toc-t { font-size: 14px; }
  }
</style>

Here is the consensus, with the spread across outlets shown for every team.

<a id="consensus"></a>

<div id="pop-root" class="pop-root">
  <div class="pop-header">
    <div class="pop-kicker">2026 season · Week 2 · poll of polls</div>
    <h2 class="pop-headline">Nine outlets, one consensus.</h2>
    <p class="pop-lede">Each row is a team. The score is measured in rank standard deviations, so a value of +1.5 is roughly one and a half rank-spreads above the median team. The strip shows where each of the nine outlets placed that team, from first on the left to 32nd on the right. Click a row to see its individual ballots.</p>
  </div>

  <div class="pop-podium">
    <div class="pop-podium-row">
      <div class="pop-podium-team">
        <span class="pop-podium-rank">1</span>
        <span class="pop-mark pop-mark--lg" id="pop-p1-logo"></span>
        <span class="pop-podium-name">Seattle Seahawks</span>
      </div>
      <div class="pop-podium-meta">
        <span class="pop-podium-score" id="pop-p1-score"></span>
        <span class="pop-podium-p" id="pop-p1-p"></span>
      </div>
    </div>
    <div class="pop-podium-row">
      <div class="pop-podium-team">
        <span class="pop-podium-rank">2</span>
        <span class="pop-mark pop-mark--lg" id="pop-p2-logo"></span>
        <span class="pop-podium-name">Buffalo Bills</span>
      </div>
      <div class="pop-podium-meta">
        <span class="pop-podium-score" id="pop-p2-score"></span>
        <span class="pop-podium-p" id="pop-p2-p"></span>
      </div>
    </div>
    <p class="pop-podium-note" id="pop-tie-note"></p>
  </div>

  <div class="pop-controls">
    <div class="pop-chips" role="group" aria-label="Filter the consensus table">
      <button type="button" class="pop-chip is-on" data-filter="all">All 32 <span id="pop-count-all"></span></button>
      <button type="button" class="pop-chip" data-filter="AFC">AFC <span id="pop-count-afc"></span></button>
      <button type="button" class="pop-chip" data-filter="NFC">NFC <span id="pop-count-nfc"></span></button>
      <button type="button" class="pop-chip" data-filter="playoff">Playoff picture</button>
      <button type="button" class="pop-chip" data-filter="contested">Most contested</button>
    </div>
    <div class="pop-readout" id="pop-readout">Select any row for that team's nine ballots.</div>
  </div>

  <div class="pop-table-wrap">
    <table class="pop-table" id="pop-table">
      <thead>
        <tr>
          <th class="pop-th-rank">#</th>
          <th class="pop-th-team">Team</th>
          <th class="pop-th-num">Score</th>
          <th class="pop-th-num pop-hide-sm">95% CI</th>
          <th class="pop-th-num pop-hide-sm">Mean</th>
          <th class="pop-th-spread">Spread across nine outlets</th>
          <th class="pop-th-num" title="League-wide rank from the panel">Panel</th>
          <th class="pop-th-num">P(No. 1)</th>        </tr>
      </thead>
      <tbody id="pop-body"></tbody>
    </table>
  </div>
  <div class="pop-legend">
    <span class="pop-legend-item"><span class="pop-swatch pop-swatch-band"></span> interquartile spread of the nine ballots</span>
    <span class="pop-legend-item"><span class="pop-swatch pop-swatch-dot"></span> one outlet's rank</span>
    <span class="pop-legend-item">Scale: 1 → 32, left to right</span>
  </div>

  <div class="pop-sources">
    <div class="pop-sources-title">The panel — agreement with the consensus</div>
    <div class="pop-source-grid" id="pop-source-grid"></div>
  </div>

  <div class="pop-footnote">
    Scores are pooled and shrunk toward the panel mean (empirical Bayes). Rank intervals and P(No. 1) come from 4,000 bootstrap resamples over the nine sources. Club marks are the official team logos, used here for identification only. Full derivation, code, and the weekly replication checklist are documented at the end of this post.
  </div>
</div>

<style>
  .pop-root {
    --ink: #0a0a0a;
    --muted: #6b6b6b;
    --hair: #e0dcd4;
    --paper: #fbfaf7;
    --wash: rgba(255, 255, 255, 0.55);
    --signal: #c2472f;
    --signal-deep: #7e2b1f;
    background: var(--paper);
    color: var(--ink);
    border: 1px solid var(--hair);
    border-radius: 2px;
    padding: 28px 24px 22px;
    margin: 32px 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    box-sizing: border-box;
    width: 100%;
  }
  .pop-root *, .pop-root *::before, .pop-root *::after { box-sizing: border-box; }

  /* The widget renders inside `.prose-post`, whose article styles are right for
     prose and wrong for a data table: `prose-post img` draws a 1px frame plus
     vertical margins (which boxed every logo), and `prose-post th/td` draw full
     cell borders and a tinted header. Neither is scoped away, so reset them
     once here and let the component styles below do the painting. */
  .pop-root img { border: 0; margin: 0; max-width: none; }
  .pop-root table { margin-block: 0; border-collapse: collapse; }
  .pop-root th, .pop-root td {
    border: 0;
    padding: 0;
    background: none;
    font-weight: inherit;
    text-align: inherit;
  }
  .pop-kicker { font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }
  .pop-headline {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 34px; line-height: 1.02; letter-spacing: -0.03em;
    margin: 0; color: var(--ink);
  }
  .pop-lede { color: #525252; font-size: 14.5px; line-height: 1.62; margin: 14px 0 0; max-width: 760px; }

  .pop-podium {
    margin: 22px 0 6px;
    border: 1px solid var(--hair);
    background: var(--wash);
    border-radius: 2px;
    padding: 4px 16px 12px;
  }
  .pop-podium-row {
    display: flex; align-items: baseline; justify-content: space-between; gap: 16px;
    padding: 10px 0; border-bottom: 1px solid var(--hair);
    flex-wrap: wrap;
  }
  .pop-podium-row:last-of-type { border-bottom: 0; }
  .pop-podium-team { display: flex; align-items: center; gap: 12px; }
  .pop-podium-rank {
    font-family: Georgia, "Times New Roman", serif; font-size: 26px; color: var(--signal);
    min-width: 22px;
  }
  .pop-podium-name { font-size: 16px; font-weight: 600; }
  .pop-podium-meta { display: flex; align-items: baseline; gap: 14px; }
  .pop-podium-score { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; color: var(--ink); }
  .pop-podium-p { font-size: 12px; color: var(--muted); }
  .pop-podium-note { font-size: 12.5px; color: var(--muted); line-height: 1.55; margin: 8px 0 2px; }

  .pop-controls { display: flex; flex-direction: column; gap: 10px; margin: 20px 0 14px; }
  .pop-control-group { display: flex; align-items: center; gap: 10px; }
  .pop-label { font-size: 12px; color: var(--muted); }
  .pop-select {
    padding: 6px 10px; font-size: 13px; color: var(--ink);
    background: rgba(255,255,255,0.9); border: 1px solid #cfcac1; border-radius: 2px;
  }
  .pop-chips { display: flex; flex-wrap: wrap; gap: 7px; }
  .pop-chip {
    font: inherit; font-size: 12.5px; color: var(--ink); cursor: pointer;
    background: rgba(255,255,255,0.75); border: 1px solid #cfcac1;
    border-radius: 999px; padding: 5px 12px;
    transition: background 140ms ease-out, border-color 140ms ease-out, color 140ms ease-out;
  }
  .pop-chip:hover { background: #fff; border-color: #a9a29a; }
  .pop-chip.is-on {
    background: var(--signal); border-color: var(--signal); color: #fff; font-weight: 600;
  }
  .pop-chip span { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; opacity: 0.75; }
  .pop-group-head td {
    padding: 16px 8px 5px; font-size: 10.5px; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--muted); border-bottom: 1px solid var(--hair);
  }
  .pop-readout { font-size: 13px; color: #404040; min-height: 1.3em; }
  .pop-readout strong { color: var(--ink); }

  .pop-table-wrap { width: 100%; overflow-x: auto; }
  .pop-table { width: 100%; border-collapse: collapse; font-size: 13.5px; min-width: 560px; }
  .pop-table thead th {
    text-align: left; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--muted); font-weight: 500; padding: 6px 8px; border-bottom: 1px solid var(--ink);
    white-space: nowrap;
  }
  .pop-th-rank { width: 34px; }
  .pop-th-num { text-align: right !important; }
  .pop-th-spread { width: 42%; min-width: 200px; }
  .pop-table tbody tr { border-bottom: 1px solid var(--hair); cursor: pointer; }
  .pop-table tbody tr:hover { background: rgba(194, 71, 47, 0.05); }
  .pop-table tbody tr.is-open { background: rgba(194, 71, 47, 0.08); }
  .pop-table td { padding: 7px 8px; vertical-align: middle; }
  .pop-td-rank { font-family: Georgia, "Times New Roman", serif; font-size: 17px; color: var(--ink); }
  .pop-td-team { white-space: nowrap; }
  .pop-team-cell { display: flex; align-items: center; gap: 10px; }

  /* Club marks. The logos are irregularly shaped (a star, a horse, a letter),
     so a circular medallion gives every row the same silhouette.
     The disc is FLAT white with one hairline ring and one soft halo. An earlier
     version stacked a radial gradient, an inset ring, a drop shadow and two
     halo layers, and the combination moired into visible concentric rings at
     small sizes. Flat fill plus a single ring is visually quieter and renders
     cleanly at every size. */
  .pop-mark {
    position: relative; flex: none; display: inline-flex;
    align-items: center; justify-content: center;
    border-radius: 50%; background: #fff;
    box-shadow:
      0 0 0 1px rgba(110, 100, 90, 0.22),
      0 0 12px 2px rgba(194, 71, 47, 0.28);
    transition: box-shadow 180ms ease-out;
  }
  /* `prose-post img` (src/styles/global.css) frames every image in a post body
     with a 1px hairline border and vertical margins. The reset above removes
     it; this rule pins the geometry of the mark itself. */
  .pop-root .pop-mark img {
    border: 0;
    margin: 0;
    padding: 0;
    max-width: none;
    width: 72%; height: 72%;
    object-fit: contain;
    display: block;
  }
  .pop-mark--lg { width: 40px; height: 40px; }
  .pop-mark--md { width: 30px; height: 30px; }
  .pop-mark--sm { width: 22px; height: 22px; }
  .pop-table tbody tr:hover .pop-mark {
    box-shadow:
      0 0 0 1px rgba(126, 43, 31, 0.45),
      0 0 18px 5px rgba(194, 71, 47, 0.45);
  }
  .pop-team-text { display: flex; flex-direction: column; min-width: 0; }
  .pop-team-name { line-height: 1.2; }
  .pop-abbr { font-size: 10px; letter-spacing: 0.1em; color: var(--muted); margin-left: 6px; }
  .pop-div { font-size: 10.5px; color: var(--muted); display: block; margin-top: 1px; }
  .pop-td-num { text-align: right; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12.5px; white-space: nowrap; }
  .pop-ci { color: var(--muted); }
  .pop-spread { position: relative; height: 20px; }
  .pop-track {
    position: absolute; left: 0; right: 0; top: 9px; height: 1px; background: var(--hair);
  }
  .pop-band {
    position: absolute; top: 5px; height: 9px; border-radius: 5px;
    background: rgba(120, 113, 104, 0.16);
  }
  .pop-dot {
    position: absolute; top: 6px; width: 7px; height: 7px; border-radius: 50%;
    transform: translateX(-3.5px); background: #2f2c28; border: 1px solid var(--paper);
  }
  .pop-dot.is-neg { background: #b9b2a7; }
  .pop-flag {
    display: inline-block; margin-left: 8px; font-size: 9.5px; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--signal-deep); border: 1px solid rgba(194,71,47,0.35);
    padding: 1px 5px; border-radius: 2px; white-space: nowrap;
  }
  .pop-ballots { background: rgba(255,255,255,0.6); }
  .pop-ballots-inner { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 6px 16px; padding: 12px 4px 14px; }
  .pop-ballot-head {
    grid-column: 1 / -1; display: flex; align-items: center; gap: 9px;
    font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted);
    padding-bottom: 8px; margin-bottom: 2px; border-bottom: 1px solid var(--hair);
  }
  .pop-ballot { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; font-size: 12px; border-bottom: 1px dotted var(--hair); padding-bottom: 4px; }
  .pop-ballot-outlet { color: var(--muted); }
  .pop-ballot-rank { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--ink); }

  .pop-legend { display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 12px; font-size: 11.5px; color: var(--muted); }
  .pop-legend-item { display: inline-flex; align-items: center; gap: 6px; }
  .pop-swatch { display: inline-block; }
  .pop-swatch-band { width: 20px; height: 8px; border-radius: 4px; background: rgba(120, 113, 104, 0.22); }
  .pop-swatch-dot { width: 8px; height: 8px; border-radius: 50%; background: #2f2c28; }

  .pop-sources { margin-top: 26px; padding-top: 18px; border-top: 1px solid var(--hair); }
  .pop-sources-title { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }
  .pop-source-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }
  .pop-source {
    border: 1px solid var(--hair); background: var(--wash); border-radius: 2px;
    padding: 10px 12px; font-size: 12.5px; line-height: 1.45;
  }
  .pop-source-outlet { font-weight: 600; color: var(--ink); }
  .pop-source-analyst { color: var(--muted); font-size: 11.5px; margin-top: 1px; }
  .pop-source-stats { margin-top: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; color: #444; }
  .pop-source a { color: var(--signal-deep); text-decoration: underline; text-underline-offset: 3px; }

  .pop-footnote { margin-top: 20px; padding-top: 14px; border-top: 1px solid var(--hair); font-size: 11.5px; color: var(--muted); line-height: 1.6; }

  @media (max-width: 620px) {
    .pop-headline { font-size: 27px; }
    .pop-hide-sm { display: none; }
    .pop-th-spread { min-width: 150px; }
  }
</style>

<script>
(function () {
  // The data bundle is injected as window.__POP_DATA__ by the page build, which
  // runs the Python pipeline in analysis/nfl-power-rankings/ and points this
  // post at src/data/nfl-power-rankings-latest.json.
  var DATA = window.__POP_DATA__ || null;
  if (!DATA) { return; }

  var teams = DATA.teams;
  var sources = DATA.sources;
  var ranked = teams.slice().sort(function (a, b) { return a.rank - b.rank; });
  var band = function (values) {
    var sorted = values.slice().sort(function (a, b) { return a - b; });
    var q = function (p) {
      var pos = p * (sorted.length - 1);
      var lo = Math.floor(pos), hi = Math.ceil(pos);
      if (lo === hi) { return sorted[lo]; }
      return sorted[lo] * (1 - (pos - lo)) + sorted[hi] * (pos - lo);
    };
    return [q(0.25), q(0.75)];
  };
  var scale = function (rank) { return ((rank - 1) / 31) * 100; };
  var pct = function (x) { return Math.round(x * 100) + '%'; };
  var filterSummary = '';
  var groupHeads = [];
  // Club marks are served from the site's own /images/nfl/, fetched once by
  // analysis/nfl-power-rankings/tools/fetch_logos.py. `onerror` hides the image
  // so a missing file degrades to a text-only row instead of a broken icon.
  var logoUrl = function (abbr) { return '/images/nfl/' + abbr.toLowerCase() + '.svg'; };
  var logoTag = function (abbr, size) {
    return '<span class="pop-mark pop-mark--' + size + '">' +
      '<img src="' + logoUrl(abbr) + '" alt="" aria-hidden="true"' +
      ' loading="lazy" decoding="async" onerror="this.style.display=\'none\'">' +
      '</span>';
  };

  function renderPodium() {
    var first = ranked[0], second = ranked[1];
    var p1 = document.getElementById('pop-p1-score');
    var p2 = document.getElementById('pop-p2-score');
    if (p1) { p1.textContent = (first.score > 0 ? '+' : '') + first.score.toFixed(3); }
    if (p2) { p2.textContent = (second.score > 0 ? '+' : '') + second.score.toFixed(3); }
    document.getElementById('pop-p1-p').textContent = pct(first.pTop1) + ' chance of No. 1';
    document.getElementById('pop-p2-p').textContent = pct(second.pTop1) + ' chance of No. 1';
    document.getElementById('pop-p1-logo').innerHTML = logoTag(first.abbr, 'lg');
    document.getElementById('pop-p2-logo').innerHTML = logoTag(second.abbr, 'lg');
    var gap = Math.abs(first.score - second.score);
    var third = ranked[2];
    var nextGap = Math.abs(second.score - third.score);
    var ratio = gap > 0 ? Math.round(nextGap / gap) : null;
    document.getElementById('pop-tie-note').textContent =
      'The top two are separated by ' + gap.toFixed(3) + ' rank standard deviations' +
      (ratio ? ', against ' + nextGap.toFixed(3) + ' between second and third — a gap ' +
        ratio + '× wider.' : '.');
  }

  function renderRows() {
    var body = document.getElementById('pop-body');
    var html = '';
    for (var i = 0; i < teams.length; i++) {
      var t = teams[i];
      var ranks = [];
      for (var s = 0; s < sources.length; s++) {
        var value = t.bySource[sources[s].id];
        if (typeof value === 'number') { ranks.push(value); }
      }
      var quartiles = band(ranks);
      var mean = t.meanRank;
      var dots = '';
      for (var k = 0; k < ranks.length; k++) {
        var dev = ranks[k] - mean;
        var cls = dev > 2.5 ? 'pop-dot is-neg' : 'pop-dot';
        dots += '<span class="' + cls + '" style="left:' + scale(ranks[k]) + '%" title="rank ' + ranks[k] + '"></span>';
      }
      var contested = t.spread >= 10
        ? '<span class="pop-flag">' + t.spread + '-rank gap</span>'
        : '';
      html +=
        '<tr tabindex="0" role="button" aria-expanded="false" data-team="' + t.team + '"' +
          ' data-conf="' + t.conference + '" data-div="' + t.division + '"' +
          ' data-spread="' + t.spread + '" data-index="' + i + '">' +
          '<td class="pop-td-rank">' + t.rank + '</td>' +
          '<td class="pop-td-team"><div class="pop-team-cell">' + logoTag(t.abbr, 'md') +
            '<div class="pop-team-text"><span class="pop-team-name">' + t.team +
              '<span class="pop-abbr">' + t.abbr + '</span></span>' +
              '<span class="pop-div">' + t.conference + ' ' + t.division + '</span></div>' +
            '</div></td>' +
          '<td class="pop-td-num">' + (t.score > 0 ? '+' : '') + t.score.toFixed(3) + '</td>' +
          '<td class="pop-td-num pop-ci pop-hide-sm">' + t.ciLow.toFixed(2) + ' … ' + t.ciHigh.toFixed(2) + '</td>' +
          '<td class="pop-td-num pop-hide-sm">' + t.meanRank.toFixed(2) + '</td>' +
          '<td><div class="pop-spread"><span class="pop-track"></span>' +
            '<span class="pop-band" style="left:' + scale(quartiles[0]) + '%;width:' + (scale(quartiles[1]) - scale(quartiles[0])) + '%"></span>' +
            dots + '</div></td>' +
          '<td class="pop-td-num pop-td-league pop-ci"></td>' +
          '<td class="pop-td-num">' + pct(t.pTop1) + contested + '</td>' +
        '</tr>';
    }
    body.innerHTML = html;
  }

  // Which rows pass the active filter. One predicate, used both to show/hide and
  // to insert the conference/division group headings when a conference is shown.
  function matchesFilter(row, filter) {
    if (filter === 'all') { return true; }
    if (filter === 'AFC' || filter === 'NFC') { return row.getAttribute('data-conf') === filter; }
    if (filter === 'playoff') { return parseInt(row.getAttribute('data-index'), 10) < 14; }
    if (filter === 'contested') { return parseInt(row.getAttribute('data-spread'), 10) >= 10; }
    return true;
  }

  function computeRanks(rows, filter) {
    // In a conference view the table is grouped by division, and divisions have
    // no inherent order — so the displayed rank is the team's standing *within
    // the filtered set*, not its league-wide rank. The league number is kept in
    // a column that fills in only when the two differ.
    for (var i = 0; i < rows.length; i++) { if (!rows[i]._leagueRank) { rows[i]._leagueRank = i + 1; } }

    if (filter === 'AFC' || filter === 'NFC') {
      var byDivision = {};
      for (var j = 0; j < rows.length; j++) {
        var key = rows[j].getAttribute('data-div');
        (byDivision[key] = byDivision[key] || []).push(rows[j]);
      }
      var order = Object.keys(byDivision).sort();
      var counter = 0;
      for (var k = 0; k < order.length; k++) {
        var group = byDivision[order[k]];
        for (var g = 0; g < group.length; g++) { group[g]._rank = ++counter; }
      }
      return order.map(function (d) { return { label: filter + ' ' + d, rows: byDivision[d] }; });
    }

    var sorted = rows.slice().sort(function (a, b) { return a._leagueRank - b._leagueRank; });
    for (var n = 0; n < sorted.length; n++) { sorted[n]._rank = n + 1; }
    return [{ label: null, rows: sorted }];
  }

  function applyFilter() {
    var chip = document.querySelector('.pop-chip.is-on');
    var filter = chip ? chip.getAttribute('data-filter') : 'all';
    var body = document.getElementById('pop-body');

    // League rank is cached on each row the first time it is read, so a later
    // reorder can never lose the league-wide anchor.
    var all = body.querySelectorAll('tr[data-team]');
    for (var t = 0; t < all.length; t++) {
      if (!all[t]._leagueRank) {
        all[t]._leagueRank = parseInt(all[t].getAttribute('data-index'), 10) + 1;
      }
      all[t].style.display = matchesFilter(all[t], filter) ? '' : 'none';
    }

    var visible = [];
    for (var i = 0; i < all.length; i++) { if (all[i].style.display !== 'none') { visible.push(all[i]); } }

    // Group headings are rebuilt from scratch on every pass. They are tracked
    // in their own array because they are not tr[data-team], so leaving them
    // behind would accumulate headings across filter changes.
    for (var d = 0; d < groupHeads.length; d++) {
      if (groupHeads[d].parentNode) { groupHeads[d].parentNode.removeChild(groupHeads[d]); }
    }
    groupHeads = [];

    var groups = computeRanks(visible, filter);
    for (var gi = 0; gi < groups.length; gi++) {
      if (groups[gi].label) {
        var head = document.createElement('tr');
        head.className = 'pop-group-head';
        var cell = document.createElement('td');
        cell.colSpan = 8;
        cell.textContent = groups[gi].label;
        head.appendChild(cell);
        body.appendChild(head);
        groupHeads.push(head);
      }
      for (var ri = 0; ri < groups[gi].rows.length; ri++) {
        body.appendChild(groups[gi].rows[ri]);  // re-appending moves the node
      }
    }

    for (var v = 0; v < visible.length; v++) {
      var row = visible[v];
      var number = row.querySelector('.pop-td-rank');
      if (number) { number.textContent = row._rank; }
      var panelColumn = row.querySelector('.pop-td-league');
      if (panelColumn) {
        panelColumn.textContent = (row._leagueRank === row._rank) ? '' : '#' + row._leagueRank;
      }
    }

    var open = body.querySelectorAll('tr.pop-ballots');
    for (var c = 0; c < open.length; c++) { open[c].parentNode.removeChild(open[c]); }
    var openRows = body.querySelectorAll('tr.is-open');
    for (var o = 0; o < openRows.length; o++) { openRows[o].classList.remove('is-open'); }

    var conference = filter === 'AFC' || filter === 'NFC';
    filterSummary = visible.length + ' of ' + all.length + ' teams' +
      (conference ? ' · ' + filter + ' only, grouped by division' : '');
    renderReadout(null);
  }

  function renderSources() {
    var grid = document.getElementById('pop-source-grid');
    var html = '';
    for (var i = 0; i < sources.length; i++) {
      var s = sources[i];
      html +=
        '<div class="pop-source">' +
          '<div class="pop-source-outlet">' + s.outlet + '</div>' +
          '<div class="pop-source-analyst">' + s.analyst + '</div>' +
          '<div class="pop-source-stats">&rho; vs consensus ' + s.rho_consensus.toFixed(3) +
            ' · mean gap ' + s.mean_abs_dev.toFixed(2) + ' ranks</div>' +
          '<div><a href="' + s.url + '" rel="nofollow noopener" target="_blank">this week&rsquo;s ranking</a></div>' +
        '</div>';
    }
    grid.innerHTML = html;
  }

  function renderReadout(team) {
    var out = document.getElementById('pop-readout');
    if (!team) {
      out.textContent = filterSummary || 'Select any row for that team&rsquo;s nine ballots.';
      return;
    }
    out.innerHTML = '<strong>' + team.team + '</strong> — consensus #' + team.rank +
      ', ranked ' + team.rankMin + ' to ' + team.rankMax + ' by the panel.';
  }

  function renderBallots(team, row) {
    var existing = row.nextElementSibling;
    if (existing && existing.classList.contains('pop-ballots')) {
      existing.parentNode.removeChild(existing);
      row.classList.remove('is-open');
      row.setAttribute('aria-expanded', 'false');
      renderReadout(null);
      return;
    }
    var clear = document.querySelectorAll('.pop-ballots');
    for (var c = 0; c < clear.length; c++) { clear[c].parentNode.removeChild(clear[c]); }
    var open = document.querySelectorAll('.pop-table tbody tr.is-open');
    for (var o = 0; o < open.length; o++) {
      open[o].classList.remove('is-open');
      open[o].setAttribute('aria-expanded', 'false');
    }

    var cells = '';
    for (var i = 0; i < sources.length; i++) {
      var rank = team.bySource[sources[i].id];
      cells += '<div class="pop-ballot"><span class="pop-ballot-outlet">' + sources[i].outlet +
        '</span><span class="pop-ballot-rank">' + (typeof rank === 'number' ? rank : '—') + '</span></div>';
    }
    var tr = document.createElement('tr');
    tr.className = 'pop-ballots';
    tr.innerHTML = '<td colspan="8"><div class="pop-ballots-inner">' +
      '<div class="pop-ballot-head">' + logoTag(team.abbr, 'sm') +
        '<span>' + team.team + ' — every ballot</span></div>' + cells + '</div></td>';
    row.parentNode.insertBefore(tr, row.nextSibling);
    row.classList.add('is-open');
    row.setAttribute('aria-expanded', 'true');
    renderReadout(team);
  }

  renderPodium();
  renderRows();
  renderSources();

  // Chip counts, so a reader can see the split before clicking.
  var afc = teams.filter(function (t) { return t.conference === 'AFC'; }).length;
  var nfc = teams.length - afc;
  document.getElementById('pop-count-all').textContent = teams.length;
  document.getElementById('pop-count-afc').textContent = afc;
  document.getElementById('pop-count-nfc').textContent = nfc;

  var chips = document.querySelectorAll('.pop-chip');
  for (var c = 0; c < chips.length; c++) {
    chips[c].addEventListener('click', function (event) {
      for (var j = 0; j < chips.length; j++) { chips[j].classList.remove('is-on'); }
      event.currentTarget.classList.add('is-on');
      applyFilter();
    });
  }
  applyFilter();

  var body = document.getElementById('pop-body');
  function toggleFrom(event) {
    var row = event.target.closest('tr[data-team]');
    if (!row) { return; }
    var team = null;
    for (var i = 0; i < teams.length; i++) {
      if (teams[i].team === row.getAttribute('data-team')) { team = teams[i]; break; }
    }
    if (team) { renderBallots(team, row); }
  }
  body.addEventListener('click', toggleFrom);
  body.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggleFrom(event);
    }
  });
})();
</script>

<a id="h2h"></a>

## This week's matchups

Every team plays in Week 2, so the slate is a clean test of what the panel
thinks. All 16 games are priced below from the consensus alone, followed by a
sandbox for building any matchup you like. The derivation, the calibration and
its limits sit in the methodology further down.

<div id="h2h-root" class="h2h-root">
  <div class="h2h-head">
    <div class="h2h-kicker" id="h2h-kicker">2026 season · Week 2 · head to head</div>
    <h3 class="h2h-title">What the consensus says about this week.</h3>
    <p class="h2h-lede">Every game, priced from the poll of polls alone. Win probability is the shaded side. The market column is shown for comparison and was <em>not</em> an input — on this slate the two agree on the favourite in 15 of 16 games.</p>
  </div>

  <div class="h2h-filter">
    <label class="h2h-label" for="h2h-view">Show</label>
    <select id="h2h-view" class="h2h-select">
      <option value="all">All 16 games</option>
      <option value="close">Closest 5</option>
      <option value="lopsided">Most lopsided 5</option>
    </select>
    <span class="h2h-note" id="h2h-note"></span>
  </div>

  <div class="h2h-games" id="h2h-games"></div>

  <div class="h2h-picker">
    <div class="h2h-picker-title">Or build any matchup</div>
    <div class="h2h-picker-controls">
      <label class="h2h-team">
        <span>Team A</span>
        <select id="h2h-a" class="h2h-select"></select>
      </label>
      <label class="h2h-team">
        <span>Team B</span>
        <select id="h2h-b" class="h2h-select"></select>
      </label>
      <label class="h2h-team">
        <span>Venue</span>
        <select id="h2h-venue" class="h2h-select">
          <option value="home">A hosts B</option>
          <option value="neutral">Neutral field</option>
        </select>
      </label>
    </div>
    <div class="h2h-result" id="h2h-result"></div>
  </div>

  <div class="h2h-foot">
    <span id="h2h-model"></span>
    Schedule from nflverse. Closing lines shown for reference only.
    <span class="h2h-more">How these numbers are derived, and how well they hold up, is in the methodology below.</span>
  </div>
</div>

<style>
  .h2h-root {
    --ink: #0a0a0a; --muted: #6b6b6b; --hair: #e0dcd4; --paper: #fbfaf7;
    --wash: rgba(255, 255, 255, 0.55); --signal: #c2472f; --signal-deep: #7e2b1f;
    background: var(--paper); color: var(--ink);
    border: 1px solid var(--hair); border-radius: 2px;
    padding: 28px 24px 22px; margin: 32px 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    box-sizing: border-box; width: 100%;
  }
  .h2h-root *, .h2h-root *::before, .h2h-root *::after { box-sizing: border-box; }
  /* Same reset as the consensus widget: this renders inside `.prose-post`,
     where img gets a frame and th/td get borders that would box everything. */
  .h2h-root img { border: 0; margin: 0; max-width: none; display: block; }
  .h2h-root table { margin-block: 0; border-collapse: collapse; }
  .h2h-root th, .h2h-root td {
    border: 0; padding: 0; background: none; font-weight: inherit; text-align: inherit;
  }
  .h2h-kicker { font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }
  .h2h-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 26px; line-height: 1.05; letter-spacing: -0.025em; margin: 0;
  }
  .h2h-lede { color: #525252; font-size: 14px; line-height: 1.6; margin: 12px 0 0; max-width: 760px; }
  .h2h-lede em { font-style: italic; }
  .h2h-filter { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin: 20px 0 12px; }
  .h2h-label { font-size: 12px; color: var(--muted); }
  .h2h-select {
    padding: 6px 10px; font-size: 13px; color: var(--ink);
    background: rgba(255,255,255,0.9); border: 1px solid #cfcac1; border-radius: 2px;
  }
  .h2h-note { font-size: 12px; color: var(--muted); }

  .h2h-games { display: grid; gap: 8px; }
  .h2h-game {
    display: grid; grid-template-columns: 1fr auto 1fr;
    align-items: center; gap: 10px;
    border: 1px solid var(--hair); background: var(--wash);
    border-radius: 2px; padding: 9px 12px;
  }
  .h2h-side { display: flex; align-items: center; gap: 9px; min-width: 0; }
  .h2h-side.is-away { justify-content: flex-end; text-align: right; }
  .h2h-side.is-away .h2h-team-text { align-items: flex-end; }
  .h2h-mark { width: 30px; height: 30px; border-radius: 50%; background: #fff; flex: none;
    display: inline-flex; align-items: center; justify-content: center;
    box-shadow: 0 0 0 1px rgba(110,100,90,.22), 0 0 10px 1px rgba(194,71,47,.22); }
  .h2h-mark img { width: 72%; height: 72%; object-fit: contain; }
  .h2h-team-text { display: flex; flex-direction: column; min-width: 0; }
  .h2h-abbr { font-size: 15px; font-weight: 600; letter-spacing: 0.01em; }
  .h2h-team-name { font-size: 10.5px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .h2h-pick-tag { font-size: 9.5px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--signal-deep); }
  .h2h-centre { text-align: center; min-width: 118px; }
  .h2h-when { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
  .h2h-prob { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 15px; }
  .h2h-prob .win { color: var(--ink); font-weight: 600; }
  .h2h-prob .lose { color: var(--muted); }
  .h2h-bar { height: 4px; border-radius: 2px; background: var(--hair); overflow: hidden; margin-top: 5px; }
  .h2h-bar span { display: block; height: 100%; background: var(--signal); }
  .h2h-meta { font-size: 10.5px; color: var(--muted); margin-top: 3px; }
  .h2h-delta { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }

  .h2h-picker { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--hair); }
  .h2h-picker-title { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }
  .h2h-picker-controls { display: flex; gap: 14px; flex-wrap: wrap; }
  .h2h-team { display: flex; flex-direction: column; gap: 5px; font-size: 11.5px; color: var(--muted); }
  .h2h-result {
    margin-top: 16px; border: 1px solid var(--hair); border-radius: 2px;
    background: var(--wash); padding: 16px;
  }
  .h2h-result-inner { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
  .h2h-verdict { font-family: Georgia, "Times New Roman", serif; font-size: 22px; letter-spacing: -0.015em; }
  .h2h-verdict strong { color: var(--signal-deep); }
  .h2h-split { flex: 1; min-width: 220px; }
  .h2h-split-bar { display: flex; height: 26px; border-radius: 2px; overflow: hidden; border: 1px solid var(--hair); }
  .h2h-split-bar span { display: flex; align-items: center; justify-content: center;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
  .h2h-split-a { background: var(--signal); color: #fff; }
  .h2h-split-b { background: #e8e4dc; color: var(--ink); }
  .h2h-split-legend { display: flex; justify-content: space-between; font-size: 11px; color: var(--muted); margin-top: 5px; }
  .h2h-more { display: block; margin-top: 6px; color: #525252; }
  .h2h-foot { margin-top: 20px; padding-top: 14px; border-top: 1px solid var(--hair); font-size: 11.5px; color: var(--muted); line-height: 1.6; }

  @media (max-width: 620px) {
    .h2h-game { grid-template-columns: 1fr; }
    .h2h-side.is-away { justify-content: flex-start; text-align: left; }
    .h2h-side.is-away .h2h-team-text { align-items: flex-start; }
    .h2h-centre { text-align: left; min-width: 0; }
  }
</style>

<script>
(function () {
  var DATA = (window.__POP_DATA__ && window.__POP_DATA__.headToHead) || null;
  if (!DATA) { return; }

  var games = DATA.games || [];
  var model = DATA.model || {};
  var scores = {};
  var names = {};
  var abbrs = {};
  (window.__POP_DATA__.teams || []).forEach(function (t) {
    scores[t.team] = t.score;
    names[t.abbr] = t.team;
    abbrs[t.team] = t.abbr;
  });

  var logoUrl = function (abbr) { return '/images/nfl/' + abbr.toLowerCase() + '.svg'; };
  var mark = function (abbr) {
    return '<span class="h2h-mark"><img src="' + logoUrl(abbr) + '" alt="" aria-hidden="true"' +
      ' loading="lazy" decoding="async" onerror="this.style.display=\'none\'"></span>';
  };
  var pct = function (x) { return (x * 100).toFixed(x < 0.1 || x > 0.9 ? 1 : 0) + '%'; };
  var signed = function (x) { return (x > 0 ? '+' : '') + x.toFixed(1); };
  var dayLabel = function (g) {
    if (!g.gameday) { return g.kickoff || ''; }
    var parts = g.gameday.split('-');
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var label = months[parseInt(parts[1], 10) - 1] + ' ' + parseInt(parts[2], 10);
    return g.kickoff ? label + ' · ' + g.kickoff : label;
  };

  function gameRow(g) {
    var homeFav = g.homeWinProbability >= 0.5;
    var p = g.homeWinProbability;
    var market = g.marketSpread === null || g.marketSpread === undefined
      ? 'no line' : 'market ' + signed(g.marketSpread);
    var delta = (g.marketSpread === null || g.marketSpread === undefined)
      ? '' : ' <span class="h2h-delta">(' + signed(g.expectedMargin - g.marketSpread) + ')</span>';
    return '<div class="h2h-game">' +
      '<div class="h2h-side is-away">' +
        '<div class="h2h-team-text">' +
          '<span class="h2h-abbr">' + g.awayAbbr + (homeFav ? '' : ' <span class="h2h-pick-tag">pick</span>') + '</span>' +
          '<span class="h2h-team-name">' + g.away + ' · ' + g.awayScore.toFixed(2) + '</span>' +
        '</div>' + mark(g.awayAbbr) +
      '</div>' +
      '<div class="h2h-centre">' +
        '<div class="h2h-when">' + dayLabel(g) + '</div>' +
        '<div class="h2h-prob"><span class="win">' + pct(Math.max(p, 1 - p)) + '</span> ' +
          '<span class="lose">' + (homeFav ? g.homeAbbr : g.awayAbbr) + '</span></div>' +
        '<div class="h2h-bar"><span style="width:' + (p * 100) + '%"></span></div>' +
        '<div class="h2h-meta">' + g.pick + ' · ' + market + delta + '</div>' +
      '</div>' +
      '<div class="h2h-side">' + mark(g.homeAbbr) +
        '<div class="h2h-team-text">' +
          '<span class="h2h-abbr">' + g.homeAbbr + (homeFav ? ' <span class="h2h-pick-tag">pick</span>' : '') + '</span>' +
          '<span class="h2h-team-name">' + g.home + ' · ' + g.homeScore.toFixed(2) + '</span>' +
        '</div>' +
      '</div>' +
    '</div>';
  }

  function renderGames() {
    var view = document.getElementById('h2h-view').value;
    var list = games.slice();
    if (view === 'close') {
      list.sort(function (a, b) { return Math.abs(a.homeWinProbability - 0.5) - Math.abs(b.homeWinProbability - 0.5); });
      list = list.slice(0, 5);
    } else if (view === 'lopsided') {
      list.sort(function (a, b) { return Math.abs(b.homeWinProbability - 0.5) - Math.abs(a.homeWinProbability - 0.5); });
      list = list.slice(0, 5);
    }
    document.getElementById('h2h-games').innerHTML = list.map(gameRow).join('');
    document.getElementById('h2h-note').textContent =
      view === 'all' ? games.length + ' games this week' : 'showing ' + list.length + ' of ' + games.length;
  }

  function predict(homeScore, awayScore, neutral) {
    var edge = neutral ? 0 : model.homeField;
    var margin = model.k * (homeScore - awayScore) + edge;
    // Phi via an Abramowitz-Stegun style erf approximation, matching the parser.
    var z = margin / model.sigma;
    var t = 1 / (1 + 0.2316419 * Math.abs(z));
    var d = 0.3989422804014327 * Math.exp(-z * z / 2);
    var poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
    var cdf = z >= 0 ? 1 - d * poly : d * poly;
    return { margin: margin, home: cdf };
  }

  function renderPicker() {
    var a = document.getElementById('h2h-a').value;
    var b = document.getElementById('h2h-b').value;
    var neutral = document.getElementById('h2h-venue').value === 'neutral';
    var result = predict(scores[a], scores[b], neutral);
    var aWins = result.home >= 0.5;
    var favourite = aWins ? a : b;
    var pFav = Math.max(result.home, 1 - result.home);
    var pA = result.home;
    document.getElementById('h2h-result').innerHTML =
      '<div class="h2h-result-inner">' +
        '<div class="h2h-verdict"><strong>' + abbrs[favourite] + '</strong> by ' +
          Math.abs(result.margin).toFixed(1) + '</div>' +
        '<div class="h2h-split">' +
          '<div class="h2h-split-bar">' +
            '<span class="h2h-split-a" style="width:' + (pA * 100) + '%">' + (pA >= 0.14 ? pct(pA) : '') + '</span>' +
            '<span class="h2h-split-b" style="width:' + ((1 - pA) * 100) + '%">' + ((1 - pA) >= 0.14 ? pct(1 - pA) : '') + '</span>' +
          '</div>' +
          '<div class="h2h-split-legend">' +
            '<span>' + names[a] + ' ' + (neutral ? '(neutral)' : '(home)') + '</span>' +
            '<span>' + names[b] + '</span>' +
          '</div>' +
        '</div>' +
      '</div>';
  }

  // Team selects, ordered by consensus.
  var ordered = Object.keys(abbrs).sort(function (x, y) { return scores[y] - scores[x]; });
  var options = ordered.map(function (t) {
    return '<option value="' + t + '">' + abbrs[t] + ' — ' + t + '</option>';
  }).join('');
  var selectA = document.getElementById('h2h-a');
  var selectB = document.getElementById('h2h-b');
  selectA.innerHTML = options;
  selectB.innerHTML = options;
  // Set both values explicitly: relying on the browser to default a fresh
  // <select> to its first option leaves .value empty if the options were
  // injected as markup, which silently produced "undefined" in the readout.
  if (ordered.length) {
    selectA.value = ordered[0];
    selectB.value = ordered[1] || ordered[0];
  }

  document.getElementById('h2h-view').addEventListener('change', renderGames);
  [selectA, selectB, document.getElementById('h2h-venue')].forEach(function (el) {
    el.addEventListener('change', renderPicker);
  });
  document.getElementById('h2h-model').textContent =
    'Model: k = ' + model.k + ' pts per score unit, home field ' + model.homeField +
    ' pts, sigma = ' + model.sigma + ' pts. ' + (model.nGames || 0).toLocaleString() +
    ' games fitted. ';

  renderGames();
  renderPicker();
})();
</script>

<a id="top"></a>

## A tie at the top is the correct answer

Buffalo and Seattle split the first-place votes four apiece, with Baltimore taking the ninth. The bootstrap gives Buffalo a **59% chance** of topping a randomly re-drawn panel, but Seattle wins the point estimate, because Seattle's worst ballot is fourth while Buffalo slips to fourth three times. The gap between the two scores is 0.002 z-units. For scale, the gap between second and third is 0.156 — nearly eighty times larger.

So the honest headline is not "Seattle is No. 1." It is "Seattle and Buffalo are tied, and you should be suspicious of anyone who tells you otherwise after one week."

<a id="argument"></a>

## The middle is where the argument is

The top of the table is boring for a statistical reason: between-team variance is enormous and the panel agrees closely, so the shrinkage reliability λ is 0.991 and the intervals are tight. The interesting teams are the ones nobody can place.

| Team | Consensus | Highest | Lowest | Gap |
|------|-----------|---------|--------|-----|
| Pittsburgh Steelers | 19 | 13 | 27 | 14 |
| Philadelphia Eagles | 10 | 6 | 18 | 12 |
| Tampa Bay Buccaneers | 21 | 14 | 26 | 12 |
| Chicago Bears | 5 | 2 | 13 | 11 |
| Cincinnati Bengals | 9 | 4 | 14 | 10 |

Chicago is the sharpest example. The Bears are fifth overall and have an 11-rank spread: two outlets have them second, one has them thirteenth. That is not a rounding error, it is a genuine disagreement about whether a 59-point opening week was signal or noise. The poll of polls reports the disagreement rather than resolving it by fiat.

<a id="panel"></a>

## The panel

| Outlet | Analyst | Mean gap (ranks) | ρ vs consensus |
|--------|---------|------------------|----------------|
| NFL.com UK | Neil Reynolds | 1.12 | 0.985 |
| CBS Sports | Pete Prisco | 1.44 | 0.975 |
| theScore | theScore NFL desk | 1.62 | 0.977 |
| Sports Illustrated | Conor Orr | 1.81 | 0.963 |
| FOX Sports | Ralph Vacchiano | 1.94 | 0.969 |
| Sharp Football Analysis | Raymond Summerlin | 1.94 | 0.960 |
| NFL.com | Nick Shook | 2.06 | 0.950 |
| USA Today | Nate Davis | 2.06 | 0.956 |
| Sporting News | Vinnie Iyer | 2.44 | 0.947 |

Mean pairwise agreement across the panel is **ρ = 0.926**, with a range of 0.86 to 0.97. That is high enough for the consensus to mean something, and low enough that the consensus is not just one opinion copied nine times.

ESPN is deliberately absent. Every URL on the site — including the homepage — returns an empty `HTTP 202` to a plain request, and its JSON API returns 403. Rather than scrape awkwardly or hand-transcribe a ballot, the panel documents the omission. When a headless renderer is worth the complexity, ESPN belongs in the panel.

<a id="pricing"></a>

## How the matchups are priced

A ranking is an ordering, not a score, so pricing a game means giving the consensus a scale in points. That model has three constants and no free parameters:

```
margin(away @ home) = k * (consensus_home - consensus_away) + H
margin              ~ Normal(mean = margin, sd = sigma)
P(home wins)        = Phi(margin / sigma)
```

`k` converts a gap in consensus score into a gap in points, `H` is home-field advantage, and `sigma` is how far an actual margin typically lands from its expectation. Under the fitted values — **k = 4.59 points per score unit, H = 2.56 points, sigma = 13.16 points** — a team one full score-unit better than its opponent is about 4.6 points better on a neutral field, and the 13.2-point spread of outcomes is what keeps a 7-point edge from being a 90% win probability.

Those constants are not chosen by eye. `tools/calibrate.py` fits them from **6,719 completed regular-season games across 2000–2025**:

1. Build each team's strength from that season's point differentials, standardised — and **leave the game being predicted out** of the ratings that predict it.
2. Fit `k` and `H` by least squares of the realised margin on the rating difference. Points are measured in points, so this fixes the scale directly.
3. Take `sigma` as the residual standard deviation, which is precisely the spread the probability step needs.

### One methodological trap worth naming

The obvious approach is to grid-search all three constants by minimising log-loss on completed games. It produces beautiful probabilities and a nonsense scale, because **the win/loss likelihood only identifies the ratios** `k/sigma` and `H/sigma`. The optimum sits on a flat ridge, and the grid search returns whichever ridge point it happens to touch: a narrow grid gave `k = 5.7, sigma = 15.5`, and widening the same grid gave `k = 8.25, sigma = 21.1` — identical log-loss, but the second would project 21-point margins between ordinary teams. The scale has to come from the quantity that carries units. That is why the fit is staged rather than joint, and why log-loss appears below as a check instead of an objective.

A second trap, caught the same way: without the leave-one-out step, a game helps set its own ratings and the slope inflates — `k = 5.66` where the honest number is `4.78` for 2025 alone.

### Does it work?

Graded on those 26 seasons, the model lands where a coin flip and the closing line bracket it:

| | log-loss (lower is better) |
|---|---|
| Coin flip | 0.693 |
| **This model** | **0.612** |
| Closing lines | 0.609 |

It picks 66.8% of games correctly, and it is well calibrated: in the 2025 season, games it called at 80–90% went 67% of the time in the 80–90% band, and 90%+ calls hit 92%.

The honest comparison is the closing line, and the model is close to it — which is the expected result, not a triumph. Nine thoughtful rankings contain most of what a market knows, plus noise, and no amount of statistical care extracts information that was never in the ballots.

### What this is not

This is not a betting model, and it should not be read as one. It uses **only** what the nine rankings say. No injury reports, rest, travel, weather, or market information enters a published number; closing lines appear in the pipeline solely as the independent benchmark in the table above. It also inherits every blind spot of the panel: if all nine outlets misjudge a team the same way, the probability is confidently wrong. `sigma` is sized to absorb that, which is why a decent edge still leaves a live underdog.

<a id="method"></a>

## How the numbers are made

The four steps, in order. Full derivations with citations are in the pipeline's `METHODOLOGY.md`.

**1. Standardise.** A ballot is a permutation of 1–32, so its mean (16.5) and standard deviation (9.30) are known analytically. Every rank becomes a z-score with the sign flipped so positive is better. A source that spreads teams out and one that clusters them end up on the same scale, so neither gains influence from style.

**2. Pool.** Sources are weighted by the credibility priors in `sources.json` (all between 0.75 and 1.00), which keeps any one outlet from swinging the result.

**3. Measure the uncertainty two ways.** A **jackknife** drops one outlet at a time and recomputes the consensus; how much a team's score moves is that team's sampling variance. Separately, a **split-half** procedure correlates the consensus computed from two random halves of the panel, then steps the correlation up with the Spearman-Brown formula. That answers the question every poll of polls should answer and almost none do: *how many independent voices is this panel actually worth?* For these nine outlets, ρ between halves is 0.983 and the effective count is 9.0 — the panel is unusually independent. When a panel is not (syndicated copies, or two desks from one outlet), the effective count drops and the published intervals widen automatically.

**4. Shrink, then bootstrap the ranks.** Empirical-Bayes shrinkage pulls each team's pooled score toward the panel mean by a reliability factor estimated from the data itself. It keeps a team that exactly one outlet loves from jumping the consensus. Rank intervals and P(No. 1) come from 4,000 bootstrap resamples over the sources, so a position that depends on which outlets are in the room shows up as a wide interval.

One honest limitation: this measures the *panel*, not the truth. If all nine outlets share the same blind spot, the consensus shares it too, and no amount of clever weighting fixes that. The agreement matrix is the early-warning system — if pairwise correlations ever drift toward 0.99, it means the panel has stopped being nine opinions.

<a id="reproduce"></a>

## Reproduce it every week

The whole thing is one pure-standard-library Python package — no `numpy`, no `pandas`, no `requests`. The pipeline lives in `analysis/nfl-power-rankings/`: nine parsers, a validation gate, the estimator, and the report generator.

```bash
cd analysis/nfl-power-rankings
python3 -m unittest discover -s tests   # 50 tests, offline
python3 run.py --validate               # fetch, parse, validate — write nothing
python3 run.py                          # full run, refreshes this page's data
```

Two documents matter if you want to run it yourself each week:

- **`SOURCES.md`** is the replication manual. For all nine outlets it records the exact URL pattern, publication cadence, HTML structure, the parser that reads it, and the specific traps — USA Today's slug week *lags* the edition number, FOX writes its list backwards from 32 to 1, NFL.com's movement widget prints a number right after the rank, Sharp's URL never changes so freshness has to be checked by hand. It also has a six-step weekly checklist and a worked example of adding a tenth source.
- **`METHODOLOGY.md`** is the statistics. Jackknife variance, Spearman-Brown reliability, method-of-moments variance decomposition, the shrinkage factor, the bootstrap, and a section on what the method does *not* claim.

Every run caches the raw HTML for each source and records its SHA-256 in `consensus.json`, so any published week can be re-derived byte-for-byte. The validation gate refuses to publish unless every ballot contains all 32 clubs exactly once, no two ballots are identical syndicated copies, and at least five complete sources are available. A parser that grabs a sidebar fails the build instead of quietly contributing a wrong number.

<a id="honest"></a>

## Keeping this honest as the season runs

The interesting part is not the Week 2 numbers, which will be wrong somewhere by Sunday night. It is whether the calibration holds. Each run writes `out/matchups.csv` with one row per game — projected margin, win probability, pick, and the closing line — and the columns for the final score are left empty on purpose. When the games are played, the scores get filled in and the same metrics that graded the historical fit (log-loss, Brier score, accuracy, and the calibration curve) can be recomputed on this season's results.

That also gives the scale a weekly chance to fail. If `k` drifts, or the model's log-loss pulls away from the closing line's, that is evidence that the panel's consensus has stopped carrying information the market doesn't already have — which is worth reporting, and worth knowing before it becomes a comfortable assumption.

I will keep this updated through the season — the same nine outlets, the same estimator, with the week's URL list rotated in `sources.json`. The interesting output will not be the rankings themselves but the reliability statistics week to week: whether the panel tightens as the season reveals teams, which clubs the consensus is genuinely unsure about, and whether the head-to-head model stays within touching distance of the market.
