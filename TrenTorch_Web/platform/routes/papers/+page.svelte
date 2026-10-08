<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import SEO from '$components/SEO.svelte';
	import { paperTopics, type PaperKind } from '$data/papers';
	import { withSiteName } from '$processes/seo/with-site-name';

	const allPapers = paperTopics.flatMap((topic) => topic.papers);
	const implementationCount = allPapers.reduce(
		(sum, paper) => sum + paper.implementations.length,
		0
	);
	const kindLabels: Record<PaperKind, string> = {
		foundational: 'Foundational',
		breakthrough: 'Breakthrough'
	};

	// /papers is prerendered, so the selected track is read from the URL on the client
	// (plain history API, not SvelteKit navigation) and kept in sync with back/forward.
	let trackSlug = $state<string | null>(null);
	const activeTrack = $derived(paperTopics.find((topic) => topic.slug === trackSlug));

	function readTrack(): string | null {
		return new URLSearchParams(window.location.search).get('track');
	}

	function openTrack(slug: string | null) {
		trackSlug = slug;
		window.history.pushState({}, '', slug ? `?track=${slug}` : window.location.pathname);
		window.scrollTo({ top: 0 });
	}

	onMount(() => {
		trackSlug = readTrack();
		const onPop = () => (trackSlug = readTrack());
		window.addEventListener('popstate', onPop);
		return () => window.removeEventListener('popstate', onPop);
	});
</script>

<SEO
	title={withSiteName('Research papers, read and coded')}
	description="Foundational and breakthrough machine learning papers, with the core ideas implemented in the browser."
	path="/papers"
/>

<main class="container max-w-5xl px-4 pt-12 pb-20 md:px-6">
	{#if !activeTrack}
		<header class="mb-10">
			<p class="mb-3 font-mono text-xs tracking-wider text-muted-foreground uppercase">Learn</p>
			<h1 class="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">Research papers</h1>
			<p class="max-w-2xl text-muted-foreground">
				Pick a track, read its papers, then implement the key ideas yourself.
				{paperTopics.length} tracks, {allPapers.length} papers, {implementationCount} implementations.
			</p>
		</header>

		<ul class="grid gap-4 sm:grid-cols-2">
			{#each paperTopics as topic (topic.slug)}
				<li>
					<button
						type="button"
						onclick={() => openTrack(topic.slug)}
						class="bg-card group flex h-full w-full flex-col rounded-2xl border border-border p-5 text-left transition-colors hover:border-foreground/30 hover:bg-muted/40 focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
					>
						<h2 class="text-lg font-semibold tracking-tight group-hover:text-primary">
							{topic.title}
						</h2>
						<p class="mt-1 flex-1 text-sm text-muted-foreground">{topic.description}</p>
						<p class="mt-4 font-mono text-xs text-muted-foreground tabular-nums">
							{topic.papers.length} papers
						</p>
					</button>
				</li>
			{/each}
		</ul>
	{:else}
		<header class="mb-8">
			<button
				type="button"
				onclick={() => openTrack(null)}
				class="mb-4 inline-block text-sm text-muted-foreground hover:text-foreground focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
			>
				&larr; All tracks
			</button>
			<h1 class="mb-2 text-3xl font-bold tracking-tight sm:text-4xl">{activeTrack.title}</h1>
			<p class="max-w-2xl text-muted-foreground">{activeTrack.description}</p>
			<p class="mt-3 font-mono text-xs text-muted-foreground tabular-nums">
				{activeTrack.papers.length} papers
			</p>
		</header>

		<ul class="bg-card divide-y divide-border overflow-hidden rounded-2xl border border-border">
			{#each activeTrack.papers as paper (paper.slug)}
				<li
					class="group relative flex flex-col gap-4 p-5 transition-colors hover:bg-muted/40 sm:flex-row sm:items-center"
				>
					<div class="min-w-0 flex-1">
						<div class="mb-1.5 flex flex-wrap items-center gap-2">
							<span
								class="rounded-md px-2 py-0.5 text-[11px] font-medium {paper.kind === 'breakthrough'
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
						<a
							href={`https://arxiv.org/abs/${paper.arxivId}`}
							target="_blank"
							rel="noopener noreferrer"
							class="rounded-md border border-border px-2 py-1 font-mono text-[11px] text-muted-foreground hover:text-foreground focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
							aria-label="View {paper.title} on arXiv"
						>
							arXiv {paper.arxivId}
						</a>
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
	{/if}
</main>
