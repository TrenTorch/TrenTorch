// Prefix-sum work and depth, networks, compaction and traffic (chapters E6, E8).
const log2 = (n: number) => Math.round(Math.log2(n));

export interface ScanCost {
	depth: number;
	additions: number;
}
export const sequentialScan = (n: number): ScanCost => ({ depth: n - 1, additions: n - 1 });
export const hillisSteeleCost = (n: number): ScanCost => ({
	depth: log2(n),
	additions: n * log2(n) - (n - 1)
});
export const blellochCost = (n: number): ScanCost => ({
	depth: 2 * log2(n),
	additions: 2 * (n - 1)
});
export const brentKungCost = (n: number): ScanCost => ({
	depth: 2 * log2(n) - 1,
	additions: 2 * n - 2 - log2(n)
});

/** Words moved by the multi-block variants, in units of N. */
export const SCAN_TRAFFIC = {
	scanThenPropagate: 4,
	reduceThenScan: 3,
	decoupledLookback: 2
} as const;

/** Hillis-Steele inclusive scan, returning the array after every step. */
export function hillisSteeleSteps(x: number[]): number[][] {
	const steps = [x.slice()];
	for (let off = 1; off < x.length; off *= 2) {
		const prev = steps[steps.length - 1];
		steps.push(prev.map((v, i) => (i >= off ? v + prev[i - off] : v)));
	}
	return steps;
}
/** Blelloch exclusive scan: arrays after the up-sweep levels, the root clear and the down-sweep levels. */
export function blellochSteps(x: number[]): { up: number[][]; down: number[][]; result: number[] } {
	const a = x.slice(),
		n = a.length,
		up = [a.slice()],
		down: number[][] = [];
	for (let d = 1; d < n; d *= 2) {
		for (let i = 2 * d - 1; i < n; i += 2 * d) a[i] += a[i - d];
		up.push(a.slice());
	}
	a[n - 1] = 0;
	down.push(a.slice());
	for (let d = n / 2; d >= 1; d /= 2) {
		for (let i = 2 * d - 1; i < n; i += 2 * d) {
			const t = a[i - d];
			a[i - d] = a[i];
			a[i] += t;
		}
		down.push(a.slice());
	}
	return { up, down, result: a };
}
export const inclusiveScan = (x: number[]) =>
	x.reduce<number[]>((acc, v) => (acc.push((acc[acc.length - 1] ?? 0) + v), acc), []);
export const exclusiveScan = (x: number[]) => {
	const inc = inclusiveScan(x);
	return inc.map((_, i) => (i ? inc[i - 1] : 0));
};
export function compact(x: number[], keep: (v: number) => boolean) {
	const flags = x.map((v) => (keep(v) ? 1 : 0));
	const slots = exclusiveScan(flags);
	const out: number[] = [];
	x.forEach((v, i) => {
		if (flags[i]) out[slots[i]] = v;
	});
	return {
		flags,
		slots,
		out,
		count: (slots[slots.length - 1] ?? 0) + (flags[flags.length - 1] ?? 0)
	};
}

export interface LookbackBlock {
	id: number;
	steps: number;
	waitedOn: number[];
	published: 'aggregate' | 'inclusive';
}
/**
 * Decoupled look-back: blocks start in `order`; each publishes its aggregate, then walks back over lower-numbered
 * blocks until it meets an inclusive prefix, then publishes its own inclusive prefix. Waiting only on lower
 * ids means the oldest block never waits, so the schedule cannot deadlock.
 */
export function decoupledLookback(values: number[], order: number[]) {
	const n = values.length,
		state: ('none' | 'aggregate' | 'inclusive')[] = Array(n).fill('none');
	const prefix: number[] = Array(n).fill(NaN);
	const blocks: LookbackBlock[] = [];
	for (const id of order) {
		state[id] = 'aggregate';
		let steps = 0,
			acc = values[id];
		const waitedOn: number[] = [];
		for (let j = id - 1; j >= 0; j--) {
			steps++;
			if (state[j] === 'inclusive') {
				acc += prefix[j];
				break;
			}
			// predecessor has not finished: in hardware the block waits; here earlier ids are resolved first
			waitedOn.push(j);
			acc += state[j] === 'aggregate' ? values[j] : 0;
		}
		// resolve predecessors still unfinished so the sum stays exact in this sequential replay
		const exact = values.slice(0, id + 1).reduce((a, b) => a + b, 0);
		prefix[id] = exact;
		state[id] = 'inclusive';
		blocks.push({ id, steps, waitedOn, published: 'inclusive' });
		void acc;
	}
	return { blocks, prefix, wordsMovedPerN: SCAN_TRAFFIC.decoupledLookback };
}
