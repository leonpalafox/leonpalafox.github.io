// Interactive parts of /teaching/vibe-coding/. Every page is server-rendered in
// its default state from the same data module, so this only has to react to input.
import {
  BANS,
  CHECKLIST,
  COLUMN_PITFALLS,
  DEFAULT_SPEC,
  ENGINES,
  GRID_PARAMS,
  PIPELINE_STEPS,
  RULES,
  STYLE_LINES,
  TASKS,
  buildContract,
  buildCorrection,
  buildModelSetup,
  buildSetupPrompt,
  countCombinations,
  flattenTree,
  highlightPrompt,
  type Breach,
  type EngineId,
  type SpecState,
  type TaskId,
} from '../data/vibe-coding';

const one = <T extends Element = HTMLElement>(root: ParentNode, selector: string) => root.querySelector<T>(selector);
const all = <T extends Element = HTMLElement>(root: ParentNode, selector: string) => [
  ...root.querySelectorAll<T>(selector),
];
const setText = (root: ParentNode, selector: string, text: string) => {
  const el = one(root, selector);
  if (el) el.textContent = text;
};
const setPrompt = (name: string, text: string) => {
  const el = one(document, `[data-vc-text="${name}"]`);
  if (el) el.innerHTML = highlightPrompt(text);
};
const escapeHtml = (text: string) => text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const pct = (value: number, digits = 1) => `${(value * 100).toFixed(digits)}%`;
const SVG_NS = 'http://www.w3.org/2000/svg';

/* ---------- Copy buttons ---------- */

async function copyText(text: string, source: Element | null): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Clipboard API unavailable (older browser, insecure context): select the
    // text so a manual copy is one keystroke away.
    if (source) {
      const range = document.createRange();
      range.selectNodeContents(source);
      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
    }
    return false;
  }
}

function mountCopy(): void {
  for (const button of all<HTMLButtonElement>(document, '[data-vc-copy]')) {
    const source = one(button.closest('.vc-prompt') ?? document, 'pre');
    const label = button.textContent?.trim() || 'Copy';
    let timer = 0;
    button.hidden = false;
    button.addEventListener('click', async () => {
      const ok = await copyText(source?.textContent ?? '', source);
      button.textContent = ok ? 'Copied' : 'Selected: press ⌘/Ctrl+C';
      button.dataset.done = 'true';
      window.clearTimeout(timer);
      timer = window.setTimeout(() => {
        button.textContent = label;
        delete button.dataset.done;
      }, 2200);
    });
  }
}

/** Buttons that behave as a single-choice group via aria-pressed. */
function choose(buttons: HTMLElement[], active: HTMLElement): void {
  for (const button of buttons) button.setAttribute('aria-pressed', String(button === active));
}

/* ---------- Rule 1: environment ---------- */

function mountEngines(root: HTMLElement): void {
  const buttons = all(root, '[data-engine]');
  for (const button of buttons) {
    button.addEventListener('click', () => {
      const engine = ENGINES.find((e) => e.id === (button.dataset.engine as EngineId));
      if (!engine) return;
      choose(buttons, button);
      setText(root, '[data-engine-what]', engine.what);
      for (const [key, value] of Object.entries(engine.facts)) setText(root, `[data-fact="${key}"]`, value);
      setPrompt('rule-1', engine.block);
    });
  }
}

/* ---------- Rule 2: data contract ---------- */

function mountContract(root: HTMLElement): void {
  const chips = all(root, '[data-pitfall]');
  const selected = () => chips.filter((c) => c.getAttribute('aria-pressed') === 'true').map((c) => c.dataset.pitfall!);
  for (const chip of chips) {
    chip.addEventListener('click', () => {
      const on = chip.getAttribute('aria-pressed') !== 'true';
      chip.setAttribute('aria-pressed', String(on));
      const pitfall = COLUMN_PITFALLS.find((p) => p.id === chip.dataset.pitfall);
      if (pitfall) {
        setText(root, '[data-pitfall-label]', pitfall.label);
        setText(root, '[data-pitfall-guess]', pitfall.guess);
      }
      setPrompt('rule-2', buildContract(selected()));
    });
  }
}

/* ---------- Rule 3: search space ---------- */

function mountGrid(root: HTMLElement): void {
  const chips = all(root, '[data-param]');
  const foldButtons = all(root, '[data-folds]');
  let folds = Number(foldButtons.find((b) => b.getAttribute('aria-pressed') === 'true')?.dataset.folds ?? 5);

  const chosen = () => {
    const out: Record<string, string[]> = {};
    for (const param of GRID_PARAMS) {
      out[param.name] = chips
        .filter((c) => c.dataset.param === param.name && c.getAttribute('aria-pressed') === 'true')
        .map((c) => c.dataset.value!);
    }
    return out;
  };

  const update = () => {
    const state = chosen();
    const combos = countCombinations(state);
    const sizes = GRID_PARAMS.map((p) => state[p.name].length);
    setText(root, '[data-grid-math]', `${sizes.join(' × ')} = ${combos.toLocaleString('en-US')} combinations`);
    setText(root, '[data-grid-fits]', (combos * folds).toLocaleString('en-US'));
    setText(root, '[data-grid-folds]', String(folds));
    setPrompt('rule-3', buildModelSetup(state));
  };

  for (const chip of chips) {
    chip.addEventListener('click', () => {
      const on = chip.getAttribute('aria-pressed') === 'true';
      const siblings = chips.filter((c) => c.dataset.param === chip.dataset.param);
      // A parameter needs at least one value, so the last one stays on.
      if (on && siblings.filter((c) => c.getAttribute('aria-pressed') === 'true').length === 1) return;
      chip.setAttribute('aria-pressed', String(!on));
      update();
    });
  }
  for (const button of foldButtons) {
    button.addEventListener('click', () => {
      folds = Number(button.dataset.folds);
      choose(foldButtons, button);
      update();
    });
  }
}

/* ---------- Rule 4: where each step learns from ---------- */

const FLOW_VERDICT = {
  vague: 'The test rows took part in four decisions and then graded the result.',
  rule: 'Every decision stays inside train. The test rows are read once, to report.',
};

function mountFlow(root: HTMLElement): void {
  const buttons = all(root, '[data-mode]');
  const rows = all(root, '[data-flow-row]');
  const render = (mode: 'vague' | 'rule') => {
    rows.forEach((row, index) => {
      const step = PIPELINE_STEPS[index][mode];
      const train = one(row, '[data-seg="train"]');
      const test = one(row, '[data-seg="test"]');
      const usesTrain = step.rows === 'all' || step.rows === 'train';
      train?.setAttribute('data-on', String(usesTrain));
      const testState = step.rows === 'test-once' ? 'once' : step.rows === 'train' ? 'false' : 'leak';
      test?.setAttribute('data-on', testState);
      if (train) train.textContent = usesTrain ? 'used' : '';
      if (test) test.textContent = testState === 'once' ? 'once' : testState === 'leak' ? 'used' : '';
      setText(row, '[data-flow-note]', step.note);
    });
    setText(root, '[data-flow-verdict]', FLOW_VERDICT[mode]);
  };
  for (const button of buttons) {
    button.addEventListener('click', () => {
      choose(buttons, button);
      render(button.dataset.mode === 'rule' ? 'rule' : 'vague');
    });
  }
}

/* ---------- Rule 5: choosing by test score ---------- */

function mulberry32(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let value = Math.imul(state ^ (state >>> 15), 1 | state);
    value = (value + Math.imul(value ^ (value >>> 7), 61 | value)) ^ value;
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function popcount(bits: number): number {
  let v = bits - ((bits >>> 1) & 0x55555555);
  v = (v & 0x33333333) + ((v >>> 2) & 0x33333333);
  return (((v + (v >>> 4)) & 0x0f0f0f0f) * 0x01010101) >>> 24;
}

/** Correct answers out of n for a model that guesses: an exact Binomial(n, 0.5) draw. */
function coinFlipHits(n: number): number {
  let hits = 0;
  for (let left = n; left > 0; left -= 32) {
    let bits = (Math.random() * 4294967296) >>> 0;
    if (left < 32) bits &= (1 << left) - 1;
    hits += popcount(bits);
  }
  return hits;
}

/** Mean of the largest of k standard normal draws, by simulation (fixed seed, cached per k). */
const expectedMaxZ = new Map<number, number>();
function meanMaxZ(k: number): number {
  if (k <= 1) return 0;
  const cached = expectedMaxZ.get(k);
  if (cached !== undefined) return cached;
  const random = mulberry32(k * 7919 + 17);
  const runs = 1500;
  let total = 0;
  for (let run = 0; run < runs; run++) {
    let best = -Infinity;
    for (let i = 0; i < k; i++) {
      const z = Math.sqrt(-2 * Math.log(1 - random())) * Math.cos(2 * Math.PI * random());
      if (z > best) best = z;
    }
    total += best;
  }
  const mean = total / runs;
  expectedMaxZ.set(k, mean);
  return mean;
}

function mountSelection(root: HTMLElement): void {
  const kInput = one<HTMLInputElement>(root, '[data-sel-k]')!;
  const nInput = one<HTMLInputElement>(root, '[data-sel-n]')!;
  const host = one(root, '[data-sel-strip]')!;
  const LO = 0.4;
  const HI = 0.6;
  let scores: number[] = [];

  const draw = () => {
    const width = Math.max(260, Math.round(host.clientWidth));
    const height = 128;
    const padX = 16;
    const axisY = 98;
    const x = (v: number) => padX + ((Math.min(HI, Math.max(LO, v)) - LO) / (HI - LO)) * (width - padX * 2);
    const best = scores.indexOf(Math.max(...scores));
    const svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('class', 'vc-strip');
    svg.setAttribute('role', 'img');
    svg.setAttribute(
      'aria-label',
      `Test accuracy of ${scores.length} configurations that all guess at random. The best one scores ${pct(scores[best])}; the true accuracy of every one is 50%.`,
    );
    const add = (tag: string, attrs: Record<string, string | number>, text?: string) => {
      const el = document.createElementNS(SVG_NS, tag);
      for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
      if (text !== undefined) el.textContent = text;
      svg.appendChild(el);
      return el;
    };

    add('line', { x1: padX, x2: width - padX, y1: axisY, y2: axisY, stroke: '#cfc9bc', 'stroke-width': 1 });
    for (const tick of [0.4, 0.45, 0.5, 0.55, 0.6]) {
      add('line', { x1: x(tick), x2: x(tick), y1: axisY, y2: axisY + 4, stroke: '#cfc9bc', 'stroke-width': 1 });
      add('text', { x: x(tick), y: axisY + 18, 'text-anchor': 'middle' }, `${Math.round(tick * 100)}%`);
    }
    add('line', { x1: x(0.5), x2: x(0.5), y1: 26, y2: axisY, stroke: '#141412', 'stroke-width': 1 });

    const y = (index: number) => {
      const jitter = Math.abs(Math.sin((index + 1) * 12.9898) * 43758.5453) % 1;
      return 38 + jitter * (axisY - 12 - 38);
    };
    scores.forEach((score, index) => {
      if (index === best) return;
      const dot = add('circle', {
        cx: x(score),
        cy: y(index),
        r: 4,
        fill: '#8c877c',
        'fill-opacity': 0.6,
        stroke: '#efede7',
        'stroke-width': 1.5,
      });
      const title = document.createElementNS(SVG_NS, 'title');
      title.textContent = `Configuration ${index + 1}: ${pct(score)} on test`;
      dot.appendChild(title);
    });
    const bx = x(scores[best]);
    const by = y(best);
    const bestDot = add('circle', { cx: bx, cy: by, r: 5.5, fill: '#e2371b', stroke: '#efede7', 'stroke-width': 2 });
    const bestTitle = document.createElementNS(SVG_NS, 'title');
    bestTitle.textContent = `Best configuration: ${pct(scores[best])} on test`;
    bestDot.appendChild(bestTitle);
    const nearRight = bx > width - 70;
    add(
      'text',
      {
        x: bx + (nearRight ? 4 : -4),
        y: 18,
        'text-anchor': nearRight ? 'end' : 'start',
        class: 'vc-strip__value',
      },
      pct(scores[best]),
    );
    add('line', { x1: bx, x2: bx, y1: 23, y2: by - 7, stroke: '#e2371b', 'stroke-width': 1 });
    host.replaceChildren(svg);
  };

  const run = () => {
    const k = Number(kInput.value);
    const n = Number(nInput.value);
    scores = Array.from({ length: k }, () => coinFlipHits(n) / n);
    const best = Math.max(...scores);
    const typical = 0.5 + (0.5 / Math.sqrt(n)) * meanMaxZ(k);
    setText(root, '[data-sel-k-val]', String(k));
    setText(root, '[data-sel-n-val]', n.toLocaleString('en-US'));
    setText(root, '[data-sel-best]', pct(best));
    setText(root, '[data-sel-typical]', pct(typical));
    setText(
      root,
      '[data-sel-line]',
      k === 1
        ? 'One configuration, scored once. Nothing was chosen, so the score is an honest estimate.'
        : `Pick the best of ${k} by test score and a model with no skill typically reports ${pct(typical)}.`,
    );
    draw();
  };

  kInput.addEventListener('input', run);
  nInput.addEventListener('input', run);
  one(root, '[data-sel-redraw]')?.addEventListener('click', run);
  if ('ResizeObserver' in window) {
    let width = 0;
    new ResizeObserver(() => {
      const next = Math.round(host.clientWidth);
      if (next !== width && scores.length) {
        width = next;
        draw();
      }
    }).observe(host);
  }
  run();
}

/* ---------- Rule 6: the do-nothing model ---------- */

function mountBaseline(root: HTMLElement): void {
  const input = one<HTMLInputElement>(root, '[data-base-share]')!;
  const update = () => {
    const positives = Number(input.value) * 10; // per 1,000 rows
    const negatives = 1000 - positives;
    const accuracy = negatives / 1000;
    setText(root, '[data-base-share-val]', `${input.value}%`);
    setText(root, '[data-base-acc]', pct(accuracy, 0));
    setText(root, '[data-base-caught]', `0 of ${positives}`);
    setText(root, '[data-cell="tn"]', negatives.toLocaleString('en-US'));
    setText(root, '[data-cell="fn"]', positives.toLocaleString('en-US'));
    setText(
      root,
      '[data-base-line]',
      positives === 500
        ? 'With balanced classes the do-nothing model scores 50%, and accuracy starts to mean something.'
        : `On this data, any model below ${pct(accuracy, 0)} accuracy is worse than doing nothing, and one at ${pct(accuracy, 0)} may have caught no positives at all.`,
    );
  };
  input.addEventListener('input', update);
  update();
}

/* ---------- Rule 8: correction prompt ---------- */

function mountCorrection(root: HTMLElement): void {
  const select = one<HTMLSelectElement>(root, '[data-fix-rule]')!;
  const input = one<HTMLInputElement>(root, '[data-fix-what]')!;
  const update = () => setPrompt('correction', buildCorrection([{ rule: Number(select.value), what: input.value }]));
  select.addEventListener('change', () => {
    input.value = RULES[Number(select.value) - 1]?.breach ?? '';
    update();
  });
  input.addEventListener('input', update);
}

/* ---------- Prompt builder ---------- */

const STORE_KEY = 'vc-spec-v1';

function readSpec(form: HTMLFormElement): SpecState {
  const data = new FormData(form);
  const get = (key: string) => String(data.get(key) ?? '');
  return {
    goal: get('goal'),
    task: (get('task') || DEFAULT_SPEC.task) as TaskId,
    engine: (get('engine') || DEFAULT_SPEC.engine) as EngineId,
    project: get('project'),
    structure: data.has('structure'),
    source: get('source'),
    rows: get('rows'),
    cols: get('cols'),
    target: get('target'),
    targetNote: get('targetNote'),
    columnNotes: get('columnNotes'),
    models: get('models'),
    grid: get('grid'),
    bans: data.getAll('bans').map(String),
    seed: get('seed'),
    testPct: get('testPct'),
    folds: get('folds'),
    score: get('score'),
    threshold: get('threshold'),
    outcome: get('outcome'),
    metrics: get('metrics'),
    style: data.getAll('style').map(String),
  };
}

function applySpec(form: HTMLFormElement, state: SpecState): void {
  const groups: Record<string, string[]> = { bans: state.bans, style: state.style };
  for (const el of all<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>(form, '[name]')) {
    const value = (state as unknown as Record<string, unknown>)[el.name];
    if (el instanceof HTMLInputElement && el.type === 'checkbox') {
      el.checked = el.name in groups ? groups[el.name].includes(el.value) : Boolean(value);
    } else if (el instanceof HTMLInputElement && el.type === 'radio') {
      el.checked = el.value === value;
    } else if (typeof value === 'string') {
      el.value = value;
    }
  }
}

function mountBuilder(form: HTMLFormElement): void {
  const score = one<HTMLInputElement>(form, '[name="score"]')!;
  const metrics = one<HTMLInputElement>(form, '[name="metrics"]')!;
  const preset = (task: string) => TASKS.find((t) => t.id === task) ?? TASKS[0];
  let task = DEFAULT_SPEC.task as string;

  const render = () => {
    const state = readSpec(form);
    // Switching the task swaps the default score and metrics, unless they were edited.
    if (state.task !== task) {
      const before = preset(task);
      const after = preset(state.task);
      if (score.value.trim() === '' || score.value === before.score) score.value = after.score;
      if (metrics.value.trim() === '' || metrics.value === before.metrics) metrics.value = after.metrics;
      task = state.task;
      state.score = score.value;
      state.metrics = metrics.value;
    }
    for (const el of all(form, '[data-only-task]')) el.hidden = el.dataset.onlyTask !== state.task;
    for (const el of all(form, '[data-only-local]')) el.hidden = state.engine === 'colab';
    setText(form, '[data-baseline]', preset(state.task).baseline);
    const text = buildSetupPrompt(state);
    setPrompt('setup', text);
    const blanks = (text.match(/<[^>\n]+>/g) ?? []).length;
    setText(
      document,
      '[data-vc-blanks]',
      blanks === 0 ? 'No blanks left. Ready to send.' : `${blanks} ${blanks === 1 ? 'blank' : 'blanks'} left to fill.`,
    );
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(state));
    } catch {
      // Storage blocked or full: the builder still works, it just forgets on reload.
    }
  };

  try {
    const saved = JSON.parse(localStorage.getItem(STORE_KEY) ?? 'null') as Partial<SpecState> | null;
    if (saved && typeof saved === 'object') {
      const state = { ...DEFAULT_SPEC, ...saved };
      state.bans = (Array.isArray(saved.bans) ? saved.bans : DEFAULT_SPEC.bans).filter((id) => BANS.some((b) => b.id === id));
      state.style = (Array.isArray(saved.style) ? saved.style : DEFAULT_SPEC.style).filter((id) =>
        STYLE_LINES.some((s) => s.id === id),
      );
      applySpec(form, state);
      task = TASKS.some((t) => t.id === state.task) ? state.task : DEFAULT_SPEC.task;
    }
  } catch {
    // Unreadable saved state: start from the defaults.
  }

  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (event) => event.preventDefault());
  one(document, '[data-vc-reset]')?.addEventListener('click', () => {
    applySpec(form, DEFAULT_SPEC);
    task = DEFAULT_SPEC.task;
    render();
  });

  const download = one<HTMLButtonElement>(document, '[data-vc-download]');
  if (download) {
    download.hidden = false;
    download.addEventListener('click', () => {
      const url = URL.createObjectURL(new Blob([`${buildSetupPrompt(readSpec(form))}\n`], { type: 'text/markdown' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = '00_setup.md';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
  }
  render();
}

/* ---------- Prompt folder ---------- */

function mountTree(root: HTMLElement): void {
  const nodes = flattenTree();
  const buttons = all(root, '[data-key]');
  const panel = one(root, '[data-vc-tree-panel]');
  for (const button of buttons) {
    button.addEventListener('click', () => {
      const node = nodes.find((n) => n.key === button.dataset.key);
      if (!node || !panel) return;
      choose(buttons, button);
      panel.innerHTML = [
        `<p class="micro-label text-signal-deep">${node.isDir ? 'Folder' : 'File'}</p>`,
        `<h3 class="mt-2 font-mono text-lg">${escapeHtml(node.key)}</h3>`,
        node.what ? `<p class="mt-3 text-sm leading-relaxed">${escapeHtml(node.what)}</p>` : '',
        node.rule
          ? `<p class="mt-3 border-l-2 border-signal pl-3 text-sm leading-relaxed text-muted">${escapeHtml(node.rule)}</p>`
          : '',
        node.pre ? `<pre tabindex="0">${escapeHtml(node.pre)}</pre>` : '',
      ].join('');
    });
  }
}

/* ---------- Review checklist ---------- */

function mountReview(root: HTMLElement): void {
  const items = all(root, '[data-item]');
  const verdict = (item: HTMLElement) =>
    one(item, '[data-verdict][aria-pressed="true"]')?.dataset.verdict as 'ok' | 'broken' | undefined;

  const update = () => {
    const breaches: Breach[] = [];
    let ok = 0;
    let broken = 0;
    for (const item of items) {
      const state = verdict(item);
      const evidence = one(item, '[data-evidence]');
      if (evidence) evidence.hidden = state !== 'broken';
      if (state === 'ok') ok++;
      if (state === 'broken') {
        broken++;
        const check = CHECKLIST.find((c) => c.id === item.dataset.item);
        const what = one<HTMLInputElement>(item, '[data-evidence] input')?.value ?? '';
        if (check) breaches.push({ rule: check.rule, what: what.trim() || check.what });
      }
    }
    const open = items.length - ok - broken;
    setText(root, '[data-review-ok]', String(ok));
    setText(root, '[data-review-broken]', String(broken));
    setText(root, '[data-review-open]', String(open));
    const fix = one(root, '[data-review-fix]');
    const clear = one(root, '[data-review-clear]');
    const waiting = one(root, '[data-review-waiting]');
    if (fix) fix.hidden = broken === 0;
    if (clear) clear.hidden = !(broken === 0 && open === 0);
    if (waiting) waiting.hidden = !(broken === 0 && open > 0);
    setText(
      root,
      '[data-review-waiting-line]',
      `${open} ${open === 1 ? 'check' : 'checks'} still open. Go through all of them before you type “next”.`,
    );
    if (broken) setPrompt('review', buildCorrection(breaches));
  };

  for (const item of items) {
    const buttons = all(item, '[data-verdict]');
    for (const button of buttons) {
      button.addEventListener('click', () => {
        const on = button.getAttribute('aria-pressed') === 'true';
        for (const other of buttons) other.setAttribute('aria-pressed', 'false');
        button.setAttribute('aria-pressed', String(!on));
        update();
      });
    }
    one(item, '[data-evidence] input')?.addEventListener('input', update);
  }
  one(root, '[data-review-reset]')?.addEventListener('click', () => {
    for (const item of items) {
      for (const button of all(item, '[data-verdict]')) button.setAttribute('aria-pressed', 'false');
      const input = one<HTMLInputElement>(item, '[data-evidence] input');
      if (input) input.value = input.defaultValue;
    }
    update();
  });
  update();
}

/* ---------- Entry point ---------- */

export function mountVibeCoding(): void {
  mountCopy();
  const mounts: [string, (root: HTMLElement) => void][] = [
    ['[data-vc-engines]', mountEngines],
    ['[data-vc-contract]', mountContract],
    ['[data-vc-grid]', mountGrid],
    ['[data-vc-flow]', mountFlow],
    ['[data-vc-selection]', mountSelection],
    ['[data-vc-baseline]', mountBaseline],
    ['[data-vc-correction]', mountCorrection],
    ['[data-vc-tree]', mountTree],
    ['[data-vc-review]', mountReview],
  ];
  for (const [selector, mount] of mounts) {
    const root = one(document, selector);
    if (root) mount(root);
  }
  const builder = one<HTMLFormElement>(document, 'form[data-vc-builder]');
  if (builder) mountBuilder(builder);
}
