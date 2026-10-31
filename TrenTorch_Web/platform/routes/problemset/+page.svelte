<script lang="ts">
	import { resolve } from '$app/paths';
	import FilterBar from '$components/FilterBar.svelte';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { ArrowRight, ChevronLeft, ChevronRight, RotateCcw } from '@lucide/svelte';
	import PagePill from '$components/PagePill.svelte';
	import ProblemsetPotdBanner from '$components/ProblemsetPotdBanner.svelte';
	import QuestionRow from '$components/QuestionRow.svelte';
	import { getPartIcon } from '$data/part-icons';
	import {
		problemsetModules,
		problemsetProblems,
		type ProblemsetDifficulty
	} from '$data/problemset';
	import { potdEntries } from '$data/potd';
	import type { PageProps } from './$types';
	import {
		filterProblemset,
		paginateProblemset,
		PROBLEMSET_PAGE_SIZE,
		type ProblemsetFilters,
		type ProblemsetStatus
	} from '$processes/problemset/filter-problems';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';

	let { data }: PageProps = $props();

	const difficulties: ProblemsetDifficulty[] = ['Beginner', 'Intermediate', 'Advanced'];
	const statuses: { value: ProblemsetStatus; label: string }[] = [
		{ value: 'all', label: 'All statuses' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'attempted', label: 'Attempted' },
		{ value: 'unsolved', label: 'Unsolved' }
	];
	const companies = [
		...new Set(
			problemsetProblems.flatMap((problem) => (problem.caseCompany ? [problem.caseCompany] : []))
		)
	].sort();
	const topics = [...new Set(problemsetProblems.map((problem) => problem.topic))].sort((a, b) =>
		topicLabel(a).localeCompare(topicLabel(b))
	);
	const topicChoices = topics.map((topic) => ({
		value: topic,
		label: topicLabel(topic),
		count: problemsetProblems.filter((problem) => problem.topic === topic).length
	}));
	const companyChoices = companies.map((company) => ({
		value: company,
		label: company,
		count: problemsetProblems.filter((problem) => problem.caseCompany === company).length
	}));
	let searchQuery = $state('');
	let activeModule = $state('');
	let activeTopic = $state('');
	let selectedCompany = $state('');
	let selectedDifficulty = $state('');
	let selectedStatus = $state<ProblemsetStatus>('all');
	let pastPotdOnly = $state(false);
	let pastPotdSlugs = $state<ReadonlySet<string>>(new Set());
	let currentPage = $state(browser ? Number(page.url.searchParams.get('page')) || 1 : 1);

	const filters = $derived<ProblemsetFilters>({
		query: searchQuery,
		moduleId: activeModule,
		topic: activeTopic,
		company: selectedCompany,
		difficulty: selectedDifficulty,
		status: selectedStatus,
		pastPotdOnly
	});
	const filteredProblems = $derived(
		filterProblemset(problemsetProblems, filters, solved.slugs, attempted.slugs, pastPotdSlugs)
	);
	const totalPages = $derived(
		Math.max(1, Math.ceil(filteredProblems.length / PROBLEMSET_PAGE_SIZE))
	);
	const pagedProblems = $derived(paginateProblemset(filteredProblems, currentPage));
	function topicLabel(topic: string): string {
		const acronyms: Record<string, string> = {
			cnn: 'CNN',
			eda: 'EDA',
			llm: 'LLM',
			pca: 'PCA',
			rlhf: 'RLHF',
			svm: 'SVM'
		};

		return topic
			.split('-')
			.filter(Boolean)
			.map((word) => acronyms[word] ?? `${word[0].toUpperCase()}${word.slice(1)}`)
			.join(' ');
	}

	function resetFilters() {
		searchQuery = '';
		activeModule = '';
		activeTopic = '';
		selectedCompany = '';
		selectedDifficulty = '';
		selectedStatus = 'all';
		pastPotdOnly = false;
	}

	function goToPage(nextPage: number) {
		currentPage = Math.min(Math.max(1, nextPage), totalPages);
		if (!browser) return;
		const url = new URL(window.location.href);
		url.searchParams.set('page', String(currentPage));
		history.replaceState(history.state, '', url);
	}

	function updatePastPotd(today: string) {
		pastPotdSlugs = new Set(
			potdEntries.filter((entry) => entry.date < today).map((entry) => entry.questionId)
		);
	}

	let filtersMounted = false;
	$effect(() => {
		void filters;
		if (filtersMounted) goToPage(1);
		filtersMounted = true;
	});

	$effect(() => {
		if (currentPage > totalPages) goToPage(totalPages);
	});
</script>

<svelte:head>
	<title>Problemset - TrenTorch</title>
	<meta
		name="description"
		content="Browse 250 hands-on machine learning and data science problems."
	/>
</svelte:head>

<main class="problemset min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px]">
		<header class="dot-texture mb-6">
			<PagePill slug="problemset/" />
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">Problem Set</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				{problemsetProblems.length} hands-on problems across {problemsetModules.length} study modules.
			</p>
		</header>

		<div class="mb-6">
			<ProblemsetPotdBanner summaries={data.potdSummaries} onDayChange={updatePastPotd} />
		</div>

		<div class="mb-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
			{#each problemsetModules as module (module.id)}
				{@const ModuleIcon = getPartIcon(module.learningPartId)}
				<a
					href={resolve('/questions/[partId]', { partId: module.learningPartId })}
					class="module-card"
				>
					<ModuleIcon class="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
					<span class="min-w-0">
						<span class="module-title">{module.title}</span>
						<span class="module-description">{module.description}</span>
					</span>
					<ArrowRight class="ml-auto size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
				</a>
			{/each}
		</div>

		<FilterBar
			bind:query={searchQuery}
			bind:moduleId={activeModule}
			bind:topic={activeTopic}
			bind:company={selectedCompany}
			bind:difficulty={selectedDifficulty}
			bind:status={selectedStatus}
			bind:pastPotd={pastPotdOnly}
			modules={problemsetModules}
			topics={topicChoices}
			companies={companyChoices}
			{difficulties}
			{statuses}
			resultCount={filteredProblems.length}
			total={problemsetProblems.length}
		/>

		{#if filteredProblems.length === 0}
			<p class="empty-state">
				{pastPotdOnly
					? 'No past Problem of the Day problems match these filters.'
					: 'No problems match these filters.'}
				<button type="button" class="empty-clear" onclick={resetFilters}>
					<RotateCcw class="size-3.5" aria-hidden="true" />
					Clear filters
				</button>
			</p>
		{:else}
			<!-- The same rows as the Problem of the Day archive: a status box, the title, what it is about, and
			     its level. -->
			<section class="overflow-hidden rounded-2xl border border-border" aria-label="Problems">
				{#each pagedProblems as problem (problem.slug)}
					<div class="border-t border-border px-4 py-3 first:border-t-0">
						<QuestionRow
							question={problem}
							meta={topicLabel(problem.topic)}
							tags={pastPotdSlugs.has(problem.slug) ? ['Past POTD'] : []}
							trackPage={false}
							wrap
						/>
					</div>
				{/each}
			</section>

			{#if totalPages > 1}
				<nav class="pagination" aria-label="Problemset pages">
					<button
						type="button"
						class="rail-arrow press"
						disabled={currentPage <= 1}
						aria-label="Previous page"
						onclick={() => goToPage(currentPage - 1)}
					>
						<ChevronLeft class="size-4" />
					</button>
					<span>Page {currentPage} of {totalPages}</span>
					<button
						type="button"
						class="rail-arrow press"
						disabled={currentPage >= totalPages}
						aria-label="Next page"
						onclick={() => goToPage(currentPage + 1)}
					>
						<ChevronRight class="size-4" />
					</button>
				</nav>
			{/if}
		{/if}

		<footer class="problemset-footer">
			<p>
				Company-tagged problems are original scenarios inspired by the kinds of challenges these
				companies can and have faced. They are not claimed to be actual interview questions asked by
				those companies.
			</p>
		</footer>
	</div>
</main>

<style>
	.problemset {
		font-variant-numeric: tabular-nums;
		min-height: calc(100vh - 3.5rem);
		background: var(--background);
		color: var(--foreground);
		font-family: var(--font-sans);
	}

	.problemset * {
		font-family: inherit;
	}

	.module-card {
		display: flex;
		min-width: 230px;
		flex: 0 0 230px;
		align-items: flex-start;
		gap: 10px;
		border: 1px solid var(--border);
		border-radius: 6px;
		background: var(--secondary);
		padding: 12px 14px;
		transition: border-color 150ms;
	}

	.module-card:hover {
		border-color: color-mix(in srgb, var(--foreground) 35%, var(--border));
	}

	.module-title,
	.module-description {
		display: block;
	}

	.module-title {
		margin: 0 0 4px;
		font-size: 0.85rem;
		font-weight: 600;
	}

	.module-description {
		display: -webkit-box;
		overflow: hidden;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		color: var(--muted-foreground);
		font-size: 0.75rem;
		line-height: 1.45;
	}

	.rail-arrow {
		display: inline-flex;
		width: 30px;
		height: 30px;
		align-items: center;
		justify-content: center;
		border: 1px solid var(--border);
		border-radius: 6px;
		background: var(--secondary);
		color: var(--foreground);
		cursor: pointer;
	}

	.rail-arrow:hover:not(:disabled) {
		border-color: color-mix(in srgb, var(--foreground) 35%, var(--border));
	}

	.rail-arrow:disabled {
		cursor: not-allowed;
		opacity: 0.4;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		border: 1px solid var(--border);
		border-radius: 12px;
		padding: 48px 12px;
		color: var(--muted-foreground);
		font-size: 0.85rem;
		text-align: center;
	}

	.empty-clear {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		margin: 14px auto 0;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--secondary);
		padding: 6px 12px;
		color: var(--foreground);
		font: inherit;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.empty-clear:hover {
		border-color: var(--primary);
	}

	.pagination {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 14px;
		padding-top: 20px;
		color: var(--muted-foreground);
		font-size: 0.78rem;
	}

	.problemset-footer {
		margin-top: 36px;
		border-top: 1px solid var(--border);
		padding-top: 16px;
	}

	.problemset-footer p {
		max-width: 720px;
		color: var(--muted-foreground);
		font-size: 0.65rem;
		font-style: italic;
		line-height: 1.5;
	}
</style>
