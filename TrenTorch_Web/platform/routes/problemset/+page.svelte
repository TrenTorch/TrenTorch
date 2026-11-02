<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { ArrowRight, ChevronLeft, ChevronRight, RotateCcw } from '@lucide/svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import PagePill from '$components/PagePill.svelte';
	import QuestionRow from '$components/QuestionRow.svelte';
	import ProblemsetPotdBanner from '$components/ProblemsetPotdBanner.svelte';
	import { getPartIcon } from '$data/part-icons';
	import {
		problemsetModules,
		problemsetProblems,
		buildPotdProblems,
		type ProblemsetDifficulty
	} from '$data/problemset';
	import { potdEntries } from '$data/potd';
	import {
		filterProblemset,
		paginateProblemset,
		PROBLEMSET_PAGE_SIZE,
		type ProblemsetFilters,
		type ProblemsetStatus
	} from '$processes/problemset/filter-problems';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	const potdProblems = $derived(buildPotdProblems(data.potdSummaries));

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
	// Everything the page lists: the study-module problems and the Problem of the Day ones. The count in the
	// heading is this, so it agrees with what the list holds.
	const totalProblems = $derived(problemsetProblems.length + potdProblems.length);
	const filteredProblems = $derived(
		filterProblemset(
			[...problemsetProblems, ...potdProblems],
			filters,
			solved.slugs,
			attempted.slugs,
			pastPotdSlugs
		)
	);
	const totalPages = $derived(
		Math.max(1, Math.ceil(filteredProblems.length / PROBLEMSET_PAGE_SIZE))
	);
	const pagedProblems = $derived(paginateProblemset(filteredProblems, currentPage));
	function topicLabel(topic: string): string {
		const phrases: Record<string, string> = {
			'ab testing': 'A/B Testing'
		};
		if (phrases[topic]) return phrases[topic];

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
	<title>Problem Set - TrenTorch</title>
	<meta
		name="description"
		content="Browse hands-on machine learning and data science problems across the study modules."
	/>
</svelte:head>

<main class="problemset min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px]">
		<header class="dot-texture mb-6">
			<PagePill slug="problemset/" />
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">Problem Set</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				{totalProblems} hands-on problems across {problemsetModules.length} study modules.
			</p>
		</header>

		<div class="mb-6">
			<ProblemsetPotdBanner summaries={data.potdSummaries} onDayChange={updatePastPotd} />
		</div>

		<div class="mb-7 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
			{#each problemsetModules as module (module.id)}
				{@const ModuleIcon = getPartIcon(module.learningPartId)}
				<a
					href={resolve('/questions/[partId]', { partId: module.learningPartId })}
					class="module-card"
				>
					<ModuleIcon class="size-6 shrink-0 text-primary" aria-hidden="true" />
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
			total={totalProblems}
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
							tags={[
								...(problem.caseCompany ? [problem.caseCompany] : []),
								...(pastPotdSlugs.has(problem.slug) ? ['Past POTD'] : [])
							]}
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
						class="rail-arrow"
						disabled={currentPage <= 1}
						aria-label="Previous page"
						onclick={() => goToPage(currentPage - 1)}
					>
						<ChevronLeft class="size-4" />
					</button>
					<span>Page {currentPage} of {totalPages}</span>
					<button
						type="button"
						class="rail-arrow"
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
		min-height: calc(100vh - 4.75rem);
		background: var(--background);
		color: var(--foreground);
		font-family: var(--font-sans);
	}

	.problemset * {
		font-family: inherit;
	}

	.module-card {
		display: flex;
		min-width: 236px;
		min-height: 104px;
		flex: 0 0 236px;
		align-items: flex-start;
		gap: 12px;
		border: 1px solid var(--border);
		border-radius: 12px;
		background: var(--secondary);
		padding: 14px;
		transition: border-color 150ms;
	}

	.module-card:hover {
		border-color: var(--primary);
	}

	.module-title,
	.module-description {
		display: block;
	}

	.module-title {
		margin: 3px 0 5px;
		font-size: 0.82rem;
	}

	.module-description {
		display: -webkit-box;
		overflow: hidden;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		color: var(--muted-foreground);
		font-size: 0.72rem;
		line-height: 1.45;
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

	.rail-arrow {
		display: inline-flex;
		width: 34px;
		height: 34px;
		align-items: center;
		justify-content: center;
		border: 1px solid var(--border);
		border-radius: 9px;
		background: var(--secondary);
		color: var(--foreground);
		cursor: pointer;
	}

	.rail-arrow:hover:not(:disabled) {
		border-color: var(--primary);
		color: color-mix(in srgb, var(--primary) 55%, var(--foreground));
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
