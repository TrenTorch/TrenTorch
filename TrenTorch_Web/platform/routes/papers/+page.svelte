<script lang="ts">
	import { resolve } from '$app/paths';
	import SEO from '$components/SEO.svelte';
	import { paperTopics } from '$data/papers';
	import { withSiteName } from '$processes/seo/with-site-name';
</script>

<SEO
	title={withSiteName('Research papers, read and coded')}
	description="Foundational and breakthrough machine learning papers, with the core ideas implemented in the browser."
	path="/papers"
/>

<main class="container max-w-5xl px-4 py-12 md:px-6">
	<p class="mb-3 font-mono text-xs tracking-wider text-muted-foreground uppercase">Learn</p>
	<h1 class="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">Research papers</h1>
	<p class="mb-10 max-w-2xl text-muted-foreground">
		Read the papers behind modern machine learning, then implement their key ideas yourself.
	</p>

	<ul class="grid gap-4 sm:grid-cols-2">
		{#each paperTopics as topic (topic.slug)}
			<li class="bg-card rounded-2xl border border-border p-6">
				<div class="mb-2 flex items-center justify-between gap-3">
					<h2 class="text-lg font-semibold">{topic.title}</h2>
					<span class="font-mono text-xs text-muted-foreground">
						{topic.papers.length}
						{topic.papers.length === 1 ? 'paper' : 'papers'}
					</span>
				</div>
				<p class="mb-4 text-sm text-muted-foreground">{topic.description}</p>
				{#if topic.papers.length}
					<ul class="flex flex-col gap-2">
						{#each topic.papers as paper (paper.slug)}
							<li>
								<a
									href={resolve('/papers/[slug]', { slug: paper.slug })}
									class="text-sm font-medium underline underline-offset-4 hover:text-primary"
								>
									{paper.title}
								</a>
							</li>
						{/each}
					</ul>
				{:else}
					<p class="font-mono text-xs text-muted-foreground">Coming soon</p>
				{/if}
			</li>
		{/each}
	</ul>
</main>
