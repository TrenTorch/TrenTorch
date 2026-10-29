<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import SolvedMark from './SolvedMark.svelte';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import type { Question } from '$data/questions';
	import type { ProblemsetDifficulty } from '$data/problemset';

	let {
		question,
		meta,
		tags = [],
		trackPage = true,
		wrap = false
	}: {
		question: {
			slug: string;
			title: string;
			difficulty: Question['difficulty'] | ProblemsetDifficulty;
		};
		meta?: string | null;
		/** Small labels right after the title, such as a company or "Past POTD". */
		tags?: string[];
		/**
		 * Carry the list's own ?page=N into the question's link, so its back arrow returns to that page.
		 * Right for the Questions and Problem of the Day lists; the Problemset has its own back target.
		 */
		trackPage?: boolean;
		/** Let the labels drop under the title on a narrow screen instead of squeezing it. */
		wrap?: boolean;
	} = $props();

	const isSolved = $derived(solved.isSolved(question.slug));
	// "Attempted" only shows on its own when the question isn't already
	// solved -- solved is the stronger state and subsumes it.
	const isAttempted = $derived(!isSolved && attempted.isAttempted(question.slug));

	// Carry the Questions page's own current page number into the IDE
	// route as ?from=N, so its "Back to Questions" link can return here
	// instead of always landing back on page 1 -- see +page.svelte's
	// backHref for the other half of this.
	const currentQuestionsPage = $derived(
		browser && trackPage ? page.url.searchParams.get('page') : null
	);
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
	<SolvedMark
		{isSolved}
		questionTitle={question.title}
		class="cursor-not-allowed"
		title={isSolved
			? 'Solved: passed every test on Submit'
			: 'Not solved yet -- open the question and Submit passing code to earn this'}
	/>
	<!-- The question's slug doubles as its IDE content id: Maanas authors
	     src/lib/data/ide-content/{slug}.json per question as the curriculum
	     content lands, and /ide/[id] already renders whatever it finds (or
	     a "not published yet" state if it doesn't). -->
	<a
		href={ideHref}
		class="flex flex-1 items-center justify-between gap-2 {wrap ? 'flex-wrap sm:flex-nowrap' : ''}"
	>
		<span
			class="flex min-w-0 items-center gap-2 {isSolved ? 'text-muted-foreground line-through' : ''}"
		>
			<span class="truncate">{question.title}</span>
			{#each tags as tag (tag)}
				<span
					class="shrink-0 rounded-sm border border-border px-2 py-0.5 font-mono text-[11px] whitespace-nowrap text-muted-foreground"
					>{tag}</span
				>
			{/each}
			{#if isAttempted}
				<span
					class="inline-flex shrink-0 items-center rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 font-mono text-[10px] leading-none text-amber-600 dark:text-amber-400"
					title="You've submitted an attempt at this question"
				>
					Attempted
				</span>
			{/if}
		</span>
		<span
			class="flex items-center {wrap
				? 'max-w-full min-w-0 flex-wrap gap-2 sm:shrink-0 sm:gap-4'
				: 'shrink-0 gap-4'}"
		>
			{#if meta}
				<span
					class="rounded-sm bg-secondary/60 px-2.5 py-1 font-mono text-xs text-muted-foreground {wrap
						? 'sm:whitespace-nowrap'
						: 'whitespace-nowrap'}">{meta}</span
				>
			{/if}
			<DifficultyBadge difficulty={question.difficulty} />
		</span>
	</a>
</div>
