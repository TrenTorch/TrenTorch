// Sorting networks and radix passes (chapter E8).
export const bitonicStages = (n: number) => {
	const k = Math.round(Math.log2(n));
	return (k * (k + 1)) / 2;
};
export const bitonicComparators = (n: number) => (n / 2) * bitonicStages(n);
export const infoTheoreticComparisons = (n: number) => n * Math.log2(n);
export const radixPasses = (keyBits: number, digitBits: number) => Math.ceil(keyBits / digitBits);
/** Lower-bound bytes: each pass reads and writes every key once (8 B per 4-byte key). */
export const radixBytes = (n: number, keyBits: number, digitBits: number, bytesPerKey = 4) =>
	radixPasses(keyBits, digitBits) * 2 * bytesPerKey * n;

/** The compare-exchange pairs of a bitonic network, stage by stage: [lo, hi] with `ascending` direction. */
export function bitonicNetwork(n: number) {
	const stages: {
		k: number;
		j: number;
		pairs: { lo: number; hi: number; ascending: boolean }[];
	}[] = [];
	for (let k = 2; k <= n; k *= 2)
		for (let j = k / 2; j > 0; j = Math.floor(j / 2)) {
			const pairs = [];
			for (let i = 0; i < n; i++) {
				const l = i ^ j;
				if (l > i) pairs.push({ lo: i, hi: l, ascending: (i & k) === 0 });
			}
			stages.push({ k, j, pairs });
		}
	return stages;
}
export function bitonicSort(x: number[]) {
	const a = x.slice();
	for (const s of bitonicNetwork(a.length))
		for (const p of s.pairs) {
			if ((p.ascending && a[p.lo] > a[p.hi]) || (!p.ascending && a[p.lo] < a[p.hi]))
				[a[p.lo], a[p.hi]] = [a[p.hi], a[p.lo]];
		}
	return a;
}

/** One LSD radix pass on `r` bits starting at `shift`: flags, per-digit offsets, destinations, stable scatter. */
export function radixPass(keys: number[], shift: number, r: number) {
	const radix = 1 << r,
		digit = (k: number) => (k >> shift) & (radix - 1);
	const counts = Array(radix).fill(0);
	keys.forEach((k) => counts[digit(k)]++);
	const offsets: number[] = [];
	let acc = 0;
	for (let d = 0; d < radix; d++) {
		offsets.push(acc);
		acc += counts[d];
	}
	const next = offsets.slice();
	const dest = keys.map((k) => next[digit(k)]++);
	const out: number[] = Array(keys.length);
	keys.forEach((k, i) => {
		out[dest[i]] = k;
	});
	return { counts, offsets, dest, out, digits: keys.map(digit) };
}
export function radixSort(keys: number[], keyBits: number, r: number) {
	let a = keys.slice();
	for (let s = 0; s < keyBits; s += r) a = radixPass(a, s, r).out;
	return a;
}
/** Quicksort partition: fraction of lanes still active as a warp partitions around a pivot (VIZ-QUICKSORT-DIVERGENCE). */
export function partitionLaneUtilization(lanes: boolean[]) {
	const left = lanes.filter(Boolean).length,
		right = lanes.length - left;
	return left === 0 || right === 0 ? 1 : lanes.length / (2 * Math.max(left, right));
}
