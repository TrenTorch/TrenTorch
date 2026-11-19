<script lang="ts">
	import { resolve } from '$app/paths';
	import glossary from '$data/cuda/glossary.json';
	// A term the learner may not know: hover (or focus) shows the definition and a link to the glossary.
	let { term }: { term: string } = $props();
	const entry = $derived((glossary as Record<string, { name: string; definition: string }>)[term]);
</script>

<a
	class="term"
	href="{resolve('/cuda/glossary')}#{term}"
	title={entry ? `${entry.name}: ${entry.definition}` : term}
>
	{entry?.name ?? term}
</a>

<style>
	.term {
		font-size: 0.75rem;
		padding: 0.05rem 0.4rem;
		border: 1px dotted var(--muted-foreground);
		border-radius: 999px;
		color: var(--muted-foreground);
		text-decoration: none;
	}
	.term:hover,
	.term:focus-visible {
		color: var(--foreground);
		border-style: solid;
	}
</style>
