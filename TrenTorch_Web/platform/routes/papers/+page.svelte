<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import { ArrowLeft, ArrowRight, ArrowUpRight } from '@lucide/svelte';
	import SEO from '$components/SEO.svelte';
	import StatTile from '$components/StatTile.svelte';
	import PagePill from '$components/PagePill.svelte';
	import type { PaperKind } from '$processes/papers/types';
	import type { PageProps } from './$types';
	import { withSiteName } from '$processes/seo/with-site-name';

	let { data }: PageProps = $props();

	const paperTopics = $derived(data.topics);
	const allPapers = $derived(paperTopics.flatMap((topic) => topic.papers));
	const implementationCount = $derived(
		allPapers.reduce((sum, paper) => sum + paper.implementations.length, 0)
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

	const pad = (n: number) => String(n).padStart(2, '0');

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

<main class="mx-auto w-full max-w-[1180px] px-4 pt-8 pb-20 sm:px-5 md:px-6 md:pt-10">
	{#if !activeTrack}
		<header class="dot-texture mb-9">
			<PagePill slug="papers/" />
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">Research papers</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				Read the paper, then write the idea yourself.
			</p>
			<div class="mt-6 grid max-w-xl grid-cols-3 gap-3 sm:gap-4">
				<StatTile label="Tracks" value={paperTopics.length} tone="positive" />
				<StatTile label="Papers" value={allPapers.length} tone="positive" />
				<StatTile label="Implementations" value={implementationCount} tone="positive" />
			</div>
		</header>

		<ul class="grid gap-4 sm:grid-cols-2">
			{#each paperTopics as topic, i (topic.slug)}
				<li>
					<button type="button" onclick={() => openTrack(topic.slug)} class="track-card group">
						<span class="track-index" aria-hidden="true">{pad(i + 1)}</span>
						<span class="min-w-0 flex-1">
							<span
								class="block font-mono text-base font-semibold tracking-tight group-hover:text-primary"
							>
								{topic.title}
							</span>
							<span class="mt-1.5 block text-sm leading-relaxed text-muted-foreground">
								{topic.description}
							</span>
							<span class="mt-4 block font-mono text-xs text-muted-foreground tabular-nums">
								{topic.papers.length} papers
							</span>
						</span>
						<ArrowRight
							class="mt-1 size-4 shrink-0 text-muted-foreground transition-all group-hover:translate-x-0.5 group-hover:text-primary"
							aria-hidden="true"
						/>
					</button>
				</li>
			{/each}
		</ul>
	{:else}
		<header class="dot-texture mb-8">
			<button
				type="button"
				onclick={() => openTrack(null)}
				class="mb-5 inline-flex items-center gap-2 rounded-full border border-border bg-secondary/50 px-3.5 py-1.5 font-mono text-xs text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
			>
				<ArrowLeft class="size-3.5" aria-hidden="true" />
				All tracks
			</button>
			<h1 class="mb-2 font-mono text-3xl font-bold tracking-tight sm:text-4xl">
				{activeTrack.title}
			</h1>
			<p class="max-w-2xl text-lg text-muted-foreground">{activeTrack.description}</p>
			<p class="mt-3 font-mono text-xs text-muted-foreground tabular-nums">
				{activeTrack.papers.length} papers
			</p>
		</header>

		<ul class="bg-card overflow-hidden rounded-2xl border border-border">
			{#each activeTrack.papers as paper, i (paper.slug)}
				<li
					class="paper-row group relative flex flex-col gap-4 border-b border-border p-5 last:border-b-0 sm:flex-row sm:items-center"
				>
					<span class="hidden w-8 shrink-0 font-mono text-sm text-muted-foreground/70 sm:block"
						>{pad(i + 1)}</span
					>
					<div class="min-w-0 flex-1">
						<div class="mb-1.5 flex flex-wrap items-center gap-2">
							<span
								class="rounded-md px-2 py-0.5 font-mono text-[11px] font-medium {paper.kind ===
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
						<a
							href={`https://arxiv.org/abs/${paper.arxivId}`}
							target="_blank"
							rel="noopener noreferrer"
							class="inline-flex items-center gap-1 rounded-md border border-border px-2 py-1 font-mono text-[11px] text-muted-foreground transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
							aria-label="View {paper.title} on arXiv"
						>
							arXiv {paper.arxivId}
							<ArrowUpRight class="size-3" aria-hidden="true" />
						</a>
						<a
							href={resolve('/papers/[slug]', { slug: paper.slug })}
							class="rounded-lg bg-primary px-3.5 py-2 text-xs font-medium text-primary-foreground transition-opacity hover:opacity-90 focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
						>
							Read paper
						</a>
					</div>
				</li>
			{/each}
		</ul>
	{/if}
</main>

<style>
	.track-card {
		position: relative;
		display: flex;
		width: 100%;
		height: 100%;
		align-items: flex-start;
		gap: 16px;
		overflow: hidden;
		border: 1px solid var(--border);
		border-radius: 16px;
		background: var(--card);
		padding: 20px;
		text-align: left;
		transition:
			border-color 150ms,
			background-color 150ms,
			transform 150ms;
	}

	/* A red edge that grows in from the left, the one bit of colour a card spends. */
	.track-card::before {
		content: '';
		position: absolute;
		inset: 0 auto 0 0;
		width: 3px;
		background: var(--primary);
		transform: scaleY(0);
		transform-origin: top;
		transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1);
	}

	.track-card:hover,
	.track-card:focus-visible {
		border-color: color-mix(in srgb, var(--primary) 40%, var(--border));
		background: color-mix(in srgb, var(--secondary) 55%, var(--card));
		outline: none;
	}

	.track-card:hover::before,
	.track-card:focus-visible::before {
		transform: scaleY(1);
	}

	.track-card:focus-visible {
		box-shadow: 0 0 0 2px color-mix(in srgb, var(--primary) 40%, transparent);
	}

	.track-index {
		flex: none;
		width: 2rem;
		padding-top: 2px;
		color: var(--primary);
		font-family: var(--font-mono);
		font-size: 0.8rem;
		font-weight: 600;
		font-variant-numeric: tabular-nums;
	}

	.paper-row:hover {
		background: color-mix(in srgb, var(--secondary) 55%, transparent);
	}

	@media (prefers-reduced-motion: reduce) {
		.track-card,
		.track-card::before {
			transition: none;
		}
	}
</style>
