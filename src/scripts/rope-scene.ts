import * as THREE from 'three';
import { Line2 } from 'three/examples/jsm/lines/Line2.js';
import { LineGeometry } from 'three/examples/jsm/lines/LineGeometry.js';
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js';
import { solveRope, ropeAt, type Point, type RopeParams, type RopeSolution } from '../lib/rope-model';

const INK = 0x141412;
const SIGNAL = 0xe2371b;
const HAIRLINE = 0xdcd7cc;

const G = 220; // grid resolution along x
const ROPES = 7;
const ROPE_GAP = 0.055; // z spacing, so the bundle reads as having depth
const MAX_POINTS = 40;

const START: Point[] = [
  { x: -0.72, y: -0.46 },
  { x: 0.72, y: 0.44 },
];

export function mountRopeScene(root: HTMLElement): () => void {
  const canvas = root.querySelector<HTMLCanvasElement>('[data-rope-canvas]')!;
  const stage = canvas.parentElement!;
  const readout = root.querySelector<HTMLElement>('[data-rope-readout]')!;
  const countEl = root.querySelector<HTMLElement>('[data-rope-count]')!;
  const playBtn = root.querySelector<HTMLButtonElement>('[data-rope-play]')!;
  const stiffness = root.querySelector<HTMLInputElement>('[data-rope-stiffness]')!;
  const tightness = root.querySelector<HTMLInputElement>('[data-rope-tightness]')!;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const grid = new Float64Array(G);
  for (let i = 0; i < G; i++) grid[i] = -1 + (2 * i) / (G - 1);

  let data: Point[] = START.map((p) => ({ ...p }));
  let params: RopeParams = { lengthscale: 0.45, noise: 0.05, amplitude: 0.72 };
  let sol: RopeSolution = solveRope(data, params, grid, ROPES);

  // ---------------------------------------------------------------- three.js
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setClearAlpha(0); // let the page's paper colour show through

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);

  // Everything lives in this group. The camera fits the data's y range to the panel
  // height, and the group's x scale stretches the x range to the panel width — the
  // usual non-uniform chart mapping, so the plot fills the frame at any aspect while
  // the perspective camera still gives the rope bundle its depth.
  const content = new THREE.Group();
  scene.add(content);
  const HALF_H = 1.12;
  const HALF_W = 1.08;
  let scaleX = 1;

  // Frame and gridlines, drawn once.
  const frame = new THREE.Group();
  const gridPts: number[] = [];
  for (let i = -2; i <= 2; i++) {
    const v = i / 2;
    gridPts.push(-1.06, v, 0, 1.06, v, 0);
    gridPts.push(v, -1.06, 0, v, 1.06, 0);
  }
  const gridGeo = new THREE.BufferGeometry();
  gridGeo.setAttribute('position', new THREE.Float32BufferAttribute(gridPts, 3));
  frame.add(
    new THREE.LineSegments(
      gridGeo,
      new THREE.LineBasicMaterial({ color: HAIRLINE, transparent: true, opacity: 0.75 }),
    ),
  );
  content.add(frame);

  // Uncertainty band: the ±2σ envelope the rope is free to move inside.
  const bandGeo = new THREE.BufferGeometry();
  const bandPos = new Float32Array(G * 2 * 3);
  const bandIdx: number[] = [];
  for (let i = 0; i < G - 1; i++) {
    const a = i * 2;
    bandIdx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
  }
  bandGeo.setAttribute('position', new THREE.BufferAttribute(bandPos, 3));
  bandGeo.setIndex(bandIdx);
  const band = new THREE.Mesh(
    bandGeo,
    new THREE.MeshBasicMaterial({
      color: SIGNAL,
      transparent: true,
      opacity: 0.13,
      side: THREE.DoubleSide,
      depthWrite: false,
    }),
  );
  band.position.z = -0.02;
  band.frustumCulled = false;
  content.add(band);

  /** Fat line whose vertex buffer we rewrite in place — no per-frame allocation. */
  function makeLine(color: number, width: number, opacity: number) {
    const geo = new LineGeometry();
    const seed = new Float32Array(G * 3);
    for (let i = 0; i < G; i++) seed[i * 3] = grid[i];
    geo.setPositions(seed);
    const mat = new LineMaterial({ color, linewidth: width, transparent: true, opacity });
    const line = new Line2(geo, mat);
    line.frustumCulled = false;
    content.add(line);
    const buf = geo.getAttribute('instanceStart').data as THREE.InstancedInterleavedBuffer;
    return { line, mat, buf, arr: buf.array as Float32Array };
  }

  const ropes = Array.from({ length: ROPES }, (_, s) => {
    // Front ropes read strongest; the ones behind fade into the bundle.
    const depth = s / (ROPES - 1);
    return { ...makeLine(SIGNAL, 1.9, 0.28 + 0.42 * (1 - depth)), z: (s - (ROPES - 1) / 2) * ROPE_GAP };
  });
  const meanLine = makeLine(INK, 2.6, 0.9);

  function writeLine(target: { buf: THREE.InstancedInterleavedBuffer; arr: Float32Array }, y: Float64Array, z: number) {
    const { arr } = target;
    for (let p = 0; p < G - 1; p++) {
      const o = p * 6;
      arr[o] = grid[p];
      arr[o + 1] = y[p];
      arr[o + 2] = z;
      arr[o + 3] = grid[p + 1];
      arr[o + 4] = y[p + 1];
      arr[o + 5] = z;
    }
    target.buf.needsUpdate = true;
  }

  // Observations.
  const dot = new THREE.InstancedMesh(
    new THREE.SphereGeometry(0.028, 20, 14),
    new THREE.MeshBasicMaterial({ color: INK }),
    MAX_POINTS,
  );
  dot.frustumCulled = false;
  content.add(dot);
  const ring = new THREE.InstancedMesh(
    new THREE.RingGeometry(0.045, 0.055, 28),
    new THREE.MeshBasicMaterial({ color: SIGNAL, transparent: true, opacity: 0.85, side: THREE.DoubleSide }),
    MAX_POINTS,
  );
  ring.frustumCulled = false;
  content.add(ring);

  const m4 = new THREE.Matrix4();
  const counter = new THREE.Vector3();
  function drawPoints() {
    const n = Math.min(data.length, MAX_POINTS);
    // Undo the group's x stretch per instance so the markers stay circular.
    counter.set(1 / scaleX, 1, 1);
    for (let i = 0; i < n; i++) {
      m4.makeTranslation(data[i].x, data[i].y, 0.06);
      m4.scale(counter);
      dot.setMatrixAt(i, m4);
      ring.setMatrixAt(i, m4);
    }
    dot.count = n;
    ring.count = n;
    dot.instanceMatrix.needsUpdate = true;
    ring.instanceMatrix.needsUpdate = true;
  }

  // -------------------------------------------------------------- recompute
  const scratch = new Float64Array(G);

  function recompute() {
    sol = solveRope(data, params, grid, ROPES);

    for (let i = 0; i < G; i++) {
      const o = i * 6;
      bandPos[o] = grid[i];
      bandPos[o + 1] = sol.mean[i] + 2 * sol.std[i];
      bandPos[o + 2] = 0;
      bandPos[o + 3] = grid[i];
      bandPos[o + 4] = sol.mean[i] - 2 * sol.std[i];
      bandPos[o + 5] = 0;
    }
    bandGeo.getAttribute('position').needsUpdate = true;

    writeLine(meanLine, sol.mean, 0.04);
    drawPoints();

    countEl.textContent = String(data.length);
    // The headline number: how much slack the rope still has, averaged over x.
    readout.textContent = `±${sol.meanStd.toFixed(2)}`;
  }

  // ------------------------------------------------------------ interaction
  const raycaster = new THREE.Raycaster();
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
  const ndc = new THREE.Vector2();
  const hit = new THREE.Vector3();

  function toData(ev: PointerEvent): Point | null {
    const r = canvas.getBoundingClientRect();
    ndc.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
    raycaster.setFromCamera(ndc, camera);
    if (!raycaster.ray.intersectPlane(plane, hit)) return null;
    const x = hit.x / scaleX; // back out of the group's x stretch into data coords
    if (Math.abs(x) > 1.02 || Math.abs(hit.y) > 1.05) return null;
    return { x, y: hit.y };
  }

  let downAt: { x: number; y: number } | null = null;
  canvas.addEventListener('pointerdown', (ev) => {
    downAt = { x: ev.clientX, y: ev.clientY };
  });
  canvas.addEventListener('pointerup', (ev) => {
    if (!downAt) return;
    const moved = Math.hypot(ev.clientX - downAt.x, ev.clientY - downAt.y);
    downAt = null;
    if (moved > 6 || data.length >= MAX_POINTS) return; // a drag, not a click
    const p = toData(ev);
    if (p) {
      data.push(p);
      recompute();
    }
  });

  // Gentle parallax; the rope bundle's depth only reads if the camera moves a little.
  let parallaxX = 0;
  let parallaxY = 0;
  let targetX = 0;
  let targetY = 0;
  stage.addEventListener('pointermove', (ev) => {
    const r = stage.getBoundingClientRect();
    targetX = ((ev.clientX - r.left) / r.width - 0.5) * 0.55;
    targetY = ((ev.clientY - r.top) / r.height - 0.5) * -0.35;
  });
  stage.addEventListener('pointerleave', () => {
    targetX = 0;
    targetY = 0;
  });

  root.querySelector('[data-rope-undo]')!.addEventListener('click', () => {
    if (data.length) {
      data.pop();
      recompute();
    }
  });
  root.querySelector('[data-rope-reset]')!.addEventListener('click', () => {
    data = START.map((p) => ({ ...p }));
    recompute();
  });
  root.querySelector('[data-rope-add]')!.addEventListener('click', () => {
    if (data.length >= MAX_POINTS) return;
    // Sample the truth the demo is implicitly fitting, so added points are informative.
    const x = -0.9 + Math.random() * 1.8;
    const truth = 0.62 * Math.sin(2.1 * x + 0.4);
    data.push({ x, y: truth + (Math.random() - 0.5) * 0.12 });
    recompute();
  });

  stiffness.addEventListener('input', () => {
    params = { ...params, lengthscale: Number(stiffness.value) };
    recompute();
  });
  tightness.addEventListener('input', () => {
    params = { ...params, noise: Number(tightness.value) };
    recompute();
  });

  let playing = !reduceMotion;
  function syncPlay() {
    playBtn.textContent = playing ? 'Pause' : 'Play';
    playBtn.setAttribute('aria-pressed', String(playing));
  }
  playBtn.addEventListener('click', () => {
    playing = !playing;
    syncPlay();
  });
  syncPlay();

  // ----------------------------------------------------------------- resize
  function resize() {
    const w = stage.clientWidth;
    const h = stage.clientHeight;
    if (!w || !h) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    renderer.setPixelRatio(dpr);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // Sit back far enough that the y range exactly fills the panel height, then
    // stretch x so the data spans the full width.
    const halfFov = THREE.MathUtils.degToRad(camera.fov) / 2;
    camera.position.z = HALF_H / Math.tan(halfFov);
    camera.updateProjectionMatrix();
    scaleX = (HALF_H * camera.aspect) / HALF_W;
    content.scale.x = scaleX;
    drawPoints();
    for (const r of ropes) r.mat.resolution.set(w * dpr, h * dpr);
    meanLine.mat.resolution.set(w * dpr, h * dpr);
  }
  const ro = new ResizeObserver(resize);
  ro.observe(stage);
  resize();

  // ------------------------------------------------------------------ frame
  let theta = 0;
  let raf = 0;
  let last = performance.now();
  let onScreen = true;

  const io = new IntersectionObserver(([e]) => {
    onScreen = e.isIntersecting;
  });
  io.observe(stage);

  function tick(now: number) {
    raf = requestAnimationFrame(tick);
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    if (!onScreen) return;

    if (playing) theta += dt * 0.85;

    parallaxX += (targetX - parallaxX) * Math.min(dt * 4, 1);
    parallaxY += (targetY - parallaxY) * Math.min(dt * 4, 1);
    camera.position.x = parallaxX;
    camera.position.y = parallaxY;
    camera.lookAt(0, 0, 0);

    for (let s = 0; s < ROPES; s++) {
      // Each rope sits at its own phase, so the bundle breathes instead of marching.
      ropeAt(sol, s, theta + (s * Math.PI * 2) / ROPES, scratch);
      writeLine(ropes[s], scratch, ropes[s].z);
    }

    renderer.render(scene, camera);
  }

  recompute();
  raf = requestAnimationFrame(tick);

  return () => {
    cancelAnimationFrame(raf);
    ro.disconnect();
    io.disconnect();
    renderer.dispose();
  };
}
