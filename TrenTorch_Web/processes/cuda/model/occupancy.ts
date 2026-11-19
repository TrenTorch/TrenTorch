// Occupancy, resource limits and wave arithmetic (chapters B3, B4, A5).
import type { GpuProfile } from './profiles';

export const WARP = 32;
export const warpsPerBlock = (threads: number) => Math.ceil(threads / WARP);

/** Fraction of lanes doing useful work when a block of `threads` is cut into warps. */
export const laneUtilization = (threads: number) => threads / (WARP * warpsPerBlock(threads));

/** Registers are allocated per warp in fixed units, so 37 registers/thread really costs 40. */
export function effectiveRegsPerThread(regs: number, unitPerWarp = 256) {
	return (Math.ceil((regs * WARP) / unitPerWarp) * unitPerWarp) / WARP;
}

export type Limiter = 'threads' | 'registers' | 'shared memory' | 'block slots';
export interface OccupancyResult {
	byThreads: number;
	byRegs: number;
	bySmem: number;
	bySlots: number;
	blocks: number;
	limiter: Limiter;
	/** every limit that equals the minimum */
	binding: Limiter[];
	threadsPerSm: number;
	warpsPerSm: number;
	occupancy: number;
	effectiveRegs: number;
	regsPerBlock: number;
}

/**
 * Blocks per SM = min(threads, registers, shared memory, block slots), with the registers rounded up to the
 * allocation unit and shared memory rounded up to `smemGranule` bytes.
 */
export function occupancy(
	p: GpuProfile,
	blockThreads: number,
	regsPerThread: number,
	smemPerBlockBytes = 0,
	opts: { rounding?: boolean; smemGranule?: number } = {}
): OccupancyResult {
	const rounding = opts.rounding ?? true;
	const granule = opts.smemGranule ?? 1024;
	const warps = warpsPerBlock(blockThreads);
	const effRegs = rounding
		? effectiveRegsPerThread(regsPerThread, p.regAllocUnitPerWarp)
		: regsPerThread;
	const regsPerBlock = effRegs * WARP * warps;
	const smem =
		smemPerBlockBytes > 0 && rounding
			? Math.ceil(smemPerBlockBytes / granule) * granule
			: smemPerBlockBytes;
	const byThreads = Math.floor(p.maxThreadsPerSm / (warps * WARP));
	const byRegs = regsPerBlock > 0 ? Math.floor(p.regsPerSm / regsPerBlock) : Infinity;
	const bySmem = smem > 0 ? Math.floor((p.smemPerSmKB * 1024) / smem) : Infinity;
	const bySlots = p.maxBlocksPerSm;
	const blocks = Math.max(0, Math.min(byThreads, byRegs, bySmem, bySlots));
	const named: [Limiter, number][] = [
		['threads', byThreads],
		['registers', byRegs],
		['shared memory', bySmem],
		['block slots', bySlots]
	];
	const binding = named.filter(([, v]) => v === blocks).map(([k]) => k);
	const warpsPerSm = blocks * warps;
	return {
		byThreads,
		byRegs,
		bySmem,
		bySlots,
		blocks,
		limiter: binding[0],
		binding,
		threadsPerSm: blocks * warps * WARP,
		warpsPerSm,
		occupancy: warpsPerSm / p.maxWarpsPerSm,
		effectiveRegs: effRegs,
		regsPerBlock
	};
}

/** Occupancy as the register count grows: the staircase of VIZ-OCCUPANCY-STAIRCASE. */
export function occupancyStaircase(
	p: GpuProfile,
	blockThreads: number,
	smemPerBlockBytes = 0,
	rounding = true,
	maxRegs = 255
) {
	const pts: { regs: number; occupancy: number; blocks: number }[] = [];
	for (let r = 16; r <= maxRegs; r++) {
		const o = occupancy(p, blockThreads, r, smemPerBlockBytes, { rounding });
		pts.push({ regs: r, occupancy: o.occupancy, blocks: o.blocks });
	}
	return pts;
}

/** Register-per-thread cap implied by __launch_bounds__(threads, minBlocks). */
export const launchBoundsRegs = (p: GpuProfile, threads: number, minBlocks: number) =>
	Math.floor(p.regsPerSm / (threads * minBlocks));

/** Largest registers/thread that still reaches `targetBlocks` resident blocks. */
export function regsForBlocks(p: GpuProfile, blockThreads: number, targetBlocks: number) {
	let best = 0;
	for (let r = 1; r <= p.maxRegsPerThread; r++)
		if (occupancy(p, blockThreads, r).blocks >= targetBlocks) best = r;
	return best;
}

export const residentCapacity = (p: GpuProfile, blocksPerSm: number) => p.sms * blocksPerSm;
export const waves = (grid: number, capacity: number) => Math.ceil(grid / capacity);
export const waveEfficiency = (grid: number, capacity: number) =>
	grid / (capacity * waves(grid, capacity));

/** A block of `blockThreads` threads, grid-stride launch size = capacity: elements per thread. */
export const elementsPerThread = (n: number, capacityBlocks: number, blockThreads: number) =>
	n / (capacityBlocks * blockThreads);

/** Blocks needed to cover n elements with `perThread` elements per thread. */
export const blocksFor = (n: number, blockThreads: number, perThread = 1) =>
	Math.ceil(n / (blockThreads * perThread));

/** Linearised thread id in a block and the 1-D voxel index for an X x Y x Z volume (x fastest). */
export const linearThreadId = (tx: number, ty: number, tz: number, bx: number, by: number) =>
	tx + ty * bx + tz * bx * by;
export const voxelIndex = (x: number, y: number, z: number, X: number, Y: number) =>
	(z * Y + y) * X + x;

/** What `int` arithmetic does to blockIdx.x * blockDim.x for large N: wraps at 2^32 (unsigned) / 2^31 (signed). */
export function wrap32(i: number) {
	const m = ((i % 2 ** 32) + 2 ** 32) % 2 ** 32;
	return m >= 2 ** 31 ? m - 2 ** 32 : m;
}
/** Issue-slot accounting (B3): warps per scheduler needed to hide latency L with c compute instructions of cpi cycles. */
export const warpsNeeded = (latency: number, computeInstrs: number, cpi = 2) =>
	1 + latency / (computeInstrs * cpi);

/** Fraction of scheduler issue slots used with `warps` warps, each with `ilp` independent chains. */
export function issueSlotUtilization(
	warps: number,
	ilp: number,
	latency: number,
	computeInstrs: number,
	cpi = 2
) {
	const busy = computeInstrs * cpi;
	return Math.min(1, (warps * ilp * busy) / (latency + busy));
}
