// The CUDA problem bank: data/cuda/problems/<NN-slug>/{meta.json, statement.md, starter.cu, solution.cu,
// explanation.md, harness.js}. Read at build time (like the DSA theory pages) and turned into the same
// QuestionContent the IDE already renders, with kind 'cuda'.
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

export const CUDA_PROBLEMS_DIR = join('data', 'cuda', 'problems');

export interface CudaProblemMeta {
	id: string; // CU-001
	slug: string;
	title: string;
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
	stage: number;
	order: number;
	lesson: string;
	topics: string[];
	mode: 'kernel' | 'program';
	externalRef?: { number: number; note: string };
	theory?: { chapter: string; anchor: string }[];
}

/** What build-metrics.mjs measured on the reference solution (simulator model, not hardware). */
export interface CudaMetrics {
	key: string;
	mode: 'kernel' | 'program';
	gpu: string;
	case?: string;
	bytes?: number;
	flops?: number;
	intensity?: number;
	ridge?: number;
	bound?: 'memory' | 'compute';
	sharedAccesses?: number;
	bankConflicts?: number;
	coalescing?: number;
	divergentBranches?: number;
	branchEvents?: number;
	atomicOps?: number;
	atomicMaxContention?: number;
	estimatedMs?: number;
	peakGBs?: number;
	peakTFLOPS?: number;
	program?: string;
	report?: string;
}

export interface CudaProblem extends CudaProblemMeta {
	/** The IDE question id, e.g. "cuda-vector-addition". */
	ideId: string;
	statement: string;
	starter: string;
	solution: string;
	explanation: string;
	harness: string;
	metrics: CudaMetrics | null;
}

export const cudaIdeId = (slug: string) => `cuda-${slug}`;

const num = (x: number) =>
	x >= 100 ? Math.round(x).toLocaleString('en-US') : Number(x.toPrecision(3)).toString();

/** The "memory-bound or compute-bound?" part of the Solution tab, written from the measured numbers. */
export function performanceSection(m: CudaMetrics | null): string {
	if (!m) return '';
	if (m.mode === 'program' || m.bytes === undefined) {
		return `### Cluster report\n\nThe reference program on simulated ${m.gpu} GPUs:\n\n\`\`\`text\n${(m.report ?? '').trim()}\n\`\`\`\n`;
	}
	const intensity = m.intensity ?? 0;
	const ridge = m.ridge ?? 0;
	const flops = m.flops ?? 0;
	const where = `the reference solution on the simulated ${m.gpu} (case "${m.case}")`;
	const lines: string[] = ['### Memory-bound or compute-bound?', ''];
	if (flops === 0) {
		lines.push(
			`Measured on ${where}: **${num(m.bytes)} bytes** move to and from global memory and there is **no arithmetic at all**. The kernel is **memory-bound**: its time is the bytes divided by the memory bandwidth (${num(m.peakGBs ?? 0)} GB/s here), so only moving fewer bytes, or moving them with better coalescing, makes it faster.`
		);
	} else {
		lines.push(
			`Measured on ${where}: **${num(m.bytes)} bytes** moved and about **${num(flops)} FLOPs** (a static estimate), so the arithmetic intensity is`,
			'',
			`$$I = \\frac{\\text{FLOPs}}{\\text{bytes}} \\approx ${num(intensity)}\\ \\text{FLOP/byte}$$`,
			'',
			`The ${m.gpu}'s ridge point is $${num(m.peakTFLOPS ?? 0)}\\ \\text{TFLOPS} \\div ${Math.round(m.peakGBs ?? 0)}\\ \\text{GB/s} \\approx ${num(ridge)}$ FLOP/byte.`,
			'',
			m.bound === 'memory'
				? `$I$ is below the ridge point, so this kernel is **memory-bound**: its time is set by the bytes moved, not by the arithmetic. Fusing it with a neighbouring kernel, or cutting the traffic, helps; extra math tricks do not.`
				: `$I$ is above the ridge point, so this kernel is **compute-bound**: the arithmetic units, not memory, set its time. Fewer or cheaper instructions (\`fmaf\`, fewer divisions) help; moving less data does not.`
		);
	}
	const facts: string[] = [];
	if (m.coalescing !== undefined)
		facts.push(
			`global-memory coalescing: **${Math.round(m.coalescing * 100)}%** of the ideal number of transactions`
		);
	if (m.sharedAccesses)
		facts.push(
			`shared memory: ${num(m.sharedAccesses)} accesses, **${num(m.bankConflicts ?? 0)} bank-conflict replays**`
		);
	if (m.branchEvents)
		facts.push(
			`divergence: ${num(m.divergentBranches ?? 0)} of ${num(m.branchEvents)} warp-level branches diverged`
		);
	if (m.atomicOps)
		facts.push(
			`atomics: ${num(m.atomicOps)}, worst contention on one address ${num(m.atomicMaxContention ?? 0)}`
		);
	if (facts.length) lines.push('', 'The same run also shows:', '', ...facts.map((f) => `- ${f}`));
	lines.push('', "_These numbers come from the simulator's model, not from real hardware._", '');
	return lines.join('\n');
}

export function listCudaProblems(dir = CUDA_PROBLEMS_DIR): CudaProblem[] {
	if (!existsSync(dir)) return [];
	return readdirSync(dir, { withFileTypes: true })
		.filter((d) => d.isDirectory() && !d.name.startsWith('_') && !d.name.startsWith('.'))
		.map((d) => d.name)
		.sort()
		.map((name) => {
			const read = (file: string) => readFileSync(join(dir, name, file), 'utf8');
			const meta = JSON.parse(read('meta.json')) as CudaProblemMeta;
			return {
				...meta,
				ideId: cudaIdeId(meta.slug),
				statement: read('statement.md'),
				starter: read('starter.cu'),
				solution: read('solution.cu'),
				explanation: read('explanation.md'),
				metrics: existsSync(join(dir, name, 'metrics.json'))
					? (JSON.parse(read('metrics.json')) as CudaMetrics)
					: null,
				harness: read('harness.js')
			};
		});
}

export function findCudaProblem(ideId: string): CudaProblem | undefined {
	return listCudaProblems().find((p) => p.ideId === ideId);
}
