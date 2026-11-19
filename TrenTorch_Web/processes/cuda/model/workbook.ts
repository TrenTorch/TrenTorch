// The calculation workbook (chapter G1): every problem is evaluated by the same model functions the
// visualizations use, so "Check" can never disagree with the figures. `answer` is the single number the
// learner types; `detail` states the other values the worked answer quotes.
import { getProfile } from './profiles';
import {
	amdahl,
	amdahlCeiling,
	bandwidthFromSpec,
	effectiveBandwidth,
	launchOverhead,
	peakBandwidth,
	peakFp32,
	ridge,
	timeModel,
	copyTime
} from './perf';
import {
	laneUtilization,
	occupancy,
	regsForBlocks,
	waveEfficiency,
	waves,
	warpsPerBlock
} from './occupancy';
import { float4Plan, naiveTransposeBytes, strideConflictDegree, strideReport } from './memory';
import { pDiverge } from './divergence';
import { blellochCost, hillisSteeleCost } from './scan';
import { radixBytes, radixPasses } from './sort';
import { privatizedGlobalAtomics } from './histogram';
import { pipelineTime, serialTime } from './pipeline';
import { matmulAI, requiredSquareTile } from './roofline';
import { idealTileLoadElements, tileLoadElements } from './tiling';
import { scoreMatrixBytes } from './attention';
import { spmvAI, spmvBytes } from './sparse';
import { convBytes, convFlops, im2colBytes } from './conv';
import { FORMATS, expOverflowLogit, sequentialStall } from './precision';
import {
	haloBytes3D,
	matmulRowSplit,
	p2pCopy,
	ringAllReduce,
	ringBytesPerGpu,
	scalingPoint
} from './multigpu';

export interface WorkbookProblem {
	n: number;
	answer: number;
	unit: string;
	/** Relative tolerance for "Check". */
	tolerance: number;
	detail: string;
	kind?: 'number' | 'choice';
}

const T4 = getProfile('T4'),
	A100 = getProfile('A100'),
	H100 = getProfile('H100');
const GiB = 2 ** 30;
const f = (x: number, d = 3) => Number(x.toPrecision(d)).toString();

export function workbook(): WorkbookProblem[] {
	const out: WorkbookProblem[] = [];
	const add = (p: Omit<WorkbookProblem, 'tolerance'> & { tolerance?: number }) =>
		out.push({ tolerance: 0.02, kind: 'number', ...p });

	// Section 1: spec-sheet arithmetic
	add({ n: 1, answer: peakFp32(T4) / 1e12, unit: 'TFLOPS', detail: '40 x 64 x 2 x 1.59 GHz' });
	add({ n: 2, answer: bandwidthFromSpec(256, 10) / 1e9, unit: 'GB/s', detail: '256 / 8 x 10' });
	add({ n: 3, answer: ridge(67e12, 3.35e12), unit: 'FLOP/B', detail: '67 TFLOPS / 3.35 TB/s' });
	{
		const e = effectiveBandwidth(4 * GiB, 4 * GiB, 5e-3, peakBandwidth(A100));
		add({ n: 4, answer: e.bw / 1e12, unit: 'TB/s', detail: `eta = ${f(e.eta * 100, 2)}%` });
	}

	// Section 2: time predictions
	add({
		n: 5,
		answer:
			timeModel({
				bytes: 12 * 2 ** 27,
				flops: 0,
				peakFlops: peakFp32(A100),
				bw: peakBandwidth(A100),
				launchSeconds: 0
			}).tMem * 1e3,
		unit: 'ms',
		detail: '12 B x 2^27 / (0.85 x 2,039 GB/s)'
	});
	add({ n: 6, answer: 2 / 12 / (2 / 320), unit: 'x', detail: '166.7 ms vs 6.25 ms' });
	add({ n: 7, answer: amdahl(0.9, 100), unit: 'x', detail: `ceiling ${amdahlCeiling(0.9)}x` });
	{
		const l = launchOverhead(10000, 3e-6, 5e-6);
		add({
			n: 8,
			answer: l.total * 1e3,
			unit: 'ms',
			detail: `${f(l.overheadShare * 100, 3)}% overhead`
		});
	}

	// Section 3: indexing, warps, occupancy
	add({
		n: 9,
		answer: warpsPerBlock(400),
		unit: 'warps',
		tolerance: 0,
		detail: `lane utilization ${f(laneUtilization(400) * 100, 3)}%`
	});
	{
		const o = occupancy(A100, 512, 40);
		add({
			n: 10,
			answer: o.occupancy * 100,
			unit: '%',
			detail: `${o.blocks} blocks, ${o.threadsPerSm} threads, limiter ${o.limiter}`
		});
	}
	{
		const o = occupancy(A100, 256, 80);
		add({
			n: 11,
			answer: o.occupancy * 100,
			unit: '%',
			detail: `100% needs <= ${regsForBlocks(A100, 256, 8)} registers/thread`
		});
	}
	add({
		n: 12,
		answer: waveEfficiency(2000, 864) * 100,
		unit: '%',
		detail: `${waves(2000, 864)} waves`
	});
	{
		const p = float4Plan(10_000_001, 256);
		add({
			n: 13,
			answer: p.blocks,
			unit: 'blocks',
			tolerance: 0,
			detail: `${p.vec} float4 elements, ${p.tail} tail element`
		});
	}

	// Section 4: memory patterns
	{
		const r = strideReport(4);
		add({ n: 14, answer: r.efficiency * 100, unit: '%', detail: `${r.sectors} sectors per warp` });
	}
	add({ n: 15, answer: strideConflictDegree(4), unit: '-way', tolerance: 0, detail: 'gcd(4, 32)' });
	add({ n: 16, answer: pDiverge(0.02) * 100, unit: '%', detail: '1 - 0.98^32 - 0.02^32' });
	add({ n: 17, answer: naiveTransposeBytes(1024).ratio, unit: 'x', detail: '36 N^2 / 8 N^2' });

	// Section 5: algorithms
	add({
		n: 18,
		answer: hillisSteeleCost(256).additions,
		unit: 'additions (Hillis-Steele)',
		tolerance: 0,
		detail: `Blelloch ${blellochCost(256).additions}`
	});
	add({
		n: 19,
		answer: (radixBytes(2 ** 26, 32, 8) / (0.85 * peakBandwidth(A100))) * 1e3,
		unit: 'ms',
		detail: `${radixPasses(32, 8)} passes`
	});
	add({
		n: 20,
		answer: privatizedGlobalAtomics(128, 1024),
		unit: 'atomics',
		tolerance: 0,
		detail: '128 x 1,024'
	});
	add({
		n: 21,
		answer: ringAllReduce(400e6, 4, 50e9, 0).bandwidth * 1e3,
		unit: 'ms',
		detail: `${f(ringBytesPerGpu(400e6, 4) / 1e6, 3)} MB per GPU`
	});
	{
		const t = pipelineTime({ h: 60, k: 20, d: 60, chunks: 6 });
		add({
			n: 22,
			answer: t,
			unit: 'ms',
			detail: `serial ${serialTime(60, 20, 60)} ms, speed-up ${f(serialTime(60, 20, 60) / t, 2)}x`
		});
	}

	// Section 6: roofline and tiling
	add({
		n: 23,
		answer: matmulAI(64, 128),
		unit: 'FLOP/B',
		detail: `ridge ${f(ridge(peakFp32(A100), peakBandwidth(A100)), 3)}: compute-bound`
	});
	add({
		n: 24,
		answer: requiredSquareTile(ridge(peakFp32(T4), peakBandwidth(T4))),
		unit: 'tile side',
		tolerance: 0.03,
		detail: 'T/4 >= ridge'
	});
	add({
		n: 25,
		answer: tileLoadElements(100, 100, 100, 16),
		unit: 'elements',
		tolerance: 0,
		detail: `ideal ${idealTileLoadElements(100, 100, 100, 16)}`
	});

	// Section 7: attention, sparse, precision
	add({ n: 26, answer: scoreMatrixBytes(8192) / 1e6, unit: 'MB', detail: '8,192^2 x 4 B' });
	{
		const t = spmvBytes(1e8) / (0.85 * peakBandwidth(A100));
		add({
			n: 27,
			answer: t * 1e3,
			unit: 'ms',
			detail: `${f(2e8 / t / 1e9, 3)} GFLOP/s attainable (AI ${f(spmvAI(), 3)})`
		});
	}
	add({
		n: 28,
		answer: convFlops(32, 64, 128, 56, 56, 3) / 1e9,
		unit: 'GFLOP',
		detail: `im2col buffer ${f(im2colBytes(32, 64, 56, 56, 3) / 1e6, 3)} MB (input ${f(convBytes(32, 64, 128, 56, 56, 3).input / 1e6, 3)} MB)`
	});
	add({
		n: 29,
		answer: sequentialStall(FORMATS.FP16),
		unit: '(FP16 stall point)',
		tolerance: 0,
		detail: `FP32 stops at ${sequentialStall(FORMATS.FP32).toLocaleString('en-US')}`
	});
	add({
		n: 30,
		answer: 12 > expOverflowLogit(FORMATS.FP16) ? 1 : 0,
		unit: '1 = yes, 0 = no',
		tolerance: 0,
		kind: 'choice',
		detail: `exp overflows above ${f(expOverflowLogit(FORMATS.FP16), 4)}`
	});

	// Section 8: multi-GPU
	add({
		n: 31,
		answer: haloBytes3D(512, 1) / 1e6,
		unit: 'MB',
		detail: `PCIe ${f(copyTime(haloBytes3D(512, 1), 25e9, 0) * 1e6, 3)} us, NVLink ${f(copyTime(haloBytes3D(512, 1), 300e9, 0) * 1e6, 3)} us`
	});
	{
		const base = { mode: 'strong' as const, t1: 100, serial: 0, comm: () => 5.8 };
		const a = scalingPoint({ ...base, overlap: false }, 8),
			b = scalingPoint({ ...base, overlap: true }, 8);
		add({
			n: 32,
			answer: a.speedup,
			unit: 'x (no overlap)',
			detail: `efficiency ${f(a.efficiency * 100, 3)}%; with perfect overlap ${f(b.speedup, 3)}x, ${f(b.efficiency * 100, 3)}%`
		});
	}
	{
		const m = matmulRowSplit(8192, 4, 15.6e12, 300e9);
		add({
			n: 33,
			answer: m.flopsPerGpu / 1e9,
			unit: 'GFLOP per GPU',
			detail: `${f(m.computeSeconds * 1e3, 3)} ms compute, ${f(m.bcastSeconds * 1e3, 2)} ms to broadcast B`
		});
	}
	{
		const c = p2pCopy(1e9, 300e9, 25e9);
		add({
			n: 34,
			answer: c.speedup,
			unit: 'x faster direct',
			detail: `${f(c.direct * 1e3, 3)} ms direct vs ${f(c.staged * 1e3, 3)} ms staged`
		});
	}
	void H100;
	return out;
}
export const checkAnswer = (p: WorkbookProblem, given: number) =>
	p.tolerance === 0
		? Math.abs(given - p.answer) < 1e-9 + (p.n === 9 ? 0 : 0.5)
		: Math.abs(given - p.answer) <= p.tolerance * Math.abs(p.answer);
export { GPU_NAMES } from './profiles';
