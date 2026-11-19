// Number formats, rounding and accumulation error (chapters E2, E3, F8).
export interface Format {
	name: string;
	expBits: number;
	mantBits: number;
	maxFinite: number;
	bits: number;
}
export const FORMATS: Record<string, Format> = {
	FP32: { name: 'FP32', expBits: 8, mantBits: 23, maxFinite: 3.4028235e38, bits: 32 },
	TF32: { name: 'TF32', expBits: 8, mantBits: 10, maxFinite: 3.4028235e38, bits: 19 },
	FP16: { name: 'FP16', expBits: 5, mantBits: 10, maxFinite: 65504, bits: 16 },
	BF16: { name: 'BF16', expBits: 8, mantBits: 7, maxFinite: 3.3895314e38, bits: 16 },
	E4M3: { name: 'FP8 E4M3', expBits: 4, mantBits: 3, maxFinite: 448, bits: 8 },
	E5M2: { name: 'FP8 E5M2', expBits: 5, mantBits: 2, maxFinite: 57344, bits: 8 }
};
/** Unit roundoff u = 2^-(mantissa bits + 1). */
export const unitRoundoff = (f: Format) => 2 ** -(f.mantBits + 1);
/** Largest x for which exp(x) is finite in this format. */
export const expOverflowLogit = (f: Format) => Math.log(f.maxFinite);

/** Round x to the nearest value of the format (ties to even); overflow becomes Infinity. */
export function roundTo(x: number, f: Format): number {
	if (!Number.isFinite(x) || x === 0) return x;
	const bias = 2 ** (f.expBits - 1) - 1;
	const minExp = 1 - bias; // smallest normal exponent
	const sign = x < 0 ? -1 : 1,
		a = Math.abs(x);
	let e = Math.floor(Math.log2(a));
	if (2 ** e > a) e--;
	else if (2 ** (e + 1) <= a) e++;
	const useE = Math.max(e, minExp); // subnormals share the smallest exponent
	const quantum = 2 ** (useE - f.mantBits);
	const q = a / quantum;
	let r = Math.round(q);
	if (Math.abs(q - Math.trunc(q) - 0.5) < 1e-12 && r % 2 === 1) r -= 1; // tie to even
	const out = r * quantum;
	return out > f.maxFinite ? sign * Infinity : sign * out;
}
/** Spacing between neighbouring representable values at x. */
export const spacingAt = (x: number, f: Format) => {
	const bias = 2 ** (f.expBits - 1) - 1;
	return 2 ** (Math.max(Math.floor(Math.log2(Math.abs(x) || 1)), 1 - bias) - f.mantBits);
};

export type Accumulation = 'sequential' | 'tree' | 'kahan';
/** Sum of `n` ones in format `f`, simulated with real rounding at every addition (keep n modest). */
export function sumOfOnes(n: number, f: Format, how: Accumulation): number {
	const r = (v: number) => (f.name === 'FP32' ? Math.fround(v) : roundTo(v, f));
	if (how === 'sequential') {
		let s = 0;
		for (let i = 0; i < n; i++) {
			const next = r(s + 1);
			if (next === s) return s;
			s = next;
		} // stalled: stays forever
		return s;
	}
	if (how === 'kahan') {
		let s = 0,
			c = 0;
		for (let i = 0; i < n; i++) {
			const y = r(1 - c);
			const t = r(s + y);
			c = r(r(t - s) - y);
			s = t;
		}
		return s;
	}
	// pairwise: halve the count at every level
	let level = new Array(n).fill(1);
	while (level.length > 1) {
		const next: number[] = [];
		for (let i = 0; i < level.length; i += 2)
			next.push(i + 1 < level.length ? r(level[i] + level[i + 1]) : level[i]);
		level = next;
	}
	return level[0] ?? 0;
}
/** Analytic stall point of a sequential sum of ones: spacing reaches 2 at 2^(mantBits+1). */
export const sequentialStall = (f: Format) => 2 ** (f.mantBits + 1);

/** Worst-case relative error bounds for summing n terms. */
export const sequentialErrorBound = (n: number, u: number) => (n - 1) * u;
export const pairwiseErrorBound = (n: number, u: number) => Math.ceil(Math.log2(n)) * u;
/** Dot product of K terms: accumulate in the low format (~K u) or in FP32 (~u + K 2^-24). */
export const dotErrorLowAccum = (k: number, f: Format) => k * unitRoundoff(f);
export const dotErrorFp32Accum = (k: number, f: Format) => unitRoundoff(f) + k * 2 ** -24;
export const bytesFor = (n: number, f: Format) => (n * f.bits) / 8;
