<script lang="ts">
	import CudaFooter from '$components/cuda/CudaFooter.svelte';
	import PagePill from '$components/PagePill.svelte';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { RotateCcw } from '@lucide/svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import SolvedMark from '$components/SolvedMark.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import {
		CUDA_STAGES,
		countSolvedIn,
		filterCuda,
		statusOf,
		topicChoices,
		type CudaStatus
	} from '$processes/cuda/cuda-progress';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const difficulties = ['Beginner', 'Intermediate', 'Advanced'];
	const statuses: { value: CudaStatus; label: string }[] = [
		{ value: 'all', label: 'All Statuses' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'attempted', label: 'Attempted' },
		{ value: 'unsolved', label: 'Unsolved' }
	];

	let query = $state(browser ? (page.url.searchParams.get('q') ?? '') : '');
	let difficulty = $state('');
	let topic = $state('');
	let status = $state<CudaStatus>('all');

	const topics = $derived(topicChoices(data.problems));
	const visible = $derived(
		filterCuda(data.problems, { query, difficulty, topic, status }, solved.slugs, attempted.slugs)
	);
	const filtering = $derived(Boolean(query.trim() || difficulty || topic || status !== 'all'));
	const overall = $derived(countSolvedIn(data.problems, solved.slugs));
	const percent = $derived(overall.total ? Math.round((overall.solved / overall.total) * 100) : 0);
	const stages = $derived(
		Object.keys(CUDA_STAGES)
			.map(Number)
			.map((stage) => {
				const all = data.problems.filter((p) => p.stage === stage);
				return {
					stage,
					title: CUDA_STAGES[stage],
					problems: visible.filter((p) => p.stage === stage),
					...countSolvedIn(all, solved.slugs)
				};
			})
			.filter((s) => s.problems.length > 0)
	);

	function reset() {
		query = '';
		difficulty = '';
		topic = '';
		status = 'all';
	}
</script>

<svelte:head>
	<title>CUDA problems | TrenTorch</title>
	<meta
		name="description"
		content="{data.problems
			.length} CUDA kernel problems, from vector addition to fused attention and multi-GPU training. Write CUDA C++ and run it free on a virtual NVIDIA A100, multi-GPU included."
	/>
</svelte:head>

<main class="mx-auto w-full max-w-4xl px-4 py-8">
	<PagePill slug="cuda/problems/" area="cuda" />
	<div class="mb-2 flex flex-wrap items-baseline justify-between gap-2">
		<h1 class="font-mono text-3xl font-bold tracking-tight">CUDA problems</h1>
		<p class="text-sm text-muted-foreground">{overall.solved} / {overall.total} solved</p>
	</div>
	<div
		class="mb-5 h-1.5 overflow-hidden rounded-full bg-secondary"
		role="progressbar"
		aria-valuenow={percent}
		aria-valuemin="0"
		aria-valuemax="100"
		aria-label="Solved problems"
	>
		<div class="h-full rounded-full bg-primary" style="width: {percent}%"></div>
	</div>
	<p class="mb-5 text-sm text-muted-foreground">
		Each problem opens in the IDE. You write the kernel; the tests launch it and report correctness,
		memory traffic, coalescing, bank conflicts and divergence. Read the
		<a class="underline" href={resolve('/modules/gpu/theory')}>theory</a> when a problem needs an idea
		you have not met yet.
	</p>

	<FilterBar
		bind:query
		bind:difficulty
		bind:status
		bind:topic
		{topics}
		{difficulties}
		{statuses}
		resultCount={visible.length}
		total={data.problems.length}
		placeholder="Search problems or topics..."
		noun="problem"
	/>

	{#if stages.length === 0}
		<p class="mt-8 text-sm text-muted-foreground">
			No problems match these filters.
			<button type="button" class="ml-2 inline-flex items-center gap-1 underline" onclick={reset}>
				<RotateCcw class="size-3.5" aria-hidden="true" /> Clear filters
			</button>
		</p>
	{/if}

	{#each stages as stage (stage.stage)}
		<h2
			id="stage-{stage.stage}"
			class="mt-8 mb-2 flex items-baseline justify-between text-lg font-medium"
		>
			<span>Stage {stage.stage}: {stage.title}</span>
			<span class="text-xs font-normal text-muted-foreground"
				>{stage.solved} / {stage.total} solved</span
			>
		</h2>
		<ul class="divide-y divide-border rounded-lg border border-border">
			{#each stage.problems as p (p.id)}
				{@const state = statusOf(p.id, solved.slugs, attempted.slugs)}
				<li>
					<a
						class="flex items-center gap-3 px-4 py-3 hover:bg-secondary"
						href={resolve('/ide/[id]', { id: p.id })}
					>
						<SolvedMark isSolved={state === 'solved'} questionTitle={p.title} />
						<span class="w-16 shrink-0 font-mono text-xs text-muted-foreground">{p.number}</span>
						<span class="min-w-0 flex-1 truncate">{p.title}</span>
						{#if state === 'attempted'}
							<span class="hidden text-xs text-amber-600 sm:inline dark:text-amber-400"
								>attempted</span
							>
						{/if}
						<span class="hidden text-xs text-muted-foreground md:inline"
							>{p.topics.slice(0, 2).join(', ')}</span
						>
						<DifficultyBadge difficulty={p.difficulty} />
					</a>
				</li>
			{/each}
		</ul>
	{/each}
	{#if filtering && stages.length > 0}
		<p class="mt-6 text-center text-xs text-muted-foreground">
			Showing {visible.length} of {data.problems.length} problems.
		</p>
	{/if}
</main>

<CudaFooter />
