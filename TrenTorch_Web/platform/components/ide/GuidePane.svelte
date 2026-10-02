<script lang="ts">
	import { marked } from 'marked';
	import markedKatex from 'marked-katex-extension';
	import { tick } from 'svelte';
	import DOMPurify from 'isomorphic-dompurify';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { Badge } from '$components/ui/badge';
	import DiscussionTab from '$components/discussion/DiscussionTab.svelte';
	import type { QuestionContent, QuestionMetadata } from '$data/curriculum/types';
	import type { CompanyTag } from '$data/questions';
	import CompaniesBadge from '$components/CompaniesBadge.svelte';
	import { extractSimpleVersion } from '$processes/ide-content/extract-simple-version';
	import { CheckCircle2, ChevronLeft, ChevronRight } from '@lucide/svelte';
	import {
		embeddedWidgetIds as embeddedWidgetIdsIn,
		mathVisualizerIdSet,
		systemsVisualizerIdSet,
		classicalMLVisualizerIdSet,
		widgetRegistry
	} from '../../widgets/registry.js';
	import '../../widgets/widget-base.css';

	// Registered once, module-wide -- READMEs write formulas as $inline$ or
	// $$block$$ LaTeX, and this is what turns that into real, rendered math
	// instead of literal dollar-sign text.
	marked.use(markedKatex({ throwOnError: false }));

	// Curriculum markdown is first-party today, but nothing enforces that
	// invariant upstream -- sanitize the rendered HTML before it goes into
	// {@html} so a future less-trusted content source (or a compromised
	// `marked`/`marked-katex-extension` release) can't ship a script tag
	// straight to every visitor. DOMPurify's default allowlist covers KaTeX's
	// HTML+MathML output without extra config.
	function toSafeHtml(markdown: string): string {
		return DOMPurify.sanitize(marked.parse(markdown, { async: false }) as string);
	}

	let {
		content,
		isCompleted = false,
		prevId = null,
		nextId = null,
		visibleTabs = ['description', 'theory', 'solution'],
		companies = undefined
	} = $props<{
		content: QuestionContent;
		isCompleted?: boolean;
		prevId?: string | null;
		nextId?: string | null;
		/** Which guide tabs to offer for this question -- the ide/[id] page
		 * narrows this for Problem of the Day questions (today's: just
		 * Description; a past one: Description + Theory, still no Solution).
		 * Every other question gets the full default set. */
		visibleTabs?: ('description' | 'theory' | 'solution' | 'discussion')[];
		/** From data/questions.ts's Question.companies, looked up by slug in
		 * +page.ts -- most questions legitimately have none. */
		companies?: CompanyTag;
	}>();

	// Carry ?from=N (the Questions page this session originally came from,
	// set by QuestionRow.svelte) along through prev/next navigation too --
	// otherwise stepping to an adjacent question drops it, and "Back to
	// Questions" a few steps later lands on page 1 again.
	let fromPage = $derived(browser ? page.url.searchParams.get('from') : null);
	let prevHref = $derived(
		prevId
			? fromPage
				? resolve(`/ide/[id]?from=${fromPage}`, { id: prevId })
				: resolve('/ide/[id]', { id: prevId })
			: null
	);
	let nextHref = $derived(
		nextId
			? fromPage
				? resolve(`/ide/[id]?from=${fromPage}`, { id: nextId })
				: resolve('/ide/[id]', { id: nextId })
			: null
	);

	let activeTab = $state<'description' | 'theory' | 'solution' | 'discussion'>('description');
	let showSolution = $state(false);
	let theoryContainer: HTMLElement | undefined = $state();
	let generatedVisualizerRoot: HTMLDivElement | undefined = $state();

	let descriptionParts = $derived.by(() => {
		const constraintsHeading = /^#{1,6}\s+constraints\b.*$/im.exec(content.descriptionMarkdown);
		return constraintsHeading
			? {
					before: content.descriptionMarkdown.slice(0, constraintsHeading.index),
					constraints: content.descriptionMarkdown.slice(constraintsHeading.index)
				}
			: { before: content.descriptionMarkdown, constraints: '' };
	});
	let descriptionBeforeConstraintsHtml = $derived(toSafeHtml(descriptionParts.before));
	let constraintsHtml = $derived(
		descriptionParts.constraints ? toSafeHtml(descriptionParts.constraints) : ''
	);
	let theoryHtml = $derived(toSafeHtml(content.theoryMarkdown));
	// A question that merges several topics embeds one placeholder per
	// visualizer, `<div data-widget="<id>">`, in its Theory markdown, so each
	// part keeps its own interactive demo. Questions that declare a single
	// `widget:` or that match a generated visualizer id use the paths below.
	let embeddedWidgetIds = $derived(
		content.widgetId ? [] : embeddedWidgetIdsIn(content.theoryMarkdown)
	);
	let activeVisualizerId = $derived(content.widgetId ?? embeddedWidgetIds[0] ?? content.id);
	let hasInteractiveVisualizer = $derived(
		Boolean(
			embeddedWidgetIds.length > 0 ||
			(content.widgetId && widgetRegistry[content.widgetId as keyof typeof widgetRegistry]) ||
			mathVisualizerIdSet.has(content.id) ||
			systemsVisualizerIdSet.has(content.id) ||
			classicalMLVisualizerIdSet.has(content.id)
		)
	);
	// Shown collapsed under the Description so the plain-language idea is in
	// the static page for search engines. Only when this question is allowed
	// to show Theory at all: a Problem of the Day keeps it hidden until its
	// date has passed, so it must not leak here either.
	let simpleVersionHtml = $derived.by(() => {
		if (!visibleTabs.includes('theory')) return '';
		const section = extractSimpleVersion(content.theoryMarkdown);
		return section ? toSafeHtml(section) : '';
	});
	let solutionHtml = $derived(toSafeHtml('```python\n' + content.solutionCode + '\n```'));
	let explanationHtml = $derived(
		content.explanationMarkdown ? toSafeHtml(content.explanationMarkdown) : ''
	);

	const difficultyClass: Record<QuestionMetadata['difficulty'], string> = {
		Beginner: 'text-green-600 dark:text-green-400 border-green-600/30',
		Intermediate: 'text-yellow-600 dark:text-yellow-400 border-yellow-600/30',
		Advanced: 'text-orange-600 dark:text-orange-400 border-orange-600/30',
		Mastery: 'text-red-600 dark:text-red-400 border-red-600/30'
	};

	function selectTab(tab: 'description' | 'theory' | 'solution' | 'discussion') {
		activeTab = tab;
		// The solution only stays revealed while the Solution tab is actually
		// active -- stepping away to check Theory (or back to Description)
		// hides it again, so seeing it a second time always takes a
		// deliberate click, never leaks in as a side effect of tabbing around.
		if (tab !== 'solution') showSolution = false;
	}

	async function openInteractiveVisualizer() {
		selectTab('theory');
		await tick();
		const root =
			generatedVisualizerRoot ??
			theoryContainer?.querySelector<HTMLElement>(`[data-widget="${activeVisualizerId}"]`);
		if (!root) return;
		root.setAttribute('tabindex', '-1');
		root.focus({ preventScroll: true });
		root.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	// Reset per-question UI state whenever the question itself changes --
	// otherwise an open tab or revealed solution would leak from one
	// question into the next.
	$effect(() => {
		void content.id;
		activeTab = 'description';
		showSolution = false;
	});

	// Mount the question's interactive widget (see platform/widgets/) once
	// its markup is actually in the DOM -- {@html} only sets innerHTML, so
	// any <script> embedded in the Theory markdown itself would never run;
	// the widget's real behavior lives in a dynamically-imported module
	// instead. Re-runs (tearing the previous mount down first) whenever the
	// tab, the question, or theoryHtml itself changes.
	$effect(() => {
		const tab = activeTab;
		const widgetId =
			content.widgetId ??
			(mathVisualizerIdSet.has(content.id) ||
			systemsVisualizerIdSet.has(content.id) ||
			classicalMLVisualizerIdSet.has(content.id)
				? content.id
				: undefined);
		void content.id;
		void theoryHtml;

		if (!browser || tab !== 'theory' || !widgetId) return;

		let cancelled = false;
		let cleanup: (() => void) | undefined;

		(async () => {
			await tick();
			if (cancelled) return;
			const loader = widgetRegistry[widgetId as keyof typeof widgetRegistry];
			if (!loader) return;
			const mod = await loader();
			if (cancelled) return;
			const generatedRoot =
				!content.widgetId &&
				(mathVisualizerIdSet.has(widgetId) ||
					systemsVisualizerIdSet.has(widgetId) ||
					classicalMLVisualizerIdSet.has(widgetId));
			const root = generatedRoot
				? generatedVisualizerRoot
				: theoryContainer?.querySelector(`[data-widget="${widgetId}"]`);
			if (root instanceof HTMLElement) {
				cleanup = mod.mount(root);
			}
		})();

		return () => {
			cancelled = true;
			cleanup?.();
		};
	});

	// Mount every visualizer embedded in the Theory markdown (see
	// embeddedWidgetIds), each into its own placeholder.
	$effect(() => {
		const ids = embeddedWidgetIds;
		void theoryHtml;

		if (!browser || activeTab !== 'theory' || ids.length === 0) return;

		let cancelled = false;
		const cleanups: Array<() => void> = [];

		(async () => {
			await tick();
			for (const id of ids) {
				if (cancelled) return;
				const loader = widgetRegistry[id as keyof typeof widgetRegistry];
				const mod = await loader();
				if (cancelled) return;
				const root = theoryContainer?.querySelector(`[data-widget="${id}"]`);
				if (root instanceof HTMLElement) cleanups.push(mod.mount(root));
			}
		})();

		return () => {
			cancelled = true;
			cleanups.forEach((cleanup) => cleanup());
		};
	});
</script>

<div class="flex h-full flex-col bg-background text-foreground/90">
	<!-- Prev/next question nav -->
	<div class="flex h-8 shrink-0 items-center justify-between border-b border-border px-2">
		<a
			href={prevHref ?? undefined}
			title="Previous question"
			aria-disabled={!prevHref}
			tabindex={prevHref ? 0 : -1}
			class="flex items-center rounded-md p-1 text-muted-foreground transition-colors {prevHref
				? 'hover:bg-secondary hover:text-foreground'
				: 'pointer-events-none opacity-30'}"
		>
			<ChevronLeft class="size-3.5" />
		</a>
		<a
			href={nextHref ?? undefined}
			title="Next question"
			aria-disabled={!nextHref}
			tabindex={nextHref ? 0 : -1}
			class="flex items-center rounded-md p-1 text-muted-foreground transition-colors {nextHref
				? 'hover:bg-secondary hover:text-foreground'
				: 'pointer-events-none opacity-30'}"
		>
			<ChevronRight class="size-3.5" />
		</a>
	</div>

	<!-- Tab bar -->
	<div class="flex h-9 shrink-0 items-center gap-1 border-b border-border px-2 font-mono text-xs">
		{#if visibleTabs.includes('description')}
			<button
				type="button"
				class="px-3 py-1.5 font-medium transition-colors {activeTab === 'description'
					? 'border-b-2 border-muted-foreground text-foreground'
					: 'text-muted-foreground hover:text-foreground'}"
				onclick={() => selectTab('description')}
			>
				Description
			</button>
		{/if}
		{#if visibleTabs.includes('theory')}
			<button
				type="button"
				class="px-3 py-1.5 font-medium transition-colors {activeTab === 'theory'
					? 'border-b-2 border-muted-foreground text-foreground'
					: 'text-muted-foreground hover:text-foreground'}"
				onclick={() => selectTab('theory')}
			>
				Theory
			</button>
		{/if}
		{#if visibleTabs.includes('solution')}
			<button
				type="button"
				class="px-3 py-1.5 font-medium transition-colors {activeTab === 'solution'
					? 'border-b-2 border-muted-foreground text-foreground'
					: 'text-muted-foreground hover:text-foreground'}"
				onclick={() => selectTab('solution')}
			>
				Solution
			</button>
		{/if}
		{#if visibleTabs.includes('discussion')}
			<button
				type="button"
				class="px-3 py-1.5 font-medium transition-colors {activeTab === 'discussion'
					? 'border-b-2 border-foreground text-foreground'
					: 'text-muted-foreground hover:text-foreground'}"
				onclick={() => selectTab('discussion')}
			>
				Discussion
			</button>
		{/if}
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
				{#if companies}
					<CompaniesBadge {companies} />
				{/if}
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
			<div class="question-prose">{@html descriptionBeforeConstraintsHtml}</div>
			{#if hasInteractiveVisualizer}
				<button
					type="button"
					class="interactive-visualizer-cta"
					onclick={openInteractiveVisualizer}
				>
					<span class="interactive-visualizer-cta-kicker">Try it live</span>
					<span class="interactive-visualizer-cta-copy"> Explore the idea interactively </span>
					<span class="interactive-visualizer-cta-action">Open in Theory →</span>
				</button>
			{/if}
			{#if constraintsHtml}
				<!-- eslint-disable-next-line svelte/no-at-html-tags -->
				<div class="question-prose">{@html constraintsHtml}</div>
			{/if}
			{#if simpleVersionHtml}
				<details class="mt-6 border-t border-border pt-4">
					<summary
						class="cursor-pointer font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
					>
						The simple version
					</summary>
					<!-- eslint-disable-next-line svelte/no-at-html-tags -->
					<div class="question-prose mt-3">{@html simpleVersionHtml}</div>
				</details>
			{/if}
		{:else if activeTab === 'theory'}
			<div class="question-prose" bind:this={theoryContainer}>
				<!-- eslint-disable-next-line svelte/no-at-html-tags -->
				{@html theoryHtml}
				{#if !content.widgetId && (mathVisualizerIdSet.has(content.id) || systemsVisualizerIdSet.has(content.id) || classicalMLVisualizerIdSet.has(content.id))}
					<div bind:this={generatedVisualizerRoot} data-widget={content.id}></div>
				{/if}
			</div>
		{:else if activeTab === 'solution' && !showSolution}
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
		{:else if activeTab === 'solution'}
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
		{:else}
			<DiscussionTab questionId={content.id} />
		{/if}
	</div>
</div>
