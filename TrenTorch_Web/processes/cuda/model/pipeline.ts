// Copy/compute overlap with streams (chapter F2).
export interface PipelineInputs {
	h: number;
	k: number;
	d: number;
	chunks: number;
	copyEngines?: 1 | 2;
	chunkOverhead?: number;
}
/**
 * T(S) = (h + k + d) + (S - 1) max(h, k, d) with per-chunk times h = H/S, k = K/S, d = D/S. With a single copy
 * engine the in/out copies serialize and the max becomes max(h + d, k).
 */
export function pipelineTime({
	h: H,
	k: K,
	d: D,
	chunks: S,
	copyEngines = 2,
	chunkOverhead = 0
}: PipelineInputs) {
	const h = H / S,
		k = K / S,
		d = D / S;
	const stage = copyEngines === 2 ? Math.max(h, k, d) : Math.max(h + d, k);
	const fill = h + k + d;
	return fill + (S - 1) * stage + S * chunkOverhead;
}
export const serialTime = (H: number, K: number, D: number) => H + K + D;
export const pipelineLowerBound = (H: number, K: number, D: number) => Math.max(H, K, D);
