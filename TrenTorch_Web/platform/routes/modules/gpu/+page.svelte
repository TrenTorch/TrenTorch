<script lang="ts">
	import CudaFooter from '$components/cuda/CudaFooter.svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import { ArrowRight, BookOpen, Layers, RotateCcw } from '@lucide/svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import GpuArt from '$components/GpuArt.svelte';
	import ModuleAccordion, { startPage } from '$components/ModuleAccordion.svelte';
	import PagePill from '$components/PagePill.svelte';
	import SEO from '$components/SEO.svelte';
	import SolvedMark from '$components/SolvedMark.svelte';
	import StatTile from '$components/StatTile.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { recent } from '$processes/progress-tracking/recent.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import {
		CUDA_STAGES,
		countSolvedIn,
		filterCuda,
		resumeTarget,
		statusOf,
		topicChoices,
		type CudaStatus
	} from '$processes/cuda/cuda-progress';
	import { buildBreadcrumbJsonLd } from '$processes/seo/build-breadcrumb-json-ld';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const PARTS: Record<string, string> = {
		A: 'GPU Foundations',
		B: 'The Programming Model',
		C: 'Control Flow',
		D: 'Memory Performance',
		E: 'Parallel Patterns',
		F: 'Advanced and Systems',
		G: 'Calculation Workbook'
	};
	const difficulties = ['Beginner', 'Intermediate', 'Advanced'];
	const statuses: { value: CudaStatus; label: string }[] = [
		{ value: 'all', label: 'All Statuses' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'attempted', label: 'Attempted' },
		{ value: 'unsolved', label: 'Unsolved' }
	];
	const RESUME_LABEL = {
		continue: 'continue problem',
		start: 'first problem',
		next: 'next problem'
	};

	// The domain has two ways in: read a part, or follow the problem path. Both lists show, theory first,
	// until the Show filter picks one, so nobody takes either for the whole domain.
	type View = '' | 'theory' | 'problems';
	const VIEWS = [
		{ value: 'theory', label: 'Theory' },
		{ value: 'problems', label: 'Problem Path' }
	];
	const linked = browser ? page.url.searchParams.get('view') : null;
	let view = $state<View>(linked === 'problems' || linked === 'theory' ? linked : '');
	let query = $state('');
	let difficulty = $state('');
	let topic = $state('');
	let status = $state<CudaStatus>('all');

	const topics = $derived(
		topicChoices(data.problems).map((t) => ({
			...t,
			label: t.label.replace(/\b\w/g, (c) => c.toUpperCase())
		}))
	);
	const visible = $derived(
		filterCuda(data.problems, { query, difficulty, topic, status }, solved.slugs, attempted.slugs)
	);
	const q = $derived(query.trim().toLowerCase());
	const filtering = $derived(Boolean(q || difficulty || topic || status !== 'all'));
	const overall = $derived(countSolvedIn(data.problems, solved.slugs));
	const resume = $derived(resumeTarget(data.problems, solved.slugs, attempted.slugs));
	const green = $derived(
		resume
			? {
					label: RESUME_LABEL[resume.kind],
					href: resolve('/ide/[id]', { id: resume.entry.id })
				}
			: null
	);

	const parts = $derived(
		Object.keys(PARTS)
			.map((id) => {
				const all = data.chapters.filter((c) => c.part === id);
				return {
					id,
					name: PARTS[id],
					chapters: q
						? all.filter((c) => `${c.id} ${c.title} ${PARTS[id]}`.toLowerCase().includes(q))
						: all,
					minutes: all.reduce((n, c) => n + c.estMinutes, 0)
				};
			})
			.filter((p) => p.chapters.length)
	);
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

	// Chapters have no difficulty, topic or status, so those filters leave only the problem path.
	const problemFilters = $derived(Boolean(difficulty || topic || status !== 'all'));
	const showTheory = $derived(view !== 'problems' && !problemFilters);
	const showProblems = $derived(view !== 'theory');
	const rows = $derived([
		...(showTheory
			? parts.map((p) => ({
					id: p.id,
					title: p.name,
					icon: BookOpen,
					count: p.chapters.length,
					solved: 0,
					noun: 'chapter'
				}))
			: []),
		...(showProblems
			? stages.map((s) => ({
					id: String(s.stage),
					title: s.title,
					icon: Layers,
					count: s.total,
					solved: s.solved,
					noun: 'problem'
				}))
			: [])
	]);
	const nothing = $derived(rows.length === 0);

	const initialOpen = browser ? page.url.searchParams.get('open') : null;
	let currentPage = $state(startPage(rows, initialOpen));
	// A new view or filter changes what "page 2" means; the first run keeps a shared link's page.
	let mounted = false;
	$effect(() => {
		void view;
		void query;
		void difficulty;
		void topic;
		void status;
		if (mounted) currentPage = 1;
		mounted = true;
	});

	function reset() {
		query = '';
		difficulty = '';
		topic = '';
		status = 'all';
	}
</script>

<SEO
	title={withSiteName('GPU Programming')}
	description="Free CUDA course: {data.chapters.length} interactive theory chapters and {data
		.problems
		.length} CUDA C++ kernel problems, including multi-GPU (NCCL collectives, data parallel training). Your code runs free in the browser on a virtual NVIDIA A100 and reports memory traffic, coalescing, bank conflicts and divergence."
	path="/modules/gpu"
	jsonLd={buildBreadcrumbJsonLd([
		{ name: 'Home', path: '/' },
		{ name: 'Modules', path: '/modules' },
		{ name: 'GPU Programming', path: '/modules/gpu' }
	])}
/>

<main class="min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px] space-y-8">
		<header class="dot-texture flex flex-wrap items-start justify-between gap-6">
			<div class="min-w-0 flex-1">
				<PagePill
					slug="modules/gpu/"
					area="cuda"
					resume={green}
					up={{ label: 'all domains', href: resolve('/modules') }}
				/>
				<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">
					GPU Programming
				</h1>
				<p class="max-w-xl text-lg text-muted-foreground">
					Understand the GPU from ground-up, and write the kernels that run on it
				</p>
				<div class="mt-6 grid max-w-md grid-cols-2 gap-3 sm:gap-4">
					<StatTile
						label="Problems"
						value={overall.total}
						tone="positive"
						progress={{ done: overall.solved, total: overall.total }}
					/>
					<StatTile label="Theory chapters" value={data.chapters.length} tone="positive" />
				</div>
			</div>
		</header>

		<FilterBar
			bind:view
			views={VIEWS}
			bind:query
			bind:difficulty
			bind:status
			bind:topic
			{topics}
			{difficulties}
			{statuses}
			resultCount={visible.length}
			total={data.problems.length}
			placeholder="Search chapters, problems or topics..."
			noun="problem"
		/>

		{#if nothing}
			<p class="py-12 text-center text-sm text-muted-foreground">
				Nothing matches these filters.
				<button type="button" class="ml-2 inline-flex items-center gap-1 underline" onclick={reset}>
					<RotateCcw class="size-3.5" aria-hidden="true" /> Clear filters
				</button>
			</p>
		{:else}
			<!-- keyed so each view and each filtered state starts from its own open rows -->
			{#key `${view}-${filtering}`}
				<ModuleAccordion
					items={rows}
					forceOpen={filtering}
					{initialOpen}
					hue="#7fb59a"
					bind:page={currentPage}
				>
					{#snippet art(item)}
						<GpuArt id={item.id} />
					{/snippet}
					{#snippet children(item)}
						{@const part = parts.find((p) => p.id === item.id)}
						<div class="flex flex-col gap-2 p-3">
							{#if part}
								{#each part.chapters as c (c.step)}
									<a
										class="row"
										href={resolve('/modules/gpu/theory/[chapter]', { chapter: c.step })}
									>
										<BookOpen class="size-4 shrink-0" aria-hidden="true" />
										<span class="mono">{c.id}</span>
										<span class="min-w-0 flex-1 font-semibold">{c.title}</span>
										<span class="mono">{c.estMinutes} min</span>
										<ArrowRight class="size-4 shrink-0" aria-hidden="true" />
									</a>
								{/each}
							{:else}
								{@const stage = stages.find((s) => String(s.stage) === item.id)}
								{#each stage?.problems ?? [] as p (p.id)}
									{@const state = statusOf(p.id, solved.slugs, attempted.slugs)}
									<a
										class="row"
										href={resolve('/ide/[id]', { id: p.id })}
										onclick={() => recent.note('cuda', p.id)}
									>
										<SolvedMark isSolved={state === 'solved'} questionTitle={p.title} />
										<span class="mono">{p.number}</span>
										<span class="min-w-0 flex-1 font-semibold">{p.title}</span>
										{#if state === 'attempted'}<span class="text-xs text-amber-600">attempted</span
											>{/if}
										<DifficultyBadge difficulty={p.difficulty} />
									</a>
								{/each}
							{/if}
						</div>
					{/snippet}
				</ModuleAccordion>
			{/key}
		{/if}
	</div>
</main>

<CudaFooter />

<style>
	.row {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 11px 16px;
		border: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		border-radius: 10px;
		background: color-mix(in oklab, var(--foreground) 3%, var(--background));
		color: var(--foreground);
	}
	.row:hover {
		background: color-mix(in oklab, var(--foreground) 7%, var(--background));
	}
	.mono {
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 0.75rem;
		color: var(--muted-foreground);
		white-space: nowrap;
	}
</style>
