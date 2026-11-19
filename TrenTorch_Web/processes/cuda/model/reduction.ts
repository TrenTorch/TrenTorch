// The reduction ladder (chapter E2) and warp shuffles (F1), as step-by-step models.
import { conflictDegree } from './memory';

export type ReductionVariant = 1 | 2 | 3 | 4 | 5 | 6;
export const REDUCTION_VARIANTS: Record<ReductionVariant, string> = {
	1: 'Interleaved, divergent (tid % 2s == 0)',
	2: 'Interleaved, non-divergent (strided index)',
	3: 'Sequential addressing',
	4: 'First add during load',
	5: 'Warp shuffle for the last 5 levels',
	6: 'Multi-block with atomicAdd'
};
export interface ReduceStep {
	label: string;
	active: boolean[];
	reads: [number, number][];
	bankDegree: number;
	barrier: boolean;
	shuffle?: number;
	values: number[];
}
export interface ReduceTrace {
	steps: ReduceStep[];
	threads: number;
	result: number;
	barriers: number;
	warpEfficiency: number;
	bankConflictCycles: number;
	atomics: number;
}

/** Simulates variant `v` on `x` (length a power of two). All variants return the same sum. */
export function reduceTrace(v: ReductionVariant, x: number[]): ReduceTrace {
	const n = x.length;
	const steps: ReduceStep[] = [];
	let a = x.slice();
	const push = (
		label: string,
		active: boolean[],
		reads: [number, number][],
		words: number[],
		barrier: boolean,
		shuffle?: number
	) =>
		steps.push({
			label,
			active,
			reads,
			bankDegree: words.length ? conflictDegree(words.slice(0, 32)) : 1,
			barrier,
			shuffle,
			values: a.slice()
		});
	let threads = n,
		atomics = 0;
	if (v === 1)
		for (let s = 1; s < n; s *= 2) {
			const act = a.map((_, t) => t % (2 * s) === 0),
				reads: [number, number][] = [];
			a = a.map((val, t) => {
				if (!act[t]) return val;
				reads.push([t, t + s]);
				return val + a[t + s];
			});
			push(
				`s = ${s}`,
				act,
				reads,
				act.flatMap((on, t) => (on ? [t + s] : [])),
				true
			);
		}
	else if (v === 2)
		for (let s = 1; s < n; s *= 2) {
			const act = a.map((_, t) => t < n / (2 * s)),
				reads: [number, number][] = [],
				words: number[] = [];
			const next = a.slice();
			for (let t = 0; t < n / (2 * s); t++) {
				const i = 2 * s * t;
				next[i] = a[i] + a[i + s];
				reads.push([i, i + s]);
				words.push(i);
			}
			a = next;
			push(`s = ${s}`, act, reads, words, true);
		}
	else if (v === 3 || v === 5 || v === 6 || v === 4) {
		if (v === 4) {
			threads = n / 2;
			a = Array.from({ length: n / 2 }, (_, t) => x[t] + x[t + n / 2]);
			push(
				'load: each thread adds two elements',
				Array(n / 2).fill(true),
				Array.from({ length: n / 2 }, (_, t) => [t, t + n / 2] as [number, number]),
				[],
				false
			);
		}
		const len = a.length;
		for (let s = len / 2; s >= 1; s = Math.floor(s / 2)) {
			const shuffle = v >= 5 && s < 32 ? s : undefined;
			const act = a.map((_, t) => t < s),
				reads: [number, number][] = [];
			const next = a.slice();
			for (let t = 0; t < s; t++) {
				next[t] = a[t] + a[t + s];
				reads.push([t, t + s]);
			}
			a = next;
			push(
				shuffle ? `shuffle down by ${s}` : `s = ${s}`,
				act,
				reads,
				Array.from({ length: s }, (_, t) => t),
				!shuffle,
				shuffle
			);
		}
		if (v === 6) {
			atomics = 1;
			push('one atomicAdd of the block total', [true], [], [], false);
		}
	}
	const result = a[0];
	const used = steps.reduce((acc, st) => acc + st.active.filter(Boolean).length, 0);
	let slots = 0;
	for (const st of steps) {
		const warps = Math.ceil(st.active.length / 32);
		for (let w = 0; w < warps; w++)
			if (st.active.slice(w * 32, w * 32 + 32).some(Boolean)) slots += 32;
	}
	return {
		steps,
		threads,
		result,
		barriers: steps.filter((s) => s.barrier).length,
		warpEfficiency: slots ? used / slots : 1,
		bankConflictCycles: steps.reduce((acc, s) => acc + (s.bankDegree - 1), 0),
		atomics
	};
}

// ---- warp primitives ----
export const shflDown = (vals: number[], delta: number) =>
	vals.map((v, i) => (i + delta < vals.length ? vals[i + delta] : v));
export const shflUp = (vals: number[], delta: number) =>
	vals.map((v, i) => (i - delta >= 0 ? vals[i - delta] : v));
export const shflXor = (vals: number[], mask: number) => vals.map((_, i) => vals[i ^ mask]);
export const shflBroadcast = (vals: number[], src: number) => vals.map(() => vals[src]);
export const popc = (x: number) => {
	let c = 0;
	for (let v = x >>> 0; v; v &= v - 1) c++;
	return c;
};
export const ballot = (preds: boolean[]) =>
	preds.reduce((acc, p, i) => (p ? (acc | (1 << i)) >>> 0 : acc), 0);
/** rank = popc(ballot & ((1 << lane) - 1)) */
export const ballotRank = (mask: number, lane: number) => popc((mask & ((1 << lane) - 1)) >>> 0);
/** Warp sum with shuffle-down offsets 16, 8, 4, 2, 1: lane 0 holds the total. */
export function warpReduceSteps(vals: number[]) {
	const steps = [vals.slice()];
	for (let off = 16; off >= 1; off >>= 1) {
		const prev = steps[steps.length - 1],
			sh = shflDown(prev, off);
		steps.push(prev.map((v, i) => v + (i + off < 32 ? sh[i] : 0)));
	}
	return steps;
}
/** Sum of `values` across a 256-thread block with shared memory only vs with shuffles (F1). */
export const barrierCount = (threads: number) => ({
	sharedOnly: Math.log2(threads),
	withShuffle: 1
});
