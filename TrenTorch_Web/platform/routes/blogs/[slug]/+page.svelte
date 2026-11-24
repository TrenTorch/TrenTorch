<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowLeft } from '@lucide/svelte';
	import SEO from '$components/SEO.svelte';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const dateLabel = $derived(
		new Date(`${data.post.date}T00:00:00Z`).toLocaleDateString('en-GB', {
			day: 'numeric',
			month: 'long',
			year: 'numeric',
			timeZone: 'UTC'
		})
	);
</script>

<SEO
	title={withSiteName(data.post.title)}
	description={data.post.summary}
	path={`/blogs/${data.post.slug}`}
	type="article"
/>

<main class="mx-auto w-full max-w-3xl px-4 py-10 md:px-6">
	<a
		href={resolve('/blogs')}
		class="mb-8 inline-flex items-center gap-2 rounded-full border border-border bg-secondary/50 px-3.5 py-1.5 font-mono text-xs text-muted-foreground transition-colors hover:text-foreground"
	>
		<ArrowLeft class="size-3.5" aria-hidden="true" />
		All posts
	</a>
	<header class="mb-8">
		<p class="mb-3 font-mono text-xs tracking-wider text-muted-foreground uppercase">
			{dateLabel} · {data.post.readingMinutes} min read
		</p>
		<h1 class="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">{data.post.title}</h1>
		<p class="mb-4 text-sm text-muted-foreground">{data.post.author}</p>
		<p class="text-lg text-muted-foreground">{data.post.summary}</p>
	</header>
	<article class="question-prose min-w-0">
		<!-- eslint-disable-next-line svelte/no-at-html-tags -- sanitised with DOMPurify at build time -->
		{@html data.html}
	</article>
</main>
