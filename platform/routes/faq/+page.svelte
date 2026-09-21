<script lang="ts">
	import { resolve } from '$app/paths';
	import SEO from '$components/SEO.svelte';
	import { buildFaqEntries, FAQ_DISCLAIMER } from '$data/faq';
	import { buildBreadcrumbJsonLd } from '$processes/seo/build-breadcrumb-json-ld';
	import { buildFaqJsonLd } from '$processes/seo/build-faq-json-ld';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	const entries = $derived(buildFaqEntries(data.questionCount));
</script>

<SEO
	title={withSiteName('FAQ: free ML practice, PyTorch from scratch')}
	description="Answers about TrenTorch: it is free, runs in your browser, and covers machine learning, inference, and systems-performance practice problems."
	path="/faq"
	jsonLd={[
		buildFaqJsonLd(entries),
		buildBreadcrumbJsonLd([
			{ name: 'Home', path: '/' },
			{ name: 'FAQ', path: '/faq' }
		])
	]}
/>

<div class="container max-w-3xl px-4 py-12 md:px-6">
	<h1 class="mb-1 font-mono text-2xl font-bold tracking-tight">Frequently asked questions</h1>
	<p class="mb-8 text-sm text-muted-foreground">
		Short answers about what TrenTorch is and how it works. Ready to start? Browse the
		<a href={resolve('/questions')} class="underline underline-offset-4 hover:text-primary"
			>practice questions</a
		>.
	</p>

	<div class="question-prose">
		{#each entries as entry (entry.question)}
			<h2>{entry.question}</h2>
			<p>{entry.answer}</p>
		{/each}

		<hr />
		<p class="text-sm text-muted-foreground">{FAQ_DISCLAIMER}</p>
	</div>
</div>
