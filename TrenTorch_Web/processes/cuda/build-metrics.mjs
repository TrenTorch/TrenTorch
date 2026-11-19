// Runs every reference solution on the simulator and writes data/cuda/problems/<dir>/metrics.json: the numbers
// the Solution tab quotes ("memory-bound or compute-bound?"). Run with `npm run cuda:metrics` after changing a
// solution or harness; problems.spec.ts fails when a metrics file is stale.
import { createRequire } from 'node:module';
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { createWorkerVm } from './worker-vm.mjs';
import { metricsKey } from './metrics-key.mjs';

const DIR = join('data', 'cuda', 'problems');
const require = createRequire(import.meta.url);
require(join(process.cwd(), 'platform', 'static', 'gpubox', '1.0.0-tt2', 'gpu-profiles.js'));
const getProfile = (name) => globalThis.GPU_PROFILES.getProfile(name);
const REF_GPU = 'A100';

export function classify(c, profile) {
	const bytes = c.globalLoadBytes + c.globalStoreBytes;
	const flops = c.flopCount;
	const ridge = (profile.fp32TFLOPS * 1000) / profile.memoryBandwidthGBs; // FLOP per byte
	const intensity = bytes ? flops / bytes : 0;
	return { bytes, flops, intensity, ridge, bound: intensity < ridge ? 'memory' : 'compute' };
}

const vm = createWorkerVm();
const profile = getProfile(REF_GPU);
let written = 0;
for (const name of readdirSync(DIR).sort()) {
	const read = (f) => readFileSync(join(DIR, name, f), 'utf8');
	const meta = JSON.parse(read('meta.json'));
	const solution = read('solution.cu'),
		harness = read('harness.js');
	const reply = vm.call({ action: 'test', source: solution, harness });
	if (!reply.ok) throw new Error(`${meta.id}: ${reply.error}`);
	const failed = reply.results.filter((r) => !r.passed);
	if (failed.length)
		throw new Error(`${meta.id}: reference fails "${failed[0].name}": ${failed[0].error}`);
	let out;
	if (meta.mode === 'program') {
		const r = reply.results[0];
		out = { mode: 'program', gpu: REF_GPU, program: r.name, report: r.report };
	} else {
		const best = reply.results
			.filter((r) => r.counters)
			.sort(
				(a, b) =>
					b.counters.globalLoadBytes +
					b.counters.globalStoreBytes -
					(a.counters.globalLoadBytes + a.counters.globalStoreBytes)
			)[0];
		const c = best.counters;
		out = {
			mode: 'kernel',
			gpu: REF_GPU,
			case: best.name,
			...classify(c, profile),
			sharedAccesses: c.sharedLoads + c.sharedStores,
			bankConflicts: c.bankConflicts,
			coalescing: c.coalescingEfficiency,
			divergentBranches: c.divergentBranches,
			branchEvents: c.branchEvents,
			atomicOps: c.atomicOps,
			atomicMaxContention: c.atomicMaxContention,
			estimatedMs: c.estimatedTimeMs,
			occupancy: c.occupancy,
			peakGBs: profile.memoryBandwidthGBs,
			peakTFLOPS: profile.fp32TFLOPS
		};
	}
	writeFileSync(
		join(DIR, name, 'metrics.json'),
		JSON.stringify({ key: metricsKey(solution, harness), ...out }, null, 2) + '\n'
	);
	written++;
}
console.log(`wrote metrics for ${written} problems`);
