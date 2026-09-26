<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { Check } from '@lucide/svelte';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import type { Question } from '$data/questions';

	let { question, meta }: { question: Question; meta?: string | null } = $props();

	const isSolved = $derived(solved.isSolved(question.slug));
	// "Attempted" only shows on its own when the question isn't already
	// solved -- solved is the stronger state and subsumes it.
	const isAttempted = $derived(!isSolved && attempted.isAttempted(question.slug));

	// Carry the Questions page's own current page number into the IDE
	// route as ?from=N, so its "Back to Questions" link can return here
	// instead of always landing back on page 1 -- see +page.svelte's
	// backHref for the other half of this.
	const currentQuestionsPage = $derived(browser ? page.url.searchParams.get('page') : null);
	// Opened from the Problem of the Day page: ?src=potd sends the IDE's back
	// arrow there instead of to /questions.
	const fromPotd = $derived(page.url.pathname.startsWith('/potd'));
	const ideHref = $derived.by(() => {
		const id = { id: question.slug };
		if (currentQuestionsPage && fromPotd) {
			return resolve(`/ide/[id]?from=${currentQuestionsPage}&src=potd`, id);
		}
		if (fromPotd) return resolve('/ide/[id]?src=potd', id);
		if (currentQuestionsPage) return resolve(`/ide/[id]?from=${currentQuestionsPage}`, id);
		return resolve('/ide/[id]', id);
	});
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
		class="flex size-4 shrink-0 cursor-not-allowed items-center justify-center rounded-[4px] border {isSolved
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
	<a href={ideHref} class="flex flex-1 items-center justify-between gap-2">
		<span class="flex min-w-0 items-center gap-2 {isSolved ? 'text-muted-foreground line-through' : ''}">
			<span class="truncate">{question.title}</span>
			{#if isAttempted}
				<span
					class="inline-flex shrink-0 items-center rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 font-mono text-[10px] leading-none text-amber-600 dark:text-amber-400"
					title="You've submitted an attempt at this question"
				>
					Attempted
				</span>
			{/if}
		</span>
		<span class="flex shrink-0 items-center gap-4">
			{#if meta}
				<span
					class="rounded-sm bg-secondary/60 px-2.5 py-1 font-mono text-xs whitespace-nowrap text-muted-foreground"
					>{meta}</span
				>
			{/if}
			<DifficultyBadge difficulty={question.difficulty} />
		</span>
	</a>
</div>
