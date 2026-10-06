<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import SEO from '$components/SEO.svelte';
	import { paperTopics, type Paper, type PaperKind } from '$data/papers';
	import { withSiteName } from '$processes/seo/with-site-name';

	type KindFilter = 'all' | PaperKind;

	const allPapers = paperTopics.flatMap((topic) => topic.papers);
	const implementationCount = allPapers.reduce(
		(sum, paper) => sum + paper.implementations.length,
		0
	);
	const kindLabels: Record<PaperKind, string> = {
		foundational: 'Foundational',
		breakthrough: 'Breakthrough'
	};
	const kinds: { value: KindFilter; label: string }[] = [
		{ value: 'all', label: 'All' },
		{ value: 'foundational', label: 'Foundational' },
		{ value: 'breakthrough', label: 'Breakthrough' }
	];

	let query = $state('');
	let activeTopic = $state<string>('all');
	let activeKind = $state<KindFilter>('all');
	let searchInput: HTMLInputElement | undefined = $state();

	const normalizedQuery = $derived(query.trim().toLowerCase());

	function matches(paper: Paper): boolean {
		if (activeKind !== 'all' && paper.kind !== activeKind) return false;
		if (!normalizedQuery) return true;
		return [paper.title, paper.authors, paper.summary, String(paper.year), paper.arxivId]
			.join(' ')
			.toLowerCase()
			.includes(normalizedQuery);
	}

	const visibleTopics = $derived(
		paperTopics
			.filter((topic) => activeTopic === 'all' || topic.slug === activeTopic)
			.map((topic) => ({ ...topic, papers: topic.papers.filter(matches) }))
			.filter((topic) => topic.papers.length > 0)
	);

	const visibleCount = $derived(visibleTopics.reduce((sum, topic) => sum + topic.papers.length, 0));

	function clearFilters() {
		query = '';
		activeTopic = 'all';
		activeKind = 'all';
	}

	onMount(() => {
		function onKey(event: KeyboardEvent) {
			if (event.key !== '/' || event.metaKey || event.ctrlKey || event.altKey) return;
			const target = event.target as HTMLElement | null;
			if (target && (target.isContentEditable || ['INPUT', 'TEXTAREA'].includes(target.tagName)))
				return;
			event.preventDefault();
			searchInput?.focus();
		}
		window.addEventListener('keydown', onKey);
		return () => window.removeEventListener('keydown', onKey);
	});
</script>

<SEO
	title={withSiteName('Research papers, read and coded')}
	description="Foundational and breakthrough machine learning papers, with the core ideas implemented in the browser."
	path="/papers"
/>

<main class="container max-w-5xl px-4 pt-12 pb-20 md:px-6">
	<header class="mb-10">
		<p class="mb-3 font-mono text-xs tracking-wider text-muted-foreground uppercase">Learn</p>
		<h1 class="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">Research papers</h1>
		<p class="max-w-2xl text-muted-foreground">
			Read the papers behind modern machine learning, highlight what matters, then implement the key
			ideas yourself.
		</p>

		<dl class="mt-8 grid grid-cols-3 gap-3 sm:max-w-md">
			{#each [{ label: 'Topics', value: paperTopics.length }, { label: 'Papers', value: allPapers.length }, { label: 'Implementations', value: implementationCount }] as stat (stat.label)}
				<div class="bg-card rounded-xl border border-border px-4 py-3">
					<dt class="font-mono text-[11px] tracking-wider text-muted-foreground uppercase">
						{stat.label}
					</dt>
					<dd class="mt-1 text-2xl font-semibold tabular-nums">{stat.value}</dd>
				</div>
			{/each}
		</dl>
	</header>

	<section
		aria-label="Filter papers"
		class="sticky top-0 z-10 -mx-4 mb-8 bg-background/90 px-4 pt-2 pb-4 backdrop-blur md:-mx-6 md:px-6"
	>
		<div class="relative">
			<svg
				aria-hidden="true"
				class="pointer-events-none absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-muted-foreground"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
			>
				<circle cx="11" cy="11" r="7" />
				<path d="m20 20-3.5-3.5" />
			</svg>
			<input
				bind:this={searchInput}
				bind:value={query}
				type="search"
				placeholder="Search by title, author, year or arXiv id"
				aria-label="Search papers"
				class="bg-card h-11 w-full rounded-xl border border-border pr-14 pl-10 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
			/>
			<kbd
				class="pointer-events-none absolute top-1/2 right-3 -translate-y-1/2 rounded border border-border px-1.5 font-mono text-[11px] text-muted-foreground"
				aria-hidden="true">/</kbd
			>
		</div>

		<div class="mt-3 flex flex-wrap items-center gap-2" role="group" aria-label="Filter by topic">
			{#each [{ slug: 'all', title: 'All topics' }, ...paperTopics] as chip (chip.slug)}
				<button
					type="button"
					aria-pressed={activeTopic === chip.slug}
					onclick={() => (activeTopic = chip.slug)}
					class="rounded-full border px-3 py-1.5 text-xs font-medium transition-colors focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none {activeTopic ===
					chip.slug
						? 'border-primary bg-primary text-primary-foreground'
						: 'border-border text-muted-foreground hover:border-foreground/30 hover:text-foreground'}"
				>
					{chip.title}
				</button>
			{/each}
		</div>

		<div class="mt-2 flex flex-wrap items-center gap-2" role="group" aria-label="Filter by kind">
			{#each kinds as kind (kind.value)}
				<button
					type="button"
					aria-pressed={activeKind === kind.value}
					onclick={() => (activeKind = kind.value)}
					class="rounded-full border px-3 py-1 text-xs font-medium transition-colors focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none {activeKind ===
					kind.value
						? 'border-foreground bg-foreground text-background'
						: 'border-border text-muted-foreground hover:border-foreground/30 hover:text-foreground'}"
				>
					{kind.label}
				</button>
			{/each}
			<p class="ml-auto text-xs text-muted-foreground tabular-nums" aria-live="polite">
				{visibleCount} of {allPapers.length} papers
			</p>
		</div>
	</section>

	{#if visibleTopics.length === 0}
		<div class="rounded-2xl border border-dashed border-border px-6 py-16 text-center">
			<p class="font-medium">No papers match these filters.</p>
			<p class="mt-1 text-sm text-muted-foreground">
				Try a different search term or clear the filters.
			</p>
			<button
				type="button"
				onclick={clearFilters}
				class="mt-5 rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
			>
				Clear filters
			</button>
		</div>
	{:else}
		<div class="flex flex-col gap-12">
			{#each visibleTopics as topic (topic.slug)}
				<section aria-labelledby="topic-{topic.slug}">
					<div class="mb-4 flex items-end justify-between gap-4 border-b border-border pb-3">
						<div>
							<h2 id="topic-{topic.slug}" class="text-lg font-semibold tracking-tight">
								{topic.title}
							</h2>
							<p class="mt-1 text-sm text-muted-foreground">{topic.description}</p>
						</div>
						<span class="shrink-0 font-mono text-xs text-muted-foreground tabular-nums">
							{topic.papers.length}
							{topic.papers.length === 1 ? 'paper' : 'papers'}
						</span>
					</div>

					<ul
						class="bg-card divide-y divide-border overflow-hidden rounded-2xl border border-border"
					>
						{#each topic.papers as paper (paper.slug)}
							<li
								class="group relative flex flex-col gap-4 p-5 transition-colors hover:bg-muted/40 sm:flex-row sm:items-center"
							>
								<div class="min-w-0 flex-1">
									<div class="mb-1.5 flex flex-wrap items-center gap-2">
										<span
											class="rounded-md px-2 py-0.5 text-[11px] font-medium {paper.kind ===
											'breakthrough'
												? 'bg-primary/15 text-primary'
												: 'bg-muted text-muted-foreground'}"
										>
											{kindLabels[paper.kind]}
										</span>
										<span class="font-mono text-[11px] text-muted-foreground"
											>{paper.implementations.length} implementations</span
										>
									</div>
									<a
										href={resolve('/papers/[slug]', { slug: paper.slug })}
										class="leading-snug font-semibold tracking-tight text-balance after:absolute after:inset-0 hover:text-primary focus-visible:outline-none"
									>
										{paper.title}
									</a>
									<p class="mt-1 text-sm text-muted-foreground">
										{paper.authors} <span aria-hidden="true">·</span>
										{paper.year}
									</p>
								</div>

								<div class="relative z-10 flex shrink-0 items-center gap-3">
									<!-- eslint-disable svelte/no-navigation-without-resolve -->
									<a
										href={`https://arxiv.org/abs/${paper.arxivId}`}
										target="_blank"
										rel="noopener noreferrer"
										class="rounded-md border border-border px-2 py-1 font-mono text-[11px] text-muted-foreground hover:text-foreground focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
										aria-label="View {paper.title} on arXiv"
									>
										arXiv {paper.arxivId}
									</a>
									<!-- eslint-enable svelte/no-navigation-without-resolve -->
									<a
										href={resolve('/papers/[slug]', { slug: paper.slug })}
										class="rounded-lg bg-foreground px-3.5 py-2 text-xs font-medium text-background transition-opacity hover:opacity-90 focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
									>
										Read paper
									</a>
								</div>
							</li>
						{/each}
					</ul>
				</section>
			{/each}
		</div>
	{/if}
</main>
