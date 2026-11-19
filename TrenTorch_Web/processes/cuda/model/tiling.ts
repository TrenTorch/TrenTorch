// Shared-memory tiling accounting (chapter D4).
import type { GpuProfile } from './profiles';

/** Shared loads per warp-FMA for an R x R register tile: 2R loads for R^2 FMAs = 2/R. */
export const sharedLoadsPerWarpFma = (r: number) => 2 / r;
/** Smallest R with 2R <= R^2/2 (load cycles no longer exceed FMA cycles). */
export const balancedRegisterTile = () => {
	let r = 1;
	while (2 * r > (r * r) / 2) r++;
	return r;
};
export interface SharedBound {
	loadCycles: number;
	fmaCycles: number;
	limiting: 'shared memory' | 'FMA';
	fmaPeakFraction: number;
}
/** Per warp-FMA: the load pipe does `loads` warp-loads at 1/cycle (128 B/cycle), the FMA pipe runs 2 warp-FMAs/cycle. */
export function sharedBound(r: number, p?: GpuProfile): SharedBound {
	const warpLoadsPerCycle = (p?.sharedBytesPerCycle ?? 128) / 128;
	const loadCycles = sharedLoadsPerWarpFma(r) / warpLoadsPerCycle;
	const fmaCycles = 0.5;
	return {
		loadCycles,
		fmaCycles,
		limiting: loadCycles > fmaCycles ? 'shared memory' : 'FMA',
		fmaPeakFraction: fmaCycles / Math.max(loadCycles, fmaCycles)
	};
}
/** Registers per thread for an R x R accumulator tile: R^2 + 2R + ~16 for addressing. */
export const registerTileRegs = (r: number) => r * r + 2 * r + 16;
/** Elements fetched when every block loads one A and one B tile per K-tile (edge tiles zero-padded). */
export const tileLoadElements = (m: number, n: number, k: number, t: number) =>
	Math.ceil(m / t) * Math.ceil(n / t) * Math.ceil(k / t) * 2 * t * t;
export const idealTileLoadElements = (m: number, n: number, k: number, t: number) =>
	(2 * m * n * k) / t;
export const tilingBytes = (t: number) => 2 * t * t * 4;
/** Naive loads per output (2K) versus tiled (2K/T). */
export const naiveLoadsPerOutput = (k: number) => 2 * k;
export const tiledLoadsPerOutput = (k: number, t: number) => (2 * k) / t;
