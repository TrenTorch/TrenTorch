<script lang="ts">
	import { resolve } from '$app/paths';
	import LogoMark from '$lib/components/LogoMark.svelte';
	import CopyButton from '$lib/components/CopyButton.svelte';
	import Button from '$lib/components/Button.svelte';
	import { ArrowRight, Terminal } from '@lucide/svelte';
	import Github from '$lib/components/GithubIcon.svelte';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch-Web';

	const CLONE_COMMAND = `git clone ${GITHUB_URL}.git && cd TrenTorch-Web\nnpm install\nnpm run dev`;

	const FEATURES = [
		{
			title: 'No local setup',
			body: 'The same 20-module curriculum as the CLI, running straight in the browser: no Python venv, no CLI install.'
		},
		{
			title: 'Built on SvelteKit',
			body: 'A fast, small, modern web stack: no framework weight standing between the student and the material.'
		},
		{
			title: 'Same curriculum, new surface',
			body: "Tensor to Transformer, one op at a time, exactly as it's taught in TrenTorch's CLI, just reachable from a browser tab."
		},
		{
			title: 'Open source, same team',
			body: 'Built by the same maintainers, under the same governance and Code of Conduct as TrenTorch itself.'
		}
	];
</script>

<div>
	<!-- Hero -->
	<section class="container flex flex-col items-center px-4 pt-20 pb-16 text-center md:px-6">
		<LogoMark class="mb-6 h-16 w-16" />
		<h1 class="mb-4 font-mono text-4xl font-bold tracking-tight sm:text-5xl">
			TrenTorch<span class="text-primary">-Web</span>
		</h1>
		<p class="mb-2 max-w-2xl text-lg text-muted-foreground">TrenTorch, minus the terminal.</p>
		<p class="mb-8 max-w-2xl text-lg font-medium">
			The same build-it-by-hand curriculum, running straight in your browser.
		</p>
		<div class="flex flex-wrap items-center justify-center gap-3">
			<Button size="lg" href={GITHUB_URL} target="_blank" rel="noopener noreferrer">
				<Github class="size-4" />
				View on GitHub
			</Button>
			<Button size="lg" variant="outline" href={resolve('/docs')}>
				<Terminal class="size-4" />
				Read the Docs
			</Button>
			<Button size="lg" variant="ghost" href={resolve('/wiki')}>
				Visit the Wiki
				<ArrowRight class="size-4" />
			</Button>
		</div>
	</section>

	<!-- Clone snippet -->
	<section class="container px-4 pb-16 md:px-6">
		<div
			class="group/code relative mx-auto max-w-2xl overflow-x-auto border border-border bg-secondary/50 p-4 pr-12 font-mono text-sm"
		>
			<CopyButton
				text={CLONE_COMMAND}
				class="absolute top-2 right-2 opacity-0 transition-opacity group-hover/code:opacity-100 focus:opacity-100"
			/>
			<span class="text-muted-foreground select-none">$ </span>
			git clone {GITHUB_URL}.git && cd TrenTorch-Web
			<br />
			<span class="text-muted-foreground select-none">$ </span>
			npm install
			<br />
			<span class="text-muted-foreground select-none">$ </span>
			npm run dev
		</div>
		<p class="mx-auto mt-3 max-w-2xl text-center text-xs text-muted-foreground">
			Prefer the original CLI?
			<a
				href="https://github.com/TrenTorch/TrenTorch"
				class="underline underline-offset-2 hover:text-foreground"
			>
				See TrenTorch/TrenTorch
			</a>
			.
		</p>
	</section>

	<!-- Features -->
	<section class="container px-4 pb-24 md:px-6">
		<div class="mx-auto grid max-w-4xl gap-px border bg-border sm:grid-cols-2">
			{#each FEATURES as feature (feature.title)}
				<div class="bg-background p-6">
					<h3 class="mb-2 font-mono font-semibold">{feature.title}</h3>
					<p class="text-sm text-muted-foreground">{feature.body}</p>
				</div>
			{/each}
		</div>
	</section>
</div>
