<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import { ArrowLeft, ArrowRight } from '@lucide/svelte';
	import SEO from '$components/SEO.svelte';
	import StatTile from '$components/StatTile.svelte';
	import PagePill from '$components/PagePill.svelte';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const tracks = $derived(data.tracks);
	const allPosts = $derived(tracks.flatMap((track) => track.posts));
	const latest = $derived([...allPosts].sort((a, b) => b.date.localeCompare(a.date))[0]);
	// Green on the pill: the newest post, when there is one.
	const green = $derived(
		latest ? { label: 'latest post', href: resolve('/blogs/[slug]', { slug: latest.slug }) } : null
	);

	// /blogs is prerendered, so the selected track is read from the URL on the client
	// (plain history API, not SvelteKit navigation) and kept in sync with back/forward.
	let trackSlug = $state<string | null>(null);
	const activeTrack = $derived(tracks.find((track) => track.slug === trackSlug));

	function readTrack(): string | null {
		return new URLSearchParams(window.location.search).get('track');
	}

	function openTrack(slug: string | null) {
		trackSlug = slug;
		window.history.pushState({}, '', slug ? `?track=${slug}` : window.location.pathname);
		window.scrollTo({ top: 0 });
	}

	const pad = (n: number) => String(n).padStart(2, '0');
	const dateLabel = (iso: string) =>
		new Date(`${iso}T00:00:00Z`).toLocaleDateString('en-GB', {
			day: 'numeric',
			month: 'short',
			year: 'numeric',
			timeZone: 'UTC'
		});

	onMount(() => {
		trackSlug = readTrack();
		const onPop = () => (trackSlug = readTrack());
		window.addEventListener('popstate', onPop);
		return () => window.removeEventListener('popstate', onPop);
	});
</script>

<SEO
	title={withSiteName('Blogs')}
	description="Writeups from the TrenTorch team: how things are built, and what we learned building them."
	path="/blogs"
/>

<main class="mx-auto w-full max-w-[1180px] px-4 pt-8 pb-20 sm:px-5 md:px-6 md:pt-10">
	{#if !activeTrack}
		<header class="dot-texture mb-9">
			<PagePill slug="blogs/" resume={green} />
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">Blogs</h1>
			<p class="max-w-xl text-lg text-muted-foreground">Writeups from the team</p>
			<div class="mt-6 grid max-w-md grid-cols-2 gap-3 sm:gap-4">
				<StatTile label="Tracks" value={tracks.length} tone="positive" />
				<StatTile label="Posts" value={allPosts.length} tone="positive" />
			</div>
		</header>

		{#if tracks.length === 0}
			<p class="py-12 text-center text-sm text-muted-foreground">The first posts are on the way</p>
		{:else}
			<ul class="grid gap-4 sm:grid-cols-2">
				{#each tracks as track, i (track.slug)}
					<li>
						<button type="button" onclick={() => openTrack(track.slug)} class="track-card group">
							<span class="track-index" aria-hidden="true">{pad(i + 1)}</span>
							<span class="min-w-0 flex-1">
								<span
									class="block font-mono text-base font-semibold tracking-tight group-hover:text-primary"
								>
									{track.title}
								</span>
								<span class="mt-1.5 block text-sm leading-relaxed text-muted-foreground">
									{track.description}
								</span>
								<span class="mt-4 block font-mono text-xs text-muted-foreground tabular-nums">
									{track.posts.length} posts
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
		{/if}
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
				{activeTrack.posts.length} posts
			</p>
		</header>

		<ul class="bg-card overflow-hidden rounded-2xl border border-border">
			{#each activeTrack.posts as post, i (post.slug)}
				<li
					class="paper-row group relative flex flex-col gap-4 border-b border-border p-5 last:border-b-0 sm:flex-row sm:items-center"
				>
					<span class="hidden w-8 shrink-0 font-mono text-sm text-muted-foreground/70 sm:block"
						>{pad(i + 1)}</span
					>
					<div class="min-w-0 flex-1">
						<a
							href={resolve('/blogs/[slug]', { slug: post.slug })}
							class="leading-snug font-semibold tracking-tight text-balance after:absolute after:inset-0 hover:text-primary focus-visible:outline-none"
						>
							{post.title}
						</a>
						<p class="mt-1 text-sm text-muted-foreground">{post.summary}</p>
						<p class="mt-1.5 font-mono text-[11px] text-muted-foreground">
							{post.author} <span aria-hidden="true">·</span>
							{dateLabel(post.date)} <span aria-hidden="true">·</span>
							{post.readingMinutes} min read
						</p>
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
