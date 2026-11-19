// The "performance calculator" formulas of chapter A5. Every view and every report uses these functions.
import type { GpuProfile } from './profiles';

/** Peak FP32 in FLOP/s: SMs x cores/SM x 2 (an FMA is two FLOPs) x clock. */
export const peakFp32 = (p: GpuProfile) => p.sms * p.fp32PerSm * 2 * p.boostGHz * 1e9;

/** Peak bandwidth from the memory spec, bytes/s: bus width / 8 x data rate per pin. */
export const bandwidthFromSpec = (busBits: number, gbpsPerPin: number) =>
	(busBits / 8) * gbpsPerPin * 1e9;

export const peakBandwidth = (p: GpuProfile) => p.memBwGBs * 1e9;

/** Ridge point (FLOP/byte) for a given compute roof (FLOP/s) and bandwidth (bytes/s). */
export const ridge = (peakFlops: number, bw: number) => peakFlops / bw;

export const attainable = (peakFlops: number, bw: number, ai: number) =>
	Math.min(peakFlops, ai * bw);

/** Machine balance is the ridge point of the FP32 roof. */
export const machineBalance = (p: GpuProfile) => ridge(peakFp32(p), peakBandwidth(p));

export interface TimeInputs {
	bytes: number;
	flops: number;
	peakFlops: number;
	bw: number;
	etaM?: number;
	etaC?: number;
	launchSeconds?: number;
}
export interface TimeBreakdown {
	tMem: number;
	tCompute: number;
	tLaunch: number;
	total: number;
	bound: 'memory' | 'compute';
	ai: number;
	/** memory time / compute time */
	ratio: number;
}

/** t ~ max(bytes / (eta_m BW), FLOPs / (eta_c Peak)) + t_launch. */
export function timeModel(i: TimeInputs): TimeBreakdown {
	const etaM = i.etaM ?? 0.85,
		etaC = i.etaC ?? 0.8,
		tLaunch = i.launchSeconds ?? 5e-6;
	const tMem = i.bytes / (etaM * i.bw);
	const tCompute = i.flops / (etaC * i.peakFlops);
	return {
		tMem,
		tCompute,
		tLaunch,
		total: Math.max(tMem, tCompute) + tLaunch,
		bound: tMem >= tCompute ? 'memory' : 'compute',
		ai: i.bytes ? i.flops / i.bytes : 0,
		ratio: tCompute ? tMem / tCompute : Infinity
	};
}

/** Time to copy `bytes` over a link: alpha + D / B. */
export const copyTime = (bytes: number, linkBytesPerSec: number, alphaSeconds = 10e-6) =>
	alphaSeconds + bytes / linkBytesPerSec;

/** Amdahl: 1 / ((1 - p) + p / s). */
export const amdahl = (p: number, s: number) => 1 / (1 - p + p / s);
export const amdahlCeiling = (p: number) => 1 / (1 - p);

/** Little's law: bytes in flight = latency x bandwidth. */
export const bytesInFlight = (latencySeconds: number, bw: number) => latencySeconds * bw;

/** 128-byte warp loads that must be outstanding per SM to saturate memory. */
export const warpLoadsPerSm = (
	latencySeconds: number,
	bw: number,
	sms: number,
	bytesPerWarpLoad = 128
) => bytesInFlight(latencySeconds, bw) / sms / bytesPerWarpLoad;

export interface VectorAddInputs {
	cpuBw: number;
	pcieBw: number;
	gpuBw: number;
	kernels?: number;
}
/** Worked example 2 (A5): per element, CPU vs GPU with the data starting on the host. Seconds per element. */
export function vectorAddPerElement(i: VectorAddInputs) {
	const k = i.kernels ?? 1;
	const cpu = (12 * k) / i.cpuBw;
	const gpu = 12 / i.pcieBw + (12 * k) / i.gpuBw;
	return { cpu, gpu, gpuWins: gpu < cpu };
}
/** Smallest number of chained passes for which the GPU wins (real-valued crossover). */
export function crossoverKernels(i: VectorAddInputs) {
	// 12/pcie + 12k/gpu = 12k/cpu  ->  k (1/cpu - 1/gpu) = 1/pcie
	return 1 / i.pcieBw / (1 / i.cpuBw - 1 / i.gpuBw);
}

/** Launch overhead: n launches of `overhead` seconds around `work` seconds of GPU time each (not overlapped). */
export function launchOverhead(n: number, workSeconds: number, overheadSeconds: number) {
	const total = n * (workSeconds + overheadSeconds);
	return {
		total,
		overheadShare: overheadSeconds / (workSeconds + overheadSeconds),
		utilization: workSeconds / (workSeconds + overheadSeconds)
	};
}

/** Effective bandwidth of a copy kernel moving `bytesIn` + `bytesOut` in `seconds`, and eta against peak. */
export function effectiveBandwidth(
	bytesIn: number,
	bytesOut: number,
	seconds: number,
	peakBytesPerSec: number
) {
	const bw = (bytesIn + bytesOut) / seconds;
	return { bw, eta: bw / peakBytesPerSec };
}

/** Work / span. */
export const parallelism = (work: number, span: number) => work / span;
export const parallelTimeLowerBound = (work: number, span: number, p: number) =>
	Math.max(work / p, span);
