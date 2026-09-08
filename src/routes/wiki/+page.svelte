<script lang="ts">
	import { ArrowRight } from '@lucide/svelte';

	const WIKI_URL = 'https://github.com/TrenTorch/TrenTorch/wiki';

	const pages = [
		{ title: 'Getting Started', href: `${WIKI_URL}/Getting-Started` },
		{ title: 'Architecture', href: `${WIKI_URL}/Architecture` },
		{ title: 'CLI Reference', href: `${WIKI_URL}/CLI-Reference` },
		{ title: 'Curriculum and Milestones', href: `${WIKI_URL}/Curriculum-and-Milestones` },
		{ title: 'Contributing', href: `${WIKI_URL}/Contributing` }
	];
</script>

<svelte:head>
	<title>TrenTorch-Web Wiki</title>
	<meta
		name="description"
		content="Curriculum overview, CLI reference, architecture, and how to contribute."
	/>
</svelte:head>

<div class="container max-w-4xl px-4 py-12 md:px-6">
	<h1 class="mb-2 font-mono text-3xl font-bold">Wiki</h1>
	<p class="mb-10 text-muted-foreground">
		TrenTorch-Web doesn't have its own wiki yet: it shares its curriculum with TrenTorch, so here's
		that wiki until this one has content of its own.
	</p>
	<div class="grid gap-3">
		{#each pages as page (page.href)}
			<!-- All of these point at TrenTorch's own GitHub wiki, never a route
			     inside this app, so there's no route to resolve() here. -->
			<!-- eslint-disable svelte/no-navigation-without-resolve -->
			<a
				href={page.href}
				target="_blank"
				rel="noopener noreferrer"
				class="group flex items-center justify-between border border-border p-4 transition-colors hover:bg-secondary"
			>
				<span class="font-mono">{page.title}</span>
				<ArrowRight
					class="size-4 text-muted-foreground transition-transform group-hover:translate-x-1"
				/>
			</a>
			<!-- eslint-enable svelte/no-navigation-without-resolve -->
		{/each}
	</div>
</div>
