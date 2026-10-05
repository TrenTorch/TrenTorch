<script lang="ts">
	import { resolve } from '$app/paths';
	import SEO from '$components/SEO.svelte';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	let tab = $state<'read' | 'code'>('read');

	const pdfUrl = $derived(`https://arxiv.org/pdf/${data.paper.arxivId}`);
	const kindLabel = $derived(data.paper.kind === 'foundational' ? 'Foundational' : 'Breakthrough');
</script>

<SEO
	title={withSiteName(data.paper.title)}
	description={data.paper.summary}
	path={`/papers/${data.paper.slug}`}
	type="article"
/>

<nav
	class="sticky top-[4.75rem] z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
	aria-label="Paper sections"
>
	<div class="container flex max-w-5xl items-center justify-between gap-4 px-4 py-3 md:px-6">
		<p class="truncate text-sm font-medium">{data.paper.title}</p>
		<div class="flex shrink-0 items-center gap-1 rounded-full border border-border p-1">
			<button
				type="button"
				onclick={() => (tab = 'read')}
				aria-pressed={tab === 'read'}
				class="rounded-full px-4 py-1.5 text-sm transition-colors {tab === 'read'
					? 'bg-primary text-primary-foreground'
					: 'text-muted-foreground hover:text-foreground'}"
			>
				Read the paper
			</button>
			<button
				type="button"
				onclick={() => (tab = 'code')}
				aria-pressed={tab === 'code'}
				class="rounded-full px-4 py-1.5 text-sm transition-colors {tab === 'code'
					? 'bg-primary text-primary-foreground'
					: 'text-muted-foreground hover:text-foreground'}"
			>
				Code the paper
			</button>
		</div>
	</div>
</nav>

<main class="container max-w-5xl px-4 py-10 md:px-6">
	<header class="mb-8 text-center">
		<p class="mb-3 font-mono text-xs tracking-wider text-muted-foreground uppercase">
			{kindLabel} · {data.paper.year}
		</p>
		<h1 class="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">{data.paper.title}</h1>
		<p class="mb-4 text-sm text-muted-foreground">{data.paper.authors}</p>
		<p class="mx-auto max-w-2xl text-muted-foreground">{data.paper.summary}</p>
	</header>

	{#if tab === 'read'}
		<section class="bg-card overflow-hidden rounded-2xl border border-border">
			<iframe src={pdfUrl} title={data.paper.title} class="h-[80vh] w-full bg-white"></iframe>
		</section>
		<p class="mt-4 text-center text-sm text-muted-foreground">
			Having trouble viewing it?
			<!-- eslint-disable svelte/no-navigation-without-resolve -- external arXiv URL, not an app route -->
			<a
				href={pdfUrl}
				target="_blank"
				rel="noopener noreferrer"
				class="underline underline-offset-4"
			>
				Open the PDF on arXiv
			</a>
			<!-- eslint-enable svelte/no-navigation-without-resolve -->.
		</p>
	{:else}
		<section class="mx-auto max-w-2xl">
			<p class="mb-6 text-center text-sm text-muted-foreground">
				The core ideas of this paper, split into {data.paper.implementations.length} implementation exercises.
				Each runs in your browser.
			</p>
			<ol class="flex flex-col gap-3">
				{#each data.paper.implementations as impl, index (impl.slug)}
					<li>
						<a
							href={resolve('/ide/[id]', { id: impl.slug })}
							class="bg-card flex items-center gap-4 rounded-xl border border-border p-4 transition-colors hover:border-primary"
						>
							<span class="font-mono text-sm text-muted-foreground">{index + 1}</span>
							<span class="flex-1 font-medium">{impl.title}</span>
							<span class="font-mono text-xs text-muted-foreground">{impl.difficulty}</span>
						</a>
					</li>
				{/each}
			</ol>
		</section>
	{/if}
</main>
