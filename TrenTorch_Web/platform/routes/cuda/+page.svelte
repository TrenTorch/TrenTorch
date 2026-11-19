<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowRight, BookOpen, ChevronDown, RotateCcw } from '@lucide/svelte';
	import { SvelteSet } from 'svelte/reactivity';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import PagePill from '$components/PagePill.svelte';
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
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const PARTS: Record<string, string> = {
		A: 'GPU foundations',
		B: 'The programming model',
		C: 'Control flow',
		D: 'Memory performance',
		E: 'Parallel patterns',
		F: 'Advanced and systems',
		G: 'Calculation workbook'
	};
	const difficulties = ['Beginner', 'Intermediate', 'Advanced'];
	const statuses: { value: CudaStatus; label: string }[] = [
		{ value: 'all', label: 'All statuses' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'attempted', label: 'Attempted' },
		{ value: 'unsolved', label: 'Unsolved' }
	];
	const RESUME_LABEL = {
		continue: 'continue problem',
		start: 'first problem',
		next: 'next problem'
	};

	let view = $state<'all' | 'theory' | 'problems'>('all');
	let query = $state('');
	let difficulty = $state('');
	let topic = $state('');
	let status = $state<CudaStatus>('all');
	const openParts = new SvelteSet<string>();
	const openStages = new SvelteSet<string>();

	const topics = $derived(topicChoices(data.problems));
	const visible = $derived(
		filterCuda(data.problems, { query, difficulty, topic, status }, solved.slugs, attempted.slugs)
	);
	const q = $derived(query.trim().toLowerCase());
	const filtering = $derived(Boolean(q || difficulty || topic || status !== 'all'));
	const overall = $derived(countSolvedIn(data.problems, solved.slugs));
	const percent = $derived(overall.total ? Math.round((overall.solved / overall.total) * 100) : 0);
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
	const showTheory = $derived(view !== 'problems');
	const showProblems = $derived(view !== 'theory');
	const empty = $derived(
		(!showTheory || parts.length === 0) && (!showProblems || stages.length === 0)
	);

	function toggle(set: SvelteSet<string>, id: string) {
		if (set.has(id)) set.delete(id);
		else set.add(id);
	}
	function reset() {
		query = '';
		difficulty = '';
		topic = '';
		status = 'all';
	}
</script>

<svelte:head>
	<title>CUDA | TrenTorch</title>
	<meta
		name="description"
		content="Learn CUDA by writing the kernel: {data.chapters
			.length} theory chapters with interactive figures and {data.problems
			.length} kernel problems that report memory traffic, coalescing, bank conflicts and divergence."
	/>
</svelte:head>

<main class="sheet min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px]">
		<header class="dot-texture mb-7 flex flex-wrap items-start justify-between gap-6">
			<div class="min-w-0 flex-1">
				<PagePill slug="cuda/" area="cuda" resume={green} />
				<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">CUDA</h1>
				<p class="max-w-xl text-lg text-muted-foreground">
					Understand the GPU, then program it. Read a part, then write the kernels that use it.
				</p>
				<div class="mt-6 flex flex-wrap items-stretch gap-3 sm:gap-4">
					<div class="w-[calc(50%-0.375rem)] sm:w-48">
						<StatTile
							label="Problems"
							value={overall.total}
							tone="positive"
							progress={{ done: overall.solved, total: overall.total }}
						/>
					</div>
					<div class="w-[calc(50%-0.375rem)] sm:w-48">
						<StatTile label="Theory chapters" value={data.chapters.length} tone="positive" />
					</div>
				</div>
			</div>
			<div
				class="ring-card"
				role="img"
				aria-label="{percent}% of CUDA problems solved: {overall.solved} of {overall.total}"
			>
				<div class="pie" style="--progress: {percent * 3.6}deg"><span>{percent}%</span></div>
				<div class="ring-copy">
					<strong>{overall.solved} / {overall.total}</strong>
					<span>problems solved</span>
					<span class="ring-sub">{stages.length ? `${stages.length} stages` : ''}</span>
				</div>
			</div>
		</header>

		<div class="seg" role="group" aria-label="Show">
			{#each [['all', 'Everything'], ['theory', 'Theory'], ['problems', 'Problems']] as const as [v, label] (v)}
				<button type="button" aria-pressed={view === v} onclick={() => (view = v)}>{label}</button>
			{/each}
		</div>

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
			placeholder="Search chapters, problems or topics..."
			noun="problem"
		/>

		{#if empty}
			<p class="empty-state">
				Nothing matches these filters.
				<button type="button" class="empty-clear" onclick={reset}>
					<RotateCcw class="size-3.5" aria-hidden="true" /> Clear filters
				</button>
			</p>
		{/if}

		{#if showTheory && parts.length}
			<h2 class="group-title">Theory</h2>
			<div class="flex flex-col gap-4">
				{#each parts as part (part.id)}
					{@const open = Boolean(q) || openParts.has(part.id)}
					<section class="step-card" aria-labelledby="part-{part.id}">
						<button
							type="button"
							class="step-head"
							aria-expanded={open}
							aria-controls="part-body-{part.id}"
							onclick={() => toggle(openParts, part.id)}
						>
							<span class="min-w-0 flex-1 text-left">
								<span id="part-{part.id}" class="step-title">Part {part.id}: {part.name}</span>
							</span>
							<span class="meta"
								>{part.chapters.length}
								{part.chapters.length === 1 ? 'chapter' : 'chapters'} · {part.minutes} min</span
							>
							<ChevronDown
								class="chevron size-4 shrink-0 {open ? 'open' : ''}"
								aria-hidden="true"
							/>
						</button>
						{#if open}
							<div id="part-body-{part.id}" class="step-body">
								{#each part.chapters as c (c.step)}
									<a
										class="theory-row"
										href={resolve('/cuda/theory/[chapter]', { chapter: c.step })}
									>
										<BookOpen class="size-4 shrink-0" aria-hidden="true" />
										<span class="mono">{c.id}</span>
										<span class="theory-row-title">{c.title}</span>
										<span class="meta">{c.estMinutes} min</span>
										<ArrowRight class="size-4 shrink-0" aria-hidden="true" />
									</a>
								{/each}
							</div>
						{/if}
					</section>
				{/each}
			</div>
		{/if}

		{#if showProblems && stages.length}
			<h2 class="group-title">Problem path</h2>
			<div class="flex flex-col gap-4">
				{#each stages as s (s.stage)}
					{@const open = filtering || openStages.has(String(s.stage))}
					<section class="step-card" aria-labelledby="stage-{s.stage}">
						<button
							type="button"
							class="step-head"
							aria-expanded={open}
							aria-controls="stage-body-{s.stage}"
							onclick={() => toggle(openStages, String(s.stage))}
						>
							<span class="min-w-0 flex-1 text-left">
								<span id="stage-{s.stage}" class="step-title">Stage {s.stage}: {s.title}</span>
							</span>
							<span
								class="bar"
								role="progressbar"
								aria-label="Stage {s.stage} progress"
								aria-valuemin={0}
								aria-valuemax={s.total}
								aria-valuenow={s.solved}
							>
								<span style="width: {s.total ? (s.solved / s.total) * 100 : 0}%"></span>
							</span>
							<span class="meta">{s.solved} / {s.total}</span>
							<ChevronDown
								class="chevron size-4 shrink-0 {open ? 'open' : ''}"
								aria-hidden="true"
							/>
						</button>
						{#if open}
							<div id="stage-body-{s.stage}" class="step-body">
								{#each s.problems as p (p.id)}
									{@const state = statusOf(p.id, solved.slugs, attempted.slugs)}
									<a
										class="theory-row"
										href={resolve('/ide/[id]', { id: p.id })}
										onclick={() => recent.note('cuda', p.id)}
									>
										<SolvedMark isSolved={state === 'solved'} questionTitle={p.title} />
										<span class="mono">{p.number}</span>
										<span class="theory-row-title">{p.title}</span>
										{#if state === 'attempted'}<span class="attempted">attempted</span>{/if}
										<DifficultyBadge difficulty={p.difficulty} />
									</a>
								{/each}
							</div>
						{/if}
					</section>
				{/each}
			</div>
		{/if}
	</div>
</main>

<style>
	.sheet {
		font-variant-numeric: tabular-nums;
		--level-step: var(--secondary);
		--level-topic: color-mix(in oklab, var(--background) 82%, black);
	}
	:global(html:not(.dark)) .sheet {
		--level-topic: color-mix(in oklab, var(--background) 94%, var(--foreground));
	}
	.ring-card {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 16px 20px;
		border: 1px solid var(--border);
		border-radius: 14px;
		background: var(--secondary);
	}
	.pie {
		display: grid;
		place-items: center;
		width: 96px;
		height: 96px;
		border-radius: 50%;
		background: conic-gradient(var(--primary) var(--progress), var(--border) 0);
		position: relative;
	}
	.pie::before {
		content: '';
		position: absolute;
		inset: 12px;
		border-radius: 50%;
		background: var(--secondary);
	}
	.pie span {
		position: relative;
		font-family: var(--font-mono, ui-monospace, monospace);
		font-weight: 700;
		font-size: 1.15rem;
	}
	.ring-copy {
		display: flex;
		flex-direction: column;
		font-size: 0.85rem;
		color: var(--muted-foreground);
	}
	.ring-copy strong {
		color: var(--foreground);
		font-size: 1.05rem;
	}
	.ring-sub {
		font-size: 0.75rem;
	}
	.seg {
		display: inline-flex;
		margin-bottom: 12px;
		padding: 3px;
		border: 1px solid var(--border);
		border-radius: 10px;
		background: var(--secondary);
	}
	.seg button {
		padding: 6px 14px;
		border-radius: 7px;
		border: 0;
		background: transparent;
		color: var(--muted-foreground);
		font-size: 0.85rem;
		cursor: pointer;
	}
	.seg button[aria-pressed='true'] {
		background: var(--background);
		color: var(--foreground);
		font-weight: 600;
	}
	.group-title {
		margin: 28px 0 12px;
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 0.8rem;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--muted-foreground);
	}
	.empty-state {
		margin-top: 32px;
		color: var(--muted-foreground);
		font-size: 0.9rem;
	}
	.empty-clear {
		margin-left: 8px;
		display: inline-flex;
		gap: 4px;
		align-items: center;
		text-decoration: underline;
	}
	.step-card {
		border: 1px solid var(--border);
		border-radius: 12px;
		background: var(--level-step);
		overflow: hidden;
	}
	.step-card:has(.step-head[aria-expanded='true']) {
		border-color: color-mix(in oklab, var(--foreground) 22%, var(--border));
		box-shadow: inset 3px 0 0 color-mix(in oklab, var(--foreground) 20%, transparent);
	}
	.step-head {
		display: flex;
		width: 100%;
		align-items: center;
		gap: 16px;
		border: 0;
		background: transparent;
		padding: 16px 18px;
		color: var(--foreground);
		font: inherit;
		cursor: pointer;
	}
	.step-head:hover {
		background: color-mix(in oklab, var(--foreground) 5%, transparent);
	}
	.step-title {
		display: block;
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 1.05rem;
		font-weight: 700;
		letter-spacing: -0.01em;
	}
	.meta {
		font-size: 0.8rem;
		color: var(--muted-foreground);
		white-space: nowrap;
	}
	.bar {
		width: 120px;
		flex: 0 0 120px;
		height: 6px;
		border-radius: 999px;
		background: var(--border);
		overflow: hidden;
	}
	.bar span {
		display: block;
		height: 100%;
		background: var(--primary);
	}
	:global(.chevron) {
		color: var(--muted-foreground);
		transition: transform 150ms;
	}
	:global(.chevron.open) {
		transform: rotate(180deg);
	}
	.step-body {
		display: flex;
		flex-direction: column;
		gap: 8px;
		padding: 2px 14px 16px 18px;
	}
	.theory-row {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 11px 16px;
		border: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		border-radius: 10px;
		background: var(--level-topic);
		color: var(--foreground);
	}
	.theory-row:hover {
		background: color-mix(in oklab, var(--level-topic) 80%, var(--foreground) 6%);
	}
	.theory-row-title {
		flex: 1;
		font-weight: 600;
		min-width: 0;
	}
	.mono {
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 0.75rem;
		color: var(--muted-foreground);
	}
	.attempted {
		font-size: 0.75rem;
		color: #d97706;
	}
	@media (max-width: 640px) {
		.bar {
			display: none;
		}
	}
</style>
