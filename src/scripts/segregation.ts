import { CDMX_BOROUGHS } from '../data/cdmx-alcaldias';

const GROUP_A = '#243130';
const GROUP_B = '#de3b22';
const VACANT = '#f6f3eb';
const BACKDROP = '#ded9cd';
const BLOCK_LINE = '#bbb4a8';
const OUTLINE = '#56524b';
const OUTSIDE = 3;

const N = 34;

function mulberry32(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let value = Math.imul(state ^ (state >>> 15), 1 | state);
    value = (value + Math.imul(value ^ (value >>> 7), 61 | value)) ^ value;
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function isInsidePolygon(x: number, y: number, points: ReadonlyArray<readonly [number, number]>): boolean {
  let inside = false;
  for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
    const [xi, yi] = points[i];
    const [xj, yj] = points[j];
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

function isInsideCity(x: number, y: number): boolean {
  return CDMX_BOROUGHS.some((borough) => isInsidePolygon(x, y, borough.points));
}

export function mountSegregation(root: HTMLElement): () => void {
  const canvas = root.querySelector<HTMLCanvasElement>('[data-seg-canvas]')!;
  const stage = root.querySelector<HTMLElement>('[data-seg-stage]')!;
  const ctx = canvas.getContext('2d')!;

  const unhappyEl = root.querySelector<HTMLElement>('[data-seg-unhappy]')!;
  const mixEl = root.querySelector<HTMLElement>('[data-seg-mix]')!;
  const stepEl = root.querySelector<HTMLElement>('[data-seg-step]')!;
  const statusEl = root.querySelector<HTMLElement>('[data-seg-status]')!;
  const statusDot = root.querySelector<HTMLElement>('[data-seg-status-dot]')!;

  const threshold = root.querySelector<HTMLInputElement>('[data-seg-threshold]')!;
  const vacant = root.querySelector<HTMLInputElement>('[data-seg-vacant]')!;
  const thresholdVal = root.querySelector<HTMLElement>('[data-seg-threshold-val]')!;
  const vacantVal = root.querySelector<HTMLElement>('[data-seg-vacant-val]')!;
  const runBtn = root.querySelector<HTMLButtonElement>('[data-seg-run]')!;
  const stepBtn = root.querySelector<HTMLButtonElement>('[data-seg-step-button]')!;
  const reshuffleBtn = root.querySelector<HTMLButtonElement>('[data-seg-reshuffle]')!;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let grid = new Uint8Array(N * N);
  let steps = 0;
  let playing = !reduceMotion;
  let timer: number | undefined;
  let size = 640;

  const vertCount = (N + 1) * (N + 1);
  const vx = new Float32Array(vertCount);
  const vy = new Float32Array(vertCount);
  const active = new Uint8Array(N * N);
  const activeIndices: number[] = [];

  function buildCity() {
    const random = mulberry32(0xc1d0d);
    const cell = 1 / N;
    const jitter = cell * 0.3;

    for (let gy = 0; gy <= N; gy++) {
      for (let gx = 0; gx <= N; gx++) {
        const index = gy * (N + 1) + gx;
        let x = gx * cell;
        let y = gy * cell;
        if (gx !== 0 && gx !== N) x += (random() * 2 - 1) * jitter;
        if (gy !== 0 && gy !== N) y += (random() * 2 - 1) * jitter;
        vx[index] = x;
        vy[index] = y;
      }
    }

    for (let gy = 0; gy < N; gy++) {
      for (let gx = 0; gx < N; gx++) {
        const index = gy * N + gx;
        if (!isInsideCity((gx + 0.5) / N, (gy + 0.5) / N)) continue;
        active[index] = 1;
        activeIndices.push(index);
      }
    }
  }

  function reshuffle() {
    const vacancy = Number(vacant.value);
    grid = new Uint8Array(N * N);
    grid.fill(OUTSIDE);
    for (const index of activeIndices) {
      const draw = Math.random();
      if (draw < vacancy) grid[index] = 0;
      else if (draw < vacancy + (1 - vacancy) / 2) grid[index] = 1;
      else grid[index] = 2;
    }
    steps = 0;
    draw();
    updateReadouts();
  }

  const neighborsOf = (index: number): number[] => {
    const x = index % N;
    const y = (index / N) | 0;
    const neighbors: number[] = [];
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        if (dx === 0 && dy === 0) continue;
        const nextX = x + dx;
        const nextY = y + dy;
        if (nextX < 0 || nextY < 0 || nextX >= N || nextY >= N) continue;
        const neighbor = nextY * N + nextX;
        if (active[neighbor]) neighbors.push(neighbor);
      }
    }
    return neighbors;
  };

  const isHappy = (index: number, minimum: number): boolean => {
    const resident = grid[index];
    let same = 0;
    for (const neighbor of neighborsOf(index)) if (grid[neighbor] === resident) same++;
    return same >= minimum;
  };

  function stepOnce(): boolean {
    const minimum = Number(threshold.value);
    const unhappy: number[] = [];
    const empties: number[] = [];
    for (const index of activeIndices) {
      if (grid[index] === 0) empties.push(index);
      else if (!isHappy(index, minimum)) unhappy.push(index);
    }
    if (unhappy.length === 0 || empties.length === 0) return false;

    for (const origin of unhappy) {
      if (empties.length === 0) break;
      const emptyIndex = (Math.random() * empties.length) | 0;
      const destination = empties[emptyIndex];
      empties[emptyIndex] = empties[empties.length - 1];
      empties.pop();
      grid[destination] = grid[origin];
      grid[origin] = 0;
      empties.push(origin);
    }
    steps++;
    return true;
  }

  function countUnhappy(): number {
    const minimum = Number(threshold.value);
    let count = 0;
    for (const index of activeIndices) {
      if ((grid[index] === 1 || grid[index] === 2) && !isHappy(index, minimum)) count++;
    }
    return count;
  }

  function segregation(): number {
    let total = 0;
    let same = 0;
    for (const index of activeIndices) {
      const resident = grid[index];
      if (resident !== 1 && resident !== 2) continue;
      for (const neighbor of neighborsOf(index)) {
        if (grid[neighbor] !== 1 && grid[neighbor] !== 2) continue;
        total++;
        if (grid[neighbor] === resident) same++;
      }
    }
    return total > 0 ? same / total : 0;
  }

  function updateReadouts() {
    unhappyEl.textContent = String(countUnhappy());
    stepEl.textContent = String(steps).padStart(2, '0');
    mixEl.textContent = `${Math.round(segregation() * 100)}%`;
    thresholdVal.textContent = String(Number(threshold.value));
    vacantVal.textContent = `${Math.round(Number(vacant.value) * 100)}%`;
  }

  function tracePolygon(points: ReadonlyArray<readonly [number, number]>) {
    points.forEach(([x, y], index) => {
      if (index === 0) ctx.moveTo(x * size, y * size);
      else ctx.lineTo(x * size, y * size);
    });
    ctx.closePath();
  }

  function cityPath() {
    ctx.beginPath();
    for (const borough of CDMX_BOROUGHS) tracePolygon(borough.points);
  }

  function cellPath(gx: number, gy: number) {
    const a = gy * (N + 1) + gx;
    const b = a + 1;
    const c = a + (N + 1) + 1;
    const d = a + (N + 1);
    ctx.beginPath();
    ctx.moveTo(vx[a] * size, vy[a] * size);
    ctx.lineTo(vx[b] * size, vy[b] * size);
    ctx.lineTo(vx[c] * size, vy[c] * size);
    ctx.lineTo(vx[d] * size, vy[d] * size);
    ctx.closePath();
  }

  function drawTerrain() {
    ctx.save();
    ctx.strokeStyle = 'rgba(86, 82, 75, 0.12)';
    ctx.lineWidth = 0.8;
    for (let ring = 0; ring < 5; ring++) {
      ctx.beginPath();
      ctx.ellipse(size * 0.52, size * 0.52, size * (0.43 + ring * 0.035), size * (0.35 + ring * 0.032), -0.18, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawAdministrativeLines() {
    ctx.save();
    ctx.strokeStyle = 'rgba(51, 48, 44, 0.72)';
    ctx.lineWidth = Math.max(0.75, size / 680);
    for (const borough of CDMX_BOROUGHS) {
      ctx.beginPath();
      tracePolygon(borough.points);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawRoads() {
    const roads: Array<(context: CanvasRenderingContext2D) => void> = [
      (context) => {
        context.moveTo(size * 0.34, size * 0.29);
        context.bezierCurveTo(size * 0.41, size * 0.34, size * 0.58, size * 0.34, size * 0.69, size * 0.33);
      },
      (context) => {
        context.moveTo(size * 0.48, size * 0.16);
        context.bezierCurveTo(size * 0.49, size * 0.32, size * 0.46, size * 0.49, size * 0.42, size * 0.73);
      },
      (context) => {
        context.moveTo(size * 0.31, size * 0.42);
        context.bezierCurveTo(size * 0.34, size * 0.2, size * 0.62, size * 0.15, size * 0.7, size * 0.42);
        context.bezierCurveTo(size * 0.72, size * 0.51, size * 0.62, size * 0.57, size * 0.56, size * 0.6);
      },
    ];

    ctx.save();
    cityPath();
    ctx.clip();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    for (const road of roads) {
      ctx.beginPath();
      road(ctx);
      ctx.strokeStyle = 'rgba(247, 244, 236, 0.92)';
      ctx.lineWidth = Math.max(2.6, size / 150);
      ctx.stroke();
      ctx.beginPath();
      road(ctx);
      ctx.strokeStyle = 'rgba(84, 80, 73, 0.56)';
      ctx.lineWidth = Math.max(0.65, size / 820);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawLabels() {
    ctx.save();
    const mobileLabels = new Set(['GAM', 'CUAUHTÉMOC', 'IZTAPALAPA', 'XOCHIMILCO', 'TLALPAN', 'MILPA ALTA']);
    const fontSize = Math.max(5.2, size * 0.009);
    ctx.font = `600 ${fontSize}px "IBM Plex Mono", monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.lineWidth = Math.max(1.6, size / 340);
    for (const borough of CDMX_BOROUGHS) {
      if (size < 430 && !mobileLabels.has(borough.label)) continue;
      const x = borough.centroid[0] * size;
      const y = borough.centroid[1] * size;
      ctx.strokeStyle = 'rgba(246, 243, 235, 0.92)';
      ctx.strokeText(borough.label, x, y);
      ctx.fillStyle = 'rgba(45, 43, 39, 0.82)';
      ctx.fillText(borough.label, x, y);
    }
    ctx.restore();
  }

  function draw() {
    ctx.fillStyle = BACKDROP;
    ctx.fillRect(0, 0, size, size);
    drawTerrain();

    ctx.save();
    cityPath();
    ctx.clip();
    ctx.fillStyle = VACANT;
    ctx.fillRect(0, 0, size, size);

    for (let gy = 0; gy < N; gy++) {
      for (let gx = 0; gx < N; gx++) {
        const index = gy * N + gx;
        if (!active[index]) continue;
        cellPath(gx, gy);
        ctx.fillStyle = grid[index] === 1 ? GROUP_A : grid[index] === 2 ? GROUP_B : VACANT;
        ctx.fill();
        ctx.strokeStyle = grid[index] === 0 ? BLOCK_LINE : 'rgba(246, 243, 235, 0.72)';
        ctx.lineWidth = Math.max(0.45, size / 1200);
        ctx.stroke();
      }
    }
    ctx.restore();

    drawAdministrativeLines();
    drawRoads();

    cityPath();
    ctx.strokeStyle = OUTLINE;
    ctx.lineWidth = Math.max(1.05, size / 560);
    ctx.stroke();
    drawLabels();
  }

  function setStatus(label: 'Running' | 'Paused' | 'Stable') {
    statusEl.textContent = label;
    statusDot.dataset.paused = String(label !== 'Running');
  }

  function setPlaying(nextPlaying: boolean, stoppedLabel: 'Paused' | 'Stable' = 'Paused') {
    playing = nextPlaying;
    runBtn.textContent = nextPlaying ? 'Pause' : 'Run';
    runBtn.setAttribute('aria-pressed', String(nextPlaying));
    setStatus(nextPlaying ? 'Running' : stoppedLabel);
    if (nextPlaying) startTimer();
    else stopTimer();
  }

  function startTimer() {
    if (timer != null) return;
    timer = window.setInterval(() => {
      const moved = stepOnce();
      draw();
      updateReadouts();
      if (!moved) setPlaying(false, 'Stable');
    }, 85);
  }

  function stopTimer() {
    if (timer != null) {
      window.clearInterval(timer);
      timer = undefined;
    }
  }

  function resize() {
    const width = stage.clientWidth;
    if (width <= 0) return;
    size = Math.min(width, 760);
    const deviceScale = Math.min(window.devicePixelRatio || 1, 2);
    canvas.style.width = `${size}px`;
    canvas.style.height = `${size}px`;
    canvas.width = Math.round(size * deviceScale);
    canvas.height = Math.round(size * deviceScale);
    ctx.setTransform(deviceScale, 0, 0, deviceScale, 0, 0);
    draw();
  }

  runBtn.addEventListener('click', () => setPlaying(!playing));
  stepBtn.addEventListener('click', () => {
    setPlaying(false);
    const moved = stepOnce();
    draw();
    updateReadouts();
    if (!moved) setStatus('Stable');
  });
  reshuffleBtn.addEventListener('click', () => {
    setPlaying(false);
    reshuffle();
  });
  threshold.addEventListener('input', () => {
    updateReadouts();
    if (!playing) setStatus(countUnhappy() === 0 ? 'Stable' : 'Paused');
  });
  vacant.addEventListener('input', () => {
    setPlaying(false);
    reshuffle();
  });

  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(stage);

  buildCity();
  resize();
  reshuffle();
  setPlaying(playing);

  return () => {
    stopTimer();
    resizeObserver.disconnect();
  };
}
