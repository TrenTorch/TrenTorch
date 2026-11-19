// Figures for part F: advanced topics, precision, launches and multi-GPU.
import * as m from '../model';
import {
	type Cell,
	type Frame,
	type Panel,
	type Row,
	type VizConfig,
	bool,
	fmt,
	fmtBytes,
	fmtTime,
	gpu,
	num,
	pct,
	range,
	select,
	str,
	toggle
} from './types';

const P = (s: Record<string, number | string | boolean>) =>
	m.getProfile(String(s.gpu) as m.GpuName);
const tint = (i: number) => (i % 5) as 0 | 1 | 2 | 3 | 4;
const lanes32 = (f: (i: number) => Cell): Cell[] => Array.from({ length: 32 }, (_, i) => f(i));

export const vizShuffleNetwork: VizConfig = {
	id: 'shuffle-network',
	title: 'Lanes passing notes',
	controls: [
		select('op', 'Intrinsic', [
			['reduce', 'Warp reduction (offsets 16, 8, 4, 2, 1)'],
			['down', 'shfl_down'],
			['xor', 'shfl_xor'],
			['bcast', 'shfl broadcast'],
			['ballot', 'ballot']
		]),
		range('arg', 'delta / mask / source lane', 0, 31, 1, 4),
		range('thr', 'ballot: lanes with value > t', 0, 32, 1, 16)
	],
	compute(s) {
		const x = Array.from({ length: 32 }, (_, i) => i + 1),
			op = str(s, 'op'),
			a = num(s, 'arg');
		const frame = (
			label: string,
			v: number[],
			caption: string,
			active?: (i: number) => boolean
		): Frame => ({
			rows: [
				{
					label,
					lanes: true,
					cells: lanes32((i) => ({
						text: String(v[i]),
						state: active ? (active(i) ? 'active' : 'masked') : 'active'
					}))
				}
			],
			caption
		});
		let frames: Frame[],
			note = '';
		if (op === 'reduce') {
			const st = m.warpReduceSteps(x);
			frames = st.map((v, i) =>
				frame(
					i ? `offset ${16 >> (i - 1)}` : 'input',
					v,
					i
						? `Offset ${16 >> (i - 1)}: lane i adds lane i + ${16 >> (i - 1)}; lanes past the end add their own value (greyed).`
						: 'Each lane holds one value.',
					i ? (l) => l + (16 >> (i - 1)) < 32 : undefined
				)
			);
			note = `After 5 steps lane 0 holds ${st[st.length - 1][0]} with no shared memory.`;
		} else if (op === 'down') {
			const v = m.shflDown(x, a);
			frames = [
				frame('input', x, 'Input.'),
				frame(
					`shfl_down ${a}`,
					v,
					`Lane i reads lane i + ${a}; lanes with i + ${a} >= 32 get their own value back.`,
					(l) => l + a < 32
				)
			];
		} else if (op === 'xor') {
			const v = m.shflXor(x, a);
			frames = [
				frame('input', x, 'Input.'),
				frame(`shfl_xor ${a}`, v, `Lane i reads lane i XOR ${a}: pairs swap.`)
			];
		} else if (op === 'bcast') {
			const v = m.shflBroadcast(x, a);
			frames = [
				frame('input', x, 'Input.'),
				frame(`shfl from lane ${a}`, v, `Every lane receives lane ${a}'s value.`)
			];
		} else {
			const thr = num(s, 'thr'),
				preds = x.map((v) => v > thr),
				mask = m.ballot(preds);
			frames = [
				frame('predicate (value > t)', x, `${m.popc(mask)} lanes vote yes.`, (l) => preds[l]),
				frame(
					'rank = popc(mask & lanemask_lt)',
					x.map((_, l) => (preds[l] ? m.ballotRank(mask, l) : -1)),
					'Each voting lane gets a dense rank: the basis of warp-level compaction.',
					(l) => preds[l]
				)
			];
			note = `ballot mask 0x${mask.toString(16).padStart(8, '0')}, popc ${m.popc(mask)}.`;
		}
		const bc = m.barrierCount(256);
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Steps', value: String(frames.length - 1) },
				{
					label: 'Barriers for a 256-thread sum',
					value: `${bc.sharedOnly} (shared only) vs ${bc.withShuffle} (shuffles)`
				},
				...(note ? [{ label: 'Result', value: note }] : [])
			],
			live: note || `${op}: lanes exchange register values directly, no shared memory.`
		};
	}
};

export const vizStreamTimeline: VizConfig = {
	id: 'stream-timeline',
	title: 'Overlap copies and compute',
	controls: [
		range('s', 'Chunks / streams', 1, 8, 1, 4),
		range('h', 'Copy in H (ms)', 1, 100, 1, 40),
		range('k', 'Compute K (ms)', 1, 100, 1, 10),
		range('d', 'Copy out D (ms)', 1, 100, 1, 40),
		toggle('pinned', 'Pinned memory', true),
		select('eng', 'Copy engines', ['2', '1'], '2')
	],
	compute(s) {
		const S = num(s, 's'),
			H = num(s, 'h'),
			K = num(s, 'k'),
			D = num(s, 'd'),
			pinned = bool(s, 'pinned'),
			eng = Number(str(s, 'eng')) as 1 | 2;
		const eff = pinned ? S : 1; // pageable copies cannot be asynchronous: no overlap
		const total = m.pipelineTime({ h: H, k: K, d: D, chunks: eff, copyEngines: eng }),
			one = m.serialTime(H, K, D),
			bound = H >= K && H >= D ? 'H2D copy' : D >= K ? 'D2H copy' : 'compute';
		const h = H / eff,
			k = K / eff,
			d = D / eff,
			TICK = Math.max(1, total / 48);
		const lane = (name: string, ivs: [number, number][]): Row => ({
			label: name,
			cells: Array.from({ length: 48 }, (_, t) => {
				const idx = ivs.findIndex(([a, b]) => t * TICK + TICK / 2 >= a && t * TICK + TICK / 2 < b);
				return {
					state: idx >= 0 ? ('active' as const) : ('idle' as const),
					tint: idx >= 0 ? tint(idx) : undefined,
					text: idx >= 0 ? String(idx + 1) : ''
				};
			})
		});
		const hi: [number, number][] = [],
			ci: [number, number][] = [],
			di: [number, number][] = [];
		let hEnd = 0,
			cEnd = 0,
			dEnd = 0;
		for (let i = 0; i < eff; i++) {
			hi.push([hEnd, hEnd + h]);
			hEnd += h;
			const cs = Math.max(hEnd, cEnd);
			ci.push([cs, cs + k]);
			cEnd = cs + k;
			const ds = Math.max(cEnd, dEnd, eng === 1 ? hEnd : 0);
			di.push([ds, ds + d]);
			dEnd = ds + d;
		}
		return {
			panels: [
				{
					kind: 'frames',
					title: 'Lanes over time (numbers are chunk ids)',
					frames: [
						{
							rows: [lane('H2D engine', hi), lane('Compute', ci), lane('D2H engine', di)],
							caption: pinned
								? `${S} chunks overlap across the three lanes.`
								: 'Pageable memory: the copy cannot run asynchronously, so there is no overlap.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Total', value: fmtTime(total / 1000) },
				{ label: 'Serial', value: fmtTime(one / 1000) },
				{
					label: 'Speed-up vs 1 stream',
					value: `${fmt(one / total)}x`,
					tone: one / total > 1.2 ? 'good' : 'neutral'
				},
				{ label: 'Lower bound max(H, K, D)', value: fmtTime(m.pipelineLowerBound(H, K, D) / 1000) },
				{ label: 'Bottleneck lane', value: bound }
			],
			live: `${pinned ? S : 1} chunk${eff === 1 ? '' : 's'}: ${fmtTime(total / 1000)} against ${fmtTime(one / 1000)} serial; the ${bound} is the bottleneck.`
		};
	}
};

const FUSIONS: Record<
	string,
	{ name: string; ops: string[]; unfused: (t: number) => number; fused: (t: number) => number }
> = {
	biasrelu: {
		name: 'bias + ReLU',
		ops: ['bias', 'ReLU'],
		unfused: (t) => 16 * t,
		fused: (t) => 8 * t
	},
	gemmgelu: {
		name: 'matmul + bias + GELU (output tensor)',
		ops: ['matmul', 'bias', 'GELU'],
		unfused: (t) => 20 * t,
		fused: (t) => 4 * t
	},
	softmax: {
		name: 'scale + mask + softmax',
		ops: ['scale', 'mask', 'softmax'],
		unfused: (t) => 24 * t,
		fused: (t) => 8 * t
	}
};
export const vizFusionTraffic: VizConfig = {
	id: 'fusion-traffic',
	title: 'Count the round trips',
	controls: [
		select(
			'preset',
			'Pipeline',
			Object.entries(FUSIONS).map(([k, v]) => [k, v.name] as [string, string])
		),
		toggle('fuse', 'Fuse', false),
		range('mb', 'Tensor size (MB of floats)', 1, 2048, 1, 64, { log: true }),
		range('n', 'Attention sequence length N', 256, 16384, 256, 4096),
		toggle('flash', 'Flash-style tiling', false),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const f = FUSIONS[str(s, 'preset')],
			T = (num(s, 'mb') * 1e6) / 4,
			fuse = bool(s, 'fuse'),
			p = P(s);
		const bytes = fuse ? f.fused(T) : f.unfused(T),
			un = f.unfused(T),
			t = bytes / (0.85 * m.peakBandwidth(p));
		const N = num(s, 'n'),
			att = m.standardAttentionTraffic(N, 64),
			fl = m.flashAttentionTraffic(N, 64, 128);
		return {
			panels: [
				{
					kind: 'frames',
					title: 'Pipeline',
					frames: [
						{
							rows: [
								{
									label: 'operations',
									cells: f.ops.map((o) => ({ text: o, state: 'active' as const }))
								},
								{
									label: fuse ? 'registers (no intermediate writes)' : 'global memory round trips',
									cells: Array.from({ length: fuse ? 2 : 2 * (f.ops.length - 1) + 2 }, (_, i) => ({
										text: fuse ? 'reg' : i % 2 ? 'write' : 'read',
										tint: fuse ? (0 as const) : (4 as const),
										state: 'idle' as const
									}))
								}
							],
							caption: fuse
								? 'Intermediate values stay in registers.'
								: 'Every operation reads its input from global memory and writes its output back.'
						}
					]
				},
				{
					kind: 'bars',
					title: 'Bytes moved',
					bars: [
						{ label: 'unfused', segments: [{ value: un, tone: 'memory' }], note: fmtBytes(un) },
						{
							label: fuse ? 'fused (selected)' : 'fused',
							segments: [{ value: f.fused(T), tone: 'good' }],
							note: fmtBytes(f.fused(T))
						}
					],
					max: un
				},
				{
					kind: 'bars',
					title: `Attention memory at N = ${N} (one head, FP32, d = 64)`,
					bars: [
						{
							label: 'stores the N x N matrix',
							segments: [{ value: att.total, tone: 'bad' }],
							note: fmtBytes(att.total)
						},
						{
							label: 'flash-style tiling',
							segments: [{ value: bool(s, 'flash') ? fl.total : fl.l2Resident, tone: 'good' }],
							note: fmtBytes(bool(s, 'flash') ? fl.total : fl.l2Resident)
						}
					]
				}
			],
			readouts: [
				{ label: 'Bytes moved', value: fmtBytes(bytes) },
				{ label: 'Estimated time', value: fmtTime(t) },
				{ label: 'Traffic saved', value: pct(1 - f.fused(T) / un), tone: 'good' },
				{ label: 'Score matrix S', value: fmtBytes(m.scoreMatrixBytes(N)) }
			],
			live: `${f.name}: ${fuse ? 'fused' : 'unfused'} moves ${fmtBytes(bytes)} (${pct(1 - f.fused(T) / un)} less when fused).`
		};
	}
};

export const vizFusionBreakeven: VizConfig = {
	id: 'fusion-breakeven',
	title: 'How much does fusion actually save?',
	controls: [
		select('roof', 'Roof', ['FP32', 'TF32', 'FP16'], 'FP32'),
		select(
			'size',
			'Matrix size',
			[
				['s', 'M = 512'],
				['m', 'M = 2,048 (F6 example)'],
				['l', 'M = 8,192']
			],
			'm'
		),
		toggle('fuse', 'Fuse the elementwise ops', false),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const p = P(s),
			roof = str(s, 'roof') as m.Roof,
			M = ({ s: 512, m: 2048, l: 8192 } as Record<string, number>)[str(s, 'size')],
			shape = { m: M, d: 1024, h: 4096 };
		const r = m.fusionShare(p, shape, m.roofFlops(p, roof)),
			fuse = bool(s, 'fuse'),
			tExtra = fuse ? 0 : r.tExtra;
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Time per step',
					bars: [
						{
							label: fuse ? 'fused' : 'unfused',
							segments: [
								{ value: r.tGemm, tone: 'compute', label: 'GEMM' },
								{ value: tExtra, tone: 'memory', label: 'elementwise traffic' }
							],
							note: fmtTime(r.tGemm + tExtra)
						}
					],
					max: r.tGemm + r.tExtra
				}
			],
			readouts: [
				{ label: 'GEMM time', value: fmtTime(r.tGemm) },
				{ label: 'Elementwise traffic', value: fmtTime(r.tExtra) },
				{
					label: 'Elementwise share of GEMM time',
					value: pct(r.share),
					tone: r.share > 0.2 ? 'bad' : 'good'
				}
			],
			live: `On the ${roof} roof the elementwise traffic is ${pct(r.share)} of the GEMM time: ${r.share > 0.2 ? 'fusion matters.' : 'fusion is a small win.'}`,
			footnote:
				'About 5% on FP32 and about 36% on TF32 for the F3 example (M = 2,048, d = 1,024, h = 4,096).'
		};
	}
};

export const vizRingAllreduce: VizConfig = {
	id: 'ring-allreduce',
	title: 'Pass it around the ring',
	controls: [
		range('p', 'GPUs', 2, 16, 1, 4),
		select('topo', 'Topology', [
			['ring', 'NVLink ring (300 GB/s)'],
			['nvswitch', 'NVSwitch mesh (300 GB/s)'],
			['pcie', 'PCIe tree (25 GB/s, 2.5 across sockets)']
		]),
		range('gb', 'Data size (MB)', 1, 4096, 1, 1024, { log: true }),
		toggle('skip', 'Skip rank 3', false)
	],
	compute(s) {
		const p = num(s, 'p'),
			topo = str(s, 'topo'),
			D = num(s, 'gb') * 1e6,
			skip = bool(s, 'skip') && p > 3;
		const beta = topo === 'pcie' ? (p > 4 ? 2.5e9 : 25e9) : 300e9;
		const state: number[][] = Array.from({ length: p }, (_, i) =>
			Array.from({ length: p }, () => i + 1)
		);
		const frames: Frame[] = [];
		const row = (st: number[][], hi: [number, number][] = []): Row[] =>
			st.map((chunks, i) => ({
				label: `GPU ${i}`,
				cells: chunks.map((v, c) => ({
					text: String(v),
					tint: tint(c),
					state: hi.some(([a, b]) => a === i && b === c) ? ('touch' as const) : ('idle' as const)
				}))
			}));
		frames.push({
			rows: row(state),
			caption: 'Every GPU holds p chunks; chunk values start as rank + 1.'
		});
		let st = state.map((r) => r.slice());
		for (let k = 0; k < p - 1; k++) {
			const next = st.map((r) => r.slice()),
				hi: [number, number][] = [];
			for (let i = 0; i < p; i++) {
				const c = (((i - k) % p) + p) % p,
					to = (i + 1) % p;
				next[to][c] = st[to][c] + st[i][c];
				hi.push([to, c]);
			}
			st = next;
			frames.push({
				rows: row(st, hi),
				caption:
					skip && k === 1
						? 'Rank 3 never sends: the others stall, waiting for rank 3.'
						: `Reduce-scatter step ${k + 1} of ${p - 1}: chunks hop one node and add into the receiver.`
			});
		}
		for (let k = 0; k < p - 1; k++) {
			const next = st.map((r) => r.slice()),
				hi: [number, number][] = [];
			for (let i = 0; i < p; i++) {
				const c = (((i + 1 - k) % p) + p) % p,
					to = (i + 1) % p;
				next[to][c] = st[i][c];
				hi.push([to, c]);
			}
			st = next;
			frames.push({
				rows: row(st, hi),
				caption: `All-gather step ${k + 1} of ${p - 1}: finished chunks hop around until every GPU holds the total ${st[0][0]}.`
			});
		}
		const t = m.ringAllReduce(D, p, beta);
		return {
			panels: [
				{ kind: 'frames', frames: skip ? frames.slice(0, 3) : frames },
				{
					kind: 'text',
					title: skip ? 'Failure: a rank did not participate' : '',
					text: skip
						? 'WAITING for rank 3. Every collective needs every rank; the others block forever. This is how real clusters hang.'
						: ''
				}
			],
			readouts: [
				{ label: 'Steps', value: `2(p-1) = ${2 * (p - 1)}` },
				{ label: 'Bytes per GPU', value: fmtBytes(m.ringBytesPerGpu(D, p)) },
				{ label: 'Estimated time', value: fmtTime(t.total) },
				{ label: 'Volume factor', value: `${fmt((2 * (p - 1)) / p, 3)} x D` }
			],
			live: `${p} GPUs: ${2 * (p - 1)} steps, ${fmtBytes(m.ringBytesPerGpu(D, p))} per GPU (about ${fmt((2 * (p - 1)) / p, 3)} times the data), ${fmtTime(t.total)} on this topology.`,
			footnote:
				'The PCIe tree uses 2.5 GB/s across the socket link as an illustrative effective rate.'
		};
	}
};

export const vizAlphaBeta: VizConfig = {
	id: 'alpha-beta',
	title: 'Ring or tree?',
	controls: [
		range('p', 'GPUs p', 2, 256, 1, 64, { log: true }),
		range('alpha', 'alpha (us)', 1, 50, 1, 5),
		range('beta', 'beta (GB/s)', 10, 900, 10, 300),
		range('msg', 'Message size (bytes)', 1e3, 1e10, 1, 1e8, {
			log: true,
			format: (v) => fmtBytes(v)
		})
	],
	compute(s) {
		const p = Math.round(num(s, 'p')),
			a = num(s, 'alpha') * 1e-6,
			b = num(s, 'beta') * 1e9,
			D = num(s, 'msg');
		const xs = Array.from({ length: 50 }, (_, i) => 10 ** (3 + (i * 7) / 49));
		const cross = m.ringTreeCrossover(p, b, a),
			ring = m.ringAllReduce(D, p, b, a).total,
			tree = m.treeAllReduce(D, p, b, a).total;
		return {
			panels: [
				{
					kind: 'line',
					title: 'AllReduce time against message size',
					xLabel: 'message size (bytes)',
					yLabel: 'seconds',
					xLog: true,
					yLog: true,
					series: [
						{
							name: 'ring',
							tone: 'compute',
							points: xs.map((x) => [x, m.ringAllReduce(x, p, b, a).total] as [number, number])
						},
						{
							name: 'tree',
							tone: 'memory',
							points: xs.map((x) => [x, m.treeAllReduce(x, p, b, a).total] as [number, number])
						}
					],
					markers:
						cross > 1e3 && cross < 1e10
							? [{ x: cross, label: `crossover ${fmtBytes(cross)}` }]
							: [],
					point: { x: D, y: Math.min(ring, tree), label: 'your message' }
				}
			],
			readouts: [
				{ label: 'T_ring', value: fmtTime(ring) },
				{ label: 'T_tree', value: fmtTime(tree) },
				{ label: 'Winner', value: ring < tree ? 'ring' : 'tree', tone: 'good' },
				{ label: 'Crossover', value: fmtBytes(cross) }
			],
			live: `At ${fmtBytes(D)} on ${p} GPUs the ${ring < tree ? 'ring' : 'tree'} wins: small messages are latency-bound (tree), large ones bandwidth-bound (ring).`
		};
	}
};

export const vizCapstonePipeline: VizConfig = {
	id: 'capstone-pipeline',
	title: 'Your block, end to end',
	controls: [
		select('fusion', 'Fusion level', [
			['none', 'None (5 kernels)'],
			['epilogue', 'Epilogue-fused (2 kernels)']
		]),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const p = P(s),
			shape = { m: 2048, d: 1024, h: 4096 },
			l = m.mlpLedger(shape),
			fused = str(s, 'fusion') === 'epilogue',
			bytes = fused ? l.fused : l.unfused;
		const tG = l.flops / (0.8 * m.peakFp32(p)),
			tMem = bytes / (0.85 * m.peakBandwidth(p));
		const nodes = fused
			? ['x', 'matmul + bias + GELU', 'h', 'matmul + bias + residual', 'y']
			: ['x', 'matmul', 'bias', 'GELU', 'matmul', 'bias + residual', 'y'];
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{
									label: 'dataflow',
									cells: nodes.map((n, i) => ({
										text: n,
										state: i % 2 ? ('active' as const) : ('idle' as const)
									}))
								},
								{
									label: fused ? 'global writes: h, y' : 'global writes after every kernel',
									cells: Array.from({ length: fused ? 2 : 5 }, () => ({
										text: 'write',
										tint: 4 as const
									}))
								}
							],
							caption: fused
								? 'The epilogue runs while the accumulator is in registers, so the intermediate write disappears.'
								: 'Each small kernel reads and writes the full tensor.'
						}
					]
				},
				{
					kind: 'table',
					header: ['Tensor', 'Size'],
					rows: [
						['x', fmtBytes(l.x)],
						['W1', fmtBytes(l.w1)],
						['h', fmtBytes(l.h)],
						['W2', fmtBytes(l.w2)],
						['y', fmtBytes(l.y)]
					]
				}
			],
			readouts: [
				{ label: 'Total bytes', value: fmtBytes(bytes) },
				{ label: 'FLOPs', value: `${fmt(l.flops / 1e9)} GFLOP` },
				{ label: 'GEMM time (FP32, eta 0.8)', value: fmtTime(tG) },
				{ label: 'Memory time', value: fmtTime(tMem) },
				{
					label: 'GEMMs are',
					value: l.flops / l.fused > m.machineBalance(p) ? 'compute-bound' : 'memory-bound',
					tone: 'good'
				},
				{ label: 'Extra traffic if unfused', value: fmtBytes(l.extraBytes) }
			],
			live: `${fused ? 'Fused' : 'Unfused'}: ${fmtBytes(bytes)} moved for ${fmt(l.flops / 1e9)} GFLOP; the GEMMs are compute-bound, the elementwise parts memory-bound.`,
			footnote:
				'Run your own kernels in the problem workspace; this figure shows the byte and FLOP ledger.'
		};
	}
};

const REPORT_FIELDS = [
	[
		'1',
		'Global memory',
		'16384 B read, 16384 B written, 1024 transactions (1024 ideal) -> coalescing 100%',
		'Bytes moved against the lower bound, and how many 32-byte sectors were used. Anything far above 1.0x or below 100% points at the access pattern (D1).'
	],
	[
		'2',
		'Shared memory',
		'4096 loads, 4096 stores, 0 bank-conflict replays',
		'Replays above 0 on a hot loop mean lanes collide on a bank (D5). Pad or swizzle.'
	],
	[
		'3',
		'Bank heat',
		'Banks 0..31 (words touched)',
		'Which banks are busy; a single hot bank is the signature of a column access.'
	],
	[
		'4',
		'Branches',
		'0 of 256 warp-level branches diverged',
		'Divergence in the main loop costs both paths (C1).'
	],
	[
		'5',
		'FLOPs and time',
		'FLOPs (static estimate): 0; modelled time 1.72 ms; occupancy 2%',
		'Compare modelled time with the roofline floor (D2, A5). Simulator times are a model, not a measurement.'
	],
	[
		'6',
		'Diagnostics',
		'No races, no out-of-bounds, no barrier misuse',
		'Any diagnostic here names the block and thread (F5, C2).'
	]
] as const;
export const vizAnnotatedReport: VizConfig = {
	id: 'annotated-report',
	title: 'Annotated report',
	controls: [
		select(
			'c',
			'Callout',
			REPORT_FIELDS.map((f) => [f[0], `${f[0]}  ${f[1]}`] as [string, string]),
			'1'
		)
	],
	compute(s) {
		const f = REPORT_FIELDS.find((x) => x[0] === str(s, 'c'))!;
		return {
			panels: [
				{
					kind: 'table',
					title: 'A simulator report (example)',
					header: ['#', 'Field', 'Value'],
					rows: REPORT_FIELDS.map((x) => [x[0], x[1], x[2]]),
					highlight: REPORT_FIELDS.indexOf(f)
				},
				{ kind: 'text', title: `What callout ${f[0]} tells you`, text: f[3] }
			],
			readouts: [],
			live: `Callout ${f[0]}, ${f[1]}: ${f[3]}`
		};
	}
};

export const vizLaunchOverhead: VizConfig = {
	id: 'launch-overhead',
	title: 'Gaps between kernels',
	controls: [
		range('n', 'Kernels', 1, 200, 1, 100, { log: true }),
		range('work', 'GPU time per kernel (us)', 1, 5000, 1, 5, { log: true }),
		range('ov', 'Launch overhead (us)', 1, 20, 1, 5),
		select('mode', 'Mode', [
			['ind', 'Individual launches'],
			['graph', 'CUDA graph'],
			['fused', 'Fused into one kernel']
		])
	],
	compute(s) {
		const n = Math.round(num(s, 'n')),
			w = num(s, 'work') * 1e-6,
			ov = num(s, 'ov') * 1e-6,
			mode = str(s, 'mode');
		const modes = {
			ind: m.launchOverhead(n, w, ov),
			graph: m.launchOverhead(n, w, 1e-6),
			fused: m.launchOverhead(1, n * w, ov)
		};
		const r = modes[mode as 'ind'],
			tot = mode === 'graph' ? n * (w + 1e-6) + ov : r.total;
		const cells: Cell[] = Array.from({ length: 40 }, (_, i) => ({
			state:
				mode === 'fused'
					? ('active' as const)
					: i % 2 === 0
						? ('active' as const)
						: ('masked' as const)
		}));
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [{ label: 'device lane', cells }],
							caption:
								mode === 'fused'
									? 'One launch: no gaps.'
									: 'Hatched cells are the launch gaps between kernels.'
						}
					]
				},
				{
					kind: 'bars',
					title: 'Total time',
					bars: (['ind', 'graph', 'fused'] as const).map((k) => ({
						label: k === 'ind' ? 'individual' : k,
						segments: [
							{
								value: k === 'graph' ? n * (w + 1e-6) + ov : modes[k].total,
								tone: k === mode ? ('compute' as const) : ('neutral' as const)
							}
						],
						note: fmtTime(k === 'graph' ? n * (w + 1e-6) + ov : modes[k].total)
					}))
				}
			],
			readouts: [
				{ label: 'Total', value: fmtTime(tot) },
				{
					label: 'Overhead share',
					value: pct(r.overheadShare),
					tone: r.overheadShare > 0.3 ? 'bad' : 'good'
				},
				{ label: 'GPU utilization', value: pct(r.utilization) }
			],
			live: `${n} kernels of ${fmtTime(w)}: ${mode} mode takes ${fmtTime(tot)} with ${pct(r.overheadShare)} overhead.`,
			footnote: 'Launch costs are approximate (about 3 to 10 us per launch).'
		};
	},
	illustrative: true
};

export const vizPrecisionLadder: VizConfig = {
	id: 'precision-ladder',
	title: 'Same sum, four formats',
	controls: [
		select('fmt', 'Format', Object.keys(m.FORMATS), 'FP16'),
		select('op', 'Operation', [
			['ones', 'Sum of N ones'],
			['dot', 'Dot product of K terms'],
			['softmax', 'Softmax of logits']
		]),
		select('acc', 'Accumulator precision', [
			['same', 'Same as the format'],
			['fp32', 'FP32']
		]),
		range('n', 'N / K / logit', 1, 1e5, 1, 100000, {
			log: true,
			format: (v) => Math.round(v).toLocaleString('en-US')
		})
	],
	compute(s) {
		const f = m.FORMATS[str(s, 'fmt')],
			op = str(s, 'op'),
			N = Math.round(num(s, 'n')),
			wide = str(s, 'acc') === 'fp32';
		const tableRows = Object.values(m.FORMATS).map((x) => [
			x.name,
			`${x.expBits} exp / ${x.mantBits} mantissa`,
			m.unitRoundoff(x).toExponential(1),
			x.maxFinite.toExponential(2)
		]);
		let result: string, truth: string, err: number;
		if (op === 'ones') {
			const stall = m.sequentialStall(f),
				got = wide ? Math.min(N, m.sequentialStall(m.FORMATS.FP32)) : Math.min(N, stall);
			result = got.toLocaleString('en-US');
			truth = N.toLocaleString('en-US');
			err = Math.abs(got - N) / N;
		} else if (op === 'dot') {
			err = wide ? m.dotErrorFp32Accum(N, f) : m.dotErrorLowAccum(N, f);
			result = `relative error up to ${err.toExponential(1)}`;
			truth = 'exact';
		} else {
			const lim = m.expOverflowLogit(f);
			result = N > lim ? `exp(${N}) overflows (limit ${fmt(lim)})` : `exp(${N}) is finite`;
			truth = `exp(${N}) = ${N < 700 ? Math.exp(N).toExponential(2) : 'huge'}`;
			err = N > lim ? 1 : 0;
		}
		const near = op === 'ones' ? Math.min(N, wide ? 16777216 : m.sequentialStall(f)) : 1000,
			sp = m.spacingAt(near, wide ? m.FORMATS.FP32 : f);
		return {
			panels: [
				{
					kind: 'frames',
					title: 'Representable values near the running total',
					frames: [
						{
							rows: [
								{
									label: 'number line',
									cells: Array.from({ length: 12 }, (_, i) => {
										const v = near - 4 * sp + i * sp;
										return {
											text: String(Number(v.toPrecision(8))),
											state: Math.abs(v - near) < sp / 2 ? ('touch' as const) : ('idle' as const),
											tint: 4 as const
										};
									})
								}
							],
							caption: `Spacing near ${Number(near.toPrecision(5)).toLocaleString('en-US')} is ${sp}.`
						}
					]
				},
				{
					kind: 'table',
					title: 'Formats',
					header: ['Format', 'Layout', 'Unit roundoff', 'Max finite'],
					rows: tableRows
				}
			],
			readouts: [
				{ label: 'Result', value: result, tone: err > 0.01 ? 'bad' : 'good' },
				{ label: 'True value', value: truth },
				{ label: 'Relative error', value: err ? err.toExponential(1) : '0' },
				{ label: 'Bytes moved (N elements)', value: fmtBytes(m.bytesFor(N, f)) }
			],
			live: `${f.name}${wide ? ' with an FP32 accumulator' : ''}: ${result}.${op === 'ones' && !wide ? ` A sequential sum of ones stops at ${m.sequentialStall(f).toLocaleString('en-US')}.` : ''}`
		};
	}
};

const TOPOS = [
	['nvswitch8', '8 GPU, NVSwitch'],
	['mesh4', '4 GPU, NVLink mesh'],
	['pcie-tree8', '8 GPU, PCIe tree on 2 sockets']
] as const;
export const vizMultigpuTopology: VizConfig = {
	id: 'multigpu-topology',
	title: 'Who can talk to whom?',
	controls: [
		select(
			'topo',
			'Topology',
			TOPOS.map((t) => [t[0], t[1]] as [string, string])
		),
		range('src', 'Source GPU', 0, 7, 1, 0),
		range('dst', 'Destination GPU', 0, 7, 1, 5),
		range('mb', 'Data size (MB)', 1, 8192, 1, 1024, { log: true }),
		toggle('matrix', 'Show topo matrix', false)
	],
	compute(s) {
		const t = m.topologyPreset(str(s, 'topo') as 'nvswitch8'),
			src = Math.min(num(s, 'src'), t.gpus - 1),
			dst = Math.min(num(s, 'dst'), t.gpus - 1),
			r = m.route(t, src, dst),
			D = num(s, 'mb') * 1e6;
		const secs = r.bottleneckGBs === Infinity ? 0 : m.transferSeconds(D, r.bottleneckGBs);
		const panels: Panel[] = [
			{
				kind: 'frames',
				frames: [
					{
						rows: [
							{
								label: `path ${src} to ${dst}`,
								cells: r.path.map((n, i) => ({
									text: n,
									state:
										i === 0 || i === r.path.length - 1 ? ('active' as const) : ('touch' as const)
								}))
							},
							{
								label: 'link bandwidth (GB/s)',
								cells: r.links.map((l) => ({
									text: `${l.gbs}`,
									state: l.gbs === r.bottleneckGBs ? ('error' as const) : ('done' as const),
									title: `${l.type} ${l.a}-${l.b}${l.gbs === r.bottleneckGBs ? ' (bottleneck)' : ''}`
								}))
							}
						],
						caption: r.hops ? `Slowest hop outlined in red: ${r.bottleneckGBs} GB/s.` : 'Same GPU.'
					}
				]
			}
		];
		if (bool(s, 'matrix'))
			panels.push({
				kind: 'table',
				title: 'nvidia-smi topo -m (model)',
				header: ['', ...Array.from({ length: t.gpus }, (_, i) => `G${i}`)],
				rows: Array.from({ length: t.gpus }, (_, a) => [
					`G${a}`,
					...Array.from({ length: t.gpus }, (_, b) => m.route(t, a, b).code)
				])
			});
		return {
			panels,
			readouts: [
				{ label: 'Hops', value: String(r.hops) },
				{
					label: 'Bottleneck',
					value: `${r.bottleneckGBs === Infinity ? '-' : r.bottleneckGBs} GB/s`
				},
				{ label: `Time for ${fmtBytes(D)}`, value: fmtTime(secs) },
				{ label: 'Code', value: r.code }
			],
			live: `GPU ${src} to GPU ${dst}: ${r.hops} hop${r.hops === 1 ? '' : 's'}, bottleneck ${r.bottleneckGBs} GB/s (${r.code}). ${fmtBytes(D)} takes ${fmtTime(secs)}.`,
			footnote:
				'Link rates are published or approximate; the cross-socket rate on the PCIe tree is illustrative.'
		};
	},
	illustrative: true
};

export const vizP2pAccess: VizConfig = {
	id: 'p2p-access',
	title: 'Direct or via the host?',
	controls: [
		toggle('e01', 'Peer access enabled (0 to 1)', false),
		toggle('e10', 'Peer access enabled (1 to 0)', false),
		select('kernel', 'Kernel', [
			['none', 'No kernel'],
			['0r1', 'Kernel on GPU 0 reads GPU 1 memory'],
			['1r0', 'Kernel on GPU 1 reads GPU 0 memory']
		]),
		range('mb', 'Copy size (MB)', 1, 8192, 1, 1024, { log: true }),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const p = P(s),
			D = num(s, 'mb') * 1e6,
			direct = bool(s, 'e01') || bool(s, 'e10'),
			c = m.p2pCopy(D, Math.max(1, p.nvlinkGBsPerDirection || p.pcieGBs) * 1e9, p.pcieGBs * 1e9),
			k = str(s, 'kernel');
		const ok = k === '0r1' ? bool(s, 'e01') : k === '1r0' ? bool(s, 'e10') : true;
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{
									label: 'copy GPU 1 to GPU 0',
									cells: direct
										? [
												{ text: 'GPU 1', state: 'active' },
												{ text: 'link', state: 'touch' },
												{ text: 'GPU 0', state: 'active' }
											]
										: [
												{ text: 'GPU 1', state: 'active' },
												{ text: 'PCIe', state: 'touch' },
												{ text: 'host', state: 'masked' },
												{ text: 'PCIe', state: 'touch' },
												{ text: 'GPU 0', state: 'active' }
											]
								},
								...(k !== 'none'
									? [
											{
												label: 'kernel access',
												cells: [
													{
														text: ok ? 'reads over the link' : 'illegal access',
														state: ok ? ('done' as const) : ('error' as const)
													}
												]
											}
										]
									: [])
							],
							caption: 'cudaDeviceEnablePeerAccess(peer, 0) is one-directional.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Hops', value: direct ? '1 (direct)' : '2 (via host)' },
				{ label: 'Copy time', value: fmtTime(direct ? c.direct : c.staged) },
				{
					label: 'Direct vs staged',
					value: `${fmt(c.speedup)}x faster`,
					tone: direct ? 'good' : 'bad'
				},
				...(k !== 'none'
					? [
							{
								label: 'Kernel read',
								value: ok ? 'OK' : 'ILLEGAL ACCESS',
								tone: ok ? ('good' as const) : ('bad' as const)
							}
						]
					: [])
			],
			live: `${direct ? 'Direct copy' : 'Staged through the host'}: ${fmtTime(direct ? c.direct : c.staged)}. ${k !== 'none' ? (ok ? 'The kernel read works.' : 'The kernel read fails: peer access is not enabled in that direction.') : ''}`
		};
	}
};

export const vizDeviceContext: VizConfig = {
	id: 'device-context',
	title: 'Which GPU is current?',
	controls: [
		toggle('set', 'Call cudaSetDevice before each allocation', false),
		range('bufs', 'Number of buffers', 1, 16, 1, 8),
		range('gb', 'Buffer size (GB)', 1, 20, 1, 12),
		gpu('gpu', 'Profile (memory)', 'A100'),
		range('step', 'Step', 0, 16, 1, 16)
	],
	compute(s) {
		const set = bool(s, 'set'),
			n = num(s, 'bufs'),
			gb = num(s, 'gb'),
			cap = 80,
			steps = Math.min(num(s, 'step'), n);
		const used = [0, 0, 0, 0];
		let oom = -1;
		const cur: number[] = [];
		for (let i = 0; i < steps; i++) {
			const dev = set ? i % 4 : 0;
			cur.push(dev);
			if (used[dev] + gb > cap && oom < 0) oom = i;
			else used[dev] += gb;
		}
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{
									label: 'host thread: current device',
									cells: cur.map((d, i) => ({
										text: `${i}: GPU ${d}`,
										state: i === oom ? ('error' as const) : ('active' as const)
									}))
								},
								{
									label: 'GPU memory (GB used of 80)',
									cells: used.map((u, g) => ({
										text: `GPU ${g}: ${u}`,
										state:
											u + gb > cap && g === 0 && !set && oom >= 0
												? ('error' as const)
												: u > 0
													? ('active' as const)
													: ('idle' as const),
										tint: 4 as const
									}))
								}
							],
							caption: set
								? 'cudaSetDevice(d) before each allocation spreads the buffers.'
								: 'Without cudaSetDevice every allocation lands on GPU 0.'
						}
					]
				}
			],
			readouts: [
				{
					label: 'Result',
					value: oom >= 0 ? `GPU 0 out of memory at buffer ${oom}` : 'all allocations fit',
					tone: oom >= 0 ? 'bad' : 'good'
				},
				{ label: 'Used per GPU', value: used.join(' / ') + ' GB' }
			],
			live:
				oom >= 0
					? `Buffer ${oom} does not fit on GPU 0 while GPUs 1 to 3 sit empty: the current device is state on the calling thread.`
					: `${steps} buffers fit; usage per GPU is ${used.join(', ')} GB.`
		};
	}
};

export const vizHaloExchange: VizConfig = {
	id: 'halo-exchange',
	title: 'Cut the grid, pay the border',
	controls: [
		select('how', 'Decomposition', [
			['slabs', '1D slabs'],
			['blocks', '2D blocks']
		]),
		range('p', 'GPUs', 2, 16, 1, 4),
		range('r', 'Stencil radius r', 1, 4, 1, 1),
		select('link', 'Link', [
			['nvlink', 'NVLink (300 GB/s)'],
			['pcie', 'PCIe (25 GB/s)']
		]),
		toggle('overlap', 'Overlap comm with compute', false),
		range('n', 'Grid N x N', 256, 16384, 256, 4096)
	],
	compute(s) {
		const how = str(s, 'how') as 'slabs' | 'blocks',
			p = num(s, 'p'),
			r = num(s, 'r'),
			N = num(s, 'n'),
			bw = (str(s, 'link') === 'nvlink' ? 300 : 25) * 1e9;
		const h = m.halo2D(N, p, r, how),
			ratio = h.halo / h.cells,
			comm = (h.halo * 4) / bw,
			comp = (2 * h.cells * 4) / (0.85 * 2039e9),
			interior = comp,
			it = m.iterationTime(comp, comm, bool(s, 'overlap'));
		const grid = 24,
			cols = how === 'slabs' ? p : Math.ceil(Math.sqrt(p)),
			rowsN = how === 'slabs' ? 1 : Math.ceil(p / cols);
		const cells: Row[] = Array.from({ length: grid }, (_, y) => ({
			label: '',
			cells: Array.from({ length: grid }, (_, x) => {
				const tx = Math.min(cols - 1, Math.floor((x * cols) / grid)),
					ty = Math.min(rowsN - 1, Math.floor((y * rowsN) / grid));
				const edge =
					how === 'slabs'
						? x % Math.ceil(grid / cols) <= 0 ||
							x % Math.ceil(grid / cols) >= Math.ceil(grid / cols) - 1
						: x % Math.ceil(grid / cols) <= 0 ||
							x % Math.ceil(grid / cols) >= Math.ceil(grid / cols) - 1 ||
							y % Math.ceil(grid / rowsN) <= 0 ||
							y % Math.ceil(grid / rowsN) >= Math.ceil(grid / rowsN) - 1;
				return { tint: tint(ty * cols + tx), state: edge ? ('touch' as const) : ('idle' as const) };
			})
		}));
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: cells,
							caption:
								'Colours are GPUs; outlined cells are the halo borders that must be exchanged.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Compute cells / GPU', value: Math.round(h.cells).toLocaleString('en-US') },
				{ label: 'Halo cells / GPU', value: Math.round(h.halo).toLocaleString('en-US') },
				{ label: 'Surface-to-volume', value: pct(ratio), tone: ratio > 0.05 ? 'bad' : 'good' },
				{ label: 'Time / iteration', value: fmtTime(it) },
				{
					label: 'Comm hidden',
					value: pct(bool(s, 'overlap') ? m.hiddenFraction(interior, comm) : 0)
				}
			],
			live: `${how === 'slabs' ? '1D slabs' : '2D blocks'} on ${p} GPUs: halo is ${pct(ratio)} of the compute cells; an iteration takes ${fmtTime(it)}${bool(s, 'overlap') ? ' with communication overlapped' : ''}.`
		};
	}
};

export const vizScalingCurve: VizConfig = {
	id: 'scaling-curve',
	title: 'Where does scaling bend?',
	controls: [
		select('mode', 'Mode', ['strong', 'weak']),
		range('serial', 'Serial fraction', 0, 0.2, 0.005, 0.02),
		select(
			'comm',
			'Communication',
			[
				['none', 'none'],
				['const', 'constant AllReduce (5.8 ms)'],
				['ring', 'ring AllReduce, alpha-beta']
			],
			'const'
		),
		select('link', 'Link', [
			['nvlink', 'NVLink (300 GB/s)'],
			['pcie', 'PCIe (25 GB/s)']
		]),
		toggle('overlap', 'Overlap', false),
		range('sel', 'GPUs to read off', 1, 64, 1, 8)
	],
	compute(s) {
		const T1 = 100,
			ser = num(s, 'serial') * T1,
			bw = (str(s, 'link') === 'nvlink' ? 300 : 25) * 1e9,
			kind = str(s, 'comm');
		const comm = (p: number) =>
			kind === 'none' ? 0 : kind === 'const' ? 5.8 : m.ringAllReduce(1e9, p, bw).total * 1000;
		const inp = {
			mode: str(s, 'mode') as 'strong',
			t1: T1 - ser,
			serial: ser,
			comm,
			overlap: bool(s, 'overlap')
		};
		const ps = Array.from({ length: 64 }, (_, i) => i + 1),
			pts = ps.map((p) => ({ p, ...m.scalingPoint(inp, p) }));
		const sel = pts[Math.min(num(s, 'sel'), 64) - 1],
			bend = pts.find((x) => x.efficiency < 0.8);
		return {
			panels: [
				{
					kind: 'line',
					title: 'Speed-up against GPUs',
					xLabel: 'GPUs',
					yLabel: 'speed-up',
					series: [
						{
							name: 'ideal',
							tone: 'neutral',
							dashed: true,
							points: ps.map((p) => [p, p] as [number, number])
						},
						{
							name: 'model',
							tone: 'compute',
							points: pts.map((x) => [x.p, x.speedup] as [number, number])
						}
					],
					markers: bend ? [{ x: bend.p, label: `<80% at ${bend.p}` }] : [],
					point: { x: sel.p, y: sel.speedup, label: 'selected' }
				},
				{
					kind: 'line',
					title: 'Efficiency',
					xLabel: 'GPUs',
					yLabel: 'efficiency',
					yMax: 1.05,
					series: [
						{
							name: 'efficiency',
							tone: 'memory',
							points: pts.map((x) => [x.p, x.efficiency] as [number, number])
						}
					]
				}
			],
			readouts: [
				{ label: 'Speed-up', value: `${fmt(sel.speedup)}x` },
				{
					label: 'Efficiency',
					value: pct(sel.efficiency),
					tone: sel.efficiency < 0.8 ? 'bad' : 'good'
				},
				{ label: 'Comm share of step', value: pct(sel.commShare) },
				{ label: 'Efficiency < 80% from', value: bend ? `${bend.p} GPUs` : 'never (up to 64)' }
			],
			live: `At ${sel.p} GPUs the ${str(s, 'mode')} speed-up is ${fmt(sel.speedup)}x (${pct(sel.efficiency)} efficiency).`,
			footnote: 'Teaching model: T_p = T_serial + T_parallel / p + T_comm(p).'
		};
	},
	illustrative: true
};

export const partFG: VizConfig[] = [
	vizShuffleNetwork,
	vizStreamTimeline,
	vizFusionTraffic,
	vizFusionBreakeven,
	vizRingAllreduce,
	vizAlphaBeta,
	vizCapstonePipeline,
	vizAnnotatedReport,
	vizLaunchOverhead,
	vizPrecisionLadder,
	vizMultigpuTopology,
	vizP2pAccess,
	vizDeviceContext,
	vizHaloExchange,
	vizScalingCurve
];
