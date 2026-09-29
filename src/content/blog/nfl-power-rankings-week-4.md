---
title: "NFL Poll of Polls: Week 4"
description: "A new No. 1, unanimously: all eight outlets put Buffalo top after Seattle's first loss. Las Vegas climbs eight, Houston falls eight."
pubDate: 2026-09-29
lang: en
tags: ["data-viz", "nfl", "statistics"]
---

Week 3 produced the season's strangest Sunday yet. Atlanta went to Green Bay and won by three touchdowns, Chicago beat Philadelphia 27–7, New England lost by 29 in Jacksonville, and Washington knocked off the previously unbeaten Seahawks 33–31. The panel has responded.

For the first time this season there is a new No. 1, and it is unanimous: **all eight outlets rate Buffalo first**. Cincinnati fell seven places, Las Vegas climbed eight, and the Rams dropped six.

This is the same poll of polls as previous weeks — the week's rankings standardised and pooled, with every team's move charted.

<nav class="toc" aria-label="Contents">
  <details>
    <summary>
      <span class="toc-kicker">Contents</span>
      <span class="toc-count">5 sections</span>
    </summary>
    <ol>
      <li><a href="#consensus"><span class="toc-n">01</span><span class="toc-t">The consensus</span><span class="toc-d">All 32 teams, filterable by conference</span></a></li>
      <li><a href="#movers"><span class="toc-n">02</span><span class="toc-t">Who went up and down</span><span class="toc-d">Every week-over-week move</span></a></li>
      <li><a href="#h2h"><span class="toc-n">03</span><span class="toc-t">This week's matchups, priced</span><span class="toc-d">All 16 games, plus any matchup you build</span></a></li>
      <li><a href="#panel"><span class="toc-n">04</span><span class="toc-t">The panel</span><span class="toc-d">Nine outlets and how they agree</span></a></li>
      <li><a href="#sources"><span class="toc-n">05</span><span class="toc-t">Sources and method</span><span class="toc-d">Where every number comes from</span></a></li>
    </ol>
  </details>
</nav>

<style>
  .toc {
    margin: 32px 0;
    border: 1px solid #e0dcd4; border-radius: 2px;
    background: #fbfaf7; padding: 0 22px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  .toc a { text-decoration: none; color: #0a0a0a; }
  .toc summary {
    display: flex; align-items: baseline; gap: 10px;
    padding: 14px 0; cursor: pointer; list-style: none; min-height: 44px;
  }
  .toc summary::-webkit-details-marker { display: none; }
  .toc summary:hover .toc-kicker { color: #c2472f; }
  .toc summary::after {
    content: "+"; font-size: 15px; line-height: 1; color: #6b6b6b;
    margin-left: 10px; transition: color 140ms ease-out;
  }
  .toc details[open] summary::after { content: "\2212"; }
  .toc details[open] summary { border-bottom: 1px solid #e0dcd4; }
  .toc-kicker {
    font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase;
    color: #0a0a0a; font-weight: 600; transition: color 140ms ease-out;
  }
  .toc-count { font-size: 11px; color: #6b6b6b; margin-left: auto; }
  .toc ol { list-style: none; margin: 4px 0 0; padding: 0 0 14px; }
  .toc li { margin: 0; border-bottom: 1px solid #ece8e0; }
  .toc li:last-child { border-bottom: 0; }
  .toc li a { display: grid; grid-template-columns: 32px 1fr; gap: 0 10px; padding: 10px 0; }
  .toc li a:hover { color: #c2472f; }
  .toc li a:hover .toc-t { text-decoration: underline; text-underline-offset: 3px; }
  .toc-n {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px; color: #6b6b6b; padding-top: 3px;
  }
  .toc-t { font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
  .toc-d { grid-column: 2; font-size: 12.5px; color: #6b6b6b; margin-top: 2px; }
  @media (max-width: 560px) { .toc { padding: 0 16px; } .toc-t { font-size: 14px; } }
</style>

Here is where the panel landed after Week 3.

<a id="consensus"></a>

<div id="pop-root" class="pop-root">
  <div class="pop-header">
    <div class="pop-kicker">2026 season · Week 4 · poll of polls</div>
    <h2 class="pop-headline">One consensus.</h2>
    <p class="pop-lede">Each row is a team. The score is measured in rank standard deviations, so a value of +1.5 is roughly one and a half rank-spreads above the median team. The strip shows where each outlet in the panel placed that team, from first on the left to 32nd on the right. Click a row to see its individual ballots.</p>
  </div>

  <div class="pop-podium">
    <div class="pop-podium-row">
      <div class="pop-podium-team">
        <span class="pop-podium-rank">1</span>
        <span class="pop-mark pop-mark--lg" id="pop-p1-logo"></span>
        <span class="pop-podium-name" id="pop-p1-name"></span>
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
        <span class="pop-podium-name" id="pop-p2-name"></span>
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
    <div class="pop-readout" id="pop-readout">Select any row to see that team's ballots.</div>
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
          <th class="pop-th-spread">Spread across the panel</th>
          <th class="pop-th-num" title="League-wide rank from the panel">Panel</th>
          <th class="pop-th-num pop-playoff-only">Field</th>
          <th class="pop-th-num">P(No. 1)</th>        </tr>
      </thead>
      <tbody id="pop-body"></tbody>
    </table>
  </div>
  <div class="pop-legend">
    <span class="pop-legend-item"><span class="pop-swatch pop-swatch-band"></span> interquartile spread of the panel</span>
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
  .pop-playoff-only, .pop-td-field { display: none; }
  .pop-table.is-playoff .pop-playoff-only,
  .pop-table.is-playoff .pop-td-field { display: table-cell; }
  .pop-td-field { text-align: right; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10px; letter-spacing: 0.08em; }
  .pop-td-field.is-in { color: #1f6f43; font-weight: 600; }
  .pop-td-field.is-out { color: #9a958d; }
  .pop-table.is-playoff .pop-td-rank.is-seed { color: #1f6f43; }
  .pop-table.is-playoff .pop-td-rank.is-bubble { color: #9a958d; }
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
  .pop-record {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px; color: var(--ink); margin-left: 7px;
  }
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
    // Names come from the data too. Leaving them hardcoded in the markup meant
    // the podium kept showing whatever two teams topped the first edition,
    // next to the current week's logos and scores.
    document.getElementById('pop-p1-name').textContent = first.team;
    document.getElementById('pop-p2-name').textContent = second.team;
    document.getElementById('pop-p1-logo').innerHTML = logoTag(first.abbr, 'lg');
    document.getElementById('pop-p2-logo').innerHTML = logoTag(second.abbr, 'lg');
    var gap = Math.abs(first.score - second.score);
    var third = ranked[2];
    var nextGap = Math.abs(second.score - third.score);
    var ratio = gap >= 0.05 ? Math.round(nextGap / gap) : null;
    // Two different situations need different sentences: the leaders being
    // level with each other, versus the leaders being clear of the field while
    // second and third are level. The ratio decides which.
    var ratio = nextGap / gap;
    var note;
    if (ratio >= 2) {
      note = 'The top two are ' + gap.toFixed(3) + ' rank standard deviations apart, while ' +
             'second and third are ' + nextGap.toFixed(3) + ' apart — ' + Math.round(ratio) +
             '× wider. The pair are interchangeable with each other; the field behind them is not.';
    } else if (ratio <= 0.5) {
      note = 'The top two are ' + gap.toFixed(3) + ' apart, but second and third are only ' +
             nextGap.toFixed(3) + ' apart, so the ordering behind the leader carries little weight.';
    } else {
      note = 'The top two are separated by ' + gap.toFixed(3) + ' rank standard deviations, ' +
             'against ' + nextGap.toFixed(3) + ' between second and third.';
    }
    document.getElementById('pop-tie-note').textContent = note;
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
              '<span class="pop-abbr">' + t.abbr + '</span>' +
              (t.record ? '<span class="pop-record">' + t.record + '</span>' : '') + '</span>' +
              '<span class="pop-div">' + t.conference + ' ' + t.division + '</span></div>' +
            '</div></td>' +
          '<td class="pop-td-num">' + (t.score > 0 ? '+' : '') + t.score.toFixed(3) + '</td>' +
          '<td class="pop-td-num pop-ci pop-hide-sm">' + t.ciLow.toFixed(2) + ' … ' + t.ciHigh.toFixed(2) + '</td>' +
          '<td class="pop-td-num pop-hide-sm">' + t.meanRank.toFixed(2) + '</td>' +
          '<td><div class="pop-spread"><span class="pop-track"></span>' +
            '<span class="pop-band" style="left:' + scale(quartiles[0]) + '%;width:' + (scale(quartiles[1]) - scale(quartiles[0])) + '%"></span>' +
            dots + '</div></td>' +
          '<td class="pop-td-num pop-td-league pop-ci"></td>' +
          '<td class="pop-td-field"></td>' +
          '<td class="pop-td-num">' + pct(t.pTop1) + contested + '</td>' +
        '</tr>';
    }
    body.innerHTML = html;
  }

  // Which rows pass the active filter. One predicate, used both to show/hide and
  // to insert the conference/division group headings when a conference is shown.
  // Playoff field: seven per conference, which is what the NFL actually grants.
  // The previous version took the top 14 overall, which is not the same thing —
  // it produced an 8/6 split and so put the wrong team on the bubble.
  var FIELD_PER_CONFERENCE = 7;
  var BUBBLE_PER_CONFERENCE = 2;

  function conferenceRank(index, conference) {
    var seen = 0;
    for (var i = 0; i < teams.length; i++) {
      if (teams[i].conference !== conference) { continue; }
      seen++;
      if (i === index) { return seen; }
    }
    return seen;
  }

  function isAtHomeOnField(index) {
    return conferenceRank(index, teams[index].conference) <= FIELD_PER_CONFERENCE;
  }

  // NFL seeding for one conference. Rows must already be in consensus order.
  //
  //   1-4  the four division winners, ordered among themselves by consensus
  //   5-7  the best remaining teams, regardless of division
  //
  // This automatically caps a division at the four teams it could possibly
  // send, because a division winner is always seeded ahead of its rivals and
  // can therefore never occupy a wild card.
  function seedConference(rows) {
    // Sort first and never rely on the caller's order: a previous view may have
    // physically re-appended these rows, and seeding off DOM order silently
    // produced duplicated seeds on re-entry.
    rows.sort(function (a, b) { return a._leagueRank - b._leagueRank; });

    var byDivision = {};
    for (var i = 0; i < rows.length; i++) {
      var division = rows[i].getAttribute('data-div');
      // In consensus order now, so the first team seen in a division is that
      // division's highest-rated team and therefore its winner.
      if (!byDivision[division]) { byDivision[division] = rows[i]; }
    }
    var winners = Object.keys(byDivision).map(function (d) { return byDivision[d]; });
    winners.sort(function (a, b) { return a._leagueRank - b._leagueRank; });

    for (var w = 0; w < winners.length; w++) {
      winners[w]._seed = w + 1;
      winners[w]._divisionWinner = true;
      winners[w]._inField = true;
    }

    var seed = winners.length + 1;
    for (var r = 0; r < rows.length && seed <= FIELD_PER_CONFERENCE; r++) {
      if (rows[r]._inField) { continue; }   // division winners already placed
      rows[r]._seed = seed++;
      rows[r]._inField = true;
    }

    // Every row gets its conference standing (what the bubble is measured
    // against) and a flag for whether it would have been a division winner.
    for (var o = 0; o < rows.length; o++) {
      rows[o]._confStanding = o + 1;
      if (!rows[o]._inField) {
        rows[o]._seed = null;
        rows[o]._divisionWinner = false;
      }
    }
  }

  function matchesFilter(row, filter) {
    if (filter === 'all') { return true; }
    if (filter === 'AFC' || filter === 'NFC') { return row.getAttribute('data-conf') === filter; }
    if (filter === 'playoff') {
      var index = parseInt(row.getAttribute('data-index'), 10);
      return conferenceRank(index, teams[index].conference) <= FIELD_PER_CONFERENCE + BUBBLE_PER_CONFERENCE;
    }
    if (filter === 'contested') { return parseInt(row.getAttribute('data-spread'), 10) >= 10; }
    return true;
  }

  function computeRanks(rows, filter) {
    // In a conference view the table is grouped by division, and divisions have
    // no inherent order — so the displayed rank is the team's standing *within
    // the filtered set*, not its league-wide rank. The league number is kept in
    // a column that fills in only when the two differ.
    for (var i = 0; i < rows.length; i++) { if (!rows[i]._leagueRank) { rows[i]._leagueRank = i + 1; } }

    if (filter === 'playoff') {
      // Real seeding, not a flat conference cut. The NFL gives the four
      // division winners seeds 1-4 and fills 5-7 from the best remaining teams,
      // so a weak division winner is seeded ahead of better-rated wild cards —
      // a flat top seven cannot express that. See seedConference() below.
      var byConference = {};
      for (var p = 0; p < rows.length; p++) {
        var conf = rows[p].getAttribute('data-conf');
        (byConference[conf] = byConference[conf] || []).push(rows[p]);
      }
      var confOrder = Object.keys(byConference).sort();
      for (var c = 0; c < confOrder.length; c++) {
        var confRows = byConference[confOrder[c]];
        seedConference(confRows);
        // Present the field by seed, as a bracket is read, rather than in
        // consensus order — otherwise the seeds run 1, 4, 2, 5, 3 and the four
        // division winners are not adjacent.
        confRows.sort(function (a, b) {
          var seedA = a._inField ? a._seed : 99;
          var seedB = b._inField ? b._seed : 99;
          return seedA - seedB;
        });
      }
      return confOrder.map(function (name) {
        return { label: name + ' — four division winners, then three wild cards', rows: byConference[name] };
      });
    }

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
    // Reading order is taken from data-index, never from the current DOM order:
    // rows are physically re-appended when a view regroups them, so DOM order
    // drifts between switches while data-index is fixed at render time.
    // Derived state is recomputed from scratch every pass. Leaving _inField and
    // _seed set from a previous view is how a team that qualified in one pass
    // kept a seed in the next one.
    var all = body.querySelectorAll('tr[data-team]');
    for (var t = 0; t < all.length; t++) {
      all[t]._leagueRank = parseInt(all[t].getAttribute('data-index'), 10) + 1;
      all[t]._inField = false;
      all[t]._seed = null;
      all[t]._divisionWinner = false;
      all[t]._confStanding = null;
      all[t].style.display = matchesFilter(all[t], filter) ? '' : 'none';
    }
    all = Array.prototype.slice.call(all).sort(function (a, b) {
      return a._leagueRank - b._leagueRank;
    });

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
        cell.colSpan = 9;
        cell.textContent = groups[gi].label;
        head.appendChild(cell);
        body.appendChild(head);
        groupHeads.push(head);
      }
      for (var ri = 0; ri < groups[gi].rows.length; ri++) {
        body.appendChild(groups[gi].rows[ri]);  // re-appending moves the node
      }
    }

    var playoffView = filter === 'playoff';
    var table = body.closest('table');
    if (table) { table.classList.toggle('is-playoff', playoffView); }

    for (var v = 0; v < visible.length; v++) {
      var row = visible[v];
      var number = row.querySelector('.pop-td-rank');
      var panelColumn = row.querySelector('.pop-td-league');
      var fieldColumn = row.querySelector('.pop-td-field');

      if (playoffView) {
        // The rank column shows the *seed* for the seven qualifiers, and the
        // conference standing for the teams just outside.
        if (number) {
          number.textContent = row._inField ? row._seed : row._confStanding;
          number.className = 'pop-td-rank' + (row._inField ? ' is-seed' : ' is-bubble');
        }
        if (panelColumn) {
          panelColumn.textContent = (row._leagueRank === row._rank && row._inField)
            ? '' : '#' + row._leagueRank;
        }
        if (fieldColumn) {
          fieldColumn.textContent = row._divisionWinner
            ? 'DIV · IN' : (row._inField ? 'IN' : 'OUT');
          fieldColumn.className = 'pop-td-field ' + (row._inField ? 'is-in' : 'is-out');
        }
      } else {
        if (number) {
          number.textContent = row._rank;
          number.className = 'pop-td-rank';
        }
        if (panelColumn) {
          panelColumn.textContent = (row._leagueRank === row._rank) ? '' : '#' + row._leagueRank;
        }
        if (fieldColumn) {
          fieldColumn.textContent = '';
          fieldColumn.className = 'pop-td-field';
        }
      }
    }
    for (var x = 0; x < all.length; x++) {
      if (all[x].style.display === 'none') {
        var hiddenField = all[x].querySelector('.pop-td-field');
        if (hiddenField) { hiddenField.textContent = ''; }
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
      out.textContent = filterSummary || 'Select any row to see that team&rsquo;s ballots.';
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
    tr.innerHTML = '<td colspan="9"><div class="pop-ballots-inner">' +
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

Buffalo takes the top spot from Seattle, who drop to fourth after their first loss. San Francisco holds second, Kansas City climbs to third, and Minnesota is the week's quiet riser, up five to eighth.

The panel was **more** agreed this week than last, not less: mean pairwise Spearman **ρ = 0.937**, up from 0.881 in Week 3.

<a id="movers"></a>

<div id="mv-root" class="mv-root">
  <div class="mv-head">
    <div class="mv-kicker" id="mv-kicker">Week 2 → Week 3</div>
    <h3 class="mv-title" id="mv-title">Movement</h3>
    <p class="mv-summary" id="mv-summary"></p>
  </div>

  <div class="mv-chips" role="group" aria-label="Filter the movement chart">
    <button type="button" class="mv-chip is-on" data-view="all">All 32</button>
    <button type="button" class="mv-chip" data-view="big">Moves of 3+</button>
    <button type="button" class="mv-chip" data-view="up">Risers</button>
    <button type="button" class="mv-chip" data-view="down">Fallers</button>
    <button type="button" class="mv-chip" data-view="held">No change</button>
  </div>

  <div class="mv-scale" aria-hidden="true">
    <span class="mv-scale-l">← fell</span>
    <span class="mv-scale-c">no change</span>
    <span class="mv-scale-r">climbed →</span>
  </div>

  <div class="mv-list" id="mv-list"></div>
  <div class="mv-foot" id="mv-foot"></div>
</div>

<style>
  .mv-root {
    --ink: #0a0a0a; --muted: #6b6b6b; --hair: #e0dcd4; --paper: #fbfaf7;
    --wash: rgba(255, 255, 255, 0.55); --up: #1f6f43; --down: #c2472f;
    background: var(--paper); color: var(--ink);
    border: 1px solid var(--hair); border-radius: 2px;
    padding: 26px 22px 20px; margin: 32px 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    box-sizing: border-box; width: 100%;
  }
  .mv-root *, .mv-root *::before, .mv-root *::after { box-sizing: border-box; }
  /* This renders inside .prose-post, whose img/table rules would frame things. */
  .mv-root img { border: 0; margin: 0; max-width: none; display: block; }
  .mv-root table { margin-block: 0; }
  .mv-kicker { font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
  .mv-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 26px; line-height: 1.05; letter-spacing: -0.025em; margin: 0;
  }
  .mv-summary { color: #525252; font-size: 14px; line-height: 1.6; margin: 10px 0 0; max-width: 760px; }
  .mv-summary strong { color: var(--ink); }

  .mv-chips { display: flex; flex-wrap: wrap; gap: 7px; margin: 18px 0 14px; }
  .mv-chip {
    font: inherit; font-size: 12.5px; color: var(--ink); cursor: pointer;
    background: rgba(255,255,255,0.75); border: 1px solid #cfcac1;
    border-radius: 999px; padding: 5px 12px;
    transition: background 140ms ease-out, border-color 140ms ease-out, color 140ms ease-out;
  }
  .mv-chip:hover { background: #fff; border-color: #a9a29a; }
  .mv-chip.is-on { background: var(--ink); border-color: var(--ink); color: #fff; font-weight: 600; }

  .mv-scale {
    display: grid; grid-template-columns: 1fr auto 1fr;
    font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted);
    padding: 0 0 6px 0; border-bottom: 1px solid var(--ink);
  }
  .mv-scale-l { text-align: right; padding-right: 8px; }
  .mv-scale-c { padding: 0 10px; border-left: 1px dotted #b9b2a7; border-right: 1px dotted #b9b2a7; }
  .mv-scale-r { padding-left: 8px; }

  .mv-list { display: flex; flex-direction: column; }
  .mv-row {
    display: grid; grid-template-columns: 26px 1fr 130px; gap: 10px;
    align-items: center; padding: 6px 0; border-bottom: 1px solid #ece8e0;
  }
  .mv-row:last-child { border-bottom: 0; }
  .mv-row.is-held { opacity: 0.65; }
  .mv-rank {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 12px; color: var(--muted); text-align: right;
  }
  .mv-team { display: flex; align-items: center; gap: 9px; min-width: 0; }
  .mv-mark {
    width: 26px; height: 26px; border-radius: 50%; background: #fff; flex: none;
    display: inline-flex; align-items: center; justify-content: center;
    box-shadow: 0 0 0 1px rgba(110,100,90,.22), 0 0 8px 1px rgba(194,71,47,.18);
  }
  .mv-mark img { width: 72%; height: 72%; object-fit: contain; }
  .mv-names { display: flex; flex-direction: column; min-width: 0; }
  .mv-abbr { font-size: 13.5px; font-weight: 600; }
  .mv-record {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 10.5px; font-weight: 400; color: var(--ink);
  }
  .mv-name { font-size: 10.5px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .mv-was { font-size: 10.5px; color: var(--muted); }

  /* The lollipop: a zero line at the centre, bar outward, arrowhead past the tip. */
  .mv-track { position: relative; height: 22px; }
  .mv-zero {
    position: absolute; left: 50%; top: 0; bottom: 0; width: 0;
    border-left: 1px dotted #b9b2a7;
  }
  .mv-bar { position: absolute; top: 7px; height: 8px; border-radius: 2px; }
  .mv-bar.is-up { left: 50%; background: var(--up); }
  .mv-bar.is-down { right: 50%; background: var(--down); }
  .mv-arrow {
    position: absolute; top: 4px; width: 0; height: 0;
    border-top: 7px solid transparent; border-bottom: 7px solid transparent;
  }
  .mv-arrow.is-up { border-left: 8px solid var(--up); }
  .mv-arrow.is-down { border-right: 8px solid var(--down); }
  .mv-delta {
    position: absolute; top: 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px; white-space: nowrap;
  }
  .mv-delta.is-up { color: var(--up); right: 0; }
  .mv-delta.is-down { color: var(--down); left: 0; }
  .mv-delta.is-held { color: var(--muted); left: 50%; transform: translateX(-50%); }

  .mv-foot { margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--hair); font-size: 11.5px; color: var(--muted); line-height: 1.6; }
  .mv-empty { padding: 22px 0; color: var(--muted); font-size: 13px; }

  @media (max-width: 620px) {
    .mv-row { grid-template-columns: 22px 1fr 84px; }
    .mv-name { display: none; }
  }
</style>

<script>
(function () {
  var DATA = (window.__POP_DATA__ && window.__POP_DATA__.movement) || null;
  if (!DATA) { return; }

  var entries = DATA.entries.slice().sort(function (a, b) { return a.rank - b.rank; });
  var SCALE = 3.4;   // horizontal pixels per rank of movement
  var MIN_BAR = 3;   // so a one-place move is still visible

  var logoUrl = function (abbr) { return '/images/nfl/' + abbr.toLowerCase() + '.svg'; };
  var signed = function (n) { return (n > 0 ? '+' : '') + n; };

  function rowFor(e) {
    var up = e.delta > 0;
    var held = e.delta === 0;
    var width = Math.max(MIN_BAR, Math.abs(e.delta) * SCALE);
    var classes = held ? 'mv-row is-held' : 'mv-row';

    var bar = '';
    var delta = '';
    if (held) {
      delta = '<span class="mv-delta is-held">—</span>';
    } else {
      var direction = up ? 'is-up' : 'is-down';
      // Bar grows outward from the centre; the arrowhead sits just past the tip.
      var barStyle = up
        ? 'width:' + width + 'px'
        : 'width:' + width + 'px';
      var arrowStyle = up
        ? 'left:calc(50% + ' + width + 'px)'
        : 'right:calc(50% + ' + width + 'px)';
      // Labels anchor to the ends of the column rather than to each bar tip, so
      // risers and fallers each read as one clean column instead of a ragged
      // diagonal.
      var labelStyle = up ? 'right:0' : 'left:0';
      bar = '<span class="mv-bar ' + direction + '" style="' + barStyle + '"></span>' +
            '<span class="mv-arrow ' + direction + '" style="' + arrowStyle + '"></span>';
      delta = '<span class="mv-delta ' + direction + '" style="' + labelStyle + '">' +
              (up ? '▲ ' : '▼ ') + signed(e.delta) + '</span>';
    }

    return '<div class="' + classes + '">' +
      '<span class="mv-rank">' + e.rank + '</span>' +
      '<span class="mv-team">' +
        '<span class="mv-mark"><img src="' + logoUrl(e.abbr) + '" alt="" aria-hidden="true"' +
          ' loading="lazy" decoding="async" onerror="this.style.display=\'none\'"></span>' +
        '<span class="mv-names">' +
          '<span class="mv-abbr">' + e.abbr +
          (e.record ? ' <span class="mv-record">' + e.record + '</span>' : '') +
          ' <span class="mv-was">was #' + e.previousRank + '</span></span>' +
          '<span class="mv-name">' + e.team + '</span>' +
        '</span>' +
      '</span>' +
      '<span class="mv-track"><span class="mv-zero"></span>' + bar + delta + '</span>' +
    '</div>';
  }

  function visibleFor(view) {
    if (view === 'big') { return entries.filter(function (e) { return Math.abs(e.delta) >= 3; }); }
    if (view === 'up') { return entries.filter(function (e) { return e.delta > 0; }); }
    if (view === 'down') { return entries.filter(function (e) { return e.delta < 0; }); }
    if (view === 'held') { return entries.filter(function (e) { return e.delta === 0; }); }
    // "All" leads with movement, then settles into rank order for the static rows.
    return entries.slice().sort(function (a, b) {
      var moved = Math.abs(b.delta) - Math.abs(a.delta);
      return moved !== 0 ? moved : a.rank - b.rank;
    });
  }

  var chipRow = document.querySelectorAll('.mv-chip');
  function render() {
    var on = document.querySelector('.mv-chip.is-on');
    var view = on ? on.getAttribute('data-view') : 'all';
    var list = visibleFor(view);
    var host = document.getElementById('mv-list');
    host.innerHTML = list.length
      ? list.map(rowFor).join('')
      : '<div class="mv-empty">No teams in this view.</div>';
    document.getElementById('mv-foot').textContent =
      list.length + ' of ' + entries.length + ' teams shown.' +
      (view === 'all' ? ' Ordered by size of move, then by rank.' : '');
  }

  for (var i = 0; i < chipRow.length; i++) {
    chipRow[i].addEventListener('click', function (event) {
      for (var j = 0; j < chipRow.length; j++) { chipRow[j].classList.remove('is-on'); }
      event.currentTarget.classList.add('is-on');
      render();
    });
  }

  // Headline numbers, computed rather than typed, so they cannot drift.
  var riser = entries.reduce(function (a, b) { return b.delta > a.delta ? b : a; }, entries[0]);
  var faller = entries.reduce(function (a, b) { return b.delta < a.delta ? b : a; }, entries[0]);
  var moved = entries.filter(function (e) { return e.delta !== 0; }).length;
  document.getElementById('mv-kicker').textContent = 'Week ' + DATA.previousWeek + ' → this week';
  document.getElementById('mv-title').textContent =
    riser.abbr + ' up ' + riser.delta + ', ' + faller.abbr + ' down ' + Math.abs(faller.delta);
  document.getElementById('mv-summary').innerHTML =
    'Across the whole panel <strong>' + moved + ' of ' + entries.length + '</strong> teams changed ' +
    'position and ' + (entries.length - moved) + ' held still. The biggest climb is <strong>' +
    riser.team + '</strong> (' + signed(riser.delta) + ', to #' + riser.rank + ') and the biggest ' +
    'fall is <strong>' + faller.team + '</strong> (' + signed(faller.delta) + ', to #' + faller.rank + ').';

  render();
})();
</script>
<a id="h2h"></a>

## This week's matchups, priced

Every team plays in Week 4. All 16 games are priced below from the consensus alone, with a sandbox for building any matchup you like.

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
  .h2h-record {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px; font-weight: 400; color: var(--muted);
  }
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
  var records = {};
  (window.__POP_DATA__.teams || []).forEach(function (t) {
    scores[t.team] = t.score;
    names[t.abbr] = t.team;
    abbrs[t.team] = t.abbr;
    records[t.team] = t.record || '';
  });
  var recordFor = function (abbr) {
    for (var team in abbrs) { if (abbrs[team] === abbr) { return records[team]; } }
    return '';
  };

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
          '<span class="h2h-abbr">' + g.awayAbbr +
            (recordFor(g.awayAbbr) ? ' <span class="h2h-record">' + recordFor(g.awayAbbr) + '</span>' : '') +
            (homeFav ? '' : ' <span class="h2h-pick-tag">pick</span>') + '</span>' +
          '<span class="h2h-team-name">' + g.away + '</span>' +
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
          '<span class="h2h-abbr">' + g.homeAbbr +
            (recordFor(g.homeAbbr) ? ' <span class="h2h-record">' + recordFor(g.homeAbbr) + '</span>' : '') +
            (homeFav ? ' <span class="h2h-pick-tag">pick</span>' : '') + '</span>' +
          '<span class="h2h-team-name">' + g.home + '</span>' +
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
<a id="panel"></a>

## The panel

8 outlets this week. Mean distance from the consensus order, in rank positions:

| Outlet | Analyst | Mean gap | ρ vs consensus |
|--------|---------|----------|----------------|
| Bleacher Report | B/R NFL staff | 1.12 | 0.984 |
| theScore | theScore NFL desk | 1.25 | 0.983 |
| FOX Sports | Ralph Vacchiano | 1.56 | 0.968 |
| CBS Sports | Pete Prisco | 1.69 | 0.967 |
| USA Today | Nate Davis | 1.69 | 0.969 |
| Sporting News | Vinnie Iyer | 1.81 | 0.964 |
| Sports Illustrated | Conor Orr | 2.12 | 0.958 |
| Sharp Football Analysis | Raymond Summerlin | 2.12 | 0.947 |

There is no outlier this week. Every outlet sits within 2.12 positions of the consensus, and the agreement range (ρ 0.947–0.984) is the tightest of the season. Last week Sports Illustrated sat 4.2 positions out; this week Conor Orr's column is back inside the group, and it is a proper 1–32 ballot again after last week's list skipped a number and had to be dropped.

<a id="sources"></a>

## Sources and method

Every number above comes from one pipeline. Each outlet's weekly 1–32 ballot is
standardised, pooled in a measurement-error model, shrunk toward the panel mean,
and published with a range reflecting how much the outlets actually disagree.
The matchups are priced from the consensus score alone, using constants fitted
on 6,719 completed regular-season games.

The method, the calibration and the week-by-week replication checklist live with
the code rather than in every post:

- `analysis/nfl-power-rankings/SOURCES.md` — one section per outlet: URL pattern,
  cadence, markup and the specific traps. Follow this file to reproduce a week.
- `analysis/nfl-power-rankings/METHODOLOGY.md` — both derivations, and what the
  method does *not* claim.
- `analysis/nfl-power-rankings/README.md` — the pipeline and how to run it.

This week's panel — eight ballots, every one verified complete:

| Outlet | Analyst | This week's ballot |
|--------|---------|--------------------|
| CBS Sports | Pete Prisco | [cbssports.com](https://www.cbssports.com/nfl/news/2026-nfl-power-rankings-week-4-bills-vikings/) |
| FOX Sports | Ralph Vacchiano | [foxsports.com](https://www.foxsports.com/stories/nfl/2026-nfl-power-rankings-week-4) |
| Sports Illustrated | Conor Orr | [si.com](https://www.si.com/nfl/conor-orr-week-4-nfl-power-rankings-bills-take-over-top-spot) |
| USA Today | Nate Davis | [usatoday.com](https://www.usatoday.com/story/sports/nfl/columnist/nate-davis/2026/09/29/nfl-power-rankings-week-4-seahawks-bills-chiefs-49ers/91998593007/) |
| Sporting News | Vinnie Iyer | [sportingnews.com](https://www.sportingnews.com/us/nfl/news/nfl-power-rankings-week-4/7341d122c9adf1408db36e5e) |
| Sharp Football Analysis | Raymond Summerlin | [sharpfootballanalysis.com](https://www.sharpfootballanalysis.com/analysis/nfl-power-rankings/) |
| theScore | theScore NFL desk | [thescore.com](https://www.thescore.com/nfl/news/3572173/nfl-power-rankings-week-4-check-ins-for-every-team-after-1-st-month) |
| Bleacher Report | B/R NFL staff | [bleacherreport.com](https://bleacherreport.com/articles/25504118-br-experts-week-4-nfl-power-rankings) |

Two regulars are missing, and neither is a parsing failure:

- **NFL.com had not published** a Week 4 column when this ran. The templated slug
  that worked for weeks 1–3 returns 404, the article is absent from NFL.com's
  power-rankings hub, and Nick Shook's author page still lists only weeks 1–3. On
  that evidence it is late rather than gone.
- **Neil Reynolds' NFL.com UK column** also had not published. His column runs
  later in the week than the US desk's, and in Week 3 it never appeared at all.

ESPN remains absent permanently. Every URL on the site — including the homepage —
returns an empty `HTTP 202` to a plain request, so it cannot be read unattended.

The panel agreed more tightly than in any previous week: mean pairwise Spearman
**ρ = 0.933**, and all eight outlets put Buffalo first. That is what a clear
consensus looks like — worth contrasting with Week 3, when the same pipeline
found ρ = 0.881 and a genuine outlier.
