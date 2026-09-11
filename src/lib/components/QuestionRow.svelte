<script lang="ts">
	import { resolve } from '$app/paths';
	import { Check } from '@lucide/svelte';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import { solved } from '$lib/stores/solved.svelte';
	import { attempted } from '$lib/stores/attempted.svelte';
	import type { Question } from '$lib/data/questions';

	let { question }: { question: Question } = $props();

	const isSolved = $derived(solved.isSolved(question.slug));
	// "Attempted" only shows on its own when the question isn't already
	// solved -- solved is the stronger state and subsumes it.
	const isAttempted = $derived(!isSolved && attempted.isAttempted(question.slug));
</script>

<div
	class="flex items-center gap-3 border-b border-border px-3 py-2 text-sm transition-colors last:border-0 hover:bg-secondary"
>
	<!-- Status indicator, not a toggle: solved state is earned by passing
	     every hidden test on Submit in the IDE (solved.markSolved(), called
	     from pyodideService), never set directly here. A clickable checkbox
	     used to call solved.toggle() itself, which let anyone fake progress
	     with a single click -- this is intentionally not a <button> and
	     has no click handler at all. -->
	<div
		class="flex size-4 shrink-0 items-center justify-center rounded-[4px] border {isSolved
			? 'border-primary bg-primary text-primary-foreground'
			: 'border-input'}"
		role="img"
		aria-label={isSolved
			? `'${question.title}' is solved`
			: `'${question.title}' is not solved yet`}
		title={isSolved
			? 'Solved: passed every test on Submit'
			: 'Not solved yet -- open the question and Submit passing code to earn this'}
	>
		{#if isSolved}
			<Check class="size-3.5" />
		{/if}
	</div>
	<!-- The question's slug doubles as its IDE content id: Maanas authors
	     src/lib/data/ide-content/{slug}.json per question as the curriculum
	     content lands, and /ide/[id] already renders whatever it finds (or
	     a "not published yet" state if it doesn't). -->
	<a
		href={resolve('/ide/[id]', { id: question.slug })}
		class="flex flex-1 items-center justify-between gap-2"
	>
		<span
			class="flex items-center gap-2 font-mono {isSolved
				? 'text-muted-foreground line-through'
				: ''}"
		>
			{question.title}
			{#if isAttempted}
				<span
					class="inline-flex items-center rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 font-mono text-[10px] leading-none text-amber-600 dark:text-amber-400"
					title="You've submitted an attempt at this question"
				>
					Attempted
				</span>
			{/if}
		</span>
		<DifficultyBadge difficulty={question.difficulty} />
	</a>
</div>
