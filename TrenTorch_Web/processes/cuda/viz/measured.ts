// Real-hardware measurements for VIZ-FLOAT4-BANDWIDTH. There are none yet: they come from running
// scripts/colab/t4_benchmarks.ipynb on a Colab T4 and committing the numbers here. Until then the figure shows
// the simulator's model only and says so; it must never present modelled numbers as measured ones.
export interface MeasuredSeries {
	gpu: string;
	cuda: string;
	date: string;
	runs: number;
	sizesBytes: number[];
	gbs: { float: number[]; float2: number[]; float4: number[] };
}
export const T4_MEASURED: MeasuredSeries | null = null;
