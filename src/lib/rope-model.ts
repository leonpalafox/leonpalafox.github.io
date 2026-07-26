// The jumping-rope model.
//
// A rope pinned at the observations and free to thrash in between is a posterior
// over functions. This computes that posterior for an RBF-kernel Gaussian process,
// approximated with random Fourier features so everything stays M×M (M = 48)
// instead of growing with the drawing resolution.
//
// The animation trick is at the bottom: a sample drawn as
//
//   w(θ) = μ + cos(θ)·a + sin(θ)·b        with a, b independent prior draws
//
// is a valid posterior sample at *every* θ, because cos²+sin² = 1 keeps the
// covariance fixed. So rotating θ over time gives a rope that moves continuously
// while every frame it shows is an honest draw from the posterior — not a fake
// wobble layered on top of a static fit.

export interface Point {
  x: number;
  y: number;
}

export interface RopeParams {
  /** Rope stiffness: the kernel lengthscale. Larger = the rope resists bending. */
  lengthscale: number;
  /** How tightly the rope is pinned at each observation: the noise std. */
  noise: number;
  /** How far the rope swings when nothing holds it down: the prior std. */
  amplitude: number;
}

const M = 48; // random features
const SEED = 0x5eed;

/** Deterministic PRNG so the rope looks the same on every load and across reloads. */
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function gaussian(rand: () => number): number {
  // Box–Muller. u is nudged off zero so log() stays finite.
  const u = 1 - rand();
  const v = rand();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

/**
 * Fixed random basis. Frequencies are drawn once at unit lengthscale and divided
 * by ℓ on use, so dragging the stiffness slider reshapes the same rope instead of
 * swapping in a different random one.
 */
const rand = mulberry32(SEED);
const baseFreq = Array.from({ length: M }, () => gaussian(rand));
const phase = Array.from({ length: M }, () => rand() * 2 * Math.PI);

/** φ(x): the feature map, scaled so φ(x)·φ(x') approximates the RBF kernel. */
function features(x: number, p: RopeParams, out: Float64Array): void {
  const scale = p.amplitude * Math.sqrt(2 / M);
  for (let j = 0; j < M; j++) {
    out[j] = scale * Math.cos((baseFreq[j] / p.lengthscale) * x + phase[j]);
  }
}

/** In-place Cholesky, A = L·Lᵀ, lower triangle. A is M×M row-major and is overwritten. */
function cholesky(A: Float64Array, n: number): void {
  for (let i = 0; i < n; i++) {
    for (let j = 0; j <= i; j++) {
      let sum = A[i * n + j];
      for (let k = 0; k < j; k++) sum -= A[i * n + k] * A[j * n + k];
      if (i === j) {
        // Jitter guards against the tiny negatives that round-off can produce.
        A[i * n + j] = Math.sqrt(Math.max(sum, 1e-12));
      } else {
        A[i * n + j] = sum / A[j * n + j];
      }
    }
    for (let j = i + 1; j < n; j++) A[i * n + j] = 0;
  }
}

/** Solve L·x = b for lower-triangular L (forward substitution). */
function forwardSolve(L: Float64Array, b: Float64Array, x: Float64Array, n: number): void {
  for (let i = 0; i < n; i++) {
    let sum = b[i];
    for (let k = 0; k < i; k++) sum -= L[i * n + k] * x[k];
    x[i] = sum / L[i * n + i];
  }
}

/** Solve Lᵀ·x = b for lower-triangular L (back substitution). */
function backSolve(L: Float64Array, b: Float64Array, x: Float64Array, n: number): void {
  for (let i = n - 1; i >= 0; i--) {
    let sum = b[i];
    for (let k = i + 1; k < n; k++) sum -= L[k * n + i] * x[k];
    x[i] = sum / L[i * n + i];
  }
}

export interface RopeSolution {
  /** x positions the rope is evaluated at. */
  grid: Float64Array;
  /** Posterior mean — where the rope hangs on average. */
  mean: Float64Array;
  /** Posterior std at each grid point — how much slack the rope has there. */
  std: Float64Array;
  /** Per-rope cosine component. ropes[s][i] pairs with sines[s][i]. */
  cosines: Float64Array[];
  /** Per-rope sine component. */
  sines: Float64Array[];
  /** Mean std across the grid — the headline "how uncertain are we" number. */
  meanStd: number;
}

/**
 * Condition the rope on the observations.
 *
 * Cost is O(N·M² + M³ + G·M), all of it here rather than per frame: the animation
 * only has to blend the cosine/sine components this returns.
 */
export function solveRope(
  data: Point[],
  params: RopeParams,
  grid: Float64Array,
  ropeCount: number,
): RopeSolution {
  const G = grid.length;
  const N = data.length;
  const noiseVar = params.noise * params.noise;

  // A = ΦᵀΦ/σ² + I, and b = Φᵀy/σ².
  const A = new Float64Array(M * M);
  const rhs = new Float64Array(M);
  const phi = new Float64Array(M);

  for (let i = 0; i < M; i++) A[i * M + i] = 1;

  for (let n = 0; n < N; n++) {
    features(data[n].x, params, phi);
    for (let i = 0; i < M; i++) {
      rhs[i] += (phi[i] * data[n].y) / noiseVar;
      for (let j = 0; j <= i; j++) {
        A[i * M + j] += (phi[i] * phi[j]) / noiseVar;
      }
    }
  }
  // Mirror the lower triangle we filled into the upper one.
  for (let i = 0; i < M; i++) {
    for (let j = 0; j < i; j++) A[j * M + i] = A[i * M + j];
  }

  cholesky(A, M);

  // μ = A⁻¹·rhs, via the two triangular solves.
  const tmp = new Float64Array(M);
  const mu = new Float64Array(M);
  forwardSolve(A, rhs, tmp, M);
  backSolve(A, tmp, mu, M);

  // Two independent prior draws per rope become its cosine and sine components.
  // Seeded per rope index so the bundle is stable across recomputes: adding a
  // point tightens the existing ropes rather than reshuffling them.
  const cosines: Float64Array[] = [];
  const sines: Float64Array[] = [];
  for (let s = 0; s < ropeCount; s++) {
    const r = mulberry32(SEED + 977 * (s + 1));
    for (const target of [cosines, sines]) {
      const z = new Float64Array(M);
      for (let i = 0; i < M; i++) z[i] = gaussian(r);
      const w = new Float64Array(M);
      backSolve(A, z, w, M); // w = L⁻ᵀz, so cov(w) = A⁻¹ = posterior covariance
      target.push(w);
    }
  }

  // Evaluate everything on the drawing grid.
  const mean = new Float64Array(G);
  const std = new Float64Array(G);
  const cosOut = cosines.map(() => new Float64Array(G));
  const sinOut = sines.map(() => new Float64Array(G));
  const solve = new Float64Array(M);
  let stdSum = 0;

  for (let g = 0; g < G; g++) {
    features(grid[g], params, phi);

    let m = 0;
    for (let i = 0; i < M; i++) m += phi[i] * mu[i];
    mean[g] = m;

    // var = φᵀA⁻¹φ = ‖L⁻¹φ‖²
    forwardSolve(A, phi, solve, M);
    let v = 0;
    for (let i = 0; i < M; i++) v += solve[i] * solve[i];
    std[g] = Math.sqrt(Math.max(v, 0));
    stdSum += std[g];

    for (let s = 0; s < ropeCount; s++) {
      let c = 0;
      let d = 0;
      const wc = cosines[s];
      const ws = sines[s];
      for (let i = 0; i < M; i++) {
        c += phi[i] * wc[i];
        d += phi[i] * ws[i];
      }
      cosOut[s][g] = c;
      sinOut[s][g] = d;
    }
  }

  return { grid, mean, std, cosines: cosOut, sines: sinOut, meanStd: stdSum / G };
}

/**
 * The rope's position at angle θ. Every θ is a genuine posterior draw, so the
 * motion never shows a shape the data rules out.
 */
export function ropeAt(sol: RopeSolution, s: number, theta: number, out: Float64Array): void {
  const c = Math.cos(theta);
  const sn = Math.sin(theta);
  const mean = sol.mean;
  const wc = sol.cosines[s];
  const ws = sol.sines[s];
  for (let i = 0; i < out.length; i++) {
    out[i] = mean[i] + c * wc[i] + sn * ws[i];
  }
}
