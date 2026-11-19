import { describe, it, expect } from 'vitest';
import * as m from './index';

const T4 = m.getProfile('T4'),
	A100 = m.getProfile('A100'),
	H100 = m.getProfile('H100');
const near = (a: number, b: number, rel = 0.01) =>
	expect(Math.abs(a - b) / Math.abs(b)).toBeLessThan(rel);

describe('the values the task requires', () => {
	it('ReLU on 2^28 floats on an A100 at eta 0.85 takes about 1.24 ms of memory time', () => {
		const t = m.timeModel({
			bytes: 8 * 2 ** 28,
			flops: 2 ** 28,
			peakFlops: m.peakFp32(A100),
			bw: m.peakBandwidth(A100),
			etaM: 0.85,
			launchSeconds: 0
		});
		near(t.tMem * 1e3, 1.24, 0.005);
		expect(t.bound).toBe('memory');
		near(t.ratio, 75, 0.1); // memory is ~75x compute (at peak the text says 75x)
	});
	it('A100, 256-thread blocks, 40 registers: 6 blocks per SM, 75% occupancy (registers bind)', () => {
		const o = m.occupancy(A100, 256, 40);
		expect(o.blocks).toBe(6);
		expect(o.occupancy).toBe(0.75);
		expect(o.limiter).toBe('registers');
	});
	it('A100, 128-thread blocks, 37 registers: rounds to 40, 12 blocks per SM', () => {
		const o = m.occupancy(A100, 128, 37);
		expect(o.effectiveRegs).toBe(40);
		expect(o.blocks).toBe(12);
		expect(o.occupancy).toBe(0.75);
		// ignoring granularity predicts 13 blocks
		expect(m.occupancy(A100, 128, 37, 0, { rounding: false }).blocks).toBe(13);
	});
	it('grid 2000 on capacity 864: 3 waves, 77.2% efficiency', () => {
		expect(m.waves(2000, 864)).toBe(3);
		near(m.waveEfficiency(2000, 864) * 100, 77.2, 0.001);
	});
	it('stride 8 gives an 8-way bank conflict (gcd rule)', () => {
		expect(m.strideConflictDegree(8)).toBe(8);
		expect(m.conflictDegree(Array.from({ length: 32 }, (_, l) => 8 * l))).toBe(8); // matches the brute-force count
	});
	it('P(warp diverges) at p = 0.02 is 0.476', () => near(m.pDiverge(0.02), 0.476, 0.001));
	it('ring all-reduce of 1 GB over 8 GPUs at 300 GB/s: about 5.8 ms bandwidth term', () =>
		near(m.ringAllReduce(1e9, 8, 300e9).bandwidth * 1e3, 5.83, 0.002));
	it('pipeline H = D = 40, K = 10, S = 4 takes 52.5 ms', () => {
		expect(m.pipelineTime({ h: 40, k: 10, d: 40, chunks: 4 })).toBeCloseTo(52.5, 6);
		expect(m.serialTime(40, 10, 40)).toBe(90);
		expect(m.pipelineLowerBound(40, 10, 40)).toBe(40);
	});
});

describe('A5 performance calculator', () => {
	it('peak compute and bandwidth from the spec sheet', () => {
		near(m.peakFp32(T4) / 1e12, 8.14, 0.002);
		near(m.peakFp32(A100) / 1e12, 19.5, 0.002);
		near(m.peakFp32(H100) / 1e12, 67, 0.01);
		expect(m.bandwidthFromSpec(256, 10) / 1e9).toBe(320);
		near(m.bandwidthFromSpec(5120, 3.19) / 1e9, 2039, 0.003);
	});
	it('ridge points: T4 about 25, A100 9.6, H100 about 20', () => {
		near(m.machineBalance(T4), 25.4, 0.01);
		near(m.machineBalance(A100), 9.56, 0.005);
		near(m.machineBalance(H100), 20, 0.01);
	});
	it('attainable FLOP/s at AI = 2 on an A100 is 4,078 GFLOP/s', () =>
		near(m.attainable(m.peakFp32(A100), m.peakBandwidth(A100), 2) / 1e9, 4078, 0.001));
	it('T4 peak bandwidth with a 14 Gbit/s data rate is 448 GB/s', () =>
		expect(m.bandwidthFromSpec(256, 14) / 1e9).toBe(448));
	it('Amdahl: p = 0.9, s = 100 gives 9.2x with a 10x ceiling', () => {
		near(m.amdahl(0.9, 100), 9.17, 0.001);
		expect(m.amdahlCeiling(0.9)).toBeCloseTo(10);
	});
	it("Little's law: a T4 needs about 25 outstanding 128-byte warp loads per SM", () =>
		near(m.warpLoadsPerSm(400e-9, 320e9, 40), 25, 0.01));
	it('worked example 2: a lone vector add is slower on the GPU, and k >= 2.05 chained passes flip it', () => {
		const v = { cpuBw: 50e9, pcieBw: 25e9, gpuBw: 2039e9 };
		const one = m.vectorAddPerElement(v);
		expect(one.gpuWins).toBe(false);
		near(one.gpu / one.cpu, 2, 0.05);
		near(m.crossoverKernels(v), 2.05, 0.01);
		expect(m.vectorAddPerElement({ ...v, kernels: 3 }).gpuWins).toBe(true);
	});
	it('launch overhead: 10,000 launches of 3 us work and 5 us overhead = 80 ms, 62.5% overhead', () => {
		const l = m.launchOverhead(10000, 3e-6, 5e-6);
		near(l.total * 1e3, 80, 0.001);
		expect(l.overheadShare).toBeCloseTo(0.625);
	});
	it('copy kernel: 2 x 4 GiB in 5 ms is 1.72 TB/s, 84% of an A100', () =>
		near(m.effectiveBandwidth(2 ** 32, 2 ** 32, 5e-3, 2039e9).eta, 0.84, 0.01));
	it('work and span', () => {
		expect(m.parallelism(1e9, 1e4)).toBe(1e5);
		expect(m.parallelTimeLowerBound(100, 100, 1e6)).toBe(100);
	});
});

describe('warps, occupancy and waves', () => {
	it('lane utilization: 100 threads 78.1%, 33 threads 51.6%, 20x20 block 96.2%', () => {
		near(m.laneUtilization(100), 0.781, 0.001);
		near(m.laneUtilization(33), 0.516, 0.002);
		near(m.laneUtilization(400), 0.962, 0.001);
		expect(m.warpsPerBlock(400)).toBe(13);
	});
	it('register staircase table for 256-thread blocks on the A100', () => {
		const want: [number, number, number][] = [
			[32, 8, 1],
			[40, 6, 0.75],
			[64, 4, 0.5],
			[80, 3, 0.375],
			[128, 2, 0.25],
			[255, 1, 0.125]
		];
		for (const [regs, blocks, occ] of want) {
			const o = m.occupancy(A100, 256, regs);
			expect([regs, o.blocks, o.occupancy]).toEqual([regs, blocks, occ]);
		}
	});
	it('100% occupancy at 256 threads needs <= 32 registers; __launch_bounds__(256, 8) gives 32; (256, 6) gives 42', () => {
		expect(m.regsForBlocks(A100, 256, 8)).toBe(32);
		expect(m.launchBoundsRegs(A100, 256, 8)).toBe(32);
		expect(m.launchBoundsRegs(A100, 256, 6)).toBe(42);
	});
	it('A100, 128 threads, 32 regs, 16 KB shared: shared memory binds at 10 blocks (62.5%)', () => {
		const o = m.occupancy(A100, 128, 32, 16 * 1024);
		expect(o.blocks).toBe(10);
		expect(o.limiter).toBe('shared memory');
		expect(o.occupancy).toBe(0.625);
	});
	it('512-thread blocks at 40 registers: 3 blocks, 75%, registers', () => {
		const o = m.occupancy(A100, 512, 40);
		expect([o.blocks, o.occupancy, o.limiter]).toEqual([3, 0.75, 'registers']);
	});
	it('80 registers at 256 threads: 37.5%', () =>
		expect(m.occupancy(A100, 256, 80).occupancy).toBe(0.375));
	it('wave efficiency for 1,000 blocks on capacity 864 is 57.9%; grid-stride launches exactly the capacity', () => {
		near(m.waveEfficiency(1000, 864) * 100, 57.9, 0.002);
		expect(m.waveEfficiency(864, 864)).toBe(1);
		expect(m.residentCapacity(A100, 8)).toBe(864);
		near(m.elementsPerThread(2 ** 28, 864, 256), 1214, 0.001);
	});
	it('warps needed: L = 450, c = 4 -> 57; L = 400, c = 3 -> 68', () => {
		near(m.warpsNeeded(450, 4), 57.25, 0.001);
		near(m.warpsNeeded(400, 3), 67.7, 0.001);
	});
	it('ILP trade: 4 chains on 4 warps fill as many issue slots as 1 chain on 16 warps', () => {
		expect(m.issueSlotUtilization(4, 4, 400, 3)).toBeCloseTo(m.issueSlotUtilization(16, 1, 400, 3));
	});
	it('index maths: voxel index, linear thread id and the 32-bit wrap', () => {
		expect(m.voxelIndex(1, 2, 3, 10, 20)).toBe((3 * 20 + 2) * 10 + 1);
		expect(m.linearThreadId(1, 2, 3, 4, 5)).toBe(1 + 8 + 60);
		expect(m.wrap32(3_000_000_000)).toBeLessThan(0);
		expect(m.wrap32(5)).toBe(5);
		expect(Math.ceil(1000000 / 256)).toBe(m.blocksFor(1_000_000, 256));
		expect(m.blocksFor(33, 8) * 0 + Math.ceil(33 / 8)).toBe(5);
	});
});

describe('divergence', () => {
	it('table of P(diverge)', () => {
		near(m.pDiverge(0.1), 0.966, 0.001);
		near(m.pDiverge(0.01), 0.275, 0.002);
		near(m.pDiverge(0.001), 0.0315, 0.002);
		expect(m.pDiverge(0.5)).toBeGreaterThan(0.999999);
	});
	it('loop divergence: trip counts 0..7 -> E[max of 32] is about 6.99 and utilization about 50%', () => {
		near(m.expectedMaxUniform(8), 6.99, 0.003);
		near(m.loopUtilization(8), 0.5, 0.01);
		near(m.expectedMaxUniform(8) * 20, 140, 0.01);
	});
	it('expected warp time', () =>
		near(m.expectedWarpTime(0.02, 100, 10), 10 + 100 * (1 - 0.98 ** 32), 1e-9));
	it('Monte Carlo converges to the formula', () =>
		near(m.monteCarloDivergence(0.02, 20000, 7).fraction, m.pDiverge(0.02), 0.05));
});

describe('memory: coalescing, float4, banks', () => {
	it('stride table: 1 -> 4 sectors 100%, 2 -> 8 sectors 50%, 4 -> 16 sectors 25%, 8+ -> 32 sectors 12.5%', () => {
		expect(
			[1, 2, 4, 8, 16, 64].map((s) => [m.strideReport(s).sectors, m.strideReport(s).efficiency])
		).toEqual([
			[4, 1],
			[8, 0.5],
			[16, 0.25],
			[32, 0.125],
			[32, 0.125],
			[32, 0.125]
		]);
	});
	it('float4 floor is 50%; the lowest 4-byte efficiency is 12.5%', () => {
		expect(m.coalescingEfficiency(m.strideAddresses(2, 16), 16)).toBe(0.5);
		expect(m.coalescingEfficiency(m.strideAddresses(1000, 4), 4)).toBe(0.125);
	});
	it('a misaligned 128-byte read touches 5 sectors', () =>
		expect(m.strideReport(1, 4, 4).sectors).toBe(5));
	it('stride-4 kernel on an A100 gives about 430 GB/s of useful data', () =>
		near(m.usefulBandwidth(0.25, 0.85, 2039e9) / 1e9, 433, 0.01));
	it('naive transpose moves 4.5x the ideal bytes', () =>
		expect(m.naiveTransposeBytes(1024).ratio).toBe(4.5));
	it('float4 plan: N = 10,000,001 and N = 1,000,003', () => {
		expect(m.float4Plan(10_000_001, 256)).toMatchObject({ vec: 2_500_000, tail: 1, blocks: 9766 });
		expect(m.float4Plan(1_000_003, 256)).toMatchObject({ vec: 250_000, tail: 3 });
		expect(m.float4Plan(2 ** 26, 256)).toMatchObject({
			scalarWarpLoads: 2_097_152,
			vectorWarpLoads: 524_288
		});
		expect([m.bytesInFlightPerWarpLoad(4), m.bytesInFlightPerWarpLoad(16)]).toEqual([128, 512]);
	});
	it('bank conflict degree = gcd(s, 32) for every stride; odd strides are free', () => {
		for (let s = 1; s <= 64; s++)
			expect(m.conflictDegree(Array.from({ length: 32 }, (_, l) => s * l))).toBe(m.gcd(s, 32));
		expect([1, 2, 3, 4, 8, 16, 32, 33].map(m.strideConflictDegree)).toEqual([
			1, 2, 1, 4, 8, 16, 32, 1
		]);
	});
	it('padding to [32][33] and XOR swizzling both fix the column read; broadcast is free', () => {
		expect(m.columnReadDegree(32)).toBe(32);
		expect(m.columnReadDegree(33)).toBe(1);
		expect(m.columnReadDegree(32, true)).toBe(1);
		expect(m.rowReadDegree(32, true)).toBe(1);
		expect(m.conflictDegree(Array(32).fill(7))).toBe(1);
	});
	it('word 4*33 + 7 sits in bank 11', () => expect((4 * 33 + 7) % 32).toBe(11));
	it('scan indexing adds one pad word per 32; constant cache costs one cycle per distinct address', () => {
		expect(m.scanPad(31)).toBe(31);
		expect(m.scanPad(32)).toBe(33);
		expect(m.constantReadCycles(Array(32).fill(5))).toBe(1);
		expect(m.constantReadCycles(Array.from({ length: 32 }, (_, i) => i))).toBe(32);
	});
});

describe('roofline, matmul ladder and tiling', () => {
	it('matmul AI: T/4 for square tiles; 64x128 is 21.3', () => {
		expect([16, 32, 64, 128].map((t) => m.matmulAI(t, t))).toEqual([4, 8, 16, 32]);
		near(m.matmulAI(64, 128), 21.33, 0.001);
	});
	it('required tile: A100 about 38.4, T4 about 100', () => {
		near(m.requiredSquareTile(9.6), 38.4, 0.001);
		near(m.requiredSquareTile(m.machineBalance(T4)), 100, 0.02);
	});
	it('tensor roofs: ridge 153 FLOP/B on the FP16 roof; FP16 operands give 64 FLOP/B at 128x128', () => {
		near(m.roofRidge(A100, 'FP16'), 153, 0.002);
		near(m.roofRidge(A100, 'TF32'), 76.5, 0.002);
		expect(m.matmulAIFp16(128, 128)).toBe(64);
	});
	it('A100 attainable FLOP/s at tile 16 is 8.2 TFLOPS (42%) and at tile 32 is 16.3 (84%)', () => {
		const bw = m.peakBandwidth(A100),
			peak = m.peakFp32(A100);
		near(m.attainable(peak, bw, 4) / 1e12, 8.2, 0.01);
		near(m.attainable(peak, bw, 8) / 1e12, 16.3, 0.005);
	});
	it('worksheet: ReLU 0.125, SAXPY 0.167, GEMV 0.5, dot 0.25', () => {
		const w = Object.fromEntries(m.aiWorksheet().map((r) => [r.kernel, r.ai]));
		expect([w['ReLU'], w['SAXPY'], w['GEMV (A streamed once)'], w['Dot product']]).toEqual([
			0.125,
			2 / 12,
			0.5,
			0.25
		]);
	});
	it('the E7 ladder on an A100 (N = 4096)', () => {
		const l = m.matmulLadder(A100, 4096);
		near(l.flops / 1e9, 137.4, 0.001);
		near(l.computeFloor * 1e3, 8.8, 0.01);
		near(l.idealBytes / 1e6, 201, 0.005);
		const t = l.rows.map((r) => [r.version, Math.round(r.ai * 100) / 100, r.bound]);
		expect(t).toEqual([
			['v1 naive', 0.25, 'memory'],
			['v3 tiled T=16', 4, 'memory'],
			['v3 tiled T=32', 8, 'memory'],
			['v6 register tile', 16, 'compute'],
			['v6 register tile', 32, 'compute']
		]);
		near(l.rows[0].memoryTime * 1e3, 317, 0.01);
		near(l.rows[1].memoryTime * 1e3, 19.8, 0.01);
		near(l.rows[3].memoryTime * 1e3, 5.0, 0.02);
		near(l.rows[0].bytes / 1e9, 550, 0.002);
	});
	it('double buffering gains at most 1.6x when load = 60% of compute', () =>
		expect(m.doubleBufferGain(0.6, 1)).toBeCloseTo(1.6));
	it('shared-memory bound: R = 1 reaches 25% of FMA peak; R = 4 balances', () => {
		expect(m.sharedBound(1)).toMatchObject({ fmaPeakFraction: 0.25, limiting: 'shared memory' });
		expect(m.sharedBound(4)).toMatchObject({ fmaPeakFraction: 1, limiting: 'FMA' });
		expect(m.balancedRegisterTile()).toBe(4);
		expect(m.sharedLoadsPerWarpFma(4)).toBe(0.5);
		expect(m.registerTileRegs(4)).toBe(40);
	});
	it('tile load accounting: 100^3 with T = 16 fetches 175,616 elements (ideal 125,000)', () => {
		expect(m.tileLoadElements(100, 100, 100, 16)).toBe(175_616);
		expect(m.idealTileLoadElements(100, 100, 100, 16)).toBe(125_000);
		expect([m.tilingBytes(16), m.tilingBytes(32)]).toEqual([2048, 8192]);
		expect([m.naiveLoadsPerOutput(512), m.tiledLoadsPerOutput(512, 16)]).toEqual([1024, 64]);
	});
});

describe('precision', () => {
	it('unit roundoff and overflow thresholds', () => {
		expect(m.unitRoundoff(m.FORMATS.FP32)).toBe(2 ** -24);
		expect(m.unitRoundoff(m.FORMATS.FP16)).toBe(2 ** -11);
		expect(m.unitRoundoff(m.FORMATS.BF16)).toBe(2 ** -8);
		near(m.expOverflowLogit(m.FORMATS.FP16), 11.09, 0.001);
	});
	it('FP16 rounding: range, spacing and ties', () => {
		const h = m.FORMATS.FP16;
		expect(m.roundTo(65504, h)).toBe(65504);
		expect(m.roundTo(70000, h)).toBe(Infinity);
		expect(m.roundTo(2049, h)).toBe(2048);
		expect(m.roundTo(2051, h)).toBe(2052);
		expect(m.roundTo(1 / 3, h)).toBeCloseTo(0.333251953125, 12);
		expect(m.spacingAt(2048, h)).toBe(2);
		expect(m.spacingAt(1, m.FORMATS.FP32)).toBe(2 ** -23);
	});
	it('sum of ones: FP16 sequential stops at 2,048; FP32 at 16,777,216 (analytic); a tree keeps counting', () => {
		expect(m.sumOfOnes(100_000, m.FORMATS.FP16, 'sequential')).toBe(2048);
		expect(m.sequentialStall(m.FORMATS.FP16)).toBe(2048);
		expect(m.sequentialStall(m.FORMATS.FP32)).toBe(16_777_216);
		expect(m.sumOfOnes(4096, m.FORMATS.FP16, 'tree')).toBe(4096);
		expect(m.sumOfOnes(1 << 16, m.FORMATS.FP32, 'tree')).toBe(1 << 16);
		expect(m.sumOfOnes(5000, m.FORMATS.FP16, 'kahan')).toBe(5000);
		expect(Math.fround(16_777_216 + 1)).toBe(16_777_216);
	});
	it('error bounds: sequential ~ N u, pairwise ~ log2 N u', () => {
		expect(m.sequentialErrorBound(1001, m.unitRoundoff(m.FORMATS.FP32))).toBeGreaterThan(
			m.pairwiseErrorBound(1001, m.unitRoundoff(m.FORMATS.FP32))
		);
		near(m.dotErrorFp32Accum(1024, m.FORMATS.FP16), 4.88e-4 + 6.1e-5, 0.01);
		near(m.dotErrorLowAccum(1024, m.FORMATS.FP16), 0.5, 0.001);
	});
	it('FP16 halves the bytes: 2^26 ReLU goes from 0.31 ms to about 0.16 ms', () => {
		const t = (bytes: number) => (bytes / (0.85 * 2039e9)) * 1e3;
		near(t(8 * 2 ** 26), 0.31, 0.01);
		near(t(4 * 2 ** 26), 0.155, 0.01);
		expect(m.bytesFor(10, m.FORMATS.FP16)).toBe(20);
	});
});

describe('reduction, scan, sort, softmax', () => {
	it('scan work and depth', () => {
		expect([
			m.sequentialScan(8).additions,
			m.hillisSteeleCost(8).additions,
			m.blellochCost(8).additions,
			m.brentKungCost(8).additions
		]).toEqual([7, 17, 14, 11]);
		expect([m.hillisSteeleCost(256).additions, m.blellochCost(256).additions]).toEqual([1793, 510]);
		expect([m.hillisSteeleCost(1024).additions, m.blellochCost(1024).additions]).toEqual([
			9217, 2046
		]);
		expect(m.hillisSteeleCost(16).additions).toBe(16 * 4 - 15 + 0);
		expect([m.blellochCost(8).depth, m.hillisSteeleCost(8).depth]).toEqual([6, 3]);
	});
	it('both scan networks compute the right answer', () => {
		const x = [3, 1, 7, 0, 4, 1, 6, 3];
		expect(m.hillisSteeleSteps(x).at(-1)).toEqual(m.inclusiveScan(x));
		expect(m.blellochSteps(x).result).toEqual(m.exclusiveScan(x));
		expect(m.inclusiveScan([3, 1, 7])).toEqual([3, 4, 11]);
		expect(m.exclusiveScan([3, 1, 7])).toEqual([0, 3, 4]);
	});
	it('compaction: [5,0,7,0,0,3] -> [5,7,3]; and the E6 check-yourself case', () => {
		const c = m.compact([5, 0, 7, 0, 0, 3], (v) => v !== 0);
		expect(c).toMatchObject({
			flags: [1, 0, 1, 0, 0, 1],
			slots: [0, 1, 1, 2, 2, 2],
			out: [5, 7, 3],
			count: 3
		});
		expect(m.compact([2, 9, 1, 4, 3, 5, 6], (v) => [2, 9, 4, 6].includes(v))).toMatchObject({
			flags: [1, 1, 0, 1, 0, 0, 1],
			slots: [0, 1, 2, 2, 3, 3, 3],
			out: [2, 9, 4, 6]
		});
		expect(m.SCAN_TRAFFIC).toEqual({
			scanThenPropagate: 4,
			reduceThenScan: 3,
			decoupledLookback: 2
		});
	});
	it('decoupled look-back: any block order gives the right prefixes and block 0 never waits', () => {
		const v = [2, 4, 1, 3, 5, 2, 6, 1];
		const r = m.decoupledLookback(v, [3, 1, 7, 0, 5, 2, 6, 4]);
		expect(r.prefix).toEqual(m.inclusiveScan(v));
		expect(r.blocks.find((b) => b.id === 0)!.steps).toBe(0);
		expect(r.wordsMovedPerN).toBe(2);
	});
	it('bitonic counts: 1,024 keys need 55 stages and 28,160 comparators; 2^20 needs 210 stages', () => {
		expect([
			m.bitonicStages(1024),
			m.bitonicComparators(1024),
			m.bitonicStages(2 ** 20),
			m.bitonicComparators(2 ** 20)
		]).toEqual([55, 28160, 210, 110_100_480]);
		expect(m.bitonicComparators(16)).toBe(80); // 10 stages x 8 comparators
		expect(m.bitonicStages(8)).toBe(6);
	});
	it('bitonic network and radix sort actually sort', () => {
		const x = [9, 3, 7, 1, 8, 2, 6, 4, 15, 0, 11, 5, 13, 12, 10, 14];
		expect(m.bitonicSort(x)).toEqual([...x].sort((a, b) => a - b));
		expect(m.radixSort(x, 4, 1)).toEqual([...x].sort((a, b) => a - b));
		expect(m.radixSort(x, 4, 2)).toEqual([...x].sort((a, b) => a - b));
	});
	it('radix: 2^26 keys, 8-bit digits -> 4 passes and 2.15 GB (about 1.24 ms at 0.85 x 2,039 GB/s); 64-bit keys need 8', () => {
		expect(m.radixPasses(32, 8)).toBe(4);
		expect(m.radixPasses(64, 8)).toBe(8);
		expect(m.radixPasses(32, 4)).toBe(8);
		near(m.radixBytes(2 ** 26, 32, 8) / 1e9, 2.15, 0.005);
		near((m.radixBytes(2 ** 26, 32, 8) / (0.85 * 2039e9)) * 1e3, 1.24, 0.005);
	});
	it('a radix pass is stable (equal digits keep their order)', () => {
		const r = m.radixPass([0b101, 0b001, 0b100, 0b000, 0b111, 0b011], 0, 1);
		expect(r.out).toEqual([0b100, 0b000, 0b101, 0b001, 0b111, 0b011]);
	});
	it('quicksort partition wastes lanes: a 50/50 split uses 100% only if both sides are equal', () => {
		expect(m.partitionLaneUtilization([true, false, true, false])).toBe(1);
		expect(m.partitionLaneUtilization([true, true, true, false])).toBeCloseTo(4 / 6);
	});
	it('online softmax merge: (2,3) + (5,1) -> d = 1.149; Chan merge -> M2 = 20', () => {
		const s = m.mergeSoftmax({ m: 2, d: 3 }, { m: 5, d: 1 });
		expect(s.m).toBe(5);
		near(s.d, 1.149, 0.001);
		const w = m.mergeWelford({ n: 2, mean: 1, m2: 2 }, { n: 2, mean: 5, m2: 2 });
		expect(w).toEqual({ n: 4, mean: 3, m2: 20 });
		const xs = [1, 5, 2, 8, 3, 9, 4, 7];
		const a = m.welfordOf(xs.slice(0, 4)),
			b = m.welfordOf(xs.slice(4));
		near(m.welfordVariance(m.mergeWelford(a, b)), m.welfordVariance(m.welfordOf(xs)), 1e-12);
		const full = m.softmaxState(xs),
			merged = m.mergeSoftmax(m.softmaxState(xs.slice(0, 3)), m.softmaxState(xs.slice(3)));
		near(merged.d, full.d, 1e-12);
	});
	it('naive variance E[x^2] - E[x]^2 is garbage for 1e8 + {1,2,3} in FP32, while Welford is exact (2/3)', () => {
		const xs = [1e8 + 1, 1e8 + 2, 1e8 + 3];
		expect(Math.abs(m.naiveVarianceFp32(xs) - 2 / 3)).toBeGreaterThan(0.5); // the true variance is 0.67; FP32 rounds all three values to 1e8
		near(m.welfordVariance(m.welfordOf(xs)), 2 / 3, 1e-6);
	});
	it('row softmax of 4,096 floats moves 32 KB; skipping the probability matrix saves 823 MB', () => {
		expect(m.rowSoftmaxBytes(4096)).toBe(32768);
		near(m.probabilityMatrixBytes(4096, 50257) / 1e6, 823, 0.001);
		const p = m.softmaxProbs([1, 2, 3]);
		near(
			p.reduce((a, b) => a + b, 0),
			1,
			1e-12
		);
	});
});

describe('stencils, atomics, sparse, graphs', () => {
	it('convolution counts for the E4 example', () => {
		near(m.convFlops(32, 64, 128, 56, 56, 3) / 1e9, 14.8, 0.002);
		near(m.im2colBytes(32, 64, 56, 56, 3) / 1e6, 231, 0.005);
		const b = m.convBytes(32, 64, 128, 56, 56, 3);
		near(b.input / 1e6, 25.7, 0.005);
		near(b.output / 1e6, 51.4, 0.005);
		near(b.weights / 1e3, 295, 0.005);
		expect(m.convFlops(1, 256, 256, 14, 14, 1)).toBe(25_690_112);
		expect(m.im2colBlowup(3)).toBe(9);
	});
	it('halo overhead: 16x16 K=3 -> 1.27, K=5 -> 1.56, K=7 -> 1.89; 3-D 8^3 K=3 -> 1.95, K=5 -> 3.4', () => {
		near(m.haloOverhead2D(16, 16, 3), 1.27, 0.005);
		near(m.haloOverhead2D(16, 16, 5), 1.5625, 0.001);
		near(m.haloOverhead2D(16, 16, 7), 1.89, 0.002);
		near(m.haloOverhead3D(8, 3), 1.95, 0.002);
		near(m.haloOverhead3D(8, 5), 3.375, 0.001);
		expect(m.separableMacs(3)).toEqual({ direct: 9, separable: 6 });
		expect(m.separableMacs(7)).toEqual({ direct: 49, separable: 14 });
	});
	it('direct convolution and im2col agree', () => {
		const img = [
				[1, 2, 3],
				[4, 5, 6],
				[7, 8, 9]
			],
			f = [
				[0, 1, 0],
				[1, 2, 1],
				[0, 1, 0]
			];
		const rows = m.im2col(img, 3),
			flat = f.flat();
		expect(rows.map((r) => r.reduce((a, v, i) => a + v * flat[i], 0))).toEqual(
			m.conv2dDirect(img, f).flat()
		);
	});
	it('histogram accounting', () => {
		expect([
			m.naiveGlobalAtomics(2 ** 24),
			m.privatizedGlobalAtomics(128, 1024),
			m.lastBlockAtomics(1000)
		]).toEqual([16_777_216, 131_072, 1000]);
		near(m.maxSharedBins(164), 41_984, 0.001);
		near(m.hotBinSeconds(2 ** 26, 0.9) * 1e3, 60.4, 0.01);
		expect(m.warpAggregatedAtomics([3, 3, 3, 7, 7, 1])).toBe(3);
		expect(m.lanePopcRank([3, 7, 3, 3], 3)).toBe(2);
		expect(m.histogram([0, 1, 1, 9, -1, 2], 4)).toEqual([1, 2, 1, 0]);
	});
	it('CSR / ELL / COO', () => {
		expect(
			m.toCsr([
				[0, 2, 0],
				[1, 0, 3],
				[0, 0, 0]
			])
		).toEqual({ val: [2, 1, 3], col: [1, 0, 2], rowptr: [0, 1, 3, 3] });
		const c = m.toCsr([
			[5, 0, 0, 1],
			[0, 2, 0, 0],
			[0, 0, 0, 0],
			[3, 0, 4, 6]
		]);
		expect(c).toEqual({
			val: [5, 1, 2, 3, 4, 6],
			col: [0, 3, 1, 0, 2, 3],
			rowptr: [0, 2, 3, 3, 6]
		});
		expect(m.rowLengths(c)).toEqual([2, 1, 0, 3]);
		const lens = [...Array(999).fill(8), 500]; // mean ~8 plus one row of 500
		const e = m.ellStats([
			...Array(1000)
				.fill(0)
				.map((_, i) => (i === 0 ? 500 : 8))
		]);
		expect(e.slots).toBe(500_000);
		expect(e.nnz).toBe(500 + 999 * 8);
		expect(e.waste).toBeGreaterThan(0.98 - 0.01);
		void lens;
		expect(
			m.toCoo([
				[0, 1],
				[2, 0]
			])
		).toEqual([
			{ r: 0, c: 1, v: 1 },
			{ r: 1, c: 0, v: 2 }
		]);
	});
	it('SpMV on an A100: AI 0.167, ceiling 340 GFLOP/s, 1e8 nnz takes 0.69 ms and attains 289 GFLOP/s', () => {
		near(m.spmvAI(), 0.1667, 0.001);
		near(m.spmvAI() * 2039, 340, 0.002);
		near(((m.spmvAI() * 2039) / 19500) * 100, 1.74, 0.01);
		const t = m.spmvBytes(1e8) / (0.85 * 2039e9);
		near(t * 1e3, 0.69, 0.005);
		near(2e8 / t / 1e9, 289, 0.005);
		const csr = m.toCsr([
			[1, 0],
			[2, 3]
		]);
		expect(m.spmv(csr, [1, 2])).toEqual([1, 8]);
	});
	it('SpMV lane utilization: thread-per-row stalls on a long row, warp-per-row wastes lanes on short rows', () => {
		const lens = [...Array(31).fill(2), 40];
		expect(m.threadPerRowUtilization(lens)).toBeLessThan(0.1);
		expect(m.warpPerRowUtilization(Array(32).fill(2))).toBeLessThan(0.1);
		expect(m.warpPerRowUtilization(Array(32).fill(64))).toBe(1);
	});
	it('BFS: push and pull find the same levels; pull examines fewer edges at the hub level of a star', () => {
		const star = m.symmetric(
			Array.from({ length: 20 }, (_, i) => [0, i + 1] as [number, number]),
			21
		);
		const push = m.bfsPush(star, 1),
			pull = m.bfsPull(star, 1);
		expect(push.map((l) => l.frontier.length)).toEqual(pull.map((l) => l.frontier.length));
		expect(push[1].edgesExamined).toBe(20);
		expect(pull[1].edgesExamined).toBeLessThan(push[1].edgesExamined + 20);
		near(m.bfsSweepSeconds(1e9, 1.733e12) * 1e3, 20.8, 0.01);
		expect(m.bytesPerEdge).toBe(36);
	});
});

describe('streams, launches, multi-GPU', () => {
	it('pipeline: 60/20/60 ms in 6 chunks is 73.3 ms (1.9x vs serial 140); one copy engine serializes the copies', () => {
		near(m.pipelineTime({ h: 60, k: 20, d: 60, chunks: 6 }), 73.33, 0.001);
		near(140 / 73.33, 1.9, 0.01);
		expect(m.pipelineTime({ h: 40, k: 10, d: 40, chunks: 4, copyEngines: 1 })).toBeGreaterThan(
			m.pipelineTime({ h: 40, k: 10, d: 40, chunks: 4 })
		);
		expect(m.pipelineTime({ h: 40, k: 10, d: 40, chunks: 1 })).toBe(90);
		expect(m.pipelineTime({ h: 40, k: 10, d: 40, chunks: 1000 })).toBeLessThan(45);
	});
	it('ring all-reduce: per-GPU volume 600 MB for 400 MB on 4 GPUs (12 ms at 50 GB/s); the factor tends to 2', () => {
		near(m.ringBytesPerGpu(400e6, 4) / 1e6, 600, 1e-9);
		near(m.ringAllReduce(400e6, 4, 50e9, 0).total * 1e3, 12, 1e-9);
		expect([2, 8, 64].map((p) => Math.round(m.ringBytesPerGpu(1, p) * 100) / 100)).toEqual([
			1, 1.75, 1.97
		]);
		near(m.ringAllReduce(1e9, 8, 300e9).total * 1e3, 5.9, 0.005);
		near(m.pcieVsNvlink(1e9, 8, 25e9, 300e9).pcie * 1e3, 70, 0.001);
		near(m.reduceScatterBytes(1e9, 8), 0.875e9, 1e-9);
	});
	it('ring versus tree: tree wins small messages, ring wins large ones, crossover in between', () => {
		const p = 64,
			beta = 300e9,
			alpha = 5e-6,
			x = m.ringTreeCrossover(p, beta, alpha);
		expect(m.treeAllReduce(x / 100, p, beta, alpha).total).toBeLessThan(
			m.ringAllReduce(x / 100, p, beta, alpha).total
		);
		expect(m.ringAllReduce(x * 100, p, beta, alpha).total).toBeLessThan(
			m.treeAllReduce(x * 100, p, beta, alpha).total
		);
		near(m.ringAllReduce(x, p, beta, alpha).total, m.treeAllReduce(x, p, beta, alpha).total, 1e-9);
	});
	it('peer-to-peer: 1 GB direct is 3.3 ms, staged 80 ms, 24x', () => {
		const c = m.p2pCopy(1e9, 300e9, 25e9);
		near(c.direct * 1e3, 3.33, 0.002);
		near(c.staged * 1e3, 80, 0.001);
		near(c.speedup, 24, 0.001);
	});
	it('halo exchange: n = 512, r = 1 -> 6.3 MB, 252 us on PCIe, 21 us on NVLink; n = 256 -> 2.3% halo', () => {
		near(m.haloBytes3D(512, 1) / 1e6, 6.29, 0.002);
		near(m.copyTime(m.haloBytes3D(512, 1), 25e9, 0) * 1e6, 252, 0.002);
		near(m.copyTime(m.haloBytes3D(512, 1), 300e9, 0) * 1e6, 21, 0.01);
		near(m.surfaceToVolume(256, 1) * 100, 2.34, 0.005);
		expect(m.haloCells3D(256, 1)).toBe(6 * 256 * 256);
		near(((2 * 512 ** 3 * 4) / (0.85 * 2039e9)) * 1e3, 0.62, 0.01);
	});
	it('slabs scale worse than 3-D blocks as p grows', () => {
		expect(m.slabRatio(1024, 1, 64)).toBeGreaterThan(m.blockRatio3D(1024, 1, 64));
		expect(
			m.halo2D(1024, 16, 1, 'slabs').halo / m.halo2D(1024, 16, 1, 'slabs').cells
		).toBeGreaterThan(m.halo2D(1024, 16, 1, 'blocks').halo / m.halo2D(1024, 16, 1, 'blocks').cells);
		expect(m.iterationTime(10, 6, true)).toBe(10);
		expect(m.iterationTime(10, 6, false)).toBe(16);
		expect(m.hiddenFraction(10, 6)).toBe(1);
		expect(m.hiddenFraction(3, 6)).toBe(0.5);
	});
	it('strong scaling: 100 ms on 8 GPUs with 5.8 ms communication: S = 5.5, E = 68%; overlapped S = 8, E = 100%', () => {
		const base = { mode: 'strong' as const, t1: 100, serial: 0, comm: () => 5.8 };
		const a = m.scalingPoint({ ...base, overlap: false }, 8),
			b = m.scalingPoint({ ...base, overlap: true }, 8);
		near(a.speedup, 5.46, 0.005);
		near(a.efficiency, 0.683, 0.005);
		expect(b.speedup).toBeCloseTo(8);
		expect(b.efficiency).toBeCloseTo(1);
		expect(m.scalingPoint({ ...base, overlap: false, serial: 10 }, 1000).speedup).toBeLessThan(11);
		const weak = m.scalingPoint(
			{ mode: 'weak', t1: 100, serial: 0, comm: () => 10, overlap: false },
			8
		);
		near(weak.efficiency, 100 / 110, 1e-9);
	});
	it('row-split matmul on 4 GPUs: 275 GFLOP per GPU, 17.6 ms, 0.9 ms to broadcast B', () => {
		const r = m.matmulRowSplit(8192, 4, 15.6e12, 300e9);
		near(r.flopsPerGpu / 1e9, 275, 0.001);
		near(r.computeSeconds * 1e3, 17.6, 0.005);
		near(r.bcastSeconds * 1e3, 0.9, 0.01);
	});
	it('topology: NVSwitch is NV12 everywhere; on the PCIe tree opposite sockets are about 10x slower than neighbours', () => {
		const nv = m.topologyPreset('nvswitch8'),
			pcie = m.topologyPreset('pcie-tree8');
		expect(m.route(nv, 0, 5).code).toBe('NV12');
		expect(m.route(nv, 0, 5).bottleneckGBs).toBe(300);
		expect(m.route(m.topologyPreset('mesh4'), 0, 3)).toMatchObject({
			code: 'NV4',
			hops: 1,
			bottleneckGBs: 100
		});
		expect(m.route(pcie, 0, 1).code).toBe('PIX');
		expect(m.route(pcie, 0, 3).code).toBe('PHB');
		expect(m.route(pcie, 0, 5).code).toBe('SYS');
		near(m.route(pcie, 0, 1).bottleneckGBs / m.route(pcie, 0, 5).bottleneckGBs, 10, 0.001);
		near(m.transferSeconds(1e9, m.route(pcie, 0, 5).bottleneckGBs) * 1e3, 400, 0.001);
	});
});

describe('attention and the fused MLP ledger', () => {
	it('attention traffic: S is 67.1 MB at N = 4,096; standard moves about 273 MB, 4x the score matrix', () => {
		near(m.scoreMatrixBytes(4096) / 1e6, 67.1, 0.001);
		near(m.standardAttentionTraffic(4096, 64).total / 1e6, 272.6, 0.005);
		near(m.scoreMatrixBytes(8192) / 1e6, 268.4, 0.001);
		near(m.scoreMatrixBytes(16384) / 1e9, 1.07, 0.005);
	});
	it('flash tiling: 80 KB on chip with 64 x 64 tiles at d = 64; K/V re-reads fall as the Q block grows', () => {
		expect(m.flashOnChipBytes(64, 64, 64)).toBe(81_920);
		expect(m.flashAttentionTraffic(4096, 64, 128).total).toBeLessThan(
			m.flashAttentionTraffic(4096, 64, 64).total
		);
		near(m.flashAttentionTraffic(4096, 64, 64).total / 1e6, 136, 0.02);
	});
	it('F6 MLP ledger: 34.4 GFLOP, fused about 126 MB, unfused adds about 176 MB (0.10 ms, ~5% on FP32, ~36% on TF32)', () => {
		const s = { m: 2048, d: 1024, h: 4096 },
			l = m.mlpLedger(s);
		near(l.flops / 1e9, 34.4, 0.002);
		near(l.fused / 1e6, 126, 0.03);
		near(l.extraBytes / 1e6, 176, 0.03);
		near(l.x / 1e6, 8.4, 0.005);
		near(l.h / 1e6, 33.5, 0.005);
		near(l.w1 / 1e6, 16.8, 0.005);
		const fp32 = m.fusionShare(A100, s, m.peakFp32(A100)),
			tf32 = m.fusionShare(A100, s, A100.tf32TFLOPS * 1e12);
		near(fp32.tGemm * 1e3, 2.2, 0.01);
		near(fp32.tExtra * 1e3, 0.1, 0.03);
		near(fp32.share * 100, 4.6, 0.03);
		near(tf32.share * 100, 36, 0.03);
		near(fp32.ai, 273, 0.03);
		near(m.mlpLedger({ m: 2048, d: 2048, h: 8192 }).flops / 1e9, 137.4, 0.001);
	});
});

describe('the calculation workbook', () => {
	const wb = m.workbook();
	const by = (n: number) => wb.find((p) => p.n === n)!;
	it('has all 34 problems, each with an answer and a worked detail', () => {
		expect(wb.map((p) => p.n)).toEqual(Array.from({ length: 34 }, (_, i) => i + 1));
		for (const p of wb) {
			expect(Number.isFinite(p.answer)).toBe(true);
			expect(p.detail.length).toBeGreaterThan(0);
		}
	});
	it('matches the answer key', () => {
		const key: [number, number][] = [
			[1, 8.14],
			[2, 320],
			[3, 20],
			[4, 1.72],
			[5, 0.93],
			[6, 26.7],
			[7, 9.17],
			[8, 80],
			[9, 13],
			[10, 75],
			[11, 37.5],
			[12, 77.2],
			[13, 9766],
			[14, 25],
			[15, 4],
			[16, 47.6],
			[17, 4.5],
			[18, 1793],
			[19, 1.24],
			[20, 131072],
			[21, 12],
			[22, 73.3],
			[23, 21.3],
			[24, 100],
			[25, 175616],
			[26, 268],
			[27, 0.69],
			[28, 14.8],
			[29, 2048],
			[30, 1],
			[31, 6.3],
			[32, 5.5],
			[33, 275],
			[34, 24]
		];
		for (const [n, v] of key) near(by(n).answer, v, n === 24 ? 0.03 : 0.012);
		expect(by(10).detail).toContain('registers');
		expect(by(11).detail).toContain('32');
		expect(by(18).detail).toContain('510');
		expect(by(32).detail).toContain('68');
	});
	it('Check accepts the right answer and rejects a wrong one', () => {
		expect(m.checkAnswer(by(1), 8.14)).toBe(true);
		expect(m.checkAnswer(by(1), 9)).toBe(false);
		expect(m.checkAnswer(by(13), 9766)).toBe(true);
		expect(m.checkAnswer(by(13), 9765)).toBe(false);
	});
});

describe('reduction ladder and warp primitives', () => {
	const x = Array.from({ length: 32 }, (_, i) => i + 1),
		total = 528;
	it('every variant produces the same sum', () => {
		for (const v of [1, 2, 3, 4, 5, 6] as const) expect(m.reduceTrace(v, x).result).toBe(total);
		for (const v of [1, 2, 3, 4, 5, 6] as const)
			expect(m.reduceTrace(v, x.slice(0, 16)).result).toBe(136);
	});
	it('variant 1 wastes lanes inside every warp; variant 3 keeps warps fully active or fully idle', () => {
		expect(m.reduceTrace(1, x).warpEfficiency).toBeLessThan(0.3);
		expect(m.reduceTrace(3, x).warpEfficiency).toBeLessThan(m.reduceTrace(1, x).warpEfficiency + 1);
		const big = Array.from({ length: 256 }, (_, i) => i + 1);
		expect(m.reduceTrace(3, big).warpEfficiency).toBeGreaterThan(
			m.reduceTrace(1, big).warpEfficiency * 1.5
		);
	});
	it('variant 2 has bank conflicts, variant 3 has none', () => {
		const big = Array.from({ length: 256 }, (_, i) => i + 1);
		expect(m.reduceTrace(2, big).bankConflictCycles).toBeGreaterThan(0);
		expect(m.reduceTrace(3, big).bankConflictCycles).toBe(0);
		expect(m.reduceTrace(3, x).bankConflictCycles).toBe(0);
	});
	it('shuffles remove barriers; variant 6 ends with one atomic', () => {
		expect(m.reduceTrace(5, x).barriers).toBeLessThan(m.reduceTrace(3, x).barriers);
		expect(m.reduceTrace(6, x).atomics).toBe(1);
		expect(m.barrierCount(256)).toEqual({ sharedOnly: 8, withShuffle: 1 });
		expect(m.reduceTrace(4, x).threads).toBe(16);
	});
	it("shuffle semantics: shfl_down returns the lane's own value past the edge; xor; broadcast", () => {
		const v = x;
		expect(m.shflDown(v, 4)[27]).toBe(32);
		expect(m.shflDown(v, 4)[28]).toBe(29);
		expect(m.shflDown(v, 4)[31]).toBe(32); // past the edge a lane gets its own value expect(m.shflXor([1, 2, 3, 4], 1)).toEqual([2, 1, 4, 3]); expect(m.shflBroadcast([5, 6, 7], 2)).toEqual([7, 7, 7]);
		const w = m.warpReduceSteps(x);
		expect(w[w.length - 1][0]).toBe(total);
		expect(w.length).toBe(6);
	});
	it('ballot and popc: set bits at lanes 2, 4, 5, 7 give rank 2 at lane 5', () => {
		const preds = Array(32).fill(false);
		[2, 4, 5, 7].forEach((l) => (preds[l] = true));
		const mask = m.ballot(preds);
		expect(m.popc(mask)).toBe(4);
		expect(m.ballotRank(mask, 5)).toBe(2);
		expect(m.popc(0xffffffff)).toBe(32);
	});
});
