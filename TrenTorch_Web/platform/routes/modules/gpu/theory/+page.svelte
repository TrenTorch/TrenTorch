<script lang="ts">
	import CudaFooter from '$components/cuda/CudaFooter.svelte';
	import PagePill from '$components/PagePill.svelte';
	import { resolve } from '$app/paths';
	import type { PageProps } from './$types';
	let { data }: PageProps = $props();

	const PARTS: Record<string, string> = {
		A: 'GPU Foundations',
		B: 'The Programming Model',
		C: 'Control Flow',
		D: 'Memory Performance',
		E: 'Parallel Patterns',
		F: 'Advanced and Systems',
		G: 'Calculation Workbook'
	};
	const parts = $derived(
		Object.keys(PARTS)
			.map((p) => ({ id: p, name: PARTS[p], chapters: data.chapters.filter((c) => c.part === p) }))
			.filter((p) => p.chapters.length)
	);
</script>

<svelte:head><title>CUDA theory | TrenTorch</title></svelte:head>

<main class="mx-auto w-full max-w-3xl px-4 py-8">
	<PagePill slug="cuda/theory/" area="cuda" />
	<h1 class="mb-6 font-mono text-3xl font-bold tracking-tight">CUDA theory</h1>
	{#each parts as part (part.id)}
		<h2 class="mt-8 mb-2 text-lg font-medium">{part.name}</h2>
		<ul class="divide-y divide-border rounded-lg border border-border">
			{#each part.chapters as c (c.step)}
				<li>
					<a
						class="flex items-baseline justify-between gap-4 px-4 py-3 hover:bg-secondary"
						href={resolve('/modules/gpu/theory/[chapter]', { chapter: c.step })}
					>
						<span
							><span class="font-mono text-xs text-muted-foreground">{c.id}</span> {c.title}</span
						>
						<span class="text-xs text-muted-foreground">{c.estMinutes} min</span>
					</a>
				</li>
			{/each}
		</ul>
	{/each}
</main>

<CudaFooter />
