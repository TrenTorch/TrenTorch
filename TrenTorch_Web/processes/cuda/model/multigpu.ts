// Collectives, topology, domain decomposition and scaling (chapters F4, F9).
import { copyTime } from './perf';

// ---- alpha-beta model ----
/** Ring AllReduce: 2(p-1) alpha + 2 (p-1)/p D / beta. */
export const ringAllReduce = (d: number, p: number, beta: number, alpha = 5e-6) => ({
	latency: 2 * (p - 1) * alpha,
	bandwidth: 2 * ((p - 1) / p) * (d / beta),
	total: 2 * (p - 1) * alpha + 2 * ((p - 1) / p) * (d / beta)
});
/** Tree AllReduce: 2 log2(p) alpha + c D / beta (c = 2 for the double binary tree). */
export const treeAllReduce = (d: number, p: number, beta: number, alpha = 5e-6, c = 2) => ({
	latency: 2 * Math.log2(p) * alpha,
	bandwidth: c * (d / beta),
	total: 2 * Math.log2(p) * alpha + c * (d / beta)
});
/** Message size at which ring and tree take equal time (tree wins below it): alpha beta p (p - 1 - log2 p) for c = 2. */
export const ringTreeCrossover = (p: number, beta: number, alpha = 5e-6) =>
	alpha * beta * p * (p - 1 - Math.log2(p));
/** Bytes each GPU sends in a ring AllReduce: 2 (p-1)/p D. */
export const ringBytesPerGpu = (d: number, p: number) => 2 * ((p - 1) / p) * d;
export const reduceScatterBytes = (d: number, p: number) => ((p - 1) / p) * d;
export const pcieVsNvlink = (d: number, p: number, pcie: number, nvlink: number) => ({
	pcie: ringAllReduce(d, p, pcie).bandwidth,
	nvlink: ringAllReduce(d, p, nvlink).bandwidth
});

// ---- peer-to-peer ----
/** Direct GPU-to-GPU copy versus staging through the host (two PCIe hops). */
export function p2pCopy(bytes: number, directBw: number, pcieBw: number) {
	const direct = bytes / directBw,
		staged = 2 * (bytes / pcieBw);
	return { direct, staged, speedup: staged / direct };
}

// ---- halo exchange ----
export const haloCells3D = (n: number, r: number) => 6 * r * n * n;
export const computeCells3D = (n: number) => n ** 3;
export const surfaceToVolume = (n: number, r: number) => (6 * r) / n;
export const haloBytes3D = (n: number, r: number, bytesPerCell = 4) =>
	haloCells3D(n, r) * bytesPerCell;
/** Global N^3 split among p GPUs: slab ratio 2 r p / N versus a 3-D block ratio 6 r p^(1/3) / N. */
export const slabRatio = (bigN: number, r: number, p: number) => (2 * r * p) / bigN;
export const blockRatio3D = (bigN: number, r: number, p: number) => (6 * r * Math.cbrt(p)) / bigN;
/** 2-D grid N x N on p GPUs: halo cells per GPU for slabs or near-square blocks. */
export function halo2D(bigN: number, p: number, r: number, how: 'slabs' | 'blocks') {
	if (how === 'slabs') return { halo: 2 * r * bigN, cells: (bigN * bigN) / p };
	const side = bigN / Math.sqrt(p);
	return { halo: 4 * r * side, cells: side * side };
}
export const iterationTime = (compute: number, comm: number, overlap: boolean) =>
	overlap ? Math.max(compute, comm) : compute + comm;
export const hiddenFraction = (interior: number, comm: number) =>
	comm === 0 ? 1 : Math.min(1, interior / comm);

// ---- scaling ----
export interface ScalingInputs {
	mode: 'strong' | 'weak';
	t1: number; // time on one GPU (seconds) of the parallel work
	serial: number; // serial time (seconds), not divided by p
	comm: (p: number) => number;
	overlap: boolean;
}
export function scalingPoint(i: ScalingInputs, p: number) {
	const par = i.mode === 'strong' ? i.t1 / p : i.t1;
	const comm = p === 1 ? 0 : i.comm(p);
	const tp = i.serial + (i.overlap ? Math.max(par, comm) : par + comm);
	const t1 = i.serial + i.t1;
	const speedup = i.mode === 'strong' ? t1 / tp : (p * t1) / tp;
	return {
		tp,
		speedup,
		efficiency: i.mode === 'strong' ? speedup / p : t1 / tp,
		commShare: comm / (par + comm || 1)
	};
}
export const strongScaling = (t1: number, tp: number, p: number) => ({
	speedup: t1 / tp,
	efficiency: t1 / tp / p
});
/** C = A x B with rows of A split over p GPUs and B replicated. */
export function matmulRowSplit(n: number, p: number, flopsPerSec: number, bcastBw: number) {
	const flops = 2 * (n / p) * n * n;
	return {
		flopsPerGpu: flops,
		computeSeconds: flops / flopsPerSec,
		bBytes: n * n * 4,
		bcastSeconds: (n * n * 4) / bcastBw
	};
}

// ---- topology ----
export type LinkType = 'NVLink' | 'PCIe' | 'Socket';
export interface Link {
	a: string;
	b: string;
	gbs: number;
	type: LinkType;
}
export interface Topology {
	name: string;
	gpus: number;
	nodes: string[];
	links: Link[];
	socketOf: (gpu: number) => number;
}
const gname = (i: number) => `GPU${i}`;
export function topologyPreset(id: 'nvswitch8' | 'mesh4' | 'pcie-tree8'): Topology {
	if (id === 'nvswitch8') {
		const links: Link[] = Array.from({ length: 8 }, (_, i) => ({
			a: gname(i),
			b: 'NVSwitch',
			gbs: 300,
			type: 'NVLink' as const
		}));
		return {
			name: '8 GPU, NVSwitch',
			gpus: 8,
			nodes: [...Array.from({ length: 8 }, (_, i) => gname(i)), 'NVSwitch'],
			links,
			socketOf: (g) => (g < 4 ? 0 : 1)
		};
	}
	if (id === 'mesh4') {
		const links: Link[] = [];
		for (let i = 0; i < 4; i++)
			for (let j = i + 1; j < 4; j++)
				links.push({ a: gname(i), b: gname(j), gbs: 100, type: 'NVLink' });
		return {
			name: '4 GPU, NVLink mesh',
			gpus: 4,
			nodes: Array.from({ length: 4 }, (_, i) => gname(i)),
			links,
			socketOf: () => 0
		};
	}
	const links: Link[] = [];
	for (let i = 0; i < 8; i++)
		links.push({ a: gname(i), b: `SW${Math.floor(i / 2)}`, gbs: 25, type: 'PCIe' });
	for (let s = 0; s < 4; s++)
		links.push({ a: `SW${s}`, b: `CPU${s < 2 ? 0 : 1}`, gbs: 25, type: 'PCIe' });
	// illustrative: effective GPU-to-GPU rate across the socket link, including staging through host memory
	links.push({ a: 'CPU0', b: 'CPU1', gbs: 2.5, type: 'Socket' });
	return {
		name: '8 GPU, PCIe tree on 2 sockets',
		gpus: 8,
		nodes: [
			...Array.from({ length: 8 }, (_, i) => gname(i)),
			'SW0',
			'SW1',
			'SW2',
			'SW3',
			'CPU0',
			'CPU1'
		],
		links,
		socketOf: (g) => (g < 4 ? 0 : 1)
	};
}
/** Fewest hops, then widest bottleneck. */
export function route(t: Topology, from: number, to: number) {
	const src = gname(from),
		dst = gname(to);
	if (from === to)
		return { path: [src], links: [] as Link[], hops: 0, bottleneckGBs: Infinity, code: 'X' };
	const best = new Map<
		string,
		{ hops: number; bw: number; prev: string | null; link: Link | null }
	>();
	best.set(src, { hops: 0, bw: Infinity, prev: null, link: null });
	const queue = [src];
	while (queue.length) {
		const u = queue.shift()!;
		const cu = best.get(u)!;
		for (const l of t.links) {
			const v = l.a === u ? l.b : l.b === u ? l.a : null;
			if (!v) continue;
			const cand = { hops: cu.hops + 1, bw: Math.min(cu.bw, l.gbs), prev: u, link: l };
			const cur = best.get(v);
			if (!cur || cand.hops < cur.hops || (cand.hops === cur.hops && cand.bw > cur.bw)) {
				best.set(v, cand);
				queue.push(v);
			}
		}
	}
	const path: string[] = [],
		links: Link[] = [];
	for (let n: string | null = dst; n; n = best.get(n)!.prev) {
		path.unshift(n);
		const l = best.get(n)!.link;
		if (l) links.unshift(l);
	}
	const bottleneckGBs = best.get(dst)!.bw;
	const code = links.every((l) => l.type === 'NVLink')
		? `NV${Math.max(1, Math.round(bottleneckGBs / 25))}`
		: links.some((l) => l.type === 'Socket')
			? 'SYS'
			: path.some((n) => n.startsWith('CPU'))
				? 'PHB'
				: 'PIX';
	return { path, links, hops: links.length, bottleneckGBs, code };
}
export const transferSeconds = (bytes: number, gbs: number) => copyTime(bytes, gbs * 1e9, 0);
