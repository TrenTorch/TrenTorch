// GPU profiles (T4 / A100 / H100) for the theory visualizations and the workbook. The numbers live in
// data/cuda/gpu-profiles.json so no view hard-codes a hardware figure.
import raw from '../../../data/cuda/gpu-profiles.json';

export type GpuName = 'T4' | 'A100' | 'H100';

export interface GpuProfile {
	name: string;
	architecture: string;
	sms: number;
	/** GPCs on the full die (approx.) */
	gpcs: number;
	fp32PerSm: number;
	boostGHz: number;
	memBusBits: number;
	memGbpsPerPin: number;
	/** Published peak memory bandwidth, GB/s. */
	memBwGBs: number;
	l2MB: number;
	smemPerSmKB: number;
	smemPerBlockMaxKB: number;
	regsPerSm: number;
	/** Registers are allocated per warp in units of this many registers. */
	regAllocUnitPerWarp: number;
	maxRegsPerThread: number;
	maxThreadsPerSm: number;
	maxBlocksPerSm: number;
	maxWarpsPerSm: number;
	schedulersPerSm: number;
	fp32LanesPerSubpartition: number;
	sharedBytesPerCycle: number;
	/** Per-direction host link bandwidth, GB/s. */
	pcieGBs: number;
	pcieGen: number;
	nvlinkGBsPerDirection: number;
	tf32TFLOPS: number;
	fp16TensorTFLOPS: number;
	latencyCycles: { register: number; shared: number; l1: number; l2: number; dram: number };
	latencyIllustrative: boolean;
}

export const GPU_NAMES: GpuName[] = ['T4', 'A100', 'H100'];
const profiles = raw as unknown as Record<GpuName, GpuProfile>;

export function getProfile(name: GpuName): GpuProfile {
	return profiles[name];
}
