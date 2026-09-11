<script lang="ts">
	import { resolve } from '$app/paths';
	import LogoMark from '$lib/components/LogoMark.svelte';
	import Button from '$lib/components/Button.svelte';
	import StatTile from '$lib/components/StatTile.svelte';
	import Testimonials from '$lib/components/Testimonials.svelte';
	import { BookOpen } from '@lucide/svelte';
	import Github from '$lib/components/GithubIcon.svelte';
	import { curriculum, getProgressStats } from '$lib/data/questions';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch-Web';

	const totalQuestions = getProgressStats().total;
	const totalParts = curriculum.length;

	const FEATURES = [
		{
			title: 'Real PyTorch, not a stand-in',
			body: 'Functions mirror torch.nn.functional exactly: real signatures, real shape conventions, real bias=None and reduction semantics. What you implement is what the library actually does.'
		},
		{
			title: 'Tests that actually catch bugs',
			body: 'Every Submit runs an exhaustive hidden suite: edge cases, array hygiene, targeted mutation tests, some checked against real offline PyTorch output.'
		},
		{
			title: 'Linear algebra to LLM post-training',
			body: `${totalQuestions} questions across ${totalParts} tracks: classical ML, deep learning foundations, transformers, vision, and production ML engineering, all built from scratch.`
		},
		{
			title: 'Open source, same team',
			body: 'Built by the same maintainers, under the same governance and Code of Conduct as the TrenTorch CLI itself.'
		}
	];
</script>

<div>
	<!-- Hero -->
	<section class="container flex flex-col items-center px-4 pt-20 pb-16 text-center md:px-6">
		<LogoMark class="mb-6 h-36 w-36" />
		<h1 class="mb-4 font-mono text-4xl font-bold tracking-tight sm:text-5xl">
			TrenTorch<span class="text-primary">-Web</span>
		</h1>
		<p class="mb-2 max-w-2xl text-lg text-muted-foreground">TrenTorch, minus the terminal.</p>
		<p class="mb-8 max-w-2xl text-lg font-medium">
			The same build-it-by-hand curriculum, running straight in your browser.
		</p>
		<div class="flex flex-wrap items-center justify-center gap-3">
			<Button size="lg" href={resolve('/questions')}>
				<BookOpen class="size-4" />
				Questions
			</Button>
			<Button
				size="lg"
				variant="outline"
				href={GITHUB_URL}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Github class="size-4" />
				View on GitHub
			</Button>
		</div>
	</section>

	<!-- Stats -->
	<section class="container px-4 pb-16 md:px-6">
		<div class="mx-auto grid max-w-md grid-cols-2 gap-4">
			<StatTile label="Questions" value={totalQuestions} tone="positive" />
			<StatTile label="Tracks" value={totalParts} tone="positive" />
		</div>
	</section>

	<!-- Features -->
	<section class="container px-4 pb-16 md:px-6">
		<div class="mx-auto grid max-w-4xl gap-px border bg-border sm:grid-cols-2">
			{#each FEATURES as feature (feature.title)}
				<div class="bg-background p-6">
					<h3 class="mb-2 font-mono font-semibold">{feature.title}</h3>
					<p class="text-sm text-muted-foreground">{feature.body}</p>
				</div>
			{/each}
		</div>
	</section>

	<!-- Testimonials -->
	<section class="container px-4 pb-24 md:px-6">
		<h2
			class="mb-6 text-center font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
		>
			What people are saying
		</h2>
		<Testimonials />
	</section>
</div>
