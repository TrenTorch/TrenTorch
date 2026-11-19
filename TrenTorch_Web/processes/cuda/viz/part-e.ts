// Figures for part E: parallel patterns.
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
const nums = (a: number[], state?: Cell['state']): Cell[] =>
	a.map((v) => ({ text: String(v), state }));

const MAPS: Record<string, { name: string; flops: number }> = {
	relu: { name: 'ReLU', flops: 1 },
	sigmoid: { name: 'Sigmoid', flops: 40 },
	gelu: { name: 'GELU', flops: 60 }
};
export const vizMapFlow: VizConfig = {
	id: 'map-flow',
	title: 'One thread, one element',
	controls: [
		range('n', 'N', 8, 64, 1, 20),
		range('b', 'Block size', 4, 32, 4, 8),
		select('mode', 'Mode', [
			['per', 'One thread per element'],
			['stride', 'Grid-stride loop, fixed grid']
		]),
		select(
			'fn',
			'Function',
			Object.entries(MAPS).map(([k, v]) => [k, v.name] as [string, string])
		),
		gpu('gpu', 'Profile', 'A100'),
		range('step', 'Step (stride mode)', 0, 7, 1, 7)
	],
	compute(s) {
		const N = num(s, 'n'),
			B = num(s, 'b'),
			stride = str(s, 'mode') === 'stride',
			p = P(s),
			f = MAPS[str(s, 'fn')];
		const gridBlocks = stride ? Math.max(1, Math.ceil(N / B / 3)) : Math.ceil(N / B),
			T = gridBlocks * B,
			passes = Math.ceil(N / T),
			step = Math.min(num(s, 'step'), passes - 1);
		const input: Cell[] = Array.from({ length: N }, (_, i) => ({
			text: String(i),
			state: stride ? (i < (step + 1) * T ? 'touch' : 'idle') : 'touch',
			tint: tint(i % T)
		}));
		const threads: Row = {
			label: `${T} threads in ${gridBlocks} blocks`,
			cells: Array.from({ length: T }, (_, t) => ({
				text: String(t),
				state: stride
					? t < N
						? ('active' as const)
						: ('masked' as const)
					: t < N
						? ('active' as const)
						: ('masked' as const),
				tint: tint(Math.floor(t / 32))
			}))
		};
		const bytes = 8 * N,
			flops = f.flops * N,
			ai = flops / bytes,
			ridge = m.machineBalance(p);
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{ label: 'input', cells: input },
								threads,
								{ label: 'output', cells: input.map((c) => ({ ...c, state: 'done' as const })) }
							],
							caption: stride
								? `Grid-stride: each thread loops ${passes} time${passes === 1 ? '' : 's'}; step ${step + 1} of ${passes} lit.`
								: `One wave: ${N} threads work, ${T - N} tail threads are idle (hatched).`
						}
					]
				},
				...(stride
					? [
							{
								kind: 'text',
								text: `Resident capacity C = ${m.residentCapacity(p, 8)} blocks on this profile (SMs x 8 blocks per SM): a real grid-stride launch uses exactly C blocks.`
							} as Panel
						]
					: [])
			],
			readouts: [
				{ label: 'Bytes moved', value: `8N = ${bytes}` },
				{ label: 'FLOPs', value: String(flops) },
				{ label: 'AI', value: `${fmt(ai)} FLOP/B` },
				{ label: 'Bound', value: ai < ridge ? 'memory' : 'compute', tone: 'bad' },
				{ label: 'Threads', value: String(T) }
			],
			live: `${stride ? 'Grid-stride loop' : 'One thread per element'}: ${T} threads, same output as the other mode. ${f.name} is ${ai < ridge ? 'memory' : 'compute'}-bound on this profile.`
		};
	}
};

export const vizReductionTree: VizConfig = {
	id: 'reduction-tree',
	title: 'Fold the array in half',
	controls: [
		select(
			'v',
			'Variant',
			Object.entries(m.REDUCTION_VARIANTS).map(([k, v]) => [k, `${k}. ${v}`] as [string, string]),
			'3'
		),
		select('n', 'N', ['16', '32', '64', '256'], '32'),
		toggle('banks', 'Show bank numbers', false)
	],
	compute(s) {
		const n = Number(str(s, 'n')),
			v = Number(str(s, 'v')) as m.ReductionVariant,
			tr = m.reduceTrace(
				v,
				Array.from({ length: n }, (_, i) => i + 1)
			);
		const cap = 64;
		const frames: Frame[] = tr.steps.map((st) => ({
			rows: [
				{
					label: `${st.label}`,
					lanes: n <= 32 || true,
					cells: st.active.slice(0, cap).map((on, t) => ({
						text: bool(s, 'banks') ? `b${t % 32}` : String(st.values[t] ?? ''),
						state: on
							? st.bankDegree > 1
								? ('error' as const)
								: ('active' as const)
							: ('masked' as const),
						title: `thread ${t}${on ? ' active' : ' idle'}`
					}))
				}
			],
			caption: `${st.label}: ${st.active.filter(Boolean).length} of ${st.active.length} threads active${st.bankDegree > 1 ? `; ${st.bankDegree}-way bank conflict` : ''}${st.shuffle ? ' (register shuffle, no shared memory)' : ''}${st.barrier ? '; barrier' : ''}.`
		}));
		const lanes = tr.steps.map((st) => st.active.filter(Boolean).length);
		return {
			panels: [
				{ kind: 'frames', frames },
				{
					kind: 'bars',
					title: 'Active threads per step (the lane-activity graph)',
					bars: lanes.map((c, i) => ({
						label: tr.steps[i].label,
						segments: [{ value: c, tone: 'compute' as const }],
						note: String(c)
					})),
					max: Math.max(...lanes)
				}
			],
			readouts: [
				{ label: 'Steps', value: String(tr.steps.length) },
				{
					label: 'Warp efficiency',
					value: pct(tr.warpEfficiency),
					tone: tr.warpEfficiency < 0.5 ? 'bad' : 'good'
				},
				{
					label: 'Bank conflict cycles',
					value: String(tr.bankConflictCycles),
					tone: tr.bankConflictCycles ? 'bad' : 'good'
				},
				{ label: 'Barriers', value: String(tr.barriers) },
				{ label: 'Sum', value: String(tr.result) }
			],
			live: `Variant ${v}: ${tr.steps.length} steps, warp efficiency ${pct(tr.warpEfficiency)}, ${tr.bankConflictCycles} bank-conflict cycles, ${tr.barriers} barriers; the sum is ${tr.result} for every variant.`
		};
	}
};

export const vizFloatAccumulation: VizConfig = {
	id: 'float-accumulation',
	title: 'Sum of ones',
	controls: [
		select('how', 'Accumulation', [
			['sequential', 'Sequential'],
			['tree', 'Tree (pairwise)'],
			['kahan', 'Kahan']
		]),
		select('fmt', 'Format', ['FP32', 'FP16']),
		range('n', 'N', 100, 1e8, 1, 100000, {
			log: true,
			format: (v) => Math.round(v).toLocaleString('en-US')
		})
	],
	compute(s) {
		const f = m.FORMATS[str(s, 'fmt')],
			N = Math.round(num(s, 'n')),
			how = str(s, 'how') as m.Accumulation;
		const stall = m.sequentialStall(f);
		const result =
			how === 'sequential'
				? Math.min(N, stall)
				: N <= 2_000_000
					? m.sumOfOnes(N, f, how)
					: how === 'tree'
						? f.name === 'FP16' && N > f.maxFinite
							? Infinity
							: N
						: N;
		const rel = Number.isFinite(result) ? Math.abs(result - N) / N : 1;
		const near = Math.min(result, 1e9),
			sp = m.spacingAt(near, f);
		const cells: Cell[] = Array.from({ length: 12 }, (_, i) => {
			const v = near - 4 * sp + i * sp;
			return {
				text: String(Number(v.toPrecision(8))),
				state: Math.abs(v - near) < sp / 2 ? ('touch' as const) : ('idle' as const),
				tint: 4 as const
			};
		});
		return {
			panels: [
				{
					kind: 'frames',
					title: `Representable ${f.name} values near the running total`,
					frames: [
						{
							rows: [{ label: 'number line', cells }],
							caption: `Spacing near ${Number(near.toPrecision(6)).toLocaleString('en-US')} is ${sp}: adding 1 ${sp > 1 ? 'rounds back to the same value, so a sequential sum stalls' : 'changes the value'}.`
						}
					]
				}
			],
			readouts: [
				{
					label: 'Result',
					value: Number.isFinite(result) ? result.toLocaleString('en-US') : 'overflow (infinity)',
					tone: rel > 0.01 ? 'bad' : 'good'
				},
				{ label: 'Exact', value: N.toLocaleString('en-US') },
				{ label: 'Relative error', value: pct(rel), tone: rel > 0.01 ? 'bad' : 'good' },
				{ label: 'Sequential stalls at', value: stall.toLocaleString('en-US') }
			],
			live: `${how} accumulation of ${N.toLocaleString('en-US')} ones in ${f.name} gives ${Number.isFinite(result) ? result.toLocaleString('en-US') : 'infinity'}; ${f.name} stalls a sequential sum at ${stall.toLocaleString('en-US')}.`,
			footnote:
				N > 2_000_000
					? 'For N above 2 million the tree and Kahan results are extrapolated from the exact power-of-two behaviour.'
					: undefined
		};
	}
};

export const vizRowwiseSoftmax: VizConfig = {
	id: 'rowwise-softmax',
	title: 'One block per row',
	controls: [
		select('mode', 'Mode', [
			['stable', '3-pass stable'],
			['naive', 'Naive (unstable)'],
			['online', 'Online, 1 pass']
		]),
		range('scale', 'Logit scale', 1, 100, 1, 1),
		range('c', 'Row length C', 8, 4096, 8, 16, { log: true })
	],
	compute(s) {
		const mode = str(s, 'mode'),
			sc = num(s, 'scale'),
			C = Math.round(num(s, 'c')),
			row = Array.from({ length: 16 }, (_, i) => (Math.sin(i * 1.7) * 3 + (i % 5)) * sc);
		const f32 = Math.fround,
			ref = m.softmaxProbs(row);
		let out: number[], passes: number;
		if (mode === 'naive') {
			const e = row.map((x) => f32(Math.exp(x))),
				d = e.reduce((a, b) => f32(a + b), 0);
			out = e.map((v) => f32(v > 3.4e38 ? Infinity : v) / d);
			passes = 2;
		} else if (mode === 'online') {
			let st = { m: -Infinity, d: 0 };
			for (const x of row) st = m.mergeSoftmax(st.d === 0 ? { m: x, d: 0 } : st, { m: x, d: 1 });
			out = row.map((x) => Math.exp(x - st.m) / st.d);
			passes = 1;
		} else {
			const mx = Math.max(...row),
				e = row.map((x) => Math.exp(x - mx)),
				d = e.reduce((a, b) => a + b, 0);
			out = e.map((v) => v / d);
			passes = 3;
		}
		const err = Math.max(...out.map((o, i) => (Number.isNaN(o) ? Infinity : Math.abs(o - ref[i]))));
		const bytesRead = passes * 4 * C;
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{ label: 'logits x', cells: row.map((x) => ({ text: fmt(x, 3) })) },
								{
									label: mode === 'naive' ? 'exp(x)' : 'exp(x - max)',
									cells: row.map((x) => {
										const e = mode === 'naive' ? Math.exp(x) : Math.exp(x - Math.max(...row));
										return {
											text: e > 3.4e38 ? 'inf' : fmt(e, 3),
											state: e > 3.4e38 ? ('error' as const) : ('idle' as const)
										};
									})
								},
								{
									label: 'output',
									cells: out.map((o) => ({
										text: Number.isNaN(o) ? 'NaN' : fmt(o, 3),
										state: Number.isNaN(o) ? ('error' as const) : ('done' as const)
									}))
								}
							],
							caption:
								mode === 'naive' && out.some(Number.isNaN)
									? 'exp overflowed to infinity: the output row is NaN.'
									: mode === 'online'
										? 'One sweep carries a running (m, d) pair; threads then merge their pairs in a tree.'
										: 'Pass 1 max, pass 2 sum, pass 3 normalize.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Passes over the row', value: String(passes) },
				{ label: 'Bytes read (row not on chip)', value: fmtBytes(bytesRead) },
				{
					label: 'Max abs error',
					value: Number.isFinite(err) ? err.toExponential(1) : 'NaN / inf',
					tone: err > 1e-3 ? 'bad' : 'good'
				}
			],
			live: `${mode} softmax at scale ${sc}: ${passes} pass${passes === 1 ? '' : 'es'}, ${out.some(Number.isNaN) ? 'the output contains NaN' : 'the output matches the reference'}.`
		};
	}
};

export const vizHaloTile: VizConfig = {
	id: 'halo-tile',
	title: 'Tile plus a halo',
	controls: [
		select('k', 'Filter size K', ['3', '5', '7'], '3'),
		range('t', 'Tile size T', 4, 32, 4, 16),
		select('mode', 'Mode', [
			['tiled', 'Tiled with halo'],
			['none', 'No tiling']
		]),
		select('bc', 'Boundary rule', [
			['zero', 'Zero padding'],
			['clamp', 'Clamp to edge']
		])
	],
	compute(s) {
		const K = Number(str(s, 'k')),
			T = num(s, 't'),
			tiled = str(s, 'mode') === 'tiled',
			over = m.haloOverhead2D(T, T, K),
			perOut = tiled ? over : K * K;
		const n = T + K - 1;
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: Array.from({ length: Math.min(n, 12) }, (_, y) => ({
								label: y === 0 ? 'tile + halo' : '',
								cells: Array.from({ length: Math.min(n, 24) }, (_, x) => ({
									state:
										x < (K - 1) / 2 ||
										y < (K - 1) / 2 ||
										x >= T + (K - 1) / 2 ||
										y >= T + (K - 1) / 2
											? ('stalled' as const)
											: ('touch' as const),
									title: 'halo cell (loaded, not computed)'
								}))
							})),
							caption: tiled
								? `Loaded ${n * n} cells for ${T * T} outputs. Blue clock cells are halo.`
								: `Every output re-reads ${K * K} cells from global memory.`
						}
					]
				}
			],
			readouts: [
				{ label: 'Loads per output', value: fmt(perOut), tone: tiled ? 'good' : 'bad' },
				{ label: 'Total global loads (tile)', value: String(tiled ? n * n : K * K * T * T) },
				{ label: 'Halo overhead', value: tiled ? pct(over - 1) : 'n/a' },
				{ label: '3-D tile 8^3 for comparison', value: fmt(m.haloOverhead3D(8, K)) }
			],
			live: `${tiled ? `A ${T} by ${T} tile with K = ${K} needs ${fmt(over)} loads per output` : `Without tiling every output costs ${K * K} loads`}.${T <= 8 ? ' The halo now dominates, so the win shrinks.' : ''}`
		};
	}
};

export const vizIm2col: VizConfig = {
	id: 'im2col',
	title: 'Convolution as a big matrix',
	controls: [
		select('k', 'K', ['1', '3', '5'], '3'),
		range('size', 'Input size H = W', 4, 56, 1, 56),
		range('cin', 'C_in', 1, 256, 1, 64, { log: true }),
		range('cout', 'C_out', 1, 256, 1, 128, { log: true }),
		toggle('implicit', 'Implicit GEMM', false)
	],
	compute(s) {
		const K = Number(str(s, 'k')),
			H = num(s, 'size'),
			cin = Math.round(num(s, 'cin')),
			cout = Math.round(num(s, 'cout')),
			N = 32;
		const img = Array.from({ length: 4 }, (_, y) =>
				Array.from({ length: 4 }, (_, x) => y * 4 + x + 1)
			),
			rows = m.im2col(img, Math.min(K, 3));
		const flops = m.convFlops(N, cin, cout, H, H, K),
			buf = m.im2colBytes(N, cin, H, K ? H : H, K),
			b = m.convBytes(N, cin, cout, H, H, K);
		const shown = rows
			.slice(0, 6)
			.map((r, i) => ({ label: `window ${i}`, cells: r.map((v) => ({ text: String(v) })) }));
		return {
			panels: [
				{
					kind: 'frames',
					title: 'im2col on a 4 x 4 image (one row per window)',
					frames: [
						{
							rows: shown,
							caption: `Each window becomes a row of ${Math.min(K, 3) ** 2} values; the GEMM multiplies this matrix by the filter matrix.`
						}
					]
				}
			],
			readouts: [
				{
					label: 'im2col matrix',
					value: bool(s, 'implicit') ? 'never built' : fmtBytes(buf),
					tone: bool(s, 'implicit') ? 'good' : 'bad'
				},
				{ label: 'Memory blow-up', value: `about ${m.im2colBlowup(K)}x the input` },
				{ label: 'FLOPs', value: `${fmt(flops / 1e9)} GFLOP` },
				{ label: 'Input', value: fmtBytes(b.input) },
				{ label: 'Weights', value: fmtBytes(b.weights) }
			],
			live: `K = ${K}: the im2col buffer is ${bool(s, 'implicit') ? 'not materialised (implicit GEMM forms tiles on the fly)' : fmtBytes(buf)}, ${m.im2colBlowup(K)} times the input.`
		};
	}
};

export const vizAtomicContention: VizConfig = {
	id: 'atomic-contention',
	title: 'Everyone wants the same bin',
	controls: [
		range('bins', 'Number of bins', 4, 256, 1, 16, { log: true }),
		range('skew', 'Data skew (share in one bin)', 0, 0.95, 0.01, 0.5),
		select('mode', 'Mode', [
			['global', 'Global atomics'],
			['shared', 'Privatized in shared'],
			['agg', 'Warp-aggregated']
		]),
		toggle('lost', 'Show lost updates (non-atomic)', false),
		range('n', 'N (inputs)', 1e4, 1e8, 1, 2 ** 24, { log: true })
	],
	compute(s) {
		const bins = Math.round(num(s, 'bins')),
			skew = num(s, 'skew'),
			N = Math.round(num(s, 'n')),
			mode = str(s, 'mode'),
			blocks = 128;
		const hot = Math.round(N * skew + (N * (1 - skew)) / bins),
			other = (N * (1 - skew)) / bins;
		const lanes = Array.from({ length: 32 }, (_, i) =>
			(((i * 2654435761) >>> 6) % 1000) / 1000 < skew ? 0 : 1 + (i % Math.max(1, bins - 1))
		);
		const atomics =
			mode === 'global'
				? m.naiveGlobalAtomics(N)
				: mode === 'shared'
					? m.privatizedGlobalAtomics(blocks, bins)
					: Math.round((N / 32) * m.warpAggregatedAtomics(lanes));
		const time =
			mode === 'global'
				? Math.max(m.hotBinSeconds(N, hot / N), (N * 8) / (0.85 * 2039e9))
				: mode === 'agg'
					? Math.max(m.hotBinSeconds((N / 32) * 1, hot / N), (N * 4) / (0.85 * 2039e9))
					: (N * 4) / (0.85 * 2039e9) + m.hotBinSeconds(N / blocks, hot / N) * 0.1 + atomics * 1e-9;
		const lostFinal = Math.ceil(hot / 32);
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Counts per bin',
					bars: [
						{
							label: 'hottest bin',
							segments: [{ value: hot, tone: 'bad' }],
							note: hot.toLocaleString('en-US')
						},
						{
							label: 'typical bin',
							segments: [{ value: other, tone: 'tint3' }],
							note: Math.round(other).toLocaleString('en-US')
						}
					],
					max: Math.max(hot, 1)
				},
				...(bool(s, 'lost')
					? [
							{
								kind: 'text',
								title: 'Without atomics',
								text: `The hottest bin should reach ${hot.toLocaleString('en-US')} but 32 lanes read the same old value and write back old + 1, so about ${lostFinal.toLocaleString('en-US')} survive: a lost-update race.`
							} as Panel
						]
					: []),
				{
					kind: 'frames',
					title: 'One warp',
					frames: [
						{
							rows: [
								{
									label: 'bin per lane',
									lanes: true,
									cells: lanes.map((b) => ({
										text: String(b),
										state: b === 0 ? ('error' as const) : ('active' as const)
									}))
								}
							],
							caption: `${m.warpAggregatedAtomics(lanes)} distinct bins in this warp: warp aggregation issues that many atomics instead of 32.`
						}
					]
				}
			],
			readouts: [
				{
					label: 'Max queue depth',
					value: (mode === 'global' ? hot : Math.round(hot / blocks)).toLocaleString('en-US'),
					tone: hot / N > 0.5 && mode === 'global' ? 'bad' : 'neutral'
				},
				{ label: 'Global atomic ops', value: atomics.toLocaleString('en-US') },
				{ label: 'Estimated time', value: fmtTime(time) },
				{ label: 'Max bins in shared (A100)', value: m.maxSharedBins(164).toLocaleString('en-US') }
			],
			live: `${mode} mode with ${Math.round(skew * 100)}% of the data in one bin: ${atomics.toLocaleString('en-US')} global atomics, about ${fmtTime(time)}.`,
			footnote: 'The 1 ns per same-address atomic is an illustrative figure, not a measurement.'
		};
	},
	illustrative: true
};

const SCAN_INPUTS: Record<string, number[]> = {
	mixed: [3, 1, 7, 0, 4, 1, 6, 3],
	ascending: [1, 2, 3, 4, 5, 6, 7, 8],
	ones: [1, 1, 1, 1, 1, 1, 1, 1]
};
export const vizScanNetwork: VizConfig = {
	id: 'scan-network',
	title: 'Two ways to prefix-sum',
	controls: [
		select('algo', 'Algorithm', [
			['hillis', 'Hillis-Steele'],
			['blelloch', 'Blelloch']
		]),
		select('input', 'Input', [
			['mixed', '3 1 7 0 4 1 6 3'],
			['ascending', '1 2 3 4 5 6 7 8'],
			['ones', 'all ones']
		])
	],
	compute(s) {
		const x = SCAN_INPUTS[str(s, 'input')],
			hill = str(s, 'algo') === 'hillis',
			n = x.length;
		let frames: Frame[], depth: number, work: number, result: number[];
		if (hill) {
			const st = m.hillisSteeleSteps(x);
			frames = st.map((a, i) => ({
				rows: [
					{ label: i ? `offset ${2 ** (i - 1)}` : 'input', cells: nums(a, i ? 'active' : 'idle') }
				],
				caption: i
					? `Step ${i}: every element adds its partner ${2 ** (i - 1)} to the left.`
					: 'Input.'
			}));
			depth = m.hillisSteeleCost(n).depth;
			work = m.hillisSteeleCost(n).additions;
			result = st[st.length - 1];
		} else {
			const b = m.blellochSteps(x);
			frames = [
				...b.up.map((a, i) => ({
					rows: [{ label: i ? `up-sweep ${i}` : 'input', cells: nums(a, i ? 'active' : 'idle') }],
					caption: i ? 'Up-sweep: build partial sums in a shrinking tree.' : 'Input.'
				})),
				...b.down.map((a, i) => ({
					rows: [{ label: i ? `down-sweep ${i}` : 'root cleared to 0', cells: nums(a, 'active') }],
					caption: i
						? 'Down-sweep: expanding tree distributes the prefixes.'
						: 'The root is reset to 0.'
				}))
			];
			depth = m.blellochCost(n).depth;
			work = m.blellochCost(n).additions;
			result = b.result;
		}
		return {
			panels: [
				{ kind: 'frames', frames },
				{
					kind: 'table',
					title: 'Work and depth',
					header: ['N', 'Hillis-Steele additions', 'Blelloch additions'],
					rows: [8, 256, 1024].map((k) => [
						k,
						m.hillisSteeleCost(k).additions,
						m.blellochCost(k).additions
					])
				}
			],
			readouts: [
				{ label: 'Steps (depth)', value: String(depth) },
				{ label: 'Additions (work)', value: String(work) },
				{ label: hill ? 'Inclusive result' : 'Exclusive result', value: result.join(' ') }
			],
			live: `${hill ? 'Hillis-Steele' : 'Blelloch'} on 8 values: ${depth} steps and ${work} additions; the other algorithm needs ${hill ? m.blellochCost(n).additions : m.hillisSteeleCost(n).additions}.`
		};
	}
};

export const vizScanLookback: VizConfig = {
	id: 'scan-lookback',
	title: 'Single-pass scan',
	controls: [
		range('blocks', 'Blocks', 4, 12, 1, 8),
		toggle('rand', 'Random scheduling order', true)
	],
	compute(s) {
		const B = num(s, 'blocks'),
			vals = Array.from({ length: B }, (_, i) => ((i * 3 + 2) % 7) + 1),
			order = bool(s, 'rand')
				? Array.from({ length: B }, (_, i) => (i * 5 + 3) % B)
						.filter((v, i, a) => a.indexOf(v) === i)
						.concat(Array.from({ length: B }, (_, i) => i))
						.filter((v, i, a) => a.indexOf(v) === i)
				: Array.from({ length: B }, (_, i) => i);
		const r = m.decoupledLookback(vals, order);
		const frames: Frame[] = order.map((id, k) => ({
			rows: [
				{
					label: 'block status',
					cells: Array.from({ length: B }, (_, b) => {
						const done = order.indexOf(b) <= k;
						return {
							text: `B${b}`,
							state: b === id ? ('touch' as const) : done ? ('done' as const) : ('idle' as const),
							title: done ? 'inclusive prefix published' : 'not ready'
						};
					})
				}
			],
			caption: `Block ${id} publishes its aggregate, looks back ${r.blocks.find((x) => x.id === id)!.steps} step${r.blocks.find((x) => x.id === id)!.steps === 1 ? '' : 's'}, then publishes its inclusive prefix.`
		}));
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Look-back steps', value: r.blocks.map((b) => b.steps).join(', ') },
				{
					label: 'Words moved',
					value: `${m.SCAN_TRAFFIC.decoupledLookback}N vs ${m.SCAN_TRAFFIC.scanThenPropagate}N for scan-then-propagate`
				},
				{ label: 'Prefixes', value: r.prefix.join(' ') }
			],
			live: `Each block waits only on lower-numbered blocks, so block 0 never waits and the scan cannot deadlock; traffic is ${m.SCAN_TRAFFIC.decoupledLookback}N words.`
		};
	}
};

export const vizMatmulLadder: VizConfig = {
	id: 'matmul-ladder',
	title: 'Climb the ladder',
	controls: [
		range('v', 'Version (1-7)', 1, 7, 1, 1),
		select('n', 'Matrix size N', ['64', '128', '256', '4096'], '4096'),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const p = P(s),
			N = Number(str(s, 'n')),
			v = num(s, 'v');
		const VERS = [
			['v1 naive', 1, 1, 'Every thread pulls its own row and column.'],
			[
				'v2 coalescing fix',
				1,
				1,
				'Same loads, but a warp now reads one 128-byte line instead of 32 sectors.'
			],
			[
				'v3 shared tiling T=16',
				16,
				16,
				'Tile-sized loads into a shared slab: T times fewer global loads.'
			],
			['v4 thread coarsening', 32, 32, 'Each thread owns several outputs, reusing its operands.'],
			[
				'v5 float4 loads',
				32,
				32,
				'float4 loads cut load instructions by 4; the bytes stay the same.'
			],
			['v6 register tiling', 64, 64, 'Each thread owns a 4x4 block of C: both bottlenecks move.'],
			['v7 double buffering', 128, 128, 'Loading tile k+1 overlaps computing tile k.']
		] as const;
		const rows = VERS.map(([name, bm, bn], i) => {
			const flops = 2 * N ** 3,
				bytes = (N ** 3 * 4 * (bm + bn)) / (bm * bn),
				eff = i === 0 ? 0.125 : 1,
				ai = flops / bytes;
			return {
				name,
				bm,
				bn,
				bytes,
				ai,
				mem: bytes / eff / (0.85 * m.peakBandwidth(p)),
				comp: flops / (0.8 * m.peakFp32(p))
			};
		});
		const cur = rows[v - 1],
			cr = m.machineBalance(p);
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Memory time (blue) and compute floor (orange), model upper bound',
					bars: rows.map((r, i) => ({
						label: `${i + 1}. ${r.name}${i === v - 1 ? '  <-' : ''}`,
						segments: [
							{ value: r.mem, tone: i === v - 1 ? ('bad' as const) : ('memory' as const) }
						],
						note: fmtTime(r.mem)
					})),
					max: rows[0].mem
				},
				{
					kind: 'table',
					header: ['Version', 'Block tile', 'AI', 'Global bytes', 'Bound'],
					rows: rows.map((r) => [
						r.name,
						`${r.bm}x${r.bn}`,
						fmt(r.ai),
						fmtBytes(r.bytes),
						r.ai < cr ? 'memory' : 'compute'
					]),
					highlight: v - 1
				}
			],
			readouts: [
				{ label: 'Global bytes', value: fmtBytes(cur.bytes) },
				{ label: 'AI', value: `${fmt(cur.ai)} FLOP/B` },
				{ label: 'Ridge', value: fmt(cr) },
				{ label: 'Memory time (modelled)', value: fmtTime(cur.mem) },
				{ label: 'Compute floor', value: fmtTime(cur.comp) },
				{
					label: 'Bound',
					value: cur.ai < cr ? 'memory' : 'compute',
					tone: cur.ai < cr ? 'bad' : 'good'
				}
			],
			live: `${cur.name}: ${VERS[v - 1][3]} AI ${fmt(cur.ai)} against a ridge of ${fmt(cr)}.`,
			footnote:
				'Memory times use the no-cache model: an upper bound for v1. Tensor cores are not modelled.'
		};
	}
};

export const vizQuicksortDivergence: VizConfig = {
	id: 'quicksort-divergence',
	title: 'Partitioning a warp',
	controls: [
		select('shape', 'Array shape', [
			['random', 'random'],
			['sorted', 'sorted'],
			['dups', 'many duplicates']
		]),
		select('algo', 'Algorithm', [
			['quick', 'Quicksort'],
			['bitonic', 'Bitonic']
		])
	],
	compute(s) {
		const shape = str(s, 'shape'),
			N = 32,
			a =
				shape === 'sorted'
					? Array.from({ length: N }, (_, i) => i)
					: shape === 'dups'
						? Array.from({ length: N }, (_, i) => i % 3)
						: Array.from({ length: N }, (_, i) => (i * 17 + 5) % 32);
		const bit = str(s, 'algo') === 'bitonic';
		const depth = (xs: number[]): number =>
			xs.length <= 1
				? 0
				: (() => {
						const pv = xs[0],
							l = xs.slice(1).filter((x) => x < pv),
							r = xs.slice(1).filter((x) => x >= pv);
						return 1 + Math.max(depth(l), depth(r));
					})();
		const pv = a[0],
			left = a.map((x) => x < pv),
			util = bit ? 1 : m.partitionLaneUtilization(left);
		const frames: Frame[] = bit
			? m
					.bitonicNetwork(32)
					.slice(0, 4)
					.map((st, i) => ({
						rows: [
							{
								label: `stage ${i + 1} (k=${st.k}, j=${st.j})`,
								lanes: true,
								cells: Array.from({ length: 32 }, (_, l) => ({
									text: String(l),
									state: 'active' as const
								}))
							}
						],
						caption: 'Every lane compares and exchanges: 32 of 32 lanes active.'
					}))
			: [
					{
						rows: [
							{
								label: `pivot = ${pv}: x < pivot goes left`,
								lanes: true,
								cells: a.map((x, i) => ({
									text: String(x),
									state: left[i] ? ('active' as const) : ('masked' as const)
								}))
							}
						],
						caption: `Left pass: ${left.filter(Boolean).length} of 32 lanes active.`
					},
					{
						rows: [
							{
								label: 'others go right',
								lanes: true,
								cells: a.map((x, i) => ({
									text: String(x),
									state: !left[i] ? ('active' as const) : ('masked' as const)
								}))
							}
						],
						caption: `Right pass: ${left.filter((l) => !l).length} of 32 lanes active.`
					}
				];
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Lane utilization', value: pct(util), tone: util > 0.9 ? 'good' : 'bad' },
				{
					label: bit ? 'Stages' : 'Steps',
					value: String(bit ? m.bitonicStages(32) : 2 * Math.ceil(Math.log2(N)))
				},
				...(bit
					? []
					: [
							{
								label: 'Max recursion depth',
								value: String(depth(a)),
								tone: depth(a) > 12 ? ('bad' as const) : ('neutral' as const)
							}
						])
			],
			live: bit
				? 'Bitonic: 32 of 32 lanes active in every stage, whatever the input.'
				: `Quicksort on ${shape} input: partition utilization ${pct(util)}, recursion depth ${depth(a)}.`
		};
	}
};

export const vizBitonicNetwork: VizConfig = {
	id: 'bitonic-network',
	title: 'A sort that never looks at the data',
	controls: [
		select('n', 'N', ['8', '16'], '8'),
		select('input', 'Input', [
			['a', 'shuffled'],
			['b', 'reversed'],
			['c', 'already sorted']
		]),
		toggle('stage', 'Show stage number', true)
	],
	compute(s) {
		const n = Number(str(s, 'n')),
			x0 =
				str(s, 'input') === 'b'
					? Array.from({ length: n }, (_, i) => n - i)
					: str(s, 'input') === 'c'
						? Array.from({ length: n }, (_, i) => i + 1)
						: Array.from({ length: n }, (_, i) => ((i * 5 + 3) % n) + 1);
		const net = m.bitonicNetwork(n);
		const a = x0.slice();
		let swaps = 0,
			comps = 0;
		const frames: Frame[] = [
			{ rows: [{ label: 'input', cells: nums(a) }], caption: 'Input values.' }
		];
		net.forEach((st, i) => {
			const sw: number[] = [];
			for (const p of st.pairs) {
				comps++;
				if ((p.ascending && a[p.lo] > a[p.hi]) || (!p.ascending && a[p.lo] < a[p.hi])) {
					[a[p.lo], a[p.hi]] = [a[p.hi], a[p.lo]];
					swaps++;
					sw.push(p.lo, p.hi);
				}
			}
			frames.push({
				rows: [
					{
						label: bool(s, 'stage') ? `stage ${i + 1} of ${net.length}` : 'wires',
						cells: a.map((v, j) => ({
							text: String(v),
							state: sw.includes(j) ? ('touch' as const) : ('idle' as const)
						}))
					}
				],
				caption: `Stage ${i + 1}: ${st.pairs.length} compare-exchanges, ${sw.length / 2} swapped.`
			});
		});
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Stages', value: String(net.length) },
				{ label: 'Comparators', value: String(comps) },
				{ label: 'Swaps made', value: String(swaps) }
			],
			live: `The ${net.length} stages and ${comps} comparators are the same for every input; this input needed ${swaps} swaps.`
		};
	}
};

export const vizRadixPass: VizConfig = {
	id: 'radix-pass',
	title: 'One digit at a time',
	controls: [
		select('r', 'Digit bits r', ['1', '2', '4'], '1'),
		range('pass', 'Pass number', 1, 4, 1, 1),
		range('bits', 'Key bits', 4, 32, 4, 4)
	],
	compute(s) {
		const r = Number(str(s, 'r')),
			keyBits = num(s, 'bits'),
			keys = [11, 3, 14, 6, 8, 1, 12, 5, 9, 2, 15, 0, 7, 13, 4, 10].map(
				(k) => k & ((1 << Math.min(keyBits, 4)) - 1)
			);
		const passes = m.radixPasses(keyBits, r),
			pass = Math.min(num(s, 'pass'), Math.min(passes, Math.ceil(4 / r)));
		let a = keys;
		for (let i = 0; i < pass - 1; i++) a = m.radixPass(a, i * r, r).out;
		const st = m.radixPass(a, (pass - 1) * r, r);
		const bin = (k: number) => k.toString(2).padStart(4, '0');
		const frames: Frame[] = [
			{
				rows: [
					{
						label: 'keys',
						cells: a.map((k) => ({ text: bin(k), tint: tint(st.digits[a.indexOf(k)]) }))
					},
					{ label: 'digit', cells: st.digits.map((d) => ({ text: String(d), tint: tint(d) })) }
				],
				caption: 'Look at the current digit of every key.'
			},
			{
				rows: [
					{
						label: 'digit counts',
						cells: st.counts.map((c, d) => ({ text: `${d}:${c}`, tint: tint(d) }))
					},
					{
						label: 'exclusive scan',
						cells: st.offsets.map((o, d) => ({ text: String(o), tint: tint(d) }))
					}
				],
				caption: 'The exclusive scan of the counts gives each digit its first output slot.'
			},
			{
				rows: [
					{ label: 'destination', cells: st.dest.map((d) => ({ text: String(d) })) },
					{
						label: 'after scatter',
						cells: st.out.map((k) => ({ text: bin(k), state: 'done' as const }))
					}
				],
				caption:
					'Equal digits keep their relative order (stable): that is what lets the next pass work.'
			}
		];
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Passes', value: `ceil(${keyBits}/${r}) = ${passes}` },
				{ label: 'Bytes per pass', value: `${8} B x N (read + write 4-byte keys)` },
				{ label: 'Radix', value: String(1 << r) }
			],
			live: `Pass ${pass}: bits ${(pass - 1) * r} to ${pass * r - 1}; ${keyBits}-bit keys need ${passes} passes with ${r} bits per pass.`
		};
	}
};

export const vizSpmvFormats: VizConfig = {
	id: 'spmv-formats',
	title: 'Same matrix, four layouts',
	controls: [
		select('pat', 'Sparsity pattern', [
			['banded', 'banded'],
			['random', 'random'],
			['hub', 'one dense row'],
			['power', 'power-law']
		]),
		select('map', 'Mapping', [
			['tpr', 'Thread per row'],
			['wpr', 'Warp per row']
		]),
		select('fmt', 'Format shown', ['COO', 'CSR', 'ELL'], 'CSR')
	],
	compute(s) {
		const R = 16,
			pat = str(s, 'pat'),
			dense: number[][] = Array.from({ length: R }, (_, r) =>
				Array.from({ length: R }, (_, c) => {
					const h = (((r * 31 + c * 17 + 7) * 2654435761) >>> 8) % 100;
					return pat === 'banded'
						? Math.abs(r - c) <= 1
							? 1
							: 0
						: pat === 'hub'
							? r === 5
								? 1
								: h < 6 && c === r
									? 1
									: 0
							: pat === 'power'
								? h < (80 / (r + 1)) * 1.5
									? 1
									: 0
								: h < 12
									? 1
									: 0;
				})
			);
		const csr = m.toCsr(dense),
			lens = m.rowLengths(csr),
			ell = m.ellStats(lens),
			tpr = m.threadPerRowUtilization(lens, 16),
			wpr = m.warpPerRowUtilization(lens, 16),
			tprSectors = m.threadPerRowSectors(csr, 0, 0, 16);
		const bytes = {
			COO: 12,
			CSR: 8 + (4 * (R + 1)) / Math.max(1, csr.val.length),
			ELL: (8 * ell.slots) / Math.max(1, ell.nnz)
		}[str(s, 'fmt') as 'COO'];
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: dense.map((row, r) => ({
								label: `row ${r} (${lens[r]})`,
								cells: row.map((v) => ({ state: v ? ('active' as const) : ('idle' as const) }))
							})),
							caption: 'Filled cells are nonzeros.'
						}
					]
				},
				{
					kind: 'table',
					title: 'CSR arrays',
					header: ['array', 'first values'],
					rows: [
						['val', csr.val.slice(0, 12).join(' ')],
						['col', csr.col.slice(0, 12).join(' ')],
						['rowptr', csr.rowptr.join(' ')]
					]
				}
			],
			readouts: [
				{
					label: 'Lane utilization',
					value: pct(str(s, 'map') === 'tpr' ? tpr : wpr),
					tone: (str(s, 'map') === 'tpr' ? tpr : wpr) < 0.5 ? 'bad' : 'good'
				},
				{ label: 'Sectors per load (thread-per-row, step 0)', value: String(tprSectors) },
				{
					label: 'ELL padding waste',
					value: pct(ell.waste),
					tone: ell.waste > 0.5 ? 'bad' : 'good'
				},
				{ label: 'Bytes / nnz', value: fmt(bytes) }
			],
			live: `${str(s, 'map') === 'tpr' ? 'Thread per row' : 'Warp per row'} on the ${pat} pattern keeps ${pct(str(s, 'map') === 'tpr' ? tpr : wpr)} of lanes busy; ELL wastes ${pct(ell.waste)} of its slots.`
		};
	}
};

export const vizBfsFrontier: VizConfig = {
	id: 'bfs-frontier',
	title: 'Level by level',
	controls: [
		select('graph', 'Graph', [
			['grid', 'grid'],
			['random', 'random'],
			['hub', 'star with a hub'],
			['power', 'power-law']
		]),
		select('strat', 'Strategy', [
			['push', 'Push'],
			['pull', 'Pull']
		]),
		range('src', 'Source vertex', 0, 19, 1, 0)
	],
	compute(s) {
		const n = 20,
			g = str(s, 'graph'),
			edges: [number, number][] =
				g === 'hub'
					? Array.from(
							{ length: n - 1 },
							(_, i) => [i === 0 ? 0 : 0, i + 1] as [number, number]
						).concat([
							[1, 2],
							[3, 4]
						])
					: g === 'grid'
						? Array.from({ length: n }, (_, i) => [i, i + 1] as [number, number])
								.filter(([, b]) => b < n && b % 5 !== 0)
								.concat(Array.from({ length: n - 5 }, (_, i) => [i, i + 5] as [number, number]))
						: g === 'power'
							? Array.from(
									{ length: n - 1 },
									(_, i) => [Math.floor(Math.sqrt(i)), i + 1] as [number, number]
								)
							: Array.from({ length: n }, (_, i) => [i, (i * 7 + 3) % n] as [number, number])
									.concat(Array.from({ length: n }, (_, i) => [i, (i + 1) % n] as [number, number]))
									.filter(([a, b]) => a !== b);
		const graph = m.symmetric(edges, n),
			src = Math.min(num(s, 'src'), n - 1),
			push = str(s, 'strat') === 'push',
			lv = push ? m.bfsPush(graph, src) : m.bfsPull(graph, src);
		const other = push ? m.bfsPull(graph, src) : m.bfsPush(graph, src);
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Frontier size per level',
					bars: lv.map((l) => ({
						label: `level ${l.level}`,
						segments: [{ value: l.frontier.length, tone: 'compute' as const }],
						note: `${l.frontier.length}`
					}))
				},
				{
					kind: 'table',
					header: [
						'Level',
						'Frontier',
						`Edges examined (${push ? 'push' : 'pull'})`,
						`Edges examined (${push ? 'pull' : 'push'})`,
						'Claims'
					],
					rows: lv.map((l, i) => [
						l.level,
						l.frontier.length,
						l.edgesExamined,
						other[i]?.edgesExamined ?? 0,
						l.claims
					])
				}
			],
			readouts: [
				{ label: 'Levels', value: String(lv.length) },
				{
					label: 'Total edges examined',
					value: String(lv.reduce((a, l) => a + l.edgesExamined, 0))
				},
				{ label: 'Atomic claims', value: String(lv.reduce((a, l) => a + l.claims, 0)) },
				{ label: 'Bytes per edge', value: `~${m.bytesPerEdge} B` }
			],
			live: `${push ? 'Push' : 'Pull'} BFS on the ${g} graph: ${lv.length} levels, ${lv.reduce((a, l) => a + l.edgesExamined, 0)} edges examined; the other strategy examines ${other.reduce((a, l) => a + l.edgesExamined, 0)}.`
		};
	}
};

export const partE: VizConfig[] = [
	vizMapFlow,
	vizReductionTree,
	vizFloatAccumulation,
	vizRowwiseSoftmax,
	vizHaloTile,
	vizIm2col,
	vizAtomicContention,
	vizScanNetwork,
	vizScanLookback,
	vizMatmulLadder,
	vizQuicksortDivergence,
	vizBitonicNetwork,
	vizRadixPass,
	vizSpmvFormats,
	vizBfsFrontier
];
