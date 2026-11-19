<script lang="ts">
	// Phase 0 spike: proves Gpubox loads and runs in a Worker on the deployed site.
	// Delete (or keep behind noindex) once the real CUDA IDE runtime lands.
	import { onMount } from 'svelte';
	import { runKernel, pingWorker, GPUBOX_VERSION } from '$processes/cuda/gpubox-client';

	const SRC = `__global__ void vecAdd(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}`;
	const N = 1000;

	let status = $state('idle');
	let loadMs = $state<number | null>(null);
	let wallMs = $state<number | null>(null);
	let result = $state<Awaited<ReturnType<typeof runKernel>> | null>(null);
	let correct = $state<boolean | null>(null);
	let error = $state('');
	let evalAllowed = $state<boolean | null>(null);

	onMount(async () => {
		try {
			new Function('return 1')();
			evalAllowed = true;
		} catch {
			evalAllowed = false;
		}
		const start = performance.now();
		status = 'loading Gpubox worker…';
		try {
			loadMs = (await pingWorker()).loadMs;
			status = 'running vecAdd…';
			const a = Array.from({ length: N }, (_, i) => i);
			const b = Array.from({ length: N }, () => 1);
			const run = performance.now();
			result = await runKernel({
				source: SRC,
				kernel: 'vecAdd',
				grid: Math.ceil(N / 256),
				block: 256,
				profile: 'T4',
				buffers: [
					{ type: 'f32', data: a },
					{ type: 'f32', data: b },
					{ type: 'f32', data: new Array(N).fill(0), read: true }
				],
				args: [{ buf: 0 }, { buf: 1 }, { buf: 2 }, N]
			});
			wallMs = performance.now() - run;
			correct = result.outputs[2].every((v, i) => v === i + 1);
			status = 'done';
			console.log('total', performance.now() - start);
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
			status = 'failed';
		}
	});
</script>

<svelte:head>
	<title>CUDA spike | TrenTorch</title>
	<meta name="robots" content="noindex" />
</svelte:head>

<main class="container mx-auto max-w-3xl space-y-4 p-6">
	<h1 class="text-2xl font-semibold">CUDA spike (Gpubox {GPUBOX_VERSION})</h1>
	<p data-testid="status">Status: {status}</p>
	{#if error}<p class="text-red-500" data-testid="error">{error}</p>{/if}
	<ul class="list-disc pl-5 text-sm">
		<li>Main-thread eval allowed by CSP: {evalAllowed ?? '…'} (the worker needs it either way)</li>
		<li>Worker script load: {loadMs === null ? '…' : loadMs.toFixed(1) + ' ms'}</li>
		<li>First run wall time: {wallMs === null ? '…' : wallMs.toFixed(1) + ' ms'}</li>
		<li data-testid="correct">Result correct: {correct ?? '…'}</li>
	</ul>
	{#if result}
		<h2 class="font-medium">Timings (worker)</h2>
		<pre class="overflow-auto rounded bg-black/10 p-3 text-xs">{JSON.stringify(
				result.timings,
				null,
				2
			)}</pre>
		<h2 class="font-medium">Counters</h2>
		<pre class="overflow-auto rounded bg-black/10 p-3 text-xs">{JSON.stringify(
				result.counters,
				null,
				2
			)}</pre>
		<h2 class="font-medium">Diagnostics</h2>
		<pre class="overflow-auto rounded bg-black/10 p-3 text-xs">{JSON.stringify(
				result.diagnostics
			)}</pre>
	{/if}
</main>
