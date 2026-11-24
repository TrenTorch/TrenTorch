<script lang="ts">
	import CudaFooter from '$components/cuda/CudaFooter.svelte';
	import { resolve } from '$app/paths';
	import glossary from '$data/cuda/glossary.json';
	const terms = Object.entries(
		glossary as Record<string, { name: string; definition: string }>
	).sort((a, b) => a[1].name.localeCompare(b[1].name));
</script>

<svelte:head><title>CUDA glossary | TrenTorch</title></svelte:head>

<main class="mx-auto w-full max-w-3xl px-4 py-8">
	<a
		href={resolve('/modules/gpu/theory')}
		class="text-sm text-muted-foreground hover:text-foreground">← CUDA theory</a
	>
	<h1 class="mt-2 mb-6 text-3xl font-semibold tracking-tight">Glossary</h1>
	<dl class="space-y-4">
		{#each terms as [id, t] (id)}
			<div {id} class="scroll-mt-20">
				<dt class="font-medium">{t.name}</dt>
				<dd class="text-sm text-muted-foreground">{t.definition}</dd>
			</div>
		{/each}
	</dl>
</main>

<CudaFooter />
