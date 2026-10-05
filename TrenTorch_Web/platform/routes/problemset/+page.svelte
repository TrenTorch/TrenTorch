<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import {
		Building2,
		CalendarClock,
		ArrowRight,
		Check,
		ChevronLeft,
		ChevronRight,
		RotateCcw,
		Search
	} from '@lucide/svelte';
	import ProblemsetPotdBanner from '$components/ProblemsetPotdBanner.svelte';
	import { getPartIcon } from '$data/part-icons';
	import {
		problemsetModules,
		problemsetProblems,
		type ProblemsetDifficulty
	} from '$data/problemset';
	import { potdEntries } from '$data/potd';
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
	let showAllTopics = $state(false);
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
	const filtering = $derived(
		Boolean(
			searchQuery.trim() ||
			activeModule ||
			activeTopic ||
			selectedCompany ||
			selectedDifficulty ||
			selectedStatus !== 'all' ||
			pastPotdOnly
		)
	);

	function topicLabel(topic: string): string {
		const acronyms: Record<string, string> = {
			ab: 'A/B',
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

	function chooseCompany(company: string) {
		selectedCompany = selectedCompany === company ? '' : company;
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

		<div class="mb-7">
			<ProblemsetPotdBanner onDayChange={updatePastPotd} />
		</div>

		<div class="mb-3 flex items-center justify-between gap-3">
			<div>
				<p class="mb-1 font-mono text-xs tracking-wider text-muted-foreground uppercase">
					Problemset
				</p>
				<h2 class="font-mono text-lg font-semibold">Study modules</h2>
			</div>
			<button
				type="button"
				class="text-xs text-primary hover:underline"
				aria-expanded={showAllModules}
				onclick={() => (showAllModules = !showAllModules)}
			>
				{showAllModules ? 'Show fewer' : 'See all modules'}
			</button>
		</div>

		{#if showAllModules}
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
		{:else}
			<div class="relative mb-7">
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
							<ModuleIcon class="size-6 shrink-0 text-primary" aria-hidden="true" />
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
				<div class="mt-2 flex justify-end gap-2">
					<button
						type="button"
						class="rail-arrow"
						aria-label="Scroll modules left"
						onclick={() => scrollModules(-1)}
					>
						<ChevronLeft class="size-4" />
					</button>
					<button
						type="button"
						class="rail-arrow"
						aria-label="Scroll modules right"
						onclick={() => scrollModules(1)}
					>
						<ChevronRight class="size-4" />
					</button>
				</div>
			</div>
		{/if}

		<div class="topic-row mb-3" role="group" aria-label="Filter by topic">
			<button
				type="button"
				class="topic-pill {activeTopic === '' ? 'selected' : ''}"
				aria-pressed={activeTopic === ''}
				onclick={() => (activeTopic = '')}
			>
				All topics
			</button>
			{#each showAllTopics ? topics : topics.slice(0, 6) as topic (topic)}
				<button
					type="button"
					class="topic-pill {activeTopic === topic ? 'selected' : ''}"
					aria-pressed={activeTopic === topic}
					onclick={() => (activeTopic = activeTopic === topic ? '' : topic)}
				>
					{topicLabel(topic)}
					<span class="topic-count">
						{problemsetProblems.filter((problem) => problem.topic === topic).length}
					</span>
				</button>
			{/each}
			{#if topics.length > 6}
				<button
					type="button"
					class="expand-button"
					aria-expanded={showAllTopics}
					onclick={() => (showAllTopics = !showAllTopics)}
				>
					{showAllTopics ? 'Show fewer' : 'Expand'}
				</button>
			{/if}
		</div>

		<div class="mb-4 flex flex-wrap items-center gap-2">
			<label class="search-field">
				<span class="sr-only">Search problems</span>
				<Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2" />
				<input bind:value={searchQuery} type="search" placeholder="Search problems..." />
			</label>

			<label class="filter-select">
				<span class="sr-only">Filter by module</span>
				<select bind:value={activeModule}>
					<option value="">All modules</option>
					{#each problemsetModules as module (module.id)}
						<option value={module.id}>{module.title}</option>
					{/each}
				</select>
			</label>

			<button
				type="button"
				class="filter-button {pastPotdOnly ? 'active' : ''}"
				aria-pressed={pastPotdOnly}
				onclick={() => (pastPotdOnly = !pastPotdOnly)}
			>
				<CalendarClock class="size-4" aria-hidden="true" />
				Past POTD
			</button>

			<label class="filter-select">
				<span class="sr-only">Filter by status</span>
				<select bind:value={selectedStatus}>
					{#each statuses as status (status.value)}
						<option value={status.value}>{status.label}</option>
					{/each}
				</select>
			</label>

			<label class="filter-select">
				<span class="sr-only">Filter by difficulty</span>
				<select bind:value={selectedDifficulty}>
					<option value="">All difficulties</option>
					{#each difficulties as difficulty (difficulty)}
						<option value={difficulty}>{difficulty}</option>
					{/each}
				</select>
			</label>

			{#if filtering}
				<button type="button" class="clear-button" onclick={resetFilters}>
					<RotateCcw class="size-3.5" />
					Clear
				</button>
			{/if}
		</div>

		<div class="company-filter-row" role="group" aria-label="Filter by company">
			<button
				type="button"
				class:active={selectedCompany === ''}
				aria-pressed={selectedCompany === ''}
				onclick={() => chooseCompany('')}
			>
				<Building2 class="size-3.5" aria-hidden="true" />
				All companies
			</button>
			{#each companies as company (company)}
				<button
					type="button"
					class:active={selectedCompany === company}
					aria-pressed={selectedCompany === company}
					onclick={() => chooseCompany(company)}
				>
					<Building2 class="size-3.5" aria-hidden="true" />
					{company}
				</button>
			{/each}
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
							<th>Company</th>
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
									{#if problem.caseCompany}
										<span class="company-tag">{problem.caseCompany}</span>
									{/if}
								</td>
								<td>
									<span class="difficulty-badge {problem.difficulty}">
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
		--background: #0a0a0a;
		--foreground: #e8e8e8;
		--primary: #a01e1e;
		--primary-foreground: #ffffff;
		--secondary: #101010;
		--secondary-foreground: #e8e8e8;
		--muted: #101010;
		--muted-foreground: #8a8a8a;
		--border: #232323;
		--input: #232323;
		--ring: #a23a38;
		min-height: calc(100vh - 4.75rem);
		background: #0a0a0a;
		color: #e8e8e8;
		font-family: var(--font-sans);
	}

	.problemset * {
		font-family: inherit;
	}

	.topic-row {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 8px;
	}

	.topic-pill {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		white-space: nowrap;
		border: 1px solid #3a2220;
		border-radius: 999px;
		background: #241414;
		padding: 6px 13px;
		color: #e0a79f;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.topic-pill:hover,
	.topic-pill.selected {
		border-color: #a01e1e;
		background: #3a1d1a;
	}

	.topic-count {
		color: #8a5c56;
	}

	.expand-button {
		border: 0;
		background: transparent;
		padding: 6px 8px;
		color: #a01e1e;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.module-rail {
		scroll-snap-type: x proximity;
		scrollbar-color: #232323 transparent;
	}

	.module-card {
		display: flex;
		min-width: 170px;
		min-height: 124px;
		flex: 0 0 170px;
		align-items: flex-start;
		gap: 12px;
		border: 1px solid #232323;
		border-radius: 8px;
		background: #101010;
		padding: 14px;
		transition: border-color 150ms;
	}

	.module-card:hover {
		border-color: #c0392b;
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
		color: #8a8a8a;
		font-size: 0.72rem;
		line-height: 1.45;
	}

	.rail-arrow {
		display: inline-flex;
		width: 34px;
		height: 34px;
		align-items: center;
		justify-content: center;
		border: 1px solid #232323;
		border-radius: 6px;
		background: #101010;
		color: #e8e8e8;
		cursor: pointer;
	}

	.rail-arrow:hover:not(:disabled) {
		border-color: #c0392b;
		color: #e0a79f;
	}

	.rail-arrow:disabled {
		cursor: not-allowed;
		opacity: 0.4;
	}

	.filter-button,
	.filter-select select {
		display: inline-flex;
		height: 38px;
		align-items: center;
		gap: 8px;
		border: 1px solid #232323;
		border-radius: 6px;
		background: #101010;
		padding: 0 12px;
		color: #e8e8e8;
		font: inherit;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.filter-select {
		position: relative;
		display: inline-flex;
		align-items: center;
	}

	.filter-button:hover,
	.filter-button.active {
		border-color: #c0392b;
		color: #a01e1e;
	}

	.company-filter-row {
		display: flex;
		overflow-x: auto;
		gap: 6px;
		margin: -6px 0 12px;
		padding: 4px 0 8px;
		scrollbar-width: thin;
	}

	.company-filter-row button {
		display: inline-flex;
		min-height: 30px;
		flex: 0 0 auto;
		align-items: center;
		gap: 6px;
		border: 1px solid #232323;
		border-radius: 999px;
		background: #101010;
		padding: 0 10px;
		color: #8a8a8a;
		font: inherit;
		font-size: 0.72rem;
		cursor: pointer;
	}

	.company-filter-row button:hover,
	.company-filter-row button.active {
		border-color: #a01e1e;
		background: #1a1a1a;
		color: #e8e8e8;
	}

	.search-field {
		position: relative;
		min-width: 180px;
		flex: 1;
	}

	.search-field input {
		width: 100%;
		height: 38px;
		border: 1px solid #232323;
		border-radius: 6px;
		background: #101010;
		padding: 0 12px 0 36px;
		color: #e8e8e8;
		font: inherit;
		font-size: 0.78rem;
	}

	.search-field input:focus {
		border-color: #c0392b;
		outline: 1px solid #c0392b;
	}

	.search-field :global(svg) {
		color: #8a8a8a;
	}

	.clear-button {
		display: inline-flex;
		height: 38px;
		align-items: center;
		gap: 7px;
		border: 0;
		background: transparent;
		padding: 0 8px;
		color: #8a8a8a;
		font: inherit;
		font-size: 0.78rem;
		cursor: pointer;
	}

	.clear-button:hover {
		color: #e8e8e8;
	}

	.problem-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.85rem;
	}

	.problem-table thead th {
		border-bottom: 1px solid #232323;
		padding: 8px 10px;
		color: #8a8a8a;
		font-size: 0.75rem;
		font-weight: normal;
		text-align: left;
	}

	.problem-table tbody tr {
		border-bottom: 1px solid #232323;
		cursor: pointer;
	}

	.problem-table tbody tr:hover {
		background: #101010;
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
		color: #e8e8e8;
		text-decoration: none;
	}

	.problem-link:hover {
		color: #a01e1e;
	}

	.module-tag,
	.potd-tag,
	.company-tag {
		display: inline-block;
		margin-left: 8px;
		border-radius: 4px;
		padding: 2px 7px;
		font-size: 0.68rem;
	}

	.module-tag {
		border: 1px solid #3a2220;
		background: #241414;
		color: #a01e1e;
	}

	.potd-tag {
		background: #d29922;
		color: #0a0a0a;
		font-size: 0.65rem;
		font-weight: bold;
	}

	.company-tag {
		border: 1px solid #352a1c;
		background: #1a1510;
		color: #c9a878;
	}

	.difficulty-badge {
		display: inline-block;
		border-radius: 12px;
		padding: 3px 10px;
		font-size: 0.75rem;
		font-weight: bold;
	}

	.difficulty-badge.Beginner {
		background: rgb(63 185 80 / 10%);
		color: #3fb950;
	}

	.difficulty-badge.Intermediate {
		background: rgb(210 153 34 / 10%);
		color: #d29922;
	}

	.difficulty-badge.Advanced {
		background: rgb(229 83 75 / 10%);
		color: #e5534b;
	}

	.empty-state {
		border: 1px solid #232323;
		border-radius: 6px;
		padding: 48px 12px;
		color: #8a8a8a;
		font-size: 0.85rem;
		text-align: center;
	}

	.pagination {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 14px;
		padding-top: 20px;
		color: #8a8a8a;
		font-size: 0.78rem;
	}

	.problemset-footer {
		margin-top: 36px;
		border-top: 1px solid #232323;
		padding-top: 16px;
	}

	.problemset-footer p {
		max-width: 720px;
		color: #555;
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

		.status-cell {
			float: left;
			width: 30px;
			padding-top: 5px !important;
		}
	}
</style>
