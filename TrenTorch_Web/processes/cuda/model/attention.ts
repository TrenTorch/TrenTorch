// Attention and fusion ledgers (chapters F3, F6).
import { peakBandwidth, peakFp32 } from './perf';
import type { GpuProfile } from './profiles';

export const scoreMatrixBytes = (n: number) => n * n * 4;
/** Standard 3-kernel attention: write S, read S, write P, read P (four passes over the N x N matrix) plus Q, K, V, O. */
export function standardAttentionTraffic(n: number, d: number) {
	const s = scoreMatrixBytes(n),
		qkvo = 4 * n * d * 4;
	return { scoreTraffic: 4 * s, qkvo, total: 4 * s + qkvo };
}
/** Flash-style tiling: Q and O once, K and V re-read once per Q block (worst case: every re-read misses L2). */
export function flashAttentionTraffic(n: number, d: number, br: number) {
	const qo = 2 * n * d * 4,
		kv = 2 * n * d * 4;
	return { total: qo + kv * (n / br), l2Resident: 4 * n * d * 4 };
}
/** On-chip bytes: Q_i, O_i (br x d), K_j, V_j (bc x d), and the br x bc score tile. */
export const flashOnChipBytes = (br: number, bc: number, d: number) =>
	(2 * br * d + 2 * bc * d + br * bc) * 4;

export interface MlpShape {
	m: number;
	d: number;
	h: number;
}
/** F6 ledger: two GEMMs, fused epilogue (2 kernels) versus unfused (5 kernels). Bytes in FP32. */
export function mlpLedger(s: MlpShape) {
	const x = s.m * s.d * 4,
		w1 = s.d * s.h * 4,
		hid = s.m * s.h * 4,
		w2 = s.h * s.d * 4,
		y = s.m * s.d * 4;
	const flops = 4 * s.m * s.d * s.h;
	const fused = x + w1 + hid + (hid + w2 + x + y);
	const extra = 2 * hid + 2 * hid + 2 * y + 3 * y; // bias(h) r+w, gelu(h) r+w, bias(y) r+w, residual (read y, x; write y)
	return { x, w1, h: hid, w2, y, flops, fused, unfused: fused + extra, extraBytes: extra };
}
export function fusionShare(
	p: GpuProfile,
	s: MlpShape,
	roofFlops: number,
	etaM = 0.85,
	etaC = 0.8
) {
	const l = mlpLedger(s);
	const tGemm = l.flops / (etaC * roofFlops),
		tExtra = l.extraBytes / (etaM * peakBandwidth(p));
	return { tGemm, tExtra, share: tExtra / tGemm, ai: l.flops / l.fused };
}
export const fp32Roof = (p: GpuProfile) => peakFp32(p);
