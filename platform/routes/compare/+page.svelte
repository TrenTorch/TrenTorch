<script lang="ts">
	import { resolve } from '$app/paths';
	import SEO from '$components/SEO.svelte';
	import { competitors } from '$data/competitors';
	import { buildComparisonIndexSeo } from '$processes/seo/build-comparison-index-seo';
</script>

<SEO {...buildComparisonIndexSeo()} />

<main class="container max-w-3xl px-4 py-12 md:px-6">
	<a
		href={resolve('/')}
		class="mb-6 inline-flex font-mono text-xs tracking-wider text-muted-foreground uppercase hover:text-primary"
	>
		TrenTorch home
	</a>
	<h1 class="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
		Machine-learning practice alternatives
	</h1>
	<p class="mb-8 text-muted-foreground">
		These pages explain what TrenTorch offers and summarize facts checked against each product's
		official pages. Unconfirmed capabilities are labeled as such rather than treated as unavailable.
	</p>
	<ul class="space-y-4">
		{#each competitors as competitor (competitor.slug)}
			<li class="rounded-xl border border-border p-5">
				<h2 class="mb-2 text-lg font-semibold">
					<a
						href={resolve('/compare/[slug]', { slug: competitor.slug })}
						class="underline underline-offset-4 hover:text-primary"
					>
						{competitor.name} alternative for machine learning
					</a>
				</h2>
				<p class="mb-3 text-sm text-muted-foreground">{competitor.summary}</p>
				<!-- These are external URLs from the verified competitor registry. -->
				<!-- eslint-disable svelte/no-navigation-without-resolve -->
				<a
					href={competitor.url}
					target="_blank"
					rel="noopener noreferrer"
					class="text-sm underline underline-offset-4 hover:text-primary"
				>
					Visit {competitor.name}'s official site
				</a>
				<!-- eslint-enable svelte/no-navigation-without-resolve -->
			</li>
		{/each}
	</ul>
</main>
