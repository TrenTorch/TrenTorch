<script lang="ts">
	import { ChevronDown } from '@lucide/svelte';
	import QuestionRow from './QuestionRow.svelte';
	import type { Part } from '$lib/data/questions';
	import { collapsedSections } from '$lib/stores/collapsedSections.svelte';

	let { part }: { part: Part } = $props();

	// Open by default, collapses only when the section's own title is
	// clicked -- not a shared accordion (no auto-closing other sections),
	// just an independent per-section toggle. Persisted per-browser
	// (localStorage) so a student who's collapsed the Parts they've
	// already finished doesn't get them all re-opened by a page reload.
	let open = $derived(collapsedSections.isOpen(part.id));

	const questionCount = $derived(
		part.tracks.reduce((sum, track) => sum + track.questions.length, 0)
	);
</script>

<!-- content-visibility:auto lets the browser skip layout/paint/style work
     for whichever sections are off-screen (most of them on load) without
     changing the markup or behaviour. contain-intrinsic-size is a rough
     height guess per collapsed section so the scrollbar doesn't lurch as
     they render in. -->
<section
	class="overflow-hidden rounded-md border border-border [contain-intrinsic-size:auto_600px] [content-visibility:auto]"
>
	<button
		type="button"
		onclick={() => collapsedSections.toggle(part.id)}
		class="flex w-full items-center justify-between border-b border-border px-4 py-3 text-left transition-colors hover:bg-secondary"
		aria-expanded={open}
	>
		<h3 class="font-mono font-semibold">{part.title}</h3>
		<span class="flex items-center gap-2 text-xs text-muted-foreground">
			{questionCount} questions
			<ChevronDown class="size-4 transition-transform {open ? '' : '-rotate-90'}" />
		</span>
	</button>
	{#if open}
		{#each part.tracks as track (track.name)}
			<div class="border-t border-border px-4 py-2 first:border-t-0">
				<h4 class="mb-1 font-mono text-xs tracking-wider text-muted-foreground uppercase">
					{track.name}
				</h4>
				{#each track.questions as question (question.slug)}
					<QuestionRow {question} />
				{/each}
			</div>
		{/each}
	{/if}
</section>
