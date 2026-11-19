// Online softmax and variance merges (chapter E3) and the row-wise byte counts.
export interface SoftmaxState {
	m: number;
	d: number;
}
export const softmaxState = (xs: number[]): SoftmaxState => {
	const m = Math.max(...xs);
	return { m, d: xs.reduce((a, x) => a + Math.exp(x - m), 0) };
};
/** d = d1 e^(m1-M) + d2 e^(m2-M), M = max(m1, m2). */
export function mergeSoftmax(a: SoftmaxState, b: SoftmaxState): SoftmaxState {
	const m = Math.max(a.m, b.m);
	return { m, d: a.d * Math.exp(a.m - m) + b.d * Math.exp(b.m - m) };
}
export const crossEntropyFromState = (s: SoftmaxState, target: number) =>
	s.m + Math.log(s.d) - target;
export const softmaxProbs = (xs: number[]) => {
	const s = softmaxState(xs);
	return xs.map((x) => Math.exp(x - s.m) / s.d);
};

export interface Welford {
	n: number;
	mean: number;
	m2: number;
}
export const welfordOf = (xs: number[]): Welford => {
	const n = xs.length,
		mean = xs.reduce((a, b) => a + b, 0) / n;
	return { n, mean, m2: xs.reduce((a, x) => a + (x - mean) ** 2, 0) };
};
/** Chan's parallel merge. */
export function mergeWelford(a: Welford, b: Welford): Welford {
	const n = a.n + b.n,
		delta = b.mean - a.mean;
	return { n, mean: a.mean + (delta * b.n) / n, m2: a.m2 + b.m2 + (delta * delta * a.n * b.n) / n };
}
export const welfordVariance = (w: Welford) => w.m2 / w.n;
/** Variance from E[x^2] - E[x]^2 evaluated in FP32: loses everything when |mean| >> std. */
export function naiveVarianceFp32(xs: number[]) {
	const f = Math.fround,
		n = xs.length;
	let s = 0,
		s2 = 0;
	for (const x of xs) {
		s = f(s + f(x));
		s2 = f(s2 + f(f(x) * f(x)));
	}
	return f(f(s2 / n) - f(f(s / n) * f(s / n)));
}

/** Bytes moved per row by a row-resident softmax: read C floats, write C floats. */
export const rowSoftmaxBytes = (c: number) => 8 * c;
/** Unnecessary probability traffic avoided by fusing cross-entropy with softmax. */
export const probabilityMatrixBytes = (rows: number, classes: number) => rows * classes * 4;
