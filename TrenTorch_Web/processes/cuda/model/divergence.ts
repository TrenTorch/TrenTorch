// Warp divergence (chapter C1).
import { WARP } from './occupancy';

/** P(a warp executes both paths) when each lane takes the rare path with probability p. */
export const pDiverge = (p: number, lanes = WARP) => 1 - (1 - p) ** lanes - p ** lanes;

/** E[t] = b + a (1 - (1-p)^32): path B is the common one, A the rare one. */
export const expectedWarpTime = (p: number, a: number, b: number, lanes = WARP) =>
	b + a * (1 - (1 - p) ** lanes);

/** E[max of `lanes` draws], each uniform on the integers 0..n-1: the warp loops until its slowest lane is done. */
export function expectedMaxUniform(n: number, lanes = WARP) {
	let e = 0;
	for (let k = 1; k <= n - 1; k++) e += 1 - (k / n) ** lanes;
	return e;
}
export const loopUtilization = (n: number, lanes = WARP) =>
	(n - 1) / 2 / expectedMaxUniform(n, lanes);

/** Seeded Monte-Carlo: fraction of warps that diverge, plus the histogram of paths executed. */
export function monteCarloDivergence(p: number, warps: number, seed = 1, lanes = WARP) {
	let s = seed >>> 0;
	const rnd = () => (
		(s = (Math.imul(s ^ (s >>> 15), 1 | s) + 0x6d2b79f5) | 0),
		((s ^ (s >>> 14)) >>> 0) / 4294967296
	);
	let diverged = 0;
	for (let w = 0; w < warps; w++) {
		let taken = 0;
		for (let l = 0; l < lanes; l++) if (rnd() < p) taken++;
		if (taken > 0 && taken < lanes) diverged++;
	}
	return { diverged, fraction: diverged / warps };
}
