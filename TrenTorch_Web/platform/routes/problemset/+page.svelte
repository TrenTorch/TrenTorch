<script lang="ts">
	import { resolve } from '$app/paths';
	import FilterSelect from '$components/FilterSelect.svelte';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import {
		ArrowRight,
		Check,
		ChevronLeft,
		ChevronRight,
		RotateCcw,
		Search,
		SlidersHorizontal
	} from '@lucide/svelte';
	import ProblemsetPotdBanner from '$components/ProblemsetPotdBanner.svelte';
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
		getProblemsetStatus,
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
	let searchQuery = $state('');
	let activeModule = $state('');
	let activeTopic = $state('');
	let selectedCompany = $state('');
	let selectedDifficulty = $state('');
	let selectedStatus = $state<ProblemsetStatus>('all');
	let pastPotdOnly = $state(false);
	let filterOpen = $state(false);
	let filterRoot = $state<HTMLDivElement>();
	let showAllModules = $state(false);
	let pastPotdSlugs = $state<ReadonlySet<string>>(new Set());
	let moduleRail = $state<HTMLDivElement>();
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
	const activeFilterCount = $derived(
		[
			activeModule,
			activeTopic,
			selectedCompany,
			selectedDifficulty,
			selectedStatus !== 'all',
			pastPotdOnly
		].filter(Boolean).length
	);

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

	function onWindowPointerDown(event: PointerEvent) {
		const target = event.target as Element;
		if (target.closest('[data-slot="select-content"]')) return;
		if (filterOpen && filterRoot && !filterRoot.contains(target)) filterOpen = false;
	}

	function onWindowKeydown(event: KeyboardEvent) {
		if (
			filterOpen &&
			event.key === 'Escape' &&
			!document.querySelector('[data-slot="select-content"]')
		)
			filterOpen = false;
	}

	function goToPage(nextPage: number) {
		currentPage = Math.min(Math.max(1, nextPage), totalPages);
		if (!browser) return;
		const url = new URL(window.location.href);
		url.searchParams.set('page', String(currentPage));
		history.replaceState(history.state, '', url);
	}

	function scrollModules(direction: -1 | 1) {
		moduleRail?.scrollBy({ left: direction * 300, behavior: 'smooth' });
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

<svelte:window onpointerdown={onWindowPointerDown} onkeydown={onWindowKeydown} />

<svelte:head>
	<title>Problemset - TrenTorch</title>
	<meta
		name="description"
		content="Browse 250 hands-on machine learning and data science problems."
	/>
</svelte:head>

<main class="problemset min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px]">
		<h1 class="mb-1 font-mono text-[1.4rem] font-bold">Problemset</h1>
		<p class="mb-6 text-sm text-muted-foreground">
			{problemsetProblems.length} hands-on problems across {problemsetModules.length} study modules.
		</p>

		<div class="mb-6">
			<ProblemsetPotdBanner onDayChange={updatePastPotd} potdSummaries={data.potdSummaries} />
		</div>

		<div class="mb-3 flex items-center justify-between gap-3">
			<h2 class="font-mono text-lg font-semibold">Study modules</h2>
			<div class="flex items-center gap-2">
				{#if !showAllModules}
					<button
						type="button"
						class="rail-arrow press"
						aria-label="Scroll modules left"
						onclick={() => scrollModules(-1)}
					>
						<ChevronLeft class="size-4" />
					</button>
					<button
						type="button"
						class="rail-arrow press"
						aria-label="Scroll modules right"
						onclick={() => scrollModules(1)}
					>
						<ChevronRight class="size-4" />
					</button>
				{/if}
				<button
					type="button"
					class="see-all"
					aria-expanded={showAllModules}
					onclick={() => (showAllModules = !showAllModules)}
				>
					{showAllModules ? 'Show fewer' : 'See all modules'}
				</button>
			</div>
		</div>

		{#if showAllModules}
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
		{:else}
			<div class="relative mb-6">
				<div
					bind:this={moduleRail}
					class="module-rail flex snap-x snap-proximity gap-3 overflow-x-auto pb-2"
					aria-label="Study modules"
				>
					{#each problemsetModules as module (module.id)}
						{@const ModuleIcon = getPartIcon(module.learningPartId)}
						<a
							href={resolve('/questions/[partId]', { partId: module.learningPartId })}
							class="module-card snap-start"
						>
							<ModuleIcon class="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
							<span class="min-w-0">
								<span class="module-title">{module.title}</span>
								<span class="module-description">{module.description}</span>
							</span>
							<ArrowRight
								class="ml-auto size-4 shrink-0 text-muted-foreground"
								aria-hidden="true"
							/>
						</a>
					{/each}
				</div>
			</div>
		{/if}

		<div class="mb-3 flex items-center gap-2">
			<label class="search-field">
				<span class="sr-only">Search problems</span>
				<Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2" />
				<input bind:value={searchQuery} type="search" placeholder="Search problems..." />
			</label>

			<div class="relative" bind:this={filterRoot}>
				<button
					type="button"
					class="filter-trigger press {filterOpen || activeFilterCount ? 'active' : ''}"
					aria-haspopup="dialog"
					aria-expanded={filterOpen}
					onclick={() => (filterOpen = !filterOpen)}
				>
					<SlidersHorizontal class="size-4" aria-hidden="true" />
					Filters
					{#if activeFilterCount}
						<span class="filter-count">{activeFilterCount}</span>
					{/if}
				</button>

				{#if filterOpen}
					<div role="dialog" aria-label="Filters" class="filter-popover">
						<div class="filter-field">
							<span>Module</span>
							<FilterSelect
								bind:value={activeModule}
								label="Filter by module"
								class="w-full justify-between"
								options={[
									{ value: '', label: 'All modules' },
									...problemsetModules.map((module) => ({ value: module.id, label: module.title }))
								]}
							/>
						</div>
						<div class="filter-field">
							<span>Topic</span>
							<FilterSelect
								bind:value={activeTopic}
								label="Filter by topic"
								class="w-full justify-between"
								options={[
									{ value: '', label: 'All topics' },
									...topics.map((topic) => ({ value: topic, label: topicLabel(topic) }))
								]}
							/>
						</div>
						<div class="filter-field">
							<span>Company</span>
							<FilterSelect
								bind:value={selectedCompany}
								label="Filter by company"
								class="w-full justify-between"
								options={[
									{ value: '', label: 'All companies' },
									...companies.map((company) => ({ value: company, label: company }))
								]}
							/>
						</div>
						<div class="filter-field">
							<span>Status</span>
							<FilterSelect
								bind:value={selectedStatus}
								label="Filter by status"
								class="w-full justify-between"
								options={statuses}
							/>
						</div>
						<div class="filter-field">
							<span>Difficulty</span>
							<FilterSelect
								bind:value={selectedDifficulty}
								label="Filter by difficulty"
								class="w-full justify-between"
								options={[
									{ value: '', label: 'All difficulties' },
									...difficulties.map((difficulty) => ({ value: difficulty, label: difficulty }))
								]}
							/>
						</div>
						<label class="filter-check">
							<input type="checkbox" bind:checked={pastPotdOnly} />
							Past Problem of the Day only
						</label>
						{#if activeFilterCount}
							<button type="button" class="clear-button" onclick={resetFilters}>
								<RotateCcw class="size-3.5" />
								Clear filters
							</button>
						{/if}
					</div>
				{/if}
			</div>
		</div>

		<p class="mb-2 text-xs text-muted-foreground" aria-live="polite">
			{filteredProblems.length}
			{filteredProblems.length === 1 ? 'problem' : 'problems'}
		</p>

		{#if filteredProblems.length === 0}
			<p class="empty-state">
				{pastPotdOnly
					? 'No past Problem of the Day problems match these filters.'
					: 'No problems match these filters.'}
			</p>
		{:else}
			<div class="overflow-x-auto">
				<table class="problem-table">
					<thead>
						<tr>
							<th class="w-[26px]" aria-label="Status"></th>
							<th>Title</th>
							<th>Difficulty</th>
						</tr>
					</thead>
					<tbody>
						{#each pagedProblems as problem (problem.slug)}
							{@const status = getProblemsetStatus(problem.slug, solved.slugs, attempted.slugs)}
							<tr>
								<td class="status-cell">
									{#if status === 'solved'}
										<Check class="mx-auto size-4 text-[#3fb950]" aria-label="Solved" />
									{:else if status === 'attempted'}
										<span role="img" aria-label="Attempted" class="text-[#d29922]">●</span>
									{/if}
								</td>
								<td>
									<a href={resolve('/ide/[id]', { id: problem.slug })} class="problem-link">
										{problem.title}
									</a>
									<span class="module-tag">
										{problemsetModules.find((module) => module.id === problem.moduleId)?.title}
										&middot;
										{topicLabel(problem.topic)}
									</span>
									{#if pastPotdSlugs.has(problem.slug)}
										<span class="potd-tag">Past POTD</span>
									{/if}
								</td>
								<td>
									<span class="difficulty-badge {problem.difficulty}">
										<span class="difficulty-dot" aria-hidden="true"></span>
										{problem.difficulty}
									</span>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

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

	.see-all {
		border: 0;
		background: transparent;
		padding: 6px 8px;
		color: var(--muted-foreground);
		font-size: 0.78rem;
		cursor: pointer;
	}

	.see-all:hover {
		color: var(--foreground);
		text-decoration: underline;
	}

	.module-rail {
		scroll-snap-type: x proximity;
		scrollbar-color: var(--border) transparent;
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

	.filter-trigger {
		display: inline-flex;
		height: 38px;
		align-items: center;
		gap: 8px;
		border: 1px solid var(--border);
		border-radius: 6px;
		background: var(--secondary);
		padding: 0 12px;
		color: var(--foreground);
		font: inherit;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.filter-trigger.active {
		border-color: color-mix(in srgb, var(--foreground) 35%, var(--border));
		background: var(--muted);
	}

	.filter-count {
		min-width: 18px;
		border-radius: 999px;
		background: var(--foreground);
		padding: 0 5px;
		color: var(--background);
		font-size: 0.68rem;
		line-height: 18px;
		text-align: center;
	}

	.filter-popover {
		position: absolute;
		z-index: 30;
		top: calc(100% + 8px);
		right: 0;
		display: flex;
		width: 300px;
		max-width: calc(100vw - 2rem);
		flex-direction: column;
		gap: 12px;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--background);
		padding: 14px;
		box-shadow: 0 12px 32px rgb(0 0 0 / 35%);
	}

	.filter-field {
		display: flex;
		flex-direction: column;
		gap: 5px;
		color: var(--muted-foreground);
		font-size: 0.72rem;
	}

	.filter-check {
		display: flex;
		align-items: center;
		gap: 8px;
		color: var(--foreground);
		font-size: 0.8rem;
		cursor: pointer;
	}

	.search-field {
		position: relative;
		min-width: 180px;
		flex: 1;
	}

	.search-field input {
		width: 100%;
		height: 38px;
		border: 1px solid var(--border);
		border-radius: 6px;
		background: var(--secondary);
		padding: 0 12px 0 36px;
		color: var(--foreground);
		font: inherit;
		font-size: 0.78rem;
	}

	.search-field input:focus {
		border-color: var(--primary);
		outline: 1px solid var(--primary);
	}

	.search-field :global(svg) {
		color: var(--muted-foreground);
	}

	.clear-button {
		display: inline-flex;
		height: 38px;
		align-items: center;
		gap: 7px;
		border: 0;
		background: transparent;
		padding: 0 8px;
		color: var(--muted-foreground);
		font: inherit;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.clear-button:hover {
		color: var(--foreground);
	}

	.problem-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.85rem;
	}

	.problem-table thead th {
		border-bottom: 1px solid var(--border);
		padding: 8px 10px;
		color: var(--muted-foreground);
		font-size: 0.75rem;
		font-weight: normal;
		text-align: left;
	}

	.problem-table tbody tr {
		position: relative;
		border-bottom: 1px solid var(--border);
		cursor: pointer;
	}

	.problem-table tbody tr:hover {
		background: var(--secondary);
	}

	.problem-table tbody tr:last-child {
		border-bottom: 0;
	}

	.problem-table tbody td {
		padding: 11px 10px;
		vertical-align: middle;
	}

	.status-cell {
		width: 26px;
		text-align: center;
	}

	.problem-link {
		color: var(--foreground);
		text-decoration: none;
	}

	.problem-link::after {
		position: absolute;
		inset: 0;
		content: '';
	}

	.problem-link:focus-visible {
		outline-offset: -2px;
	}

	.problem-link:hover {
		color: var(--primary);
	}

	.module-tag,
	.potd-tag {
		display: inline-block;
		margin-left: 8px;
		font-size: 0.72rem;
	}

	.module-tag {
		color: var(--muted-foreground);
	}

	.potd-tag {
		border: 1px solid var(--border);
		border-radius: 4px;
		padding: 1px 7px;
		color: var(--muted-foreground);
	}

	.difficulty-badge {
		display: inline-flex;
		align-items: center;
		gap: 7px;
		font-size: 0.8rem;
	}

	.difficulty-dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		background: currentcolor;
	}

	.difficulty-badge.Beginner {
		color: color-mix(in srgb, #3fb950 75%, var(--foreground));
	}

	.difficulty-badge.Intermediate {
		color: color-mix(in srgb, #d29922 75%, var(--foreground));
	}

	.difficulty-badge.Advanced {
		color: color-mix(in srgb, #e5534b 80%, var(--foreground));
	}

	.empty-state {
		border: 1px solid var(--border);
		border-radius: 6px;
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

	@media (max-width: 640px) {
		.problem-table thead {
			display: none;
		}

		.problem-table tbody td {
			display: block;
			padding: 3px 10px;
		}

		.problem-table tbody tr {
			display: block;
			padding: 10px 0;
		}

		.problem-table tbody td:not(.status-cell) {
			padding-left: 40px;
		}

		.status-cell {
			float: left;
			width: 30px;
			padding-top: 5px !important;
		}
	}
</style>
