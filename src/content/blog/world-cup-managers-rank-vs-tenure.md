---
title: "World Cup Managers: Rank vs Tenure"
pubDate: 2026-05-13
lang: en
tags: ["data-viz", "football", "world-cup"]
---
Long managerial tenures are rare among the teams headed to the 2026 World Cup. Each bubble below is a qualified team: the x-axis is the FIFA ranking position (lower is better), the y-axis is how many years the current manager has been in charge, and the bubble size is the number of World Cup titles the team has won. Only eight nations have ever won the World Cup, so most bubbles are at the minimum size. Pick a team from the dropdown, or hover any bubble to inspect it.



<div id="wcm-root" class="wcm-root">
  <div class="wcm-header">
    <div class="wcm-kicker">2026 World Cup — Managers</div>
    <h2 class="wcm-headline">Long tenures are rare among World Cup managers.</h2>
    <p class="wcm-lede">Each bubble is a qualified team. The x-axis shows FIFA ranking, where lower is better. The y-axis shows how long the current manager has been in charge, in years. Bubble size encodes the number of World Cup titles the team has won — only Brazil (5), Germany (4), Argentina (3), France (2), Uruguay (2), England (1) and Spain (1) have ever lifted the trophy among the 48 qualifiers.</p>
  </div>
  <div class="wcm-controls">
    <div class="wcm-controls-left">
      <label class="wcm-pick-label" for="wcm-select">Pick a team</label>
      <select id="wcm-select" class="wcm-select">
        <option value="all">Show all teams</option>
      </select>
      <button type="button" id="wcm-reset" class="wcm-button">Reset</button>
    </div>
    <div id="wcm-readout" class="wcm-readout"></div>
  </div>
  <div class="wcm-grid">
    <div class="wcm-card wcm-card-chart">
      <div class="wcm-chart-wrap">
        <svg id="wcm-chart" viewBox="0 0 980 560" role="img" aria-label="Scatter plot of FIFA ranking versus manager tenure for 2026 World Cup teams, with bubble size encoding World Cup titles won">
        </svg>
      </div>
      <div class="wcm-legend" aria-label="Bubble size legend">
        <span class="wcm-legend-label">Bubble size = World Cup titles won:</span>
        <svg class="wcm-legend-svg" viewBox="0 0 360 60" aria-hidden="true">
          <g>
            <circle cx="20" cy="32" r="5" fill="#9a958d" fill-opacity="0.55" stroke="#fbfaf7" stroke-width="1"></circle>
            <text x="20" y="55" text-anchor="middle" class="wcm-legend-text">0</text>
            <circle cx="80" cy="32" r="12.6" fill="#9a958d" fill-opacity="0.55" stroke="#fbfaf7" stroke-width="1"></circle>
            <text x="80" y="55" text-anchor="middle" class="wcm-legend-text">1</text>
            <circle cx="150" cy="32" r="15.7" fill="#9a958d" fill-opacity="0.55" stroke="#fbfaf7" stroke-width="1"></circle>
            <text x="150" y="55" text-anchor="middle" class="wcm-legend-text">2</text>
            <circle cx="225" cy="32" r="18.2" fill="#9a958d" fill-opacity="0.55" stroke="#fbfaf7" stroke-width="1"></circle>
            <text x="225" y="55" text-anchor="middle" class="wcm-legend-text">3</text>
            <circle cx="300" cy="32" r="22" fill="#9a958d" fill-opacity="0.55" stroke="#fbfaf7" stroke-width="1"></circle>
            <text x="300" y="55" text-anchor="middle" class="wcm-legend-text">5 (Brazil)</text>
          </g>
        </svg>
      </div>
    </div>
    <div class="wcm-side">
      <div class="wcm-card wcm-card-note">
        <div class="wcm-eyebrow">Reading the chart</div>
        <p class="wcm-pullquote">France is the outlier: elite ranking, unusually long managerial continuity.</p>
        <p class="wcm-body">Most teams cluster below three years of tenure, even among strong football nations. A long-serving coach is more exception than norm.</p>
      </div>
      <div class="wcm-card wcm-card-note">
        <div class="wcm-eyebrow">Longest tenures</div>
        <div id="wcm-toplist" class="wcm-toplist"></div>
      </div>
      <div class="wcm-source">Data: FIFA ranking position from the April 1, 2026 ranking set; manager tenure rounded as of May 13, 2026; World Cup titles counted across all editions through 2022, with West Germany titles credited to Germany.</div>
    </div>
  </div>
</div>

<style>
  .wcm-root {
    background: #fbfaf7;
    color: #0a0a0a;
    padding: 24px;
    border-radius: 2px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    margin: 24px 0;
    box-sizing: border-box;
    width: 100%;
  }
  .wcm-root *, .wcm-root *::before, .wcm-root *::after { box-sizing: border-box; }
  .wcm-header { max-width: 880px; margin-bottom: 28px; }
  .wcm-kicker { font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: #737373; margin-bottom: 10px; }
  .wcm-headline {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 40px;
    line-height: 0.98;
    letter-spacing: -0.035em;
    color: #0a0a0a;
    margin: 0;
  }
  .wcm-lede { color: #525252; font-size: 15px; line-height: 1.6; margin-top: 14px; max-width: 720px; }

  .wcm-controls {
    display: flex; flex-direction: column; gap: 12px;
    margin-bottom: 18px;
  }
  .wcm-controls-left { display: flex; flex-direction: column; gap: 8px; }
  .wcm-pick-label { font-size: 13px; color: #737373; }
  .wcm-select {
    width: 100%; max-width: 320px;
    padding: 8px 10px;
    background: rgba(255,255,255,0.85);
    border: 1px solid #d4d4d4;
    border-radius: 2px;
    font-size: 14px;
    color: #0a0a0a;
  }
  .wcm-button {
    align-self: flex-start;
    padding: 7px 14px;
    background: rgba(255,255,255,0.75);
    border: 1px solid #d4d4d4;
    border-radius: 2px;
    font-size: 13px;
    color: #0a0a0a;
    cursor: pointer;
  }
  .wcm-button:hover { background: #fff; }
  .wcm-readout {
    font-size: 13px;
    color: #404040;
    min-height: 1.2em;
  }
  .wcm-readout strong { color: #0a0a0a; font-weight: 600; }

  @media (min-width: 720px) {
    .wcm-controls { flex-direction: row; align-items: center; justify-content: space-between; }
    .wcm-controls-left { flex-direction: row; align-items: center; gap: 10px; }
  }

  .wcm-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 24px; }

  .wcm-card {
    background: #fbfaf7;
    border: 1px solid #d4d4d4;
    border-radius: 2px;
    padding: 16px;
    min-width: 0;
  }
  .wcm-card-note { background: rgba(255,255,255,0.5); padding: 22px; }

  .wcm-chart-wrap { width: 100%; overflow-x: auto; min-width: 0; }
  #wcm-chart { width: 100%; height: auto; display: block; }

  .wcm-legend {
    display: flex; align-items: center; gap: 14px;
    margin-top: 10px; padding-top: 12px;
    border-top: 1px solid #e5e5e5;
    flex-wrap: wrap;
  }
  .wcm-legend-label { font-size: 12px; color: #525252; letter-spacing: 0.02em; }
  .wcm-legend-svg { width: 320px; max-width: 100%; height: auto; display: block; }
  .wcm-legend-text { fill: #525252; font-size: 11px; font-family: inherit; }

  .wcm-side {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 20px;
  }
  @media (min-width: 760px) {
    .wcm-side { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
    .wcm-source { grid-column: 1 / -1; }
  }
  .wcm-eyebrow { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: #737373; }
  .wcm-pullquote {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 22px; line-height: 1.18; letter-spacing: -0.015em;
    color: #0a0a0a; margin: 12px 0 0 0;
  }
  .wcm-body { color: #525252; font-size: 13px; line-height: 1.55; margin-top: 14px; }
  .wcm-source { font-size: 12px; color: #737373; line-height: 1.5; }

  .wcm-toplist { display: flex; flex-direction: column; gap: 10px; margin-top: 12px; }
  .wcm-toplist-row {
    display: flex; align-items: baseline; justify-content: space-between; gap: 14px;
    border-bottom: 1px solid #e5e5e5; padding-bottom: 8px;
    background: none; border-left: 0; border-right: 0; border-top: 0;
    width: 100%; text-align: left; cursor: pointer;
    font: inherit; color: inherit;
  }
  .wcm-toplist-row:hover .wcm-toplist-team { color: #7e2b1f; }
  .wcm-toplist-team { font-size: 13px; font-weight: 600; color: #0a0a0a; }
  .wcm-toplist-mgr { font-size: 12px; color: #737373; margin-top: 2px; }
  .wcm-toplist-val { font-family: Georgia, "Times New Roman", serif; font-size: 20px; color: #0a0a0a; }

  .wcm-dot { transition: r 180ms ease-out, opacity 180ms ease-out, fill 180ms ease-out; cursor: pointer; }
  .wcm-axis-line { stroke: #171717; }
  .wcm-grid-y { stroke: #ded9cf; }
  .wcm-grid-x { stroke: #eee8dd; }
  .wcm-tick-text, .wcm-edge-text { fill: #737373; font-size: 12px; }
  .wcm-axis-title { fill: #0a0a0a; font-size: 13px; }
  .wcm-label { fill: #0a0a0a; font-size: 12px; pointer-events: none; }
  .wcm-ref-line { stroke: #9d948a; stroke-dasharray: 4 5; opacity: 0.45; }

  @keyframes wcmFadeIn { from { opacity: 0; transform: translateY(4px);} to { opacity: 1; transform: translateY(0);} }
  .wcm-readout.is-on { animation: wcmFadeIn 240ms ease-out; }
</style>

<script>
(function(){
  var data = [
    { team: "Algeria", rank: 28, manager: "Vladimir Petković", tenure: 2.2, titles: 0 },
    { team: "Argentina", rank: 3, manager: "Lionel Scaloni", tenure: 7.5, titles: 3 },
    { team: "Australia", rank: 27, manager: "Tony Popović", tenure: 1.7, titles: 0 },
    { team: "Austria", rank: 24, manager: "Ralf Rangnick", tenure: 4.0, titles: 0 },
    { team: "Belgium", rank: 9, manager: "Rudi Garcia", tenure: 1.3, titles: 0 },
    { team: "Bosnia and Herzegovina", rank: 65, manager: "Sergej Barbarez", tenure: 2.1, titles: 0 },
    { team: "Brazil", rank: 6, manager: "Carlo Ancelotti", tenure: 1.0, titles: 5 },
    { team: "Canada", rank: 30, manager: "Jesse Marsch", tenure: 2.0, titles: 0 },
    { team: "Cabo Verde / Cape Verde", rank: 69, manager: "Bubista", tenure: 6.3, titles: 0 },
    { team: "Colombia", rank: 13, manager: "Néstor Lorenzo", tenure: 3.8, titles: 0 },
    { team: "Croatia", rank: 11, manager: "Zlatko Dalić", tenure: 8.6, titles: 0 },
    { team: "Curaçao", rank: 82, manager: "Dick Advocaat", tenure: 0.0, titles: 0 },
    { team: "Czechia", rank: 41, manager: "Miroslav Koubek", tenure: 0.4, titles: 0 },
    { team: "DR Congo", rank: 46, manager: "Sébastien Desabre", tenure: 3.7, titles: 0 },
    { team: "Ecuador", rank: 23, manager: "Sebastián Beccacece", tenure: 1.7, titles: 0 },
    { team: "Egypt", rank: 29, manager: "Hossam Hassan", tenure: 2.2, titles: 0 },
    { team: "England", rank: 4, manager: "Thomas Tuchel", tenure: 1.3, titles: 1 },
    { team: "France", rank: 1, manager: "Didier Deschamps", tenure: 13.8, titles: 2 },
    { team: "Germany", rank: 10, manager: "Julian Nagelsmann", tenure: 2.7, titles: 4 },
    { team: "Ghana", rank: 74, manager: "Carlos Queiroz", tenure: 0.1, titles: 0 },
    { team: "Haiti", rank: 83, manager: "Sébastien Migné", tenure: 1.9, titles: 0 },
    { team: "Iran", rank: 21, manager: "Amir Ghalenoei", tenure: 3.2, titles: 0 },
    { team: "Iraq", rank: 57, manager: "Graham Arnold", tenure: 1.0, titles: 0 },
    { team: "Côte d’Ivoire / Ivory Coast", rank: 34, manager: "Emerse Faé", tenure: 2.3, titles: 0 },
    { team: "Japan", rank: 18, manager: "Hajime Moriyasu", tenure: 7.8, titles: 0 },
    { team: "Jordan", rank: 63, manager: "Jamal Sellami", tenure: 1.7, titles: 0 },
    { team: "Korea Republic / South Korea", rank: 25, manager: "Hong Myung-bo", tenure: 1.8, titles: 0 },
    { team: "Mexico", rank: 15, manager: "Javier Aguirre", tenure: 1.8, titles: 0 },
    { team: "Morocco", rank: 8, manager: "Mohamed Ouahbi", tenure: 0.2, titles: 0 },
    { team: "Netherlands", rank: 7, manager: "Ronald Koeman", tenure: 3.3, titles: 0 },
    { team: "New Zealand", rank: 85, manager: "Darren Bazeley", tenure: 3.5, titles: 0 },
    { team: "Norway", rank: 31, manager: "Ståle Solbakken", tenure: 5.4, titles: 0 },
    { team: "Panama", rank: 33, manager: "Thomas Christiansen", tenure: 5.8, titles: 0 },
    { team: "Paraguay", rank: 40, manager: "Gustavo Alfaro", tenure: 1.7, titles: 0 },
    { team: "Portugal", rank: 5, manager: "Roberto Martínez", tenure: 3.3, titles: 0 },
    { team: "Qatar", rank: 55, manager: "Julen Lopetegui", tenure: 1.0, titles: 0 },
    { team: "Saudi Arabia", rank: 61, manager: "Hervé Renard", tenure: 1.6, titles: 0 },
    { team: "Scotland", rank: 43, manager: "Steve Clarke", tenure: 7.0, titles: 0 },
    { team: "Senegal", rank: 14, manager: "Pape Thiaw", tenure: 1.4, titles: 0 },
    { team: "South Africa", rank: 60, manager: "Hugo Broos", tenure: 5.0, titles: 0 },
    { team: "Spain", rank: 2, manager: "Luis de la Fuente", tenure: 3.4, titles: 1 },
    { team: "Sweden", rank: 38, manager: "Graham Potter", tenure: 0.6, titles: 0 },
    { team: "Switzerland", rank: 19, manager: "Murat Yakin", tenure: 4.7, titles: 0 },
    { team: "Tunisia", rank: 44, manager: "Sabri Lamouchi", tenure: 0.3, titles: 0 },
    { team: "Türkiye / Turkey", rank: 22, manager: "Vincenzo Montella", tenure: 2.7, titles: 0 },
    { team: "Uruguay", rank: 17, manager: "Marcelo Bielsa", tenure: 3.0, titles: 2 },
    { team: "United States", rank: 16, manager: "Mauricio Pochettino", tenure: 1.7, titles: 0 },
    { team: "Uzbekistan", rank: 50, manager: "Fabio Cannavaro", tenure: 0.6, titles: 0 }
  ];

  var keyLabels = {
    "France":1,"Spain":1,"Argentina":1,"England":1,"Portugal":1,
    "Croatia":1,"Japan":1,"Mexico":1,"United States":1,
    "Cabo Verde / Cape Verde":1,"Scotland":1,"Panama":1
  };

  var W = 980, H = 560;
  var M = { top: 36, right: 44, bottom: 66, left: 78 };
  var PW = W - M.left - M.right;
  var PH = H - M.top - M.bottom;
  var rankMin = 1, rankMax = 85;
  var tenMin = 0, tenMax = 14;
  function xS(r){ return M.left + ((r - rankMin) / (rankMax - rankMin)) * PW; }
  function yS(t){ return M.top + PH - ((t - tenMin) / (tenMax - tenMin)) * PH; }

  var titlesMin = 0, titlesMax = 5, rMin = 5, rMax = 22;
  function rS(t){
    if (t <= titlesMin) return rMin;
    if (t >= titlesMax) return rMax;
    return rMin + (rMax - rMin) * Math.sqrt(t / titlesMax);
  }

  var svgNS = "http://www.w3.org/2000/svg";
  function el(tag, attrs){
    var n = document.createElementNS(svgNS, tag);
    if (attrs) for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  function text(x, y, str, cls, anchor){
    var t = el("text", { x:x, y:y, "class": cls || "" });
    if (anchor) t.setAttribute("text-anchor", anchor);
    t.textContent = str;
    return t;
  }

  var svg = document.getElementById("wcm-chart");
  var select = document.getElementById("wcm-select");
  var reset = document.getElementById("wcm-reset");
  var readout = document.getElementById("wcm-readout");
  var toplist = document.getElementById("wcm-toplist");

  // populate dropdown
  var sorted = data.slice().sort(function(a,b){ return a.team.localeCompare(b.team); });
  for (var i = 0; i < sorted.length; i++){
    var o = document.createElement("option");
    o.value = sorted[i].team;
    o.textContent = sorted[i].team;
    select.appendChild(o);
  }

  // background
  svg.appendChild(el("rect", { x:0, y:0, width:W, height:H, fill:"#fbfaf7" }));

  // y gridlines + ticks
  var yTicks = [0,2,4,6,8,10,12,14];
  for (var i = 0; i < yTicks.length; i++){
    var t = yTicks[i];
    svg.appendChild(el("line", { x1:M.left, x2:W-M.right, y1:yS(t), y2:yS(t), "class":"wcm-grid-y" }));
    svg.appendChild(text(M.left-14, yS(t)+4, t, "wcm-tick-text", "end"));
  }
  // x gridlines + ticks
  var xTicks = [1,10,20,30,40,50,60,70,80,85];
  for (var i = 0; i < xTicks.length; i++){
    var t = xTicks[i];
    svg.appendChild(el("line", { x1:xS(t), x2:xS(t), y1:M.top, y2:H-M.bottom, "class":"wcm-grid-x" }));
    svg.appendChild(text(xS(t), H-M.bottom+28, t, "wcm-tick-text", "middle"));
  }

  // 3-year reference line
  svg.appendChild(el("line", { x1:M.left, x2:W-M.right, y1:yS(3), y2:yS(3), "class":"wcm-ref-line" }));
  svg.appendChild(text(W-M.right-6, yS(3)-8, "3-year tenure line", "wcm-tick-text", "end"));

  // axes
  svg.appendChild(el("line", { x1:M.left, x2:W-M.right, y1:H-M.bottom, y2:H-M.bottom, "class":"wcm-axis-line" }));
  svg.appendChild(el("line", { x1:M.left, x2:M.left, y1:M.top, y2:H-M.bottom, "class":"wcm-axis-line" }));

  // axis titles
  svg.appendChild(text(W/2, H-18, "FIFA ranking position — lower is better", "wcm-axis-title", "middle"));
  var yTitle = text(0, 0, "Manager tenure, years", "wcm-axis-title", "middle");
  yTitle.setAttribute("transform", "translate(20 " + (H/2) + ") rotate(-90)");
  svg.appendChild(yTitle);

  // edge labels
  svg.appendChild(text(M.left+6, M.top-14, "Better-ranked teams", "wcm-edge-text"));
  var er = text(W-M.right-6, M.top-14, "Lower-ranked teams", "wcm-edge-text", "end");
  svg.appendChild(er);

  // dots + labels
  var selected = "all";
  var hovered = null;
  var dotMap = {};
  var labelMap = {};

  function shortName(name){
    if (name.length > 18 && name.indexOf(" /") !== -1) return name.split(" /")[0];
    return name;
  }

  // sort bigger bubbles first so smaller ones paint on top and stay clickable
  var paintOrder = data.slice().sort(function(a,b){ return b.titles - a.titles; });
  for (var i = 0; i < paintOrder.length; i++){
    (function(d){
      var baseR = rS(d.titles);
      var c = el("circle", {
        cx: xS(d.rank), cy: yS(d.tenure), r: baseR,
        fill: "#9a958d", "fill-opacity": 0.28,
        stroke: "#fbfaf7", "stroke-width": 1,
        "class": "wcm-dot"
      });
      c.addEventListener("mouseenter", function(){ hovered = d.team; render(); });
      c.addEventListener("mouseleave", function(){ hovered = null; render(); });
      c.addEventListener("click", function(){ selected = d.team; select.value = d.team; render(); });
      svg.appendChild(c);
      dotMap[d.team] = c;

      var lbl = text(xS(d.rank), yS(d.tenure) - baseR - 6, shortName(d.team), "wcm-label", "middle");
      lbl.style.display = "none";
      svg.appendChild(lbl);
      labelMap[d.team] = lbl;
    })(paintOrder[i]);
  }

  function render(){
    var activeTeam = hovered || (selected !== "all" ? selected : null);

    for (var i = 0; i < data.length; i++){
      var d = data[i];
      var isSel = selected === d.team;
      var isHov = hovered === d.team;
      var focus = selected === "all" || isSel || isHov;
      var showLabel = isSel || isHov || (selected === "all" && keyLabels[d.team]);
      var baseR = rS(d.titles);
      var r = (isSel || isHov) ? baseR + 3 : baseR;

      var dot = dotMap[d.team];
      dot.setAttribute("r", r);
      dot.setAttribute("fill", focus ? "#c2472f" : "#9a958d");
      dot.setAttribute("fill-opacity", focus ? 0.88 : 0.28);
      dot.setAttribute("stroke", (isSel || isHov) ? "#7e2b1f" : "#fbfaf7");
      dot.setAttribute("stroke-width", (isSel || isHov) ? 2 : 1);

      var lbl = labelMap[d.team];
      lbl.style.display = showLabel ? "" : "none";
      lbl.setAttribute("y", yS(d.tenure) - r - 6);
    }

    if (activeTeam){
      var d = null;
      for (var i = 0; i < data.length; i++) if (data[i].team === activeTeam) { d = data[i]; break; }
      if (d){
        var wcLabel = d.titles === 0 ? "no World Cup titles" : (d.titles === 1 ? "1 World Cup title" : (d.titles + " World Cup titles"));
        readout.innerHTML = "<strong>" + d.team + "</strong> · rank #" + d.rank + " · " + d.tenure.toFixed(1) + " yrs · " + wcLabel + " · " + d.manager;
        readout.classList.remove("is-on");
        // force reflow to restart animation
        void readout.offsetWidth;
        readout.classList.add("is-on");
      }
    } else {
      readout.textContent = "";
      readout.classList.remove("is-on");
    }
  }

  select.addEventListener("change", function(){ selected = select.value; render(); });
  reset.addEventListener("click", function(){ selected = "all"; hovered = null; select.value = "all"; render(); });

  // top tenure list
  var top = data.slice().sort(function(a,b){ return b.tenure - a.tenure; }).slice(0,5);
  for (var i = 0; i < top.length; i++){
    (function(d, rank){
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "wcm-toplist-row";
      btn.innerHTML =
        '<div>' +
          '<div class="wcm-toplist-team">' + (rank+1) + '. ' + d.team + '</div>' +
          '<div class="wcm-toplist-mgr">' + d.manager + '</div>' +
        '</div>' +
        '<div class="wcm-toplist-val">' + d.tenure.toFixed(1) + '</div>';
      btn.addEventListener("click", function(){ selected = d.team; select.value = d.team; render(); });
      toplist.appendChild(btn);
    })(top[i], i);
  }

  render();
})();
</script>
