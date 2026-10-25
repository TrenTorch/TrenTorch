<script lang="ts">
	import { marked } from 'marked';
	import { markdownMath } from '$processes/markdown/markdown-math';
	import { tick } from 'svelte';
	import DOMPurify from 'isomorphic-dompurify';
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import Button from '$components/Button.svelte';
	import DiscussionTab from '$components/discussion/DiscussionTab.svelte';
	import ReportBugDialog from './ReportBugDialog.svelte';
	import type { QuestionContent, QuestionMetadata } from '$data/curriculum/types';
	import type { CompanyTag } from '$data/questions';
	import CompaniesBadge from '$components/CompaniesBadge.svelte';
	import {
		BookOpen,
		CheckCheck,
		CheckCircle2,
		ExternalLink,
		FileText,
		Lightbulb,
		MessageSquare
	} from '@lucide/svelte';
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
	marked.use(markdownMath({ throwOnError: false }));

	// Curriculum markdown is first-party today, but nothing enforces that
	// invariant upstream -- sanitize the rendered HTML before it goes into
	// {@html} so a future less-trusted content source (or a compromised
	// `marked`/`marked-katex-extension` release) can't ship a script tag
	// straight to every visitor. DOMPurify's default allowlist covers KaTeX's
	// HTML+MathML output without extra config.
	// Hints are one short line that may hold `code`.
	function toSafeInline(markdown: string): string {
		return DOMPurify.sanitize(marked.parseInline(markdown, { async: false }) as string);
	}

	function toSafeHtml(markdown: string): string {
		return DOMPurify.sanitize(marked.parse(markdown, { async: false }) as string);
	}

	let {
		content,
		isCompleted = false,
		visibleTabs = ['description', 'theory', 'solution'],
		companies = undefined
	} = $props<{
		content: QuestionContent;
		isCompleted?: boolean;
		/** Which guide tabs to offer for this question -- the ide/[id] page
		 * narrows this for Problem of the Day questions (today's: just
		 * Description; a past one: Description + Theory, still no Solution).
		 * Every other question gets the full default set. */
		visibleTabs?: ('description' | 'theory' | 'solution' | 'discussion')[];
		/** From data/questions.ts's Question.companies, looked up by slug in
		 * +page.ts -- most questions legitimately have none. */
		companies?: CompanyTag;
	}>();

	let relatedModuleHref = $derived.by(() => {
		const relatedModule = content.metadata.relatedModule;
		if (!relatedModule) return null;
		return (
			resolve('/questions/[partId]', { partId: relatedModule.partId }) +
			`?topic=${encodeURIComponent(relatedModule.topicTag)}`
		);
	});

	let activeTab = $state<'description' | 'theory' | 'hints' | 'solution' | 'discussion'>(
		'description'
	);
	let showSolution = $state(false);
	// DSA sheet hints are shown one at a time, so a student takes only as much help as needed.
	let hintsShown = $state(0);
	let reportBugOpen = $state(false);
	let scroller: HTMLElement | undefined = $state();
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
	let solutionHtml = $derived(
		toSafeHtml(
			'```' +
				(content.dbSchema !== undefined ? 'sql' : 'python') +
				'\n' +
				content.solutionCode +
				'\n```'
		)
	);
	let explanationHtml = $derived(
		content.explanationMarkdown ? toSafeHtml(content.explanationMarkdown) : ''
	);

	const tabs = [
		{ id: 'description', label: 'Description', icon: FileText },
		{ id: 'theory', label: 'Theory', icon: BookOpen },
		{ id: 'hints', label: 'Hints', icon: Lightbulb },
		{ id: 'solution', label: 'Solution', icon: CheckCheck },
		{ id: 'discussion', label: 'Discussion', icon: MessageSquare }
	] as const;

	// Difficulty is shown as a small meter (bars filled) in the theme's own colours.
	const difficultyMeter: Record<QuestionMetadata['difficulty'], { level: number; color: string }> =
		{
			Beginner: { level: 1, color: 'var(--ide-ok)' },
			Intermediate: { level: 2, color: 'var(--ide-warn)' },
			Advanced: { level: 3, color: 'color-mix(in oklab, var(--ide-warn) 50%, var(--ide-bad))' },
			Mastery: { level: 4, color: 'var(--ide-bad)' }
		};
	const meter = $derived(
		difficultyMeter[content.metadata.difficulty as QuestionMetadata['difficulty']] ??
			difficultyMeter.Beginner
	);

	function selectTab(tab: 'description' | 'theory' | 'hints' | 'solution' | 'discussion') {
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

	// Python code blocks are coloured with the chosen theme: CodeMirror's Python parser walks the
	// text and each token gets a class (syn-keyword ...), which the theme's variables paint. The
	// parser loads on first use, like the editor does.
	let painter: Promise<{
		parse: (code: string) => unknown;
		paint: (
			code: string,
			tree: unknown,
			put: (text: string, classes: string) => void,
			br: () => void
		) => void;
	}> | null = null;

	function loadPainter() {
		painter ??= Promise.all([
			import('@codemirror/lang-python'),
			import('@codemirror/language'),
			import('@lezer/highlight')
		]).then(([py, lang, hl]) => {
			const t = hl.tags;
			const style = lang.HighlightStyle.define([
				{ tag: t.comment, class: 'syn-comment' },
				{
					tag: [
						t.keyword,
						t.controlKeyword,
						t.moduleKeyword,
						t.operatorKeyword,
						t.definitionKeyword,
						t.self
					],
					class: 'syn-keyword'
				},
				{ tag: t.operator, class: 'syn-operator' },
				{
					tag: [t.function(t.variableName), t.function(t.definition(t.variableName))],
					class: 'syn-fn'
				},
				{ tag: [t.className, t.definition(t.className), t.typeName], class: 'syn-cls' },
				{ tag: [t.string, t.special(t.string), t.docString], class: 'syn-string' },
				{ tag: [t.number, t.bool, t.null], class: 'syn-number' },
				{ tag: t.propertyName, class: 'syn-property' },
				{ tag: [t.variableName, t.definition(t.variableName)], class: 'syn-variable' },
				{ tag: t.meta, class: 'syn-meta' },
				{ tag: t.invalid, class: 'syn-invalid' }
			]);
			return {
				parse: (code: string) => py.pythonLanguage.parser.parse(code),
				paint: (code, tree, put, br) =>
					// eslint-disable-next-line @typescript-eslint/no-explicit-any
					hl.highlightCode(code, tree as any, style, put, br)
			};
		});
		return painter;
	}

	async function paintBlocks() {
		const blocks = scroller?.querySelectorAll<HTMLElement>(
			'.ide-prose pre > code.language-python:not([data-painted])'
		);
		if (!blocks?.length) return;
		const { parse, paint } = await loadPainter();
		for (const code of blocks) {
			const text = code.textContent ?? '';
			const fragment = document.createDocumentFragment();
			paint(
				text,
				parse(text),
				(piece, classes) => {
					if (!classes) return void fragment.append(piece);
					const span = document.createElement('span');
					span.className = classes;
					span.textContent = piece;
					fragment.append(span);
				},
				() => fragment.append('\n')
			);
			code.replaceChildren(fragment);
			code.dataset.painted = '1';
		}
	}

	// Every code block in the reading area gets colour and a Copy button (shown on hover).
	$effect(() => {
		void [activeTab, descriptionBeforeConstraintsHtml, constraintsHtml, theoryHtml, solutionHtml];
		void [showSolution, explanationHtml];
		if (!browser) return;
		tick().then(async () => {
			try {
				await paintBlocks();
			} catch {
				// no colour is better than no code
			}
			for (const pre of scroller?.querySelectorAll<HTMLPreElement>('.ide-prose pre') ?? []) {
				if (pre.querySelector(':scope > .copy-code')) continue;
				const button = document.createElement('button');
				button.type = 'button';
				button.className = 'copy-code';
				button.textContent = 'Copy';
				button.setAttribute('aria-label', 'Copy code');
				button.addEventListener('click', async () => {
					try {
						await navigator.clipboard.writeText(pre.querySelector('code')?.innerText ?? '');
						button.textContent = 'Copied';
						setTimeout(() => (button.textContent = 'Copy'), 1500);
					} catch {
						button.textContent = 'Press Ctrl+C';
					}
				});
				pre.appendChild(button);
			}
		});
	});

	// Reset per-question UI state whenever the question itself changes --
	// otherwise an open tab or revealed solution would leak from one
	// question into the next.
	$effect(() => {
		void content.id;
		activeTab = 'description';
		showSolution = false;
		hintsShown = 0;
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

<div class="flex h-full bg-background text-foreground">
	<!-- A slim rail for the guide's sections, with the previous / next question
	     arrows at its foot -->
	<div
		class="flex w-12 shrink-0 flex-col items-center gap-1 border-r border-border bg-secondary py-2"
		role="tablist"
		aria-orientation="vertical"
		aria-label="Question sections"
	>
		{#each tabs as tab (tab.id)}
			{#if tab.id === 'hints' ? Boolean(content.metadata.hints?.length) : visibleTabs.includes(tab.id)}
				<button
					type="button"
					role="tab"
					aria-selected={activeTab === tab.id}
					aria-label={tab.label}
					title={tab.label}
					class="rail-tab relative flex size-9 items-center justify-center rounded-md transition-colors {activeTab ===
					tab.id
						? 'rail-active bg-muted text-foreground'
						: 'text-muted-foreground hover:bg-muted/60 hover:text-foreground'}"
					onclick={() => selectTab(tab.id)}
				>
					<tab.icon class="size-[18px]" />
				</button>
			{/if}
		{/each}
	</div>

	<div bind:this={scroller} class="min-w-0 flex-1 overflow-y-auto px-7 py-6 text-[15px]">
		<!-- Header info: shown on every section so difficulty/tags/solved status
		     stay visible no matter which one a student is reading. -->
		<div class="mb-6">
			<div class="mb-3.5 flex items-start justify-between gap-3">
				<h1 class="text-[2.05rem] leading-[1.15] font-semibold tracking-[-0.02em] text-foreground">
					{content.metadata.title}
				</h1>
				{#if isCompleted}
					<span
						class="mt-1.5 inline-flex shrink-0 items-center gap-1.5 text-sm font-medium text-(--ide-ok)"
					>
						<CheckCircle2 class="size-4" />
						Solved
					</span>
				{/if}
			</div>
			<div class="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs">
				<span
					class="inline-flex items-center gap-1.5 text-xs font-semibold"
					style:color={meter.color}
				>
					<span class="size-1.5 rounded-full" style:background={meter.color} aria-hidden="true"
					></span>
					{content.metadata.difficulty}
				</span>
				{#if companies}
					<CompaniesBadge {companies} />
				{/if}
			</div>
		</div>

		{#if activeTab === 'description'}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="question-prose ide-prose">{@html descriptionBeforeConstraintsHtml}</div>
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
				<div class="question-prose ide-prose">{@html constraintsHtml}</div>
			{/if}
			{#if content.metadata.tags.length}
				<div class="mt-8 border-t border-border pt-5">
					<h2 class="mb-3 text-xs font-semibold tracking-wide text-muted-foreground uppercase">
						Keywords
					</h2>
					<div class="flex flex-wrap gap-2">
						{#each content.metadata.tags as tag (tag)}
							<span class="rounded bg-muted px-2 py-1 font-mono text-[11px] text-muted-foreground"
								>{tag}</span
							>
						{/each}
					</div>
				</div>
			{/if}
			{#if content.metadata.references?.length}
				<div class="mt-8 border-t border-border pt-5">
					<h2 class="mb-3 text-xs font-semibold tracking-wide text-muted-foreground uppercase">
						References
					</h2>
					<ul class="flex flex-col gap-2">
						{#each content.metadata.references as ref (ref.url)}
							<li>
								<!-- eslint-disable svelte/no-navigation-without-resolve -- external articles, not app routes -->
								<a
									href={ref.url}
									target="_blank"
									rel="noopener noreferrer"
									class="group flex items-start gap-2 text-sm text-foreground/90 transition-colors hover:text-foreground"
								>
									<ExternalLink class="mt-0.5 size-3.5 shrink-0 text-muted-foreground" />
									<span class="min-w-0">
										<span
											class="underline decoration-border underline-offset-2 group-hover:decoration-foreground/50"
											>{ref.title}</span
										>
										<span class="block text-xs text-muted-foreground"
											>{new URL(ref.url).hostname.replace(/^www\./, '')}</span
										>
									</span>
								</a>
								<!-- eslint-enable svelte/no-navigation-without-resolve -->
							</li>
						{/each}
					</ul>
				</div>
			{/if}
			<div class="mt-8 flex flex-wrap items-center gap-3 border-t border-border pt-5">
				{#if content.metadata.kind === 'problemset' && relatedModuleHref && content.metadata.relatedModule}
					<!-- eslint-disable svelte/no-navigation-without-resolve -- already passed through resolve() in relatedModuleHref -->
					<a
						href={relatedModuleHref}
						class="rounded-md bg-muted px-3.5 py-2 text-[13px] font-medium text-foreground transition-colors hover:bg-foreground/15"
					>
						Learn: {content.metadata.relatedModule.topicTag}
					</a>
					<!-- eslint-enable svelte/no-navigation-without-resolve -->
				{/if}
				<Button variant="outline" size="sm" onclick={() => (reportBugOpen = true)}>
					Report a bug
				</Button>
			</div>
			<ReportBugDialog
				bind:open={reportBugOpen}
				questionId={content.id}
				questionTitle={content.metadata.title}
			/>
		{:else if activeTab === 'theory'}
			<div class="question-prose ide-prose" bind:this={theoryContainer}>
				<!-- eslint-disable-next-line svelte/no-at-html-tags -->
				{@html theoryHtml}
				{#if !content.widgetId && (mathVisualizerIdSet.has(content.id) || systemsVisualizerIdSet.has(content.id) || classicalMLVisualizerIdSet.has(content.id))}
					<div bind:this={generatedVisualizerRoot} data-widget={content.id}></div>
				{/if}
			</div>
		{:else if activeTab === 'hints'}
			<p class="mb-4 text-sm text-muted-foreground">
				Take only as many as you need. Each one gives away a little more.
			</p>
			<div class="space-y-3">
				{#each content.metadata.hints?.slice(0, hintsShown) ?? [] as hint, index (index)}
					<div
						class="rounded-md border border-border bg-secondary px-4 py-3 text-sm leading-relaxed"
					>
						<span class="text-xs font-semibold text-muted-foreground">
							Hint {index + 1} of {content.metadata.hints?.length}
						</span>
						<!-- eslint-disable-next-line svelte/no-at-html-tags -->
						<p class="question-prose ide-prose mt-1 font-normal">{@html toSafeInline(hint)}</p>
					</div>
				{/each}
				{#if hintsShown < (content.metadata.hints?.length ?? 0)}
					<button
						type="button"
						class="rounded-md bg-muted px-3.5 py-2 text-[13px] font-medium text-foreground transition-colors hover:bg-foreground/15"
						onclick={() => (hintsShown += 1)}
					>
						Show hint {hintsShown + 1}
					</button>
				{/if}
			</div>
		{:else if activeTab === 'solution' && !showSolution}
			<div class="flex flex-col items-center justify-center gap-3 py-16 text-center">
				<p class="max-w-xs text-xs text-muted-foreground">
					Try to solve it yourself first. The solution is here if you get stuck.
				</p>
				<button
					type="button"
					class="rounded-md bg-muted px-3.5 py-2 text-[13px] font-medium text-foreground transition-colors hover:bg-foreground/15"
					onclick={() => (showSolution = true)}
				>
					Reveal solution
				</button>
			</div>
		{:else if activeTab === 'solution'}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="question-prose ide-prose">{@html solutionHtml}</div>
			{#if explanationHtml}
				<div class="mt-6 border-t border-border pt-5">
					<h2 class="mb-2 text-xs font-semibold tracking-wide text-muted-foreground uppercase">
						Why it's written this way
					</h2>
					<!-- eslint-disable-next-line svelte/no-at-html-tags -->
					<div class="question-prose ide-prose">{@html explanationHtml}</div>
				</div>
			{/if}
		{:else}
			<DiscussionTab questionId={content.id} />
		{/if}
	</div>
</div>

<style>
	/* The reading style for a question: Inter at 15px on a 1.75 line, headings
	   that read as headings, and the "Input: / Output:" labels and code blocks
	   of an example set off as one tidy card (the label is the paragraph
	   right before a code block). Scoped to the IDE; the privacy and terms
	   pages share .question-prose and keep their own look. */
	:global(.ide-prose) {
		font-size: 0.9375rem;
		line-height: 1.75;
		font-family: var(--ide-sans);
	}
	:global(.ide-prose :where(h1, h2, h3, h4)) {
		font-family: var(--ide-sans);
		letter-spacing: -0.01em;
		color: var(--foreground);
	}
	:global(.ide-prose :where(h2)) {
		margin: 2rem 0 0.75rem;
		font-size: 1.0625rem;
		font-weight: 650;
		line-height: 1.4;
	}
	:global(.ide-prose :where(h3)) {
		margin: 1.4rem 0 0.5rem;
		font-size: 0.9375rem;
		font-weight: 600;
		line-height: 1.5;
	}
	:global(.ide-prose :where(p)) {
		margin: 0.75rem 0;
		color: color-mix(in oklab, var(--foreground) 88%, transparent);
	}
	:global(.ide-prose :where(strong)) {
		color: var(--foreground);
		font-weight: 600;
	}
	:global(.ide-prose :where(p:has(+ pre))) {
		margin: 0.85rem 0 0.35rem;
		font-size: 0.8125rem;
		font-weight: 600;
		color: var(--muted-foreground);
	}
	.rail-active::before {
		content: '';
		position: absolute;
		left: -9px;
		top: 9px;
		bottom: 9px;
		width: 3px;
		border-radius: 0 3px 3px 0;
		background: var(--ide-accent);
	}
	:global(.ide-prose :where(pre)) {
		position: relative;
		margin: 0 0 0.25rem;
		padding: 0.7rem 1rem;
		border: 1px solid var(--border);
		border-radius: 0.375rem;
		background: var(--ide-code, var(--muted));
		font-family: var(--ide-mono);
		font-size: 0.8125rem;
		font-weight: 400;
		letter-spacing: -0.005em;
		line-height: 1.7;
	}
	:global(.ide-prose :where(:not(pre) > code)) {
		border: 0;
		border-radius: 0.25rem;
		background: var(--muted);
		padding: 0.15em 0.4em;
		font-family: var(--ide-mono);
		font-size: 0.85em;
		font-weight: 450;
	}
	:global(.ide-prose :where(li)) {
		margin-block: 0.4em;
		color: color-mix(in oklab, var(--foreground) 88%, transparent);
	}
	:global(.ide-prose :where(li)::marker) {
		color: var(--muted-foreground);
	}
	:global(.ide-prose :where(details)) {
		border-color: var(--border);
		border-radius: 0.375rem;
		background: var(--secondary);
	}
	:global(.ide-prose pre code) {
		font-family: inherit;
		font-size: inherit;
		font-weight: inherit;
	}
	:global(.ide-prose :where(table)) {
		width: 100%;
		margin: 0.75rem 0;
		border-collapse: collapse;
		font-size: 0.8125rem;
		line-height: 1.5;
	}
	:global(.ide-prose :where(th, td)) {
		border-bottom: 1px solid var(--border);
		padding: 0.45rem 0.7rem;
		text-align: left;
		vertical-align: top;
	}
	:global(.ide-prose :where(th)) {
		color: var(--muted-foreground);
		font-size: 0.75rem;
		font-weight: 600;
	}
	:global(.ide-prose :where(td code)) {
		background: transparent;
		padding: 0;
		font-size: 0.78rem;
		white-space: pre-wrap;
		word-break: break-word;
	}
	:global(.ide-prose pre code) {
		color: var(--syn-fg, inherit);
	}
	:global(.ide-prose .syn-comment) {
		color: var(--syn-comment);
		font-style: italic;
	}
	:global(.ide-prose .syn-keyword) {
		color: var(--syn-keyword);
	}
	:global(.ide-prose .syn-operator) {
		color: var(--syn-operator);
	}
	:global(.ide-prose .syn-fn) {
		color: var(--syn-fn);
	}
	:global(.ide-prose .syn-cls) {
		color: var(--syn-cls);
	}
	:global(.ide-prose .syn-string) {
		color: var(--syn-string);
	}
	:global(.ide-prose .syn-number) {
		color: var(--syn-number);
	}
	:global(.ide-prose .syn-property) {
		color: var(--syn-property);
	}
	:global(.ide-prose .syn-variable) {
		color: var(--syn-variable);
	}
	:global(.ide-prose .syn-meta) {
		color: var(--syn-meta);
	}
	:global(.ide-prose .syn-invalid) {
		color: var(--syn-invalid);
	}
	:global(.ide-prose pre .copy-code) {
		position: absolute;
		top: 6px;
		right: 6px;
		border: 1px solid var(--border);
		border-radius: 6px;
		background: var(--secondary);
		padding: 1px 8px;
		font-family: var(--ide-mono);
		font-size: 10px;
		color: var(--muted-foreground);
		opacity: 0;
		transition: opacity 120ms;
		cursor: pointer;
	}
	:global(.ide-prose pre:hover .copy-code),
	:global(.ide-prose pre .copy-code:focus-visible) {
		opacity: 1;
	}
	:global(.ide-prose pre .copy-code:hover) {
		color: var(--foreground);
	}
	:global(.ide-prose :where(summary)) {
		font-family: var(--ide-sans);
	}
</style>
