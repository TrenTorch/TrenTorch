<script lang="ts">
	import { marked } from 'marked';
	import { Badge } from '$lib/components/ui/badge';
	import type { QuestionContent, QuestionMetadata } from '$lib/curriculum/types';
	import { CheckCircle2 } from '@lucide/svelte';

	let { content, isCompleted = false } = $props<{
		content: QuestionContent;
		isCompleted?: boolean;
	}>();

	let activeTab = $state<'description' | 'theory' | 'solution'>('description');
	let showSolution = $state(false);

	let descriptionHtml = $derived(
		marked.parse(content.descriptionMarkdown, { async: false }) as string
	);
	let theoryHtml = $derived(marked.parse(content.theoryMarkdown, { async: false }) as string);
	let solutionHtml = $derived(
		marked.parse('```python\n' + content.solutionCode + '\n```', { async: false }) as string
	);
	let explanationHtml = $derived(
		content.explanationMarkdown
			? (marked.parse(content.explanationMarkdown, { async: false }) as string)
			: ''
	);

	const difficultyClass: Record<QuestionMetadata['difficulty'], string> = {
		Beginner: 'text-green-600 dark:text-green-400 border-green-600/30',
		Intermediate: 'text-yellow-600 dark:text-yellow-400 border-yellow-600/30',
		Advanced: 'text-orange-600 dark:text-orange-400 border-orange-600/30',
		Mastery: 'text-red-600 dark:text-red-400 border-red-600/30'
	};

	function selectTab(tab: 'description' | 'theory' | 'solution') {
		activeTab = tab;
		// The solution only stays revealed while the Solution tab is actually
		// active -- stepping away to check Theory (or back to Description)
		// hides it again, so seeing it a second time always takes a
		// deliberate click, never leaks in as a side effect of tabbing around.
		if (tab !== 'solution') showSolution = false;
	}

	// Reset per-question UI state whenever the question itself changes --
	// otherwise an open tab or revealed solution would leak from one
	// question into the next.
	$effect(() => {
		void content.id;
		activeTab = 'description';
		showSolution = false;
	});
</script>

<div class="flex h-full flex-col bg-background text-foreground/90">
	<!-- Tab bar -->
	<div class="flex h-9 shrink-0 items-center gap-1 border-b border-border px-2 font-mono text-xs">
		<button
			type="button"
			class="px-3 py-1.5 font-medium transition-colors {activeTab === 'description'
				? 'border-b-2 border-foreground text-foreground'
				: 'text-muted-foreground hover:text-foreground'}"
			onclick={() => selectTab('description')}
		>
			Description
		</button>
		<button
			type="button"
			class="px-3 py-1.5 font-medium transition-colors {activeTab === 'theory'
				? 'border-b-2 border-foreground text-foreground'
				: 'text-muted-foreground hover:text-foreground'}"
			onclick={() => selectTab('theory')}
		>
			Theory
		</button>
		<button
			type="button"
			class="px-3 py-1.5 font-medium transition-colors {activeTab === 'solution'
				? 'border-b-2 border-foreground text-foreground'
				: 'text-muted-foreground hover:text-foreground'}"
			onclick={() => selectTab('solution')}
		>
			Solution
		</button>
	</div>

	<div class="flex-1 overflow-y-auto p-5 text-sm">
		<!-- Header info: shown on every tab so difficulty/tags/solved status
		     stay visible no matter which tab a student is reading. -->
		<div class="mb-5 border-b border-border pb-4">
			<div class="mb-2 flex flex-wrap items-center gap-2">
				<h1 class="font-mono text-lg font-semibold tracking-tight text-foreground">
					{content.metadata.title}
				</h1>
				{#if isCompleted}
					<Badge
						variant="outline"
						class="border-green-600/30 font-mono text-green-600 dark:text-green-400"
					>
						<CheckCircle2 class="size-3" />
						Solved
					</Badge>
				{/if}
			</div>
			<div class="flex flex-wrap items-center gap-1.5 text-xs">
				<Badge
					variant="outline"
					class="font-mono {difficultyClass[
						content.metadata.difficulty as QuestionMetadata['difficulty']
					]}"
				>
					{content.metadata.difficulty}
				</Badge>
				{#each content.metadata.tags as tag (tag)}
					<span
						class="inline-flex items-center rounded-md border border-border bg-muted/50 px-1.5 py-0.5 font-mono text-[11px] leading-none text-muted-foreground"
					>
						{tag}
					</span>
				{/each}
			</div>
		</div>

		{#if activeTab === 'description'}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="question-prose">{@html descriptionHtml}</div>
		{:else if activeTab === 'theory'}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="question-prose">{@html theoryHtml}</div>
		{:else if !showSolution}
			<div class="flex flex-col items-center justify-center gap-3 py-16 text-center">
				<p class="max-w-xs text-xs text-muted-foreground">
					Try to solve it yourself first. The solution is here if you get stuck.
				</p>
				<button
					type="button"
					class="border border-border bg-secondary px-3 py-1.5 font-mono text-xs font-medium text-foreground transition-colors hover:border-foreground/30 hover:bg-muted"
					onclick={() => (showSolution = true)}
				>
					Reveal solution
				</button>
			</div>
		{:else}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="question-prose">{@html solutionHtml}</div>
			{#if explanationHtml}
				<div class="mt-6 border-t border-border pt-5">
					<h2
						class="mb-2 font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
					>
						Why it's written this way
					</h2>
					<!-- eslint-disable-next-line svelte/no-at-html-tags -->
					<div class="question-prose">{@html explanationHtml}</div>
				</div>
			{/if}
		{/if}
	</div>
</div>
