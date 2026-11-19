// Arithmetic intensity, the roofline and the matmul ladder (chapters D2, E7).
import { peakBandwidth, peakFp32, ridge, timeModel } from './perf';
import type { GpuProfile } from './profiles';

export type Roof = 'FP32' | 'TF32' | 'FP16';
export function roofFlops(p: GpuProfile, roof: Roof) {
	return roof === 'FP32'
		? peakFp32(p)
		: roof === 'TF32'
			? p.tf32TFLOPS * 1e12
			: p.fp16TensorTFLOPS * 1e12;
}
export const roofRidge = (p: GpuProfile, roof: Roof) => ridge(roofFlops(p, roof), peakBandwidth(p));

/** AI of a matmul block tile (FP32): bm*bn / (2 (bm+bn)). Square T: T/4. */
export const matmulAI = (bm: number, bn: number) => (bm * bn) / (2 * (bm + bn));
/** FP16 operands (2 bytes): bm*bn / (bm+bn). */
export const matmulAIFp16 = (bm: number, bn: number) => (bm * bn) / (bm + bn);
/** Smallest square tile whose AI reaches the ridge: T/4 >= ridge. */
export const requiredSquareTile = (ridgePoint: number) => 4 * ridgePoint;

export interface AiRow {
	kernel: string;
	flops: number;
	bytes: number;
	ai: number;
}
const row = (kernel: string, flops: number, bytes: number): AiRow => ({
	kernel,
	flops,
	bytes,
	ai: flops / bytes
});
/** The arithmetic intensity worksheet of D2 (per element / output, 4-byte floats, DRAM bytes). */
export const aiWorksheet = (): AiRow[] => [
	row('ReLU', 1, 8),
	row('Vector add', 1, 12),
	row('SAXPY', 2, 12),
	row('GEMV (A streamed once)', 2, 4),
	row('Dot product', 2, 8),
	row('Softmax (row in cache)', 5, 8),
	row('LayerNorm (row in cache)', 8, 8),
	row('SpMV, CSR', 2, 12),
	row('3x3 conv, direct, no reuse', 18, 40),
	row('3x3 conv, tiled with halo', 18, 4 * 1.27 + 4)
];

export interface LadderRow {
	version: string;
	bm: number;
	bn: number;
	ai: number;
	bytes: number;
	memoryTime: number;
	bound: 'memory' | 'compute';
}
/** The E7 cost table for C = A x B with N = M = K (no-cache model). */
export function matmulLadder(
	p: GpuProfile,
	n: number,
	etaM = 0.85
): { rows: LadderRow[]; flops: number; computeFloor: number; idealBytes: number } {
	const flops = 2 * n ** 3;
	const mk = (version: string, bm: number, bn: number): LadderRow => {
		const bytes = (n ** 3 * 4 * (bm + bn)) / (bm * bn);
		const ai = flops / bytes;
		return {
			version,
			bm,
			bn,
			ai,
			bytes,
			memoryTime: bytes / (etaM * peakBandwidth(p)),
			bound: ai < ridge(peakFp32(p), peakBandwidth(p)) ? 'memory' : 'compute'
		};
	};
	return {
		rows: [
			mk('v1 naive', 1, 1),
			mk('v3 tiled T=16', 16, 16),
			mk('v3 tiled T=32', 32, 32),
			mk('v6 register tile', 64, 64),
			mk('v6 register tile', 128, 128)
		],
		flops,
		computeFloor: flops / (0.8 * peakFp32(p)),
		idealBytes: 3 * n * n * 4
	};
}

/** Double buffering upper bound: sum of load+compute versus their max. */
export const doubleBufferGain = (load: number, compute: number) =>
	(load + compute) / Math.max(load, compute);

export const kernelTime = timeModel;
