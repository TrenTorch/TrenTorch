// Figures for parts A and B: foundations and the programming model.
import * as m from '../model';
import {
	type Cell,
	type Frame,
	type Row,
	type VizConfig,
	bool,
	fmt,
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
const lanes = (f: (i: number) => Cell): Cell[] => Array.from({ length: 32 }, (_, i) => f(i));
const GB = 1e9;

export const vizCpuVsGpu: VizConfig = {
	id: 'cpu-vs-gpu',
	title: 'Two kinds of processor',
	illustrative: true,
	controls: [
		select(
			'work',
			'Workload',
			[
				['serial', 'One long dependent task'],
				['parallel', '10,000 independent tasks']
			],
			'parallel'
		)
	],
	compute(s) {
		const parallel = str(s, 'work') === 'parallel';
		const p = m.getProfile('T4');
		const cpuCores = 4,
			gpuLanes = p.sms * p.fp32PerSm,
			cpuT = 1,
			gpuT = 3; // a GPU thread is slower per task
		const tasks = parallel ? 10_000 : 1,
			chain = parallel ? 1 : 10; // serial: ten tasks, each needs the previous
		const waves = (n: number, w: number) => Math.ceil(n / w);
		const cpu = waves(tasks, cpuCores) * chain * cpuT,
			gpuTime = waves(tasks, gpuLanes) * chain * gpuT;
		const frame = (frac: number): Frame => ({
			rows: [
				{
					label: `CPU (${cpuCores} cores)`,
					cells: Array.from({ length: cpuCores }, (_, i) => ({
						state:
							i < Math.max(1, parallel ? cpuCores : 1) && frac < cpu / Math.max(cpu, gpuTime)
								? 'active'
								: 'idle',
						text: `${i + 1}`
					}))
				},
				{
					label: `GPU (${gpuLanes.toLocaleString('en-US')} lanes)`,
					cells: Array.from({ length: 32 }, (_, i) => ({
						state:
							(parallel ? true : i === 0) && frac < gpuTime / Math.max(cpu, gpuTime)
								? 'active'
								: 'idle'
					}))
				}
			],
			caption: parallel
				? 'With independent tasks the GPU lights up thousands of lanes at once.'
				: 'One dependent chain keeps only one GPU lane busy, and that lane is the slower one.'
		});
		return {
			panels: [
				{ kind: 'frames', frames: [frame(0), frame(0.5), frame(0.99)] },
				{
					kind: 'bars',
					title: 'Time to finish (arbitrary units)',
					bars: [
						{ label: 'CPU', segments: [{ value: cpu, tone: cpu <= gpuTime ? 'good' : 'neutral' }] },
						{
							label: 'GPU',
							segments: [{ value: gpuTime, tone: gpuTime < cpu ? 'good' : 'neutral' }]
						}
					]
				}
			],
			readouts: [
				{ label: 'CPU tasks/s', value: fmt(tasks / cpu) },
				{ label: 'GPU tasks/s', value: fmt(tasks / gpuTime) },
				{ label: 'Winner', value: cpu < gpuTime ? 'CPU' : 'GPU', tone: 'good' }
			],
			live: `CPU: ${cpuCores} tasks at a time, ${cpuT.toFixed(1)} s each. GPU: ${gpuLanes.toLocaleString('en-US')} tasks at a time, ${gpuT.toFixed(1)} s each. ${cpu < gpuTime ? 'The CPU' : 'The GPU'} finishes first.`,
			footnote:
				'The per-task times (1 s and 3 s) are teaching numbers; the lane count is the T4 spec.'
		};
	}
};

export const vizHostDevicePcie: VizConfig = {
	id: 'host-device-pcie',
	title: 'The expensive highway',
	controls: [
		range('mb', 'Data size', 1, 8192, 1, 1024, { log: true, format: (v) => `${fmt(v)} MB` }),
		gpu(),
		select(
			'gen',
			'PCIe generation',
			[
				['3', 'PCIe 3.0 (~12 GB/s)'],
				['4', 'PCIe 4.0 (~25 GB/s)'],
				['5', 'PCIe 5.0 (~50 GB/s)']
			],
			'4'
		),
		range('k', 'Chained kernels', 1, 10, 1, 1),
		toggle('keep', 'Keep data on device between kernels', false)
	],
	compute(s) {
		const p = P(s),
			D = num(s, 'mb') * 1e6,
			k = num(s, 'k'),
			pcie = ({ '3': 12, '4': 25, '5': 50 } as Record<string, number>)[str(s, 'gen')] * GB;
		const tIn = m.copyTime(D, pcie),
			tOut = tIn,
			tKernel = (2 * D) / (0.85 * m.peakBandwidth(p));
		const keep = bool(s, 'keep');
		const copies = keep ? 2 : 2 * k,
			total = keep ? tIn + k * tKernel + tOut : k * (tIn + tKernel + tOut);
		const slower = m.peakBandwidth(p) / pcie;
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Timeline (one bar, left to right)',
					bars: [
						{
							label: keep ? 'data stays on device' : 'copy for every kernel',
							segments: keep
								? [
										{ value: tIn, tone: 'memory', label: 'copy in' },
										{ value: k * tKernel, tone: 'compute', label: 'compute' },
										{ value: tOut, tone: 'memory', label: 'copy out' }
									]
								: Array.from({ length: k }, () => [
										{ value: tIn, tone: 'memory' as const, label: 'copy in' },
										{ value: tKernel, tone: 'compute' as const, label: 'compute' },
										{ value: tOut, tone: 'memory' as const, label: 'copy out' }
									]).flat(),
							note: fmtTime(total)
						}
					]
				}
			],
			readouts: [
				{ label: 'Copy in', value: fmtTime(tIn) },
				{ label: 'Compute (each)', value: fmtTime(tKernel) },
				{ label: 'Copy out', value: fmtTime(tOut) },
				{ label: 'Copy bars', value: String(copies), tone: keep ? 'good' : 'neutral' },
				{ label: 'PCIe vs on-device', value: `${fmt(slower)}x slower`, tone: 'bad' }
			],
			live: `Copy in: ${fmtTime(tIn)}. Compute: ${fmtTime(tKernel)}. Copy out: ${fmtTime(tOut)}. ${keep ? `With the data kept on the device there are ${copies} copies for ${k} kernels.` : `Without that there are ${copies} copies for ${k} kernels.`}`
		};
	}
};

const SIMT_PATTERNS: Record<string, (i: number) => number> = {
	positive: (i) => i + 1,
	alternating: (i) => (i % 2 ? i + 1 : -(i + 1)),
	random: (i) => [3, -7, 12, -1, 9, -4, 6, -8][(i * 5 + 3) % 8] * (1 + (i % 3))
};
export const vizSimtLockstep: VizConfig = {
	id: 'simt-lockstep',
	title: 'One instruction, thirty-two lanes',
	controls: [
		select('pattern', 'Data pattern', [
			['positive', 'all positive'],
			['alternating', 'alternating'],
			['random', 'random']
		])
	],
	compute(s) {
		const x = SIMT_PATTERNS[str(s, 'pattern')],
			prog = ['LD  r1, [in + i]', 'MAX r2, r1, 0', 'ST  [out + i], r2'];
		const mk = (step: number): Frame => {
			const r = (key: 'i' | 'r1' | 'r2') => ({
				label: key === 'i' ? 'i' : key,
				lanes: true,
				cells: lanes((i) => ({
					text:
						key === 'i'
							? String(i)
							: key === 'r1'
								? step >= 1
									? String(x(i))
									: ''
								: step >= 2
									? String(Math.max(x(i), 0))
									: '',
					state: step >= 1 && key !== 'i' ? 'active' : 'idle'
				}))
			});
			return {
				rows: [
					{
						label: 'program',
						cells: prog.map((t, i) => ({
							text: t,
							state: i === step - 1 ? 'active' : 'idle',
							title: t
						}))
					},
					r('i'),
					r('r1'),
					r('r2')
				],
				caption:
					step === 0
						? 'Before the first instruction.'
						: `Instruction ${step} of 3: ${prog[step - 1].split(/\s+/)[0]} executed by 32 of 32 lanes.`
			};
		};
		const f = [0, 1, 2, 3].map(mk);
		return {
			panels: [{ kind: 'frames', frames: f }],
			readouts: [
				{ label: 'Lanes issued', value: '32 of 32' },
				{ label: 'Instruction', value: '3 per warp' }
			],
			live: 'One instruction at a time goes to all 32 lanes; every lane holds its own register values and none is ahead of the others.'
		};
	}
};

const DIE_UNITS: Record<string, { name: string; text: string }> = {
	gigathread: {
		name: 'GigaThread Engine',
		text: 'The chip-level scheduler: it hands thread blocks to SMs as they free up.'
	},
	gpc: {
		name: 'GPC',
		text: 'A graphics processing cluster: a group of SMs sharing front-end hardware.'
	},
	sm: {
		name: 'SM',
		text: 'A streaming multiprocessor: four sub-partitions, a register file, shared memory / L1 and load-store units.'
	},
	subpartition: {
		name: 'Sub-partition',
		text: 'A warp scheduler with its own register file slice, FP32/INT32 cores, SFU and LD/ST units.'
	},
	l2: { name: 'L2 cache', text: 'The chip-wide cache between the SMs and DRAM.' },
	memctl: { name: 'Memory controller', text: 'Connects the die to HBM or GDDR memory chips.' }
};
export const vizGpuDieExplorer: VizConfig = {
	id: 'gpu-die-explorer',
	title: 'Zoom into the GPU',
	controls: [
		gpu('gpu', 'Profile', 'A100'),
		select('zoom', 'Zoom level', [
			['die', '1  Whole die'],
			['gpc', '2  One GPC'],
			['sm', '3  One SM'],
			['sub', '4  One sub-partition']
		]),
		select(
			'unit',
			'Unit (definition)',
			Object.entries(DIE_UNITS).map(([k, v]) => [k, v.name] as [string, string]),
			'sm'
		),
		range('grid', 'Blocks to launch', 4, 64, 1, 24)
	],
	compute(s) {
		const p = P(s),
			zoom = str(s, 'zoom'),
			smPerGpc = Math.ceil(p.sms / p.gpcs),
			sub = p.schedulersPerSm,
			coresPerSub = p.fp32PerSm / sub;
		let rows: Row[];
		if (zoom === 'die')
			rows = [
				{ label: 'GigaThread Engine', cells: [{ text: 'GigaThread', state: 'active' }] },
				{
					label: `${p.gpcs} GPCs`,
					cells: Array.from({ length: p.gpcs }, (_, i) => ({ text: `GPC${i}`, tint: 1 as const }))
				},
				{
					label: 'L2 + memory controllers',
					cells: [
						{ text: `${p.l2MB} MB L2`, tint: 3 },
						{ text: `${p.memBusBits}-bit bus`, tint: 4 }
					]
				},
				{ label: 'PCIe', cells: [{ text: `Gen ${p.pcieGen}`, tint: 4 }] }
			];
		else if (zoom === 'gpc')
			rows = [
				{
					label: `GPC (about ${smPerGpc} SMs)`,
					cells: Array.from({ length: smPerGpc }, (_, i) => ({ text: `SM${i}`, tint: 1 as const }))
				}
			];
		else if (zoom === 'sm')
			rows = [
				{
					label: `${sub} sub-partitions`,
					cells: Array.from({ length: sub }, (_, i) => ({ text: `SP${i}`, tint: 0 as const }))
				},
				{ label: 'Shared memory / L1', cells: [{ text: `${p.smemPerSmKB} KB`, tint: 2 }] },
				{ label: 'Registers', cells: [{ text: `${p.regsPerSm / 1024}K x 32-bit`, tint: 0 }] }
			];
		else
			rows = [
				{ label: 'Warp scheduler', cells: [{ text: '1 issue / cycle', state: 'active' }] },
				{
					label: `${coresPerSub} FP32 lanes`,
					lanes: false,
					cells: Array.from({ length: coresPerSub }, () => ({ state: 'active' as const }))
				},
				{ label: 'Other', cells: [{ text: 'INT32' }, { text: 'SFU' }, { text: 'LD/ST' }] }
			];
		const cap = p.sms * 2,
			blocks = num(s, 'grid');
		const frames: Frame[] = [0, 0.34, 0.67, 1].map((q) => ({
			rows: [
				{
					label: 'SMs (blocks resident)',
					cells: Array.from({ length: Math.min(p.sms, 48) }, (_, i) => ({
						text: String(
							Math.floor(
								(blocks * q) / Math.min(p.sms, 48) +
									(i < (blocks * q) % Math.min(p.sms, 48) ? 1 : 0)
							)
						),
						state: i < Math.ceil((blocks * q) / 2) ? 'active' : 'idle'
					}))
				}
			],
			caption: `GigaThread has dispatched ${Math.round(blocks * q)} of ${blocks} blocks (capacity ${cap} here).`
		}));
		const u = DIE_UNITS[str(s, 'unit')];
		return {
			panels: [
				{
					kind: 'frames',
					title: `${m.getProfile(str(s, 'gpu') as m.GpuName).name}: ${zoom}`,
					frames: [
						{ rows, caption: `Breadcrumb: GPU > GPC > SM > Sub-partition (viewing ${zoom}).` }
					]
				},
				{ kind: 'text', title: u.name, text: u.text },
				{ kind: 'frames', title: 'Launch a grid', frames }
			],
			readouts: [
				{ label: 'GPCs', value: String(p.gpcs) },
				{ label: 'SMs', value: String(p.sms) },
				{ label: 'FP32 cores / SM', value: String(p.fp32PerSm) },
				{ label: 'Cores / sub-partition', value: String(coresPerSub) }
			],
			live: `${p.name}: ${p.gpcs} GPCs, ${p.sms} SMs, ${p.fp32PerSm} FP32 cores per SM in ${sub} sub-partitions.`
		};
	}
};

export const vizMemoryLadder: VizConfig = {
	id: 'memory-ladder',
	title: 'The memory pyramid',
	controls: [
		gpu(),
		select(
			'state',
			'Where does the value live?',
			[
				['global', 'Only in global memory (cold)'],
				['l2', 'Also in L2'],
				['l1', 'Also in L1 (warm)']
			],
			'global'
		),
		toggle('bench', 'Copy-kernel benchmark', false)
	],
	compute(s) {
		const p = P(s),
			lat = p.latencyCycles,
			st = str(s, 'state'),
			bench = bool(s, 'bench');
		const levels = [
			['Registers', 'register', 0, 'thread'],
			['Shared memory', 'shared', 1, 'block'],
			['L1', 'l1', 2, 'SM'],
			['L2', 'l2', 3, 'chip'],
			['Global (DRAM)', 'dram', 4, 'chip']
		] as const;
		const where = st === 'global' ? 'dram' : st;
		const cost = lat[where === 'dram' ? 'dram' : (where as 'l1' | 'l2')];
		const cold = lat.dram,
			warm = lat.l1;
		const sizes = [
			`${p.regsPerSm / 1024}K regs/SM`,
			`${p.smemPerSmKB} KB/SM`,
			`${p.smemPerSmKB} KB/SM (shared with L1)`,
			`${p.l2MB} MB`,
			`${m.getProfile(str(s, 'gpu') as m.GpuName).memBwGBs} GB/s`
		];
		const eff = 0.85;
		const panels: import('./types').Panel[] = [
			{
				kind: 'frames',
				title: 'A load travels down until it hits',
				frames: levels
					.map((_, depth) => ({
						rows: [
							{
								label: 'level',
								cells: levels.map(([n, k, t, sc], i) => ({
									text: n,
									tint: t as 0 | 1 | 2 | 3 | 4,
									state: (i === depth ? 'touch' : i < depth ? 'done' : 'idle') as Cell['state'],
									title: `${n}: ${lat[k]} cycles, scope ${sc}`
								}))
							}
						],
						caption:
							depth === 0
								? 'The thread asks for a value.'
								: `Checked ${levels[depth][0]}${levels[depth][1] === where || (where === 'dram' && levels[depth][1] === 'dram') ? ': hit.' : ': miss.'}`
					}))
					.slice(0, where === 'dram' ? 5 : where === 'l2' ? 4 : 3)
			},
			{
				kind: 'bars',
				title: 'Latency (cycles)',
				bars: levels.map(([n, k, t]) => ({
					label: n,
					segments: [{ value: lat[k], tone: `tint${t}` as 'tint0' }],
					note: `${lat[k]} cycles`
				}))
			}
		];
		if (bench)
			panels.push({
				kind: 'bars',
				title: 'Copy-kernel benchmark',
				unit: 'GB/s',
				bars: [
					{ label: 'Datasheet peak', segments: [{ value: p.memBwGBs, tone: 'neutral' }] },
					{
						label: 'Achieved (eta = 0.85)',
						segments: [{ value: p.memBwGBs * eff, tone: 'good' }],
						note: `${fmt(p.memBwGBs * eff)} GB/s (85%)`
					}
				]
			});
		return {
			panels,
			readouts: [
				{ label: 'This load', value: `${cost} cycles` },
				{ label: 'Cold load', value: `${cold} cycles` },
				{ label: 'Warm load', value: `${warm} cycles` },
				{ label: 'Cold / warm', value: `${fmt(cold / warm)}x`, tone: 'bad' },
				{ label: 'Capacities', value: sizes[3] }
			],
			live: `The load is served from ${where} in ${cost} cycles; a cold load costs ${fmt(cold / warm)} times a warm one.`,
			footnote: p.latencyIllustrative ? 'Latencies for this profile are illustrative.' : undefined
		};
	}
};

export const vizScopeVisibility: VizConfig = {
	id: 'scope-visibility',
	title: 'Who can see what?',
	controls: [
		range('block', 'Selected block', 0, 1, 1, 1),
		range('thread', 'Selected thread', 0, 5, 1, 2),
		select('op', 'Operation', ['read', 'write']),
		select(
			'target',
			'Target',
			[
				['regs', 'Registers of another thread'],
				['mine', 'Registers of this thread'],
				['sharedSame', "This block's shared memory"],
				['sharedOther', "The other block's shared memory"],
				['global', 'Global memory']
			],
			'sharedOther'
		)
	],
	compute(s) {
		const b = num(s, 'block'),
			t = num(s, 'thread'),
			target = str(s, 'target'),
			op = str(s, 'op');
		const reach = { mine: true, regs: false, sharedSame: true, sharedOther: false, global: true }[
			target as 'mine'
		];
		const cells = (blk: number): Cell[] =>
			Array.from({ length: 6 }, (_, i) => ({
				text: `t${i}`,
				state: blk === b && i === t ? 'active' : blk === b ? 'done' : 'idle',
				title: `block ${blk} thread ${i} registers`
			}));
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								{ label: 'Block 0 threads', cells: cells(0) },
								{ label: 'Block 1 threads', cells: cells(1) },
								{
									label: 'Shared slabs',
									cells: [0, 1].map((blk) => ({
										text: `shared ${blk}`,
										tint: 2 as const,
										state: blk === b ? ('done' as const) : ('error' as const),
										title: blk === b ? 'visible to this block' : 'not visible'
									}))
								},
								{ label: 'Global', cells: [{ text: 'global memory', tint: 4, state: 'done' }] }
							],
							caption: `Thread ${t} of block ${b}: green = reachable, red with a cross = not visible.`
						}
					]
				}
			],
			readouts: [
				{
					label: `${op} ${target}`,
					value: reach ? 'allowed' : 'not visible',
					tone: reach ? 'good' : 'bad'
				}
			],
			live: `Thread ${t} of block ${b} ${reach ? 'can' : 'cannot'} ${op} ${{ mine: 'its own registers', regs: "another thread's registers", sharedSame: "its block's shared memory", sharedOther: "the other block's shared memory", global: 'global memory' }[target as 'mine']}.`
		};
	}
};

export const vizIndexCalculator: VizConfig = {
	id: 'index-calculator',
	title: 'Who am I?',
	controls: [
		range('n', 'N (elements)', 1, 3e9, 1, 6, {
			log: true,
			format: (v) => Math.round(v).toLocaleString('en-US')
		}),
		range('bd', 'blockDim.x', 1, 1024, 1, 4),
		range('pb', 'Pinned thread: blockIdx.x', 0, 9, 1, 1),
		range('pt', 'Pinned thread: threadIdx.x', 0, 1023, 1, 2),
		toggle('bounds', 'Show bounds check', true),
		toggle('wide', '32-bit index (wraps at 2^31)', false)
	],
	compute(s) {
		const N = Math.round(num(s, 'n')),
			B = Math.round(num(s, 'bd')),
			G = Math.ceil(N / B),
			pb = Math.min(num(s, 'pb'), G - 1),
			pt = Math.min(num(s, 'pt'), B - 1);
		const idx = pb * B + pt,
			wrapped = bool(s, 'wide') ? m.wrap32(idx) : idx,
			outside = wrapped >= N || wrapped < 0;
		const shown = Math.min(G, 6);
		const rows: Row[] = Array.from({ length: shown }, (_, b) => ({
			label: `block ${b}`,
			cells: Array.from({ length: Math.min(B, 32) }, (_, t) => {
				const i = b * B + t;
				return {
					text: String(t),
					state:
						b === pb && t === pt
							? ('touch' as const)
							: bool(s, 'bounds') && i >= N
								? ('masked' as const)
								: ('active' as const),
					title: `idx ${i}${i >= N ? ' (outside)' : ''}`
				};
			})
		}));
		const idle = G * B - N;
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [
								...rows,
								...(G > shown
									? [{ label: '...', cells: [{ text: `${G - shown} more blocks` }] }]
									: [])
							],
							caption: bool(s, 'wide')
								? 'Wrapped index shown in the readouts below.'
								: 'Filled = a thread with work, hatched = an idle tail thread.'
						}
					]
				}
			],
			readouts: [
				{ label: 'gridDim.x', value: G.toLocaleString('en-US') },
				{ label: 'idx', value: `${pb} x ${B} + ${pt} = ${idx.toLocaleString('en-US')}` },
				{
					label: bool(s, 'wide') ? 'idx as int32' : 'status',
					value: bool(s, 'wide')
						? wrapped.toLocaleString('en-US')
						: outside
							? 'outside the array'
							: 'in range',
					tone: outside ? 'bad' : 'good'
				},
				{ label: 'Idle tail threads', value: idle.toLocaleString('en-US') }
			],
			live: `Thread ${pt} of block ${pb} maps to element ${wrapped.toLocaleString('en-US')}${outside ? `, which is outside the array (N = ${N.toLocaleString('en-US')}); it does nothing.` : '.'}`
		};
	}
};

export const vizGridBuilder: VizConfig = {
	id: 'grid-builder',
	title: 'Covering a matrix',
	controls: [
		range('rows', 'Matrix rows', 4, 24, 1, 10),
		range('cols', 'Matrix cols', 4, 24, 1, 13),
		select(
			'shape',
			'Block shape (x by y)',
			[
				['8x8', '8 x 8'],
				['16x16', '16 x 16'],
				['32x8', '32 x 8'],
				['32x32', '32 x 32'],
				['4x4', '4 x 4']
			],
			'8x8'
		),
		toggle('swap', 'Swapped mapping (x -> row, y -> col)', false),
		range('pr', 'Probe row', 0, 23, 1, 3),
		range('pc', 'Probe col', 0, 23, 1, 9)
	],
	compute(s) {
		const R = num(s, 'rows'),
			C = num(s, 'cols'),
			[bx, by] = str(s, 'shape').split('x').map(Number),
			swap = bool(s, 'swap');
		const gx = Math.ceil((swap ? R : C) / bx),
			gy = Math.ceil((swap ? C : R) / by);
		const rows = Array.from({ length: gy * by }, (_, r) => ({
			label: r < R ? `row ${r}` : 'padding',
			cells: Array.from({ length: Math.min(gx * bx, 40) }, (_, c) => ({
				state: r >= R || c >= C ? ('masked' as const) : ('idle' as const),
				tint: ((Math.floor(r / by) + Math.floor(c / bx)) % 5) as 0 | 1 | 2 | 3 | 4,
				text: r < R && c < C ? '' : undefined,
				title:
					r < R && c < C
						? `block (${Math.floor(c / bx)}, ${Math.floor(r / by)}) thread (${c % bx}, ${r % by})`
						: 'out-of-range thread: idles'
			}))
		})).slice(0, 26);
		const pr = Math.min(num(s, 'pr'), R - 1),
			pc = Math.min(num(s, 'pc'), C - 1);
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows,
							caption:
								'Block borders are where the tint changes; hatched cells are threads past the matrix edge.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Grid', value: `${gx} x ${gy} blocks` },
				{ label: 'Probe cell', value: `row ${pr}, col ${pc}` },
				{ label: 'row*W + col', value: `${pr} x ${C} + ${pc} = ${pr * C + pc}` },
				{
					label: 'Owner block',
					value: `(${Math.floor((swap ? pr : pc) / bx)}, ${Math.floor((swap ? pc : pr) / by)})`
				},
				{
					label: 'Warp reads',
					value: swap ? 'a column (stride W): slow, see D1' : 'a row (contiguous): fast',
					tone: swap ? 'bad' : 'good'
				}
			],
			live: `${gx * gy} blocks cover the ${R} by ${C} matrix; ${gx * bx * gy * by - R * C} threads fall outside it. ${swap ? 'The swapped mapping is legal but makes each warp walk down a column.' : 'x maps to the column, so a warp reads a contiguous row segment.'}`
		};
	}
};

export const vizBlockScheduler: VizConfig = {
	id: 'block-scheduler',
	title: 'Blocks find a home',
	controls: [
		range('sms', '#SMs', 4, 132, 1, 108),
		range('bps', 'Blocks per SM', 1, 16, 1, 8),
		range('grid', 'Grid size (blocks)', 1, 4000, 1, 1000),
		toggle('rand', 'Random block times', false),
		range('step', 'Time step', 0, 100, 1, 100, { hint: 'scrub through the schedule' })
	],
	compute(s) {
		const sms = num(s, 'sms'),
			bps = num(s, 'bps'),
			grid = num(s, 'grid'),
			r = m.simulateBlocks({
				sms,
				blocksPerSm: bps,
				grid,
				times: m.blockTimes(Math.min(grid, 4096), bool(s, 'rand'))
			});
		const t = (num(s, 'step') / 100) * r.makespan,
			show = Math.min(sms, 24);
		const cells = Array.from({ length: show * Math.min(bps, 4) }, (_, i) => {
			const sm = Math.floor(i / Math.min(bps, 4)),
				slot = i % Math.min(bps, 4);
			const e = r.events.find((x) => x.sm === sm && x.slot === slot && x.start <= t && t < x.end);
			return {
				text: e ? String(e.block) : '',
				state: e ? ('active' as const) : ('idle' as const),
				title: e ? `block ${e.block} on SM ${sm}` : `SM ${sm} slot ${slot}: free`
			};
		});
		const eff = m.waveEfficiency(grid, sms * bps);
		return {
			panels: [
				{
					kind: 'frames',
					title: `First ${show} SMs (up to 4 slots shown) at t = ${fmt(t, 3)}`,
					frames: [
						{
							rows: [{ label: 'SM slots', cells }],
							caption: `Finishing order starts ${r.finishOrder.slice(0, 8).join(', ')}${bool(s, 'rand') ? ' (not sorted: blocks never finish in order)' : ''}.`
						}
					]
				}
			],
			readouts: [
				{ label: 'Waves', value: String(r.waves) },
				{
					label: 'Utilization',
					value: pct(r.utilization),
					tone: r.utilization > 0.9 ? 'good' : 'bad'
				},
				{ label: 'Wave efficiency', value: pct(eff) },
				{ label: 'Idle slot-time (last wave)', value: fmt(r.idleInLastWave, 3) }
			],
			live: `${grid} blocks on ${sms * bps} resident slots take ${r.waves} waves at ${pct(r.utilization)} utilization.`
		};
	}
};

export const vizWarpFormation: VizConfig = {
	id: 'warp-formation',
	title: 'How a block is sliced into warps',
	controls: [
		range('bx', 'blockDim.x', 1, 64, 1, 8),
		range('by', 'blockDim.y', 1, 32, 1, 8),
		select(
			'preset',
			'Preset',
			[
				['', 'custom'],
				['256x1', '256 x 1'],
				['16x16', '16 x 16'],
				['8x8', '8 x 8'],
				['33x1', '33 x 1'],
				['32x4', '32 x 4']
			],
			''
		)
	],
	compute(s) {
		let bx = num(s, 'bx'),
			by = num(s, 'by');
		const pre = str(s, 'preset');
		if (pre) [bx, by] = pre.split('x').map(Number);
		const T = bx * by,
			W = m.warpsPerBlock(T);
		const rows: Row[] = Array.from({ length: Math.min(by, 16) }, (_, y) => ({
			label: `y = ${y}`,
			cells: Array.from({ length: Math.min(bx, 40) }, (_, x) => {
				const tid = x + y * bx;
				return {
					text: String(Math.floor(tid / 32)),
					tint: (Math.floor(tid / 32) % 5) as 0 | 1 | 2 | 3 | 4,
					title: `tid ${tid}, warp ${Math.floor(tid / 32)}, lane ${tid % 32}`
				};
			})
		}));
		const lin: Cell[] = Array.from({ length: Math.min(T, 96) }, (_, tid) => ({
			text: tid % 32 === 0 ? `w${Math.floor(tid / 32)}` : '',
			tint: (Math.floor(tid / 32) % 5) as 0 | 1 | 2 | 3 | 4,
			title: `tid ${tid}`
		}));
		const last = T % 32;
		return {
			panels: [
				{
					kind: 'frames',
					frames: [
						{
							rows: [...rows, { label: 'Linearized order', cells: lin }],
							caption: last ? `Partial warp: ${last} of 32 lanes used.` : 'Every warp is full.'
						}
					]
				}
			],
			readouts: [
				{ label: 'Threads', value: String(T) },
				{ label: 'Warps', value: String(W) },
				{
					label: 'Lane utilization',
					value: pct(m.laneUtilization(T)),
					tone: T % 32 ? 'bad' : 'good'
				},
				{
					label: 'Rows per warp',
					value: bx >= 32 ? '1 (or less)' : String(Math.min(by, Math.floor(32 / bx)))
				}
			],
			live: `A ${bx} by ${by} block has ${T} threads in ${W} warp${W === 1 ? '' : 's'}; lane utilization ${pct(m.laneUtilization(T))}. ${bx < 32 ? `A warp spans ${Math.floor(32 / bx)} rows.` : 'A warp stays inside one row, so its memory access is contiguous.'}`
		};
	}
};

export const vizLatencyHiding: VizConfig = {
	id: 'latency-hiding',
	title: 'Never wait',
	controls: [
		range('w', 'Resident warps', 1, 32, 1, 1),
		range('lat', 'Memory latency (ticks)', 4, 60, 1, 24),
		range('c', 'Compute per load (instructions)', 1, 8, 1, 3)
	],
	compute(s) {
		const W = num(s, 'w'),
			L = num(s, 'lat'),
			c = num(s, 'c'),
			T = 72;
		const sim = m.simulateLatencyHiding({ warps: W, latency: L, compute: c, ticks: T });
		const rows: Row[] = sim.grid.slice(0, 16).map((g, i) => ({
			label: `warp ${i}`,
			cells: g.map((st) => ({
				state:
					st === 'issue'
						? ('active' as const)
						: st === 'wait'
							? ('stalled' as const)
							: ('idle' as const)
			}))
		}));
		const issue: Row = {
			label: 'issue slot',
			cells: sim.issued.map((w) => ({
				text: w >= 0 ? String(w % 10) : '',
				state: w >= 0 ? ('active' as const) : ('masked' as const)
			}))
		};
		const need = m.warpsNeeded(L, c, 1);
		return {
			panels: [
				{
					kind: 'frames',
					title: 'One scheduler, time left to right',
					frames: [
						{
							rows: [...rows, issue],
							caption:
								'Orange = issuing, blue clock = waiting for memory, hatched issue slot = idle.'
						}
					]
				}
			],
			readouts: [
				{
					label: 'Issue utilization',
					value: pct(sim.utilization),
					tone: sim.utilization > 0.9 ? 'good' : 'bad'
				},
				{ label: 'Idle slots', value: `${sim.idle} of ${T}` },
				{ label: 'Warps to saturate', value: fmt(need, 3) }
			],
			live: `${W} warp${W === 1 ? '' : 's'} keep the scheduler ${pct(sim.utilization)} busy. Saturation needs about ${fmt(need, 3)} warps (1 + latency / compute).`,
			footnote: 'A teaching model: one instruction per tick, latency in ticks.'
		};
	},
	illustrative: true
};

export const vizOccupancyCalc: VizConfig = {
	id: 'occupancy-calc',
	title: 'What limits me?',
	controls: [
		range('bs', 'Block size', 32, 1024, 32, 256),
		range('regs', 'Registers / thread', 16, 255, 1, 40),
		range('smem', 'Shared memory / block (KB)', 0, 100, 1, 0),
		gpu('gpu', 'Profile', 'A100'),
		toggle('round', 'Show granularity rounding', true)
	],
	modes: { staircase: { title: 'Register staircase' } },
	compute(s, ctx) {
		const p = P(s),
			q = (g: m.GpuName) =>
				m.occupancy(m.getProfile(g), num(s, 'bs'), num(s, 'regs'), num(s, 'smem') * 1024, {
					rounding: bool(s, 'round')
				});
		const o = q(str(s, 'gpu') as m.GpuName);
		const panels: import('./types').Panel[] = [
			{
				kind: 'bars',
				title: 'Blocks that fit per SM, by resource (smallest wins)',
				bars: [
					['threads', o.byThreads],
					['registers', o.byRegs],
					['shared memory', o.bySmem],
					['block slots', o.bySlots]
				].map(([k, v]) => ({
					label: `${k}${o.limiter === k ? '  <- limiter' : ''}`,
					segments: [
						{
							value: Number.isFinite(Number(v)) ? Number(v) : p.maxBlocksPerSm,
							tone: o.limiter === k ? ('bad' as const) : ('tint3' as const)
						}
					],
					note: Number.isFinite(Number(v)) ? String(v) : 'no limit'
				}))
			}
		];
		if (ctx.mode === 'staircase') {
			const stair = (g: m.GpuName) =>
				m.occupancyStaircase(
					m.getProfile(g),
					num(s, 'bs'),
					num(s, 'smem') * 1024,
					bool(s, 'round')
				);
			const other = (str(s, 'gpu') === 'A100' ? 'T4' : 'A100') as m.GpuName;
			panels.push({
				kind: 'line',
				title: 'Occupancy against registers per thread',
				xLabel: 'registers per thread',
				yLabel: 'occupancy',
				yMax: 1,
				series: [
					{
						name: str(s, 'gpu'),
						tone: 'compute',
						points: stair(str(s, 'gpu') as m.GpuName).map(
							(x) => [x.regs, x.occupancy] as [number, number]
						)
					},
					{
						name: other,
						tone: 'memory',
						dashed: true,
						points: stair(other).map((x) => [x.regs, x.occupancy] as [number, number])
					}
				],
				point: { x: num(s, 'regs'), y: o.occupancy, label: 'your setting' }
			});
		}
		return {
			panels,
			readouts: [
				{ label: 'Occupancy', value: pct(o.occupancy) },
				{ label: 'Blocks / SM', value: String(o.blocks) },
				{ label: 'Threads / SM', value: String(o.threadsPerSm) },
				{ label: 'Limiter', value: o.limiter, tone: 'bad' },
				{
					label: 'Registers / thread',
					value: bool(s, 'round')
						? `${num(s, 'regs')} -> ${o.effectiveRegs} (rounded)`
						: String(num(s, 'regs'))
				}
			],
			live: `${o.blocks} blocks of ${num(s, 'bs')} threads fit per SM; ${o.limiter} limits it, giving ${pct(o.occupancy)} occupancy on the ${str(s, 'gpu')}.`
		};
	}
};

export const vizHostTimeline: VizConfig = {
	id: 'host-timeline',
	title: 'Who is waiting for whom?',
	controls: [
		range('k', 'Kernel launches', 1, 4, 1, 2),
		toggle('sync', 'Insert cudaDeviceSynchronize after launch', false),
		toggle('copy', 'Use blocking cudaMemcpy', false)
	],
	compute(s) {
		const r = m.simulateHost({
			launches: num(s, 'k'),
			kernelTime: 10,
			launchCost: 0.6,
			sync: bool(s, 'sync'),
			blockingCopy: bool(s, 'copy'),
			copyTime: 2
		});
		const lane = (name: 'host' | 'device') => ({
			label: name === 'host' ? 'Host' : 'Device',
			segments: [] as { value: number; tone: import('./types').Tone; label: string }[]
		});
		const out = [lane('host'), lane('device')];
		for (const l of out) {
			let t = 0;
			for (const e of r.events.filter((x) => (x.lane === 'host') === (l.label === 'Host'))) {
				if (e.start > t) l.segments.push({ value: e.start - t, tone: 'neutral', label: 'idle' });
				l.segments.push({
					value: e.end - e.start,
					tone: e.stale
						? 'bad'
						: e.kind === 'wait'
							? 'launch'
							: e.kind === 'kernel'
								? 'compute'
								: 'memory',
					label: e.label
				});
				t = e.end;
			}
		}
		return {
			panels: [
				{
					kind: 'bars',
					title: 'Timeline (left to right)',
					max: r.total,
					bars: out.map((l) => ({
						label: l.label,
						segments: l.segments,
						note: l.segments
							.map((x) => x.label)
							.filter((x) => x !== 'idle')
							.join(', ')
					}))
				}
			],
			readouts: [
				{ label: 'Total', value: fmt(r.total, 3) },
				{
					label: 'Host reads result',
					value: r.stale ? 'STALE data (kernel still running)' : 'after the kernel finished',
					tone: r.stale ? 'bad' : 'good'
				}
			],
			live: r.stale
				? 'The host printed the result before the kernel finished: it read stale data. Launches return immediately; add a synchronize.'
				: 'The host waited for the kernel before reading the result.',
			illustrative: undefined,
			footnote: 'Teaching units: a launch costs 0.6, a kernel 10.'
		};
	},
	illustrative: true
};

export const vizPerfCalculator: VizConfig = {
	id: 'perf-calculator',
	title: 'Predict before you run',
	controls: [
		gpu(),
		range('bpe', 'Bytes per element', 1, 64, 1, 8),
		range('fpe', 'FLOPs per element', 0, 2000, 1, 1),
		range('n', 'N (elements)', 1e3, 1e10, 1, 2 ** 28, {
			log: true,
			format: (v) => v.toExponential(2)
		}),
		range('etaM', 'eta_m (memory)', 0.3, 1, 0.01, 0.85),
		range('etaC', 'eta_c (compute)', 0.3, 1, 0.01, 0.8),
		toggle('host', 'Data starts on host (adds PCIe)', false),
		range('k', 'Kernels run (k)', 1, 8, 1, 1)
	],
	compute(s) {
		const p = P(s),
			N = num(s, 'n'),
			bytes = num(s, 'bpe') * N,
			flops = num(s, 'fpe') * N,
			k = num(s, 'k');
		const t = m.timeModel({
			bytes,
			flops,
			peakFlops: m.peakFp32(p),
			bw: m.peakBandwidth(p),
			etaM: num(s, 'etaM'),
			etaC: num(s, 'etaC'),
			launchSeconds: 5e-6
		});
		const pcie = bool(s, 'host') ? 2 * m.copyTime(bytes / 2, p.pcieGBs * 1e9) : 0; // half the bytes go in, half come out
		const gpuTotal = pcie + k * t.total;
		const cpu = (k * bytes) / 50e9;
		const roof = m.attainable(m.peakFp32(p), m.peakBandwidth(p), t.ai);
		return {
			panels: [
				{
					kind: 'bars',
					title: 'The receipt: one kernel',
					unit: '',
					bars: [
						{
							label: 'memory term',
							segments: [{ value: t.tMem, tone: 'memory' }],
							note: fmtTime(t.tMem)
						},
						{
							label: 'compute term',
							segments: [{ value: t.tCompute, tone: 'compute' }],
							note: fmtTime(t.tCompute)
						},
						{
							label: 'launch',
							segments: [{ value: t.tLaunch, tone: 'launch' }],
							note: fmtTime(t.tLaunch)
						},
						...(pcie
							? [
									{
										label: 'PCIe (in + out)',
										segments: [{ value: pcie, tone: 'tint4' as const }],
										note: fmtTime(pcie)
									}
								]
							: [])
					]
				}
			],
			readouts: [
				{ label: 't_mem', value: fmtTime(t.tMem) },
				{ label: 't_compute', value: fmtTime(t.tCompute) },
				{ label: 't_launch', value: fmtTime(t.tLaunch) },
				{ label: 'Bound', value: t.bound, tone: 'bad' },
				{ label: 'AI', value: `${fmt(t.ai)} FLOP/B` },
				{ label: '% of roofline', value: pct(flops / t.total / roof) },
				{
					label: 'Memory / compute',
					value: Number.isFinite(t.ratio) ? `${fmt(t.ratio)}x` : 'no compute'
				},
				...(bool(s, 'host')
					? [
							{
								label: `GPU vs CPU (k = ${k})`,
								value: `${fmtTime(gpuTotal)} vs ${fmtTime(cpu)}: ${gpuTotal < cpu ? 'GPU wins' : 'CPU wins'}`,
								tone: (gpuTotal < cpu ? 'good' : 'bad') as 'good' | 'bad'
							}
						]
					: [])
			],
			live: `Memory term ${fmtTime(t.tMem)}, compute term ${fmtTime(t.tCompute)}, launch ${fmtTime(t.tLaunch)}. ${t.bound === 'memory' ? 'Memory-bound.' : 'Compute-bound.'}`,
			footnote: 'CPU comparison assumes 50 GB/s host memory bandwidth (an illustrative figure).'
		};
	}
};

export const vizWorkSpan: VizConfig = {
	id: 'work-span',
	title: 'How parallel is this problem?',
	controls: [
		select('preset', 'Preset', [
			['add', 'Array add (independent)'],
			['tree', 'Tree sum'],
			['fib', 'Fibonacci chain']
		]),
		range('n', 'N', 2, 64, 1, 16),
		range('p', 'Processors p', 1, 64, 1, 4)
	],
	compute(s) {
		const N = num(s, 'n'),
			p = num(s, 'p'),
			preset = str(s, 'preset');
		const levels: number[] =
			preset === 'add'
				? [N]
				: preset === 'fib'
					? Array(N).fill(1)
					: (() => {
							const l: number[] = [];
							let n = N;
							while (n > 1) {
								l.push(Math.floor(n / 2));
								n = Math.ceil(n / 2);
							}
							return l.length ? l : [0];
						})();
		const work = levels.reduce((a, b) => a + b, 0),
			span = levels.length,
			par = m.parallelism(work, span),
			lower = m.parallelTimeLowerBound(work, span, p);
		const steps = levels.flatMap((count) => {
			const out = [];
			let left = count;
			while (left > 0) {
				const run = Math.min(left, p);
				out.push(run);
				left -= run;
			}
			return out.length ? out : [0];
		});
		let done = 0;
		const frames: Frame[] = steps.map((run, i) => {
			done += run;
			return {
				rows: [
					{
						label: 'Level sizes',
						cells: levels.map((c, j) => ({
							text: String(c),
							state:
								j <= Math.floor((i * levels.length) / steps.length)
									? ('active' as const)
									: ('idle' as const)
						}))
					},
					{
						label: `p = ${p}`,
						cells: Array.from({ length: Math.min(p, 32) }, (_, j) => ({
							state: j < run ? ('active' as const) : ('idle' as const)
						}))
					}
				],
				caption: `Step ${i + 1}: ${run} operation${run === 1 ? '' : 's'} run in parallel (${done} of ${work} done).`
			};
		});
		return {
			panels: [{ kind: 'frames', frames }],
			readouts: [
				{ label: 'Work W', value: String(work) },
				{ label: 'Span S', value: String(span) },
				{ label: 'Parallelism W/S', value: fmt(par), tone: par < 2 ? 'bad' : 'good' },
				{ label: 'Time on p', value: `>= ${fmt(lower)}` }
			],
			live: `Work ${work}, span ${span}, parallelism ${fmt(par)}; on ${p} processors the time is at least ${fmt(lower)} steps${preset === 'fib' ? ': a dependency chain stays at parallelism 1 however large p is.' : '.'}`
		};
	}
};

export const vizIssueSlots: VizConfig = {
	id: 'issue-slots',
	title: 'ILP or more warps?',
	controls: [
		range('w', 'Warps per scheduler', 1, 16, 1, 4),
		select('ilp', 'ILP per thread', ['1', '2', '4'], '1'),
		range('lat', 'Memory latency (cycles)', 50, 600, 10, 400),
		range('c', 'Compute instructions between loads', 1, 16, 1, 3),
		gpu('gpu', 'Profile', 'A100')
	],
	compute(s) {
		const p = P(s),
			W = num(s, 'w'),
			ilp = Number(str(s, 'ilp')),
			L = num(s, 'lat'),
			c = num(s, 'c'),
			cpi = p.fp32LanesPerSubpartition === 16 ? 2 : 1;
		const util = m.issueSlotUtilization(W, ilp, L, c, cpi),
			need = m.warpsNeeded(L, c, cpi),
			cap = p.maxWarpsPerSm / p.schedulersPerSm;
		const sim = m.simulateLatencyHiding({
			warps: W,
			latency: Math.round(L / cpi / 8),
			compute: c * ilp,
			ticks: 64
		});
		return {
			panels: [
				{
					kind: 'frames',
					title: 'Issue slots of one sub-partition scheduler (scaled)',
					frames: [
						{
							rows: [
								{
									label: 'issue slot',
									cells: sim.issued.map((w) => ({
										text: w >= 0 ? String(w % 10) : '',
										state: w >= 0 ? ('active' as const) : ('masked' as const)
									}))
								}
							],
							caption: `An FP32 warp instruction occupies a ${p.fp32LanesPerSubpartition}-lane sub-partition for ${cpi} cycle${cpi === 1 ? '' : 's'}.`
						}
					]
				},
				{
					kind: 'bars',
					title: 'Effective warps in flight',
					bars: [
						{
							label: 'warps x ILP',
							segments: [{ value: W * ilp, tone: 'compute' }],
							note: String(W * ilp)
						},
						{
							label: 'needed (1 + L / (c x CPI))',
							segments: [{ value: need, tone: 'bad' }],
							note: fmt(need)
						},
						{
							label: 'hardware limit (warps)',
							segments: [{ value: cap, tone: 'neutral' }],
							note: String(cap)
						}
					]
				}
			],
			readouts: [
				{ label: 'Issue-slot utilization', value: pct(util), tone: util >= 0.99 ? 'good' : 'bad' },
				{ label: 'Warps needed (B3)', value: fmt(need) },
				{
					label: 'Latency-bound?',
					value: need > cap * ilp ? 'yes, at any occupancy' : 'no',
					tone: need > cap * ilp ? 'bad' : 'good'
				}
			],
			live: `${W} warps with ILP ${ilp} fill ${pct(util)} of the issue slots; the B3 formula asks for ${fmt(need)} warps per scheduler.`
		};
	}
};

export const partAB: VizConfig[] = [
	vizCpuVsGpu,
	vizHostDevicePcie,
	vizSimtLockstep,
	vizGpuDieExplorer,
	vizMemoryLadder,
	vizScopeVisibility,
	vizIndexCalculator,
	vizGridBuilder,
	vizBlockScheduler,
	vizWarpFormation,
	vizLatencyHiding,
	vizOccupancyCalc,
	vizHostTimeline,
	vizPerfCalculator,
	vizWorkSpan,
	vizIssueSlots
];
