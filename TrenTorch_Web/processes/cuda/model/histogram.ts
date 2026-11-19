// Atomics and histogram accounting (chapters C3, E5).
export const naiveGlobalAtomics = (n: number) => n;
export const privatizedGlobalAtomics = (blocks: number, bins: number) => blocks * bins;
export const maxSharedBins = (smemKB: number) => Math.floor((smemKB * 1024) / 4);
/** Illustrative: a fraction f of inputs hit one bin at ~1 ns per same-address atomic. */
export const hotBinSeconds = (n: number, f: number, nsPerAtomic = 1) => f * n * nsPerAtomic * 1e-9;
/** Warp-aggregated: lanes with equal bins merge, so atomics = number of distinct bins in the warp. */
export const warpAggregatedAtomics = (bins: number[]) => new Set(bins).size;
export const lastBlockAtomics = (grid: number) => grid;
/** rank = popc(mask & lanemask_lt): position of a lane among the lanes sharing its bin. */
export const lanePopcRank = (bins: number[], lane: number) =>
	bins.slice(0, lane).filter((b) => b === bins[lane]).length;
export const histogram = (xs: number[], bins: number) => {
	const h = Array(bins).fill(0);
	xs.forEach((x) => {
		if (x >= 0 && x < bins) h[x]++;
	});
	return h;
};
