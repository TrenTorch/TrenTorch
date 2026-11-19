// Figures for parts C and D: control flow, barriers, ordering and memory performance.
import * as m from '../model';
import { T4_MEASURED } from './measured';
import {
	type Cell,
	type Frame,
	type Panel,
	type Row,
	type VizConfig,
	bool,
	fmt,
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
const lanes32 = (f: (i: number) => Cell): Cell[] => Array.from({ length: 32 }, (_, i) => f(i));

const DIV: Record<string, (i: number) => number> = {
	positive: (i) => i + 1,
	negative: (i) => -(i + 1),
	alternating: (i) => (i % 2 ? i : -i - 1),
	random: (i) => (((i * 2654435761) >>> 7) % 2 ? 1 : -1) * (1 + ((i * 7) % 9)),
	half: (i) => (i < 16 ? i + 1 : -(i + 1))
};
export const vizDivergenceLanes: VizConfig = {
	id: 'divergence-lanes',
	title: 'Both roads, one after the other',
	controls: [
		select(
			'pattern',
			'Data pattern',
			[
				['positive', 'all positive'],
				['negative', 'all negative'],
				['alternating', 'alternating'],
				['random', 'random 50/50'],
				['half', 'first 16 positive']
			],
			'alternating'
		),
		select('form', 'Code form', [
			['branchy', 'branchy: if (x > 0) out = x; else out = 0'],
			['branchless', 'branchless: fmaxf(x, 0)']
		])
	],
	compute(s) {
		const x = DIV[str(s, 'pattern')],
			branchless = str(s, 'form') === 'branchless';
		const posLanes = Array.from({ length: 32 }, (_, i) => x(i) > 0),
			nPos = posLanes.filter(Boolean).length;
		const paths = branchless ? 1 : (nPos > 0 ? 1 : 0) + (nPos < 32 ? 1 : 0),
			ideal = 1;
		const mkLanes = (active: (i: number) => boolean) =>
			lanes32((i) => ({ text: String(x(i)), state: active(i) ? 'active' : 'masked' }));
		const frames: Frame[] = branchless
			? [
					{
						rows: [{ label: 'fmaxf pass', lanes: true, cells: mkLanes(() => true) }],
						caption: 'Pass 1 of 1: 32 of 32 lanes active.'
					}
				]
			: [
					{
						rows: [{ label: 'evaluate x > 0', lanes: true, cells: mkLanes(() => true) }],
						caption: 'Pass 0: all 32 lanes evaluate the condition.'
					},
					...(nPos > 0
						? [
								{
									rows: [
										{ label: 'Path A: out = x', lanes: true, cells: mkLanes((i) => posLanes[i]) }
									],
									caption: `Pass ${1} of ${paths}: ${nPos} of 32 lanes active.`
								}
							]
						: []),
					...(nPos < 32
						? [
								{
									rows: [
										{ label: 'Path B: out = 0', lanes: true, cells: mkLanes((i) => !posLanes[i]) }
									],
									caption: `Pass ${paths} of ${paths}: ${32 - nPos} of 32 lanes active.`
								}
							]
						: []),
					{
						rows: [{ label: 'reconverged', lanes: true, cells: mkLanes(() => true) }],
						caption: 'All lanes active again: reconvergence.'
					}
				];
		const eff = branchless
			? 1
			: (nPos > 0 ? nPos : 0) + (nPos < 32 ? 32 - nPos : 0) > 0
				? (32 / (paths * 32)) * (nPos > 0 && nPos < 32 ? 1 : 1)
				: 1;
		const activeAvg = branchless ? 32 : paths === 1 ? 32 : 32 / 2;
		return {
			panels: [
				{ kind: 'frames', frames },
				{
					kind: 'bars',
					title: 'Cycles used versus no divergence',
					unit: 'units',
					bars: [
						{ label: 'used', segments: [{ value: paths, tone: paths > 1 ? 'bad' : 'good' }] },
						{ label: 'if no divergence', segments: [{ value: ideal, tone: 'neutral' }] }
					]
				}
			],
			readouts: [
				{ label: 'Paths executed', value: String(paths) },
				{ label: 'Warp efficiency', value: pct(activeAvg / 32), tone: paths > 1 ? 'bad' : 'good' },
				{
					label: 'Active lanes per pass',
					value: branchless ? '32' : paths === 1 ? '32' : `${nPos} then ${32 - nPos}`
				}
			],
			live: branchless
				? 'Branchless form: one pass, 32 of 32 lanes active throughout.'
				: paths === 1
					? 'Every lane chose the same path: one pass, no cost.'
					: `Pass 1 of 2: ${nPos} lanes active. Pass 2 of 2: ${32 - nPos} lanes active. The warp pays for both paths.`,
			footnote:
				'The compiler may turn the branchy form into predicated code. This model shows the divergent case.',
			...(void eff, {})
		};
	}
};

export const vizDivergenceProbability: VizConfig = {
	id: 'divergence-probability',
	title: 'How often does a warp split?',
	controls: [
		range('p', 'p (lane takes the rare path)', 0.0001, 0.5, 0.0001, 0.01, {
			log: true,
			format: (v) => String(Number(v.toPrecision(2)))
		}),
		range('warps', 'Warps to simulate', 0, 5000, 100, 1000),
		range('seed', 'Seed', 1, 99, 1, 7),
		range('a', 'Rare path cost a', 1, 200, 1, 50),
		range('b', 'Common path cost b', 1, 200, 1, 10)
	],
	compute(s) {
		const p = num(s, 'p'),
			W = num(s, 'warps'),
			formula = m.pDiverge(p),
			mc = W ? m.monteCarloDivergence(p, W, num(s, 'seed')) : { fraction: NaN, diverged: 0 };
		const lane = lanes32((i) => ({
			state:
				(((i * 2654435761 + num(s, 'seed') * 40503) >>> 5) % 10000) / 10000 < p ? 'active' : 'idle'
		}));
		const xs = Array.from({ length: 60 }, (_, i) => 10 ** (-4 + (i * 3.3) / 59));
		const e = m.expectedWarpTime(p, num(s, 'a'), num(s, 'b'));
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [{ label: 'one random warp', lanes: true, cells: lane }],
							caption: 'Orange lanes took the rare path.'
						}
					]
				},
				{
					kind: 'line',
					title: 'P(warp executes both paths)',
					xLabel: 'p',
					yLabel: 'probability',
					xLog: true,
					yMax: 1,
					series: [
						{
							name: '1 - (1-p)^32 - p^32',
							tone: 'compute',
							points: xs.map((x) => [x, m.pDiverge(x)] as [number, number])
						}
					],
					point: { x: p, y: formula, label: 'your p' }
				}
			],
			readouts: [
				{ label: 'Formula', value: pct(formula), tone: formula > 0.25 ? 'bad' : 'good' },
				{ label: `Measured (${W} warps)`, value: W ? pct(mc.fraction) : 'run a simulation' },
				{ label: 'Expected warp time', value: fmt(e) },
				{ label: 'Without divergence', value: fmt(num(s, 'b') + num(s, 'a') * p) }
			],
			live: `At p = ${p}, ${pct(formula)} of warps execute both paths${W ? `; ${pct(mc.fraction)} measured over ${W} warps` : ''}.`
		};
	}
};

export const vizBarrierEpochs: VizConfig = {
	id: 'barrier-epochs',
	title: 'Who is waiting at the fence?',
	controls: [
		toggle('rm1', 'Remove barrier #1 (after the write)', false),
		toggle('rm2', 'Remove barrier #2 (before the overwrite)', false),
		toggle('inif', 'Put the barrier inside if (t < 4)', false),
		toggle('rand', 'Randomize thread speeds', false)
	],
	compute(s) {
		const T = 8,
			speeds = bool(s, 'rand') ? [1, 2, 1, 3, 2, 1, 3, 2] : [1, 1, 1, 1, 3, 1, 1, 1]; // thread 4 is slow by default: the bad schedule
		const rm1 = bool(s, 'rm1'),
			rm2 = bool(s, 'rm2'),
			inif = bool(s, 'inif');
		// program: write s[t]; BARRIER1; read s[(t+1)%8]; BARRIER2; overwrite s[t]
		const writeAt = speeds.map((v) => v),
			arrive1 = writeAt.slice();
		const barrier1 = inif ? Math.max(...arrive1.slice(0, 4)) : Math.max(...arrive1);
		const readStart = speeds.map((_, t) =>
			rm1 ? writeAt[t] : inif && t >= 4 ? writeAt[t] : barrier1
		);
		const readAt = readStart.map((v, t) => v + speeds[t] * 0.5);
		const races: string[] = [];
		for (let t = 0; t < T; t++) {
			const w = (t + 1) % T;
			if (readAt[t] < writeAt[w] + 0.001 && readStart[t] < writeAt[w])
				races.push(`thread ${t} reads slot ${w} before thread ${w} writes it (RAW)`);
		}
		const arrive2 = readAt.map((v) => v),
			barrier2 = Math.max(...arrive2);
		const overwriteAt = speeds.map((_, t) => (rm2 ? readAt[t] : barrier2));
		for (let t = 0; t < T; t++) {
			const reader = (t - 1 + T) % T;
			if (overwriteAt[t] < readAt[reader])
				races.push(`thread ${t} overwrites slot ${t} before thread ${reader} reads it (WAR)`);
		}
		const deadlock = inif && !rm1;
		const END = Math.ceil(Math.max(barrier2, ...overwriteAt) + 2);
		const rows: Row[] = Array.from({ length: T }, (_, t) => ({
			label: `thread ${t}`,
			cells: Array.from({ length: END }, (_, k) => {
				const at = k + 0.5;
				let st: Cell['state'] = 'done';
				if (at < writeAt[t]) st = 'active';
				else if (!rm1 && !(inif && t >= 4) && at < barrier1) st = 'masked';
				else if (at < readAt[t]) st = 'active';
				else if (!rm2 && at < barrier2) st = 'masked';
				else if (at < overwriteAt[t] + 0.5) st = 'active';
				if (deadlock && t >= 4) st = at < writeAt[t] ? 'active' : 'error';
				if (deadlock && t < 4 && at >= barrier1) st = 'masked';
				return {
					state: st,
					text:
						k === Math.floor(barrier1) && !rm1 ? '|' : k === Math.floor(barrier2) && !rm2 ? '|' : ''
				};
			})
		}));
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows,
							caption:
								'Orange = running, hatched = waiting at a barrier, "|" marks a barrier, red cross = never arrives.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Barriers', value: String((rm1 ? 0 : 1) + (rm2 ? 0 : 1)) },
				{
					label: 'Result',
					value: deadlock
						? 'DEADLOCK: 4 threads never reached the barrier'
						: races.length
							? `RACE: ${races[0]}`
							: 'correct',
					tone: deadlock || races.length ? 'bad' : 'good'
				}
			],
			live: deadlock
				? 'Deadlock: threads 4 to 7 never reach the barrier, so threads 0 to 3 wait forever.'
				: races.length
					? `Race detected: ${races[0]}.`
					: 'Both barriers are in place: every read happens after every write, and every overwrite after every read.',
			footnote:
				'The schedule is forced to the bad case so the race is visible; on real hardware it may pass many runs first.'
		};
	},
	illustrative: true
};

export const vizLastBlock: VizConfig = {
	id: 'last-block',
	title: 'Who finishes last?',
	controls: [
		toggle('fence', 'Include __threadfence()', false),
		toggle('late', 'Reorder visibility (block 3 write arrives late)', true)
	],
	compute(s) {
		const B = 6,
			fence = bool(s, 'fence'),
			late = bool(s, 'late'),
			order = [2, 5, 0, 3, 1, 4];
		const staleBlock = !fence && late ? 3 : -1;
		const lastBlock = order[B - 1],
			lastReadsStale = staleBlock >= 0 && lastBlock !== 3;
		const frames: Frame[] = order.map((_, step) => ({
			rows: [
				{
					label: 'blocks',
					cells: Array.from({ length: B }, (_, b) => {
						const pos = order.indexOf(b);
						return {
							text: `B${b}${pos <= step ? (pos === step ? ' ticket ' + pos : ` t${pos}`) : ''}`,
							state:
								pos < step
									? ('done' as const)
									: pos === step
										? ('active' as const)
										: ('idle' as const)
						};
					})
				},
				{
					label: 'partial[]',
					cells: Array.from({ length: B }, (_, b) => ({
						text:
							order.indexOf(b) <= step
								? b === staleBlock && order.indexOf(b) >= step - 0
									? '?'
									: 'ok'
								: '-',
						state:
							order.indexOf(b) <= step
								? b === staleBlock && step === B - 1
									? ('error' as const)
									: ('done' as const)
								: ('idle' as const)
					}))
				},
				{ label: 'counter', cells: [{ text: String(Math.min(step + 1, B)), tint: 4 }] }
			],
			caption:
				step < B - 1
					? `Block ${order[step]} writes partial${fence ? ', fences,' : ''} and takes ticket ${step}.`
					: `Block ${order[step]} takes ticket ${step} = gridDim - 1: it is last and reads all partials${lastReadsStale ? ', but partial[3] is STALE' : ''}.`
		}));
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Global atomics', value: String(m.lastBlockAtomics(B)) },
				{
					label: 'Final read',
					value: lastReadsStale ? 'stale read of partial[3]' : 'all partials visible',
					tone: lastReadsStale ? 'bad' : 'good'
				}
			],
			live: lastReadsStale
				? 'Without __threadfence() the last block read partial[3] before its write became visible: a stale read.'
				: 'The fence makes each partial visible before the ticket increments, so the last block sees everything.'
		};
	}
};

const LAYOUTS: Record<string, string> = {
	contiguous: 'Contiguous (stride)',
	aos: 'Array of 12-byte structs (read one field)',
	column: 'Column of a row-major matrix (W = 1024)'
};
export const vizCoalescing: VizConfig = {
	id: 'coalescing',
	title: 'From 32 addresses to transactions',
	controls: [
		select('stride', 'Stride (elements)', ['1', '2', '4', '8', '32'], '1'),
		range('offset', 'Offset (elements)', 0, 31, 1, 0),
		select(
			'size',
			'Element size',
			[
				['4', '4 B float'],
				['16', '16 B float4']
			],
			'4'
		),
		select('layout', 'Layout preset', Object.entries(LAYOUTS))
	],
	compute(s) {
		const w = Number(str(s, 'size')),
			stride = Number(str(s, 'stride')),
			off = num(s, 'offset') * w,
			layout = str(s, 'layout');
		const addrs =
			layout === 'aos'
				? Array.from({ length: 32 }, (_, l) => l * 12 + off)
				: layout === 'column'
					? Array.from({ length: 32 }, (_, l) => l * 1024 * 4 + off)
					: m.strideAddresses(stride, w, off);
		const width = layout === 'aos' ? 4 : w,
			set = [...m.sectors(addrs, width)].sort((a, b) => a - b);
		const useful = addrs.length * width,
			moved = set.length * m.SECTOR,
			eff = useful / moved;
		const cells: Cell[] = set.slice(0, 64).map((sec) => {
			const used =
				addrs.filter((a) => Math.floor(a / 32) === sec || Math.floor((a + width - 1) / 32) === sec)
					.length * width;
			return {
				text: `${Math.min(used, 32)}B`,
				state: 'touch' as const,
				tint: 4 as const,
				title: `sector ${sec}: ${used} useful of 32 bytes`
			};
		});
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{
									label: '32 lanes issue a load',
									lanes: true,
									cells: lanes32((i) => ({ text: String(i), state: 'active' as const }))
								},
								{
									label: `sectors touched (${set.length})`,
									cells,
									note: set.length > 64 ? 'first 64 shown' : undefined
								}
							],
							caption: `Each lit sector is one 32-byte transaction; its label is how many of its bytes were requested.`
						}
					]
				}
			],
			readouts: [
				{ label: 'Transactions (sectors)', value: String(set.length) },
				{ label: 'Bytes moved', value: String(moved) },
				{ label: 'Bytes useful', value: String(useful) },
				{ label: 'Efficiency', value: pct(eff), tone: eff > 0.9 ? 'good' : 'bad' }
			],
			live: `${LAYOUTS[layout]}${layout === 'contiguous' ? `, stride ${stride}` : ''}: ${set.length} sectors fetched, ${useful} of ${moved} bytes useful (${pct(eff)}).`
		};
	}
};

const KERNELS = [
	['Vector add', 1, 12],
	['ReLU', 1, 8],
	['SAXPY', 2, 12],
	['Softmax (row in cache)', 5, 8],
	['LayerNorm (row in cache)', 8, 8],
	['GEMV', 2, 4],
	['SpMV (CSR)', 2, 12]
] as const;
export const vizRoofline: VizConfig = {
	id: 'roofline',
	title: 'Where does my kernel live?',
	controls: [
		gpu(),
		select('roof', 'Compute roof', ['FP32', 'TF32', 'FP16']),
		range('tile', 'Matmul tile size T', 1, 128, 1, 16, { log: true }),
		range('ai', 'Custom kernel AI (FLOP/byte)', 0.01, 1000, 0.01, 2, {
			log: true,
			format: (v) => String(Number(v.toPrecision(3)))
		})
	],
	modes: { ladder: { title: 'Roof ladder and tile size' } },
	compute(s, ctx) {
		const p = P(s),
			roof = str(s, 'roof') as m.Roof,
			peak = m.roofFlops(p, roof),
			bw = m.peakBandwidth(p),
			rdg = m.ridge(peak, bw),
			T = Math.round(num(s, 'tile'));
		const mine =
			ctx.lastRun && ctx.lastRun.bytes > 0 && ctx.lastRun.flops > 0
				? { n: `My last run: ${ctx.lastRun.title}`, ai: ctx.lastRun.flops / ctx.lastRun.bytes }
				: null;
		const pts = [
			...KERNELS.map(([n, f, b]) => ({ n, ai: f / b })),
			...(mine ? [mine] : []),
			{ n: `Matmul tile ${T}`, ai: m.matmulAI(T, T) },
			{ n: 'Custom', ai: num(s, 'ai') }
		];
		const xs = Array.from({ length: 80 }, (_, i) => 10 ** (-2 + (i * 5) / 79));
		const att = (ai: number) => m.attainable(peak, bw, ai) / 1e9;
		const dots = pts.map((q) => ({
			name: q.n,
			tone: 'compute' as const,
			points: [[q.ai, att(q.ai)]] as [number, number][]
		}));
		const panels: Panel[] = [
			{
				kind: 'line',
				title: 'Roofline',
				xLabel: 'arithmetic intensity (FLOP/byte)',
				yLabel: 'GFLOP/s',
				xLog: true,
				yLog: true,
				series: [
					{
						name: 'roofline',
						tone: 'memory',
						points: xs.map((x) => [x, att(x)] as [number, number])
					},
					...dots
				],
				markers: [{ x: rdg, label: `ridge ${fmt(rdg)}` }]
			},
			{
				kind: 'table',
				header: ['Kernel', 'AI', 'Attainable GFLOP/s', '% of roof', 'Bound'],
				rows: pts.map((q) => [
					q.n,
					fmt(q.ai),
					fmt(att(q.ai)),
					pct(att(q.ai) / (peak / 1e9)),
					q.ai < rdg ? 'memory-bound' : 'compute-bound'
				])
			}
		];
		if (ctx.mode === 'ladder')
			panels.push({
				kind: 'table',
				title: 'The same tile on each roof',
				header: ['Roof', 'Peak TFLOPS', 'Ridge (FLOP/B)', 'Tile for compute-bound'],
				rows: (['FP32', 'TF32', 'FP16'] as m.Roof[]).map((r) => [
					r,
					fmt(m.roofFlops(p, r) / 1e12),
					fmt(m.roofRidge(p, r)),
					r === 'FP16' ? fmt(m.roofRidge(p, r) * 2) : fmt(m.requiredSquareTile(m.roofRidge(p, r)))
				])
			});
		const me = pts.find((q) => q.n.startsWith('Matmul tile'))!;
		return {
			panels,
			readouts: [
				{ label: 'Ridge', value: `${fmt(rdg)} FLOP/B` },
				{ label: `Tile ${T} AI`, value: fmt(me.ai) },
				{ label: 'Attainable', value: `${fmt(att(me.ai))} GFLOP/s` },
				{ label: '% of roof', value: pct(att(me.ai) / (peak / 1e9)) },
				{ label: 'Tile for compute-bound', value: fmt(m.requiredSquareTile(rdg)) }
			],
			live: `ReLU: ${fmt(0.125)} FLOP/byte, memory-bound. Ridge on ${str(s, 'gpu')} (${roof}) is ${fmt(rdg)}.`,
			footnote: mine
				? 'Includes your last simulator run (FLOPs are a static estimate).'
				: 'Run a problem in the IDE and your last run appears here.'
		};
	}
};

export const vizFloat4Bandwidth: VizConfig = {
	id: 'float4-bandwidth',
	title: 'Does wider help?',
	controls: [
		select('source', 'Source', [
			['model', 'Simulator model'],
			['measured', 'Measured on T4 (Colab)']
		]),
		gpu('gpu', 'Profile', 'T4'),
		range('warps', 'Resident warps per SM', 1, 32, 1, 8),
		toggle('aligned', 'Aligned (off: offset by 4 B)', true),
		select('op', 'Operation', [
			['copy', 'copy (8 B/elt)'],
			['relu', 'ReLU (8 B/elt)'],
			['saxpy', 'SAXPY (12 B/elt)']
		])
	],
	compute(s) {
		const p = P(s),
			peak = p.memBwGBs,
			eta = 0.85,
			latencySec = p.latencyCycles.dram / (p.boostGHz * 1e9),
			warps = num(s, 'warps'),
			aligned = bool(s, 'aligned');
		const sizes = Array.from({ length: 30 }, (_, i) => 10 ** (3 + (i * 6) / 29)); // 1 KB .. 1 GB
		const bw = (size: number, width: number) => {
			const inflight = (warps * 32 * width * p.sms) / latencySec / 1e9;
			const sustained = Math.min(peak * eta, inflight);
			const t = 5e-6 + size / (sustained * 1e9);
			return size / t / 1e9;
		};
		const eff = (width: number) => (width === 4 || !aligned ? 4 : width);
		const measured = str(s, 'source') === 'measured';
		if (measured && !T4_MEASURED)
			return {
				panels: [
					{
						kind: 'text',
						title: 'No measured data yet',
						text: 'No Colab T4 measurements have been committed. Run scripts/colab/t4_benchmarks.ipynb on a Colab T4 and commit its output to processes/cuda/viz/measured.ts. Until then this figure shows the simulator model only.'
					}
				],
				readouts: [],
				live: 'No measured T4 data is available yet, so nothing is plotted.'
			};
		const n = 1_000_003,
			plan = m.float4Plan(n, 256);
		return {
			panels: [
				{
					kind: 'line',
					title: 'Effective bandwidth (simulator model, not a measurement)',
					xLabel: 'array size (bytes)',
					yLabel: 'GB/s',
					xLog: true,
					yMax: peak,
					series: [
						{
							name: 'float',
							tone: 'tint4',
							points: sizes.map((x) => [x, bw(x, 4)] as [number, number])
						},
						{
							name: 'float2',
							tone: 'tint3',
							points: sizes.map((x) => [x, bw(x, eff(8))] as [number, number])
						},
						{
							name: 'float4',
							tone: 'compute',
							points: sizes.map((x) => [x, bw(x, eff(16))] as [number, number])
						},
						{
							name: 'peak',
							tone: 'neutral',
							dashed: true,
							points: [
								[1e3, peak],
								[1e9, peak]
							]
						}
					]
				},
				{
					kind: 'table',
					title: `Tail for N = ${n.toLocaleString('en-US')}`,
					header: ['', 'count'],
					rows: [
						['float4 elements', plan.vec.toLocaleString('en-US')],
						['scalar tail elements', plan.tail],
						['blocks (256 threads)', plan.blocks],
						['warp load instructions, scalar', fmt(n / 32)],
						['warp load instructions, float4', fmt(n / 128)]
					]
				}
			],
			readouts: [
				{ label: 'float in flight / warp load', value: `${m.bytesInFlightPerWarpLoad(4)} B` },
				{ label: 'float4 in flight / warp load', value: `${m.bytesInFlightPerWarpLoad(16)} B` },
				{ label: 'float at 1 GB', value: `${fmt(bw(1e9, 4))} GB/s` },
				{
					label: 'float4 at 1 GB',
					value: `${fmt(bw(1e9, eff(16)))} GB/s`,
					tone: aligned ? 'good' : 'bad'
				}
			],
			live: `At ${warps} resident warps per SM, float reaches ${fmt(bw(1e9, 4))} GB/s and float4 ${fmt(bw(1e9, eff(16)))} GB/s of a ${peak} GB/s peak${aligned ? '' : '; misaligned float4 falls back to scalar loads'}.`,
			footnote:
				"Modelled with Little's law (bytes in flight = latency x bandwidth); latencies are illustrative."
		};
	},
	illustrative: true
};

export const vizTilingStepper: VizConfig = {
	id: 'tiling-stepper',
	title: 'Load once, use many times',
	controls: [
		range('n', 'Matrix size (N x N x N)', 4, 32, 4, 8),
		select('t', 'Tile size T', ['2', '4', '8', '16'], '4'),
		select('mode', 'Mode', [
			['tiled', 'Tiled'],
			['naive', 'Naive']
		])
	],
	compute(s) {
		const N = num(s, 'n'),
			T = Math.min(Number(str(s, 't')), N),
			tiled = str(s, 'mode') === 'tiled',
			tiles = Math.ceil(N / T);
		const naiveLoads = 2 * N * N * N,
			tiledLoads = (2 * N * N * N) / T;
		const steps: Frame[] = [];
		const A = (hi: number): Cell[] =>
			Array.from({ length: Math.min(N * 1, 16) }, (_, k) => ({
				state: Math.floor(k / T) === hi ? ('touch' as const) : ('idle' as const),
				tint: 1 as const
			}));
		if (tiled)
			for (let k = 0; k < tiles; k++)
				for (const phase of ['load', 'barrier', 'compute', 'barrier'] as const)
					steps.push({
						rows: [
							{ label: 'A strip (K tile)', cells: A(k) },
							{
								label: `shared: As, Bs (${T}x${T} each)`,
								cells: Array.from({ length: Math.min(2 * T, 16) }, () => ({
									state:
										phase === 'load'
											? ('touch' as const)
											: phase === 'barrier'
												? ('done' as const)
												: ('active' as const),
									tint: 2 as const
								}))
							}
						],
						caption: `Tile ${k + 1} of ${tiles}: ${phase === 'load' ? `loaded ${2 * T * T} values into shared memory` : phase === 'compute' ? `${T * T * T} multiply-adds done` : '__syncthreads()'}; global loads so far: ${Math.round(tiledLoads * ((k + (phase === 'load' ? 1 : 1)) / tiles))} vs ${naiveLoads} naive.`
					});
		else
			steps.push({
				rows: [
					{
						label: 'every C cell loads its own row and column',
						cells: Array.from({ length: Math.min(N, 16) }, () => ({
							state: 'active' as const,
							tint: 4 as const
						}))
					}
				],
				caption: `Naive: ${naiveLoads} global loads (2K per output).`
			});
		return {
			panels: [{ kind: 'frames', frames: steps }],
			readouts: [
				{ label: 'Global loads (this mode)', value: String(tiled ? tiledLoads : naiveLoads) },
				{ label: 'Loads if naive', value: String(naiveLoads) },
				{
					label: 'Reduction factor',
					value: `${fmt(naiveLoads / (tiled ? tiledLoads : naiveLoads))}x`,
					tone: tiled ? 'good' : 'neutral'
				},
				{ label: 'Shared bytes', value: tiled ? String(m.tilingBytes(T)) : '0' }
			],
			live: `${tiled ? `Tile ${T}: ${tiledLoads} global loads` : `Naive: ${naiveLoads} global loads`}; the reduction factor equals T = ${tiled ? T : 1}.`
		};
	}
};

const BANK_PATTERNS: Record<string, string> = {
	row: 'Row access',
	column: 'Column access',
	stride: 'Stride s',
	broadcast: 'Broadcast (all lanes same word)'
};
export const vizBankGrid: VizConfig = {
	id: 'bank-grid',
	title: '32 lanes, 32 banks',
	controls: [
		select('pattern', 'Access pattern', Object.entries(BANK_PATTERNS), 'column'),
		range('stride', 'Stride s', 1, 64, 1, 8),
		toggle('pad', 'Row padding (pitch 33)', false),
		toggle('swz', 'XOR swizzle', false)
	],
	modes: { 'stride-sweep': { title: 'Stride sweep' } },
	compute(s, ctx) {
		const pat = str(s, 'pattern'),
			pitch = bool(s, 'pad') ? 33 : 32,
			swz = bool(s, 'swz'),
			st = num(s, 'stride');
		const words = Array.from({ length: 32 }, (_, l) =>
			pat === 'row'
				? m.tileWord(0, l, pitch, swz)
				: pat === 'column'
					? m.tileWord(l, 5, pitch, swz)
					: pat === 'stride'
						? l * st
						: 7
		);
		const deg = m.conflictDegree(words),
			perBank = Array(32).fill(0);
		new Set(words).forEach((w) => perBank[w % 32]++);
		const lane = lanes32((i) => ({
			text: String(words[i] % 32),
			state: perBank[words[i] % 32] > 1 ? ('error' as const) : ('active' as const),
			title: `lane ${i} -> bank ${words[i] % 32}`
		}));
		const panels: Panel[] = [
			{
				kind: 'frames',
				frames: [
					{
						rows: [
							{ label: 'lane -> bank', lanes: true, cells: lane },
							{
								label: 'requests per bank',
								cells: perBank.map((c, b) => ({
									text: String(c || ''),
									state:
										c > 1 ? ('error' as const) : c === 1 ? ('done' as const) : ('idle' as const),
									title: `bank ${b}: ${c} request${c === 1 ? '' : 's'}`
								}))
							}
						],
						caption:
							deg > 1
								? `${deg}-way conflict: the hardware serves the access in ${deg} cycles.`
								: 'No conflict: all requests are served in one cycle.'
					}
				]
			}
		];
		if (ctx.mode === 'stride-sweep')
			panels.push(
				{
					kind: 'bars',
					title: 'Conflict degree for strides 1 to 64 (gcd(s, 32))',
					bars: Array.from({ length: 64 }, (_, i) => i + 1)
						.filter((x) => x <= 40)
						.map((x) => ({
							label: `s = ${x}`,
							segments: [
								{
									value: m.strideConflictDegree(x),
									tone: m.strideConflictDegree(x) > 1 ? ('bad' as const) : ('good' as const)
								}
							],
							note: `${m.strideConflictDegree(x)}-way`
						}))
				},
				{
					kind: 'text',
					text: `Padding turns stride 32 into stride 33 (degree ${m.strideConflictDegree(33)}); an XOR swizzle keeps the power-of-two pitch.`
				}
			);
		return {
			panels,
			readouts: [
				{ label: 'Max conflict degree', value: `${deg}-way`, tone: deg > 1 ? 'bad' : 'good' },
				{ label: 'Cycles', value: String(deg) },
				{ label: 'Slowdown', value: `${deg}x` },
				...(pat === 'stride'
					? [{ label: 'gcd(s, 32)', value: String(m.strideConflictDegree(st)) }]
					: [])
			],
			live: `${BANK_PATTERNS[pat]}${pat === 'stride' ? ` with s = ${st}` : ''}${bool(s, 'pad') ? ', padded' : ''}${swz ? ', swizzled' : ''}: ${deg === 1 ? 'no conflict, 1 cycle' : `${deg}-way conflict, ${deg} cycles`}.`
		};
	}
};

export const vizSharedBound: VizConfig = {
	id: 'shared-bound',
	title: 'The hidden bottleneck in tiling',
	controls: [
		select('r', 'Register tile R', ['1', '2', '4', '8'], '1'),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const R = Number(str(s, 'r')),
			b = m.sharedBound(R, P(s));
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Cycles per warp-FMA',
					bars: [
						{
							label: 'shared-memory loads',
							segments: [
								{ value: b.loadCycles, tone: b.limiting === 'shared memory' ? 'bad' : 'tint2' }
							],
							note: fmt(b.loadCycles)
						},
						{
							label: 'FMA issue',
							segments: [{ value: b.fmaCycles, tone: b.limiting === 'FMA' ? 'good' : 'compute' }],
							note: fmt(b.fmaCycles)
						}
					]
				}
			],
			readouts: [
				{ label: 'Loads per warp-FMA (2/R)', value: fmt(m.sharedLoadsPerWarpFma(R)) },
				{
					label: 'Limiting resource',
					value: b.limiting,
					tone: b.limiting === 'FMA' ? 'good' : 'bad'
				},
				{ label: '% of FMA peak', value: pct(b.fmaPeakFraction) },
				{ label: 'Registers / thread', value: String(m.registerTileRegs(R)) }
			],
			live: `R = ${R}: ${fmt(m.sharedLoadsPerWarpFma(R))} shared loads per warp-FMA; ${b.limiting} limits, at ${pct(b.fmaPeakFraction)} of FMA peak.`
		};
	}
};

export const vizRegisterPressure: VizConfig = {
	id: 'register-pressure',
	title: 'The register budget',
	controls: [
		range('need', 'Registers the kernel needs', 16, 255, 1, 64),
		range('cap', 'Compiler cap per thread', 16, 255, 1, 255),
		range('bs', 'Block size', 32, 1024, 32, 256),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const p = P(s),
			need = num(s, 'need'),
			cap = num(s, 'cap'),
			used = Math.min(need, cap),
			spill = Math.max(0, need - cap);
		const o = m.occupancy(p, num(s, 'bs'), used);
		return {
			panels: [
				{
					kind: 'bars',
					title: `Registers of one SM (${p.regsPerSm.toLocaleString('en-US')})`,
					bars: [
						{
							label: 'used by resident blocks',
							segments: [{ value: o.blocks * o.regsPerBlock, tone: 'tint0' }],
							note: `${(o.blocks * o.regsPerBlock).toLocaleString('en-US')}`
						},
						{
							label: 'spilled to local memory',
							segments: [{ value: spill * o.warpsPerSm * 32, tone: 'bad' }],
							note: `${spill} regs/thread`
						}
					],
					max: p.regsPerSm
				},
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{
									label: 'resident warps',
									cells: Array.from({ length: p.maxWarpsPerSm }, (_, i) => ({
										state: i < o.warpsPerSm ? ('active' as const) : ('idle' as const)
									}))
								}
							],
							caption: `${o.warpsPerSm} of ${p.maxWarpsPerSm} warps resident.`
						}
					]
				}
			],
			readouts: [
				{ label: 'Occupancy', value: pct(o.occupancy) },
				{ label: 'Blocks / SM', value: String(o.blocks) },
				{
					label: 'Spill',
					value: spill ? `${spill} regs/thread (+${spill * 2} local accesses)` : 'none',
					tone: spill ? 'bad' : 'good'
				}
			],
			live: spill
				? `Capped at ${cap} registers, ${spill} values per thread spill to local memory: extra memory traffic.`
				: `${used} registers per thread gives ${pct(o.occupancy)} occupancy, no spills.`
		};
	}
};

export const partCD: VizConfig[] = [
	vizDivergenceLanes,
	vizDivergenceProbability,
	vizBarrierEpochs,
	vizLastBlock,
	vizCoalescing,
	vizRoofline,
	vizFloat4Bandwidth,
	vizTilingStepper,
	vizBankGrid,
	vizSharedBound,
	vizRegisterPressure
];
