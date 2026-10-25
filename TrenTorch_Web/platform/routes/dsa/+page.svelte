<script lang="ts">
	import { resolve } from '$app/paths';
	import FilterSelect from '$components/FilterSelect.svelte';
	import { SvelteSet } from 'svelte/reactivity';
	import {
		ArrowRight,
		Check,
		CheckCircle2,
		ChevronDown,
		Gauge,
		RotateCcw,
		Search
	} from '@lucide/svelte';
	import { dsaQuestions, dsaSteps } from '$data/dsa-sheet';
	import {
		countSolved,
		filterSheet,
		getSheetStatus,
		nextUnsolved,
		type SheetFilters,
		type SheetStatus
	} from '$processes/dsa-sheet/filter-sheet';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';

	const difficulties = ['Beginner', 'Intermediate', 'Advanced'];
	const statuses: { value: SheetStatus; label: string }[] = [
		{ value: 'all', label: 'All statuses' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'attempted', label: 'Attempted' },
		{ value: 'unsolved', label: 'Unsolved' }
	];

	let searchQuery = $state('');
	let selectedDifficulty = $state('');
	let selectedStatus = $state<SheetStatus>('all');
	// Steps and topics the visitor opened. Everything starts closed.
	const openSteps = new SvelteSet<string>();
	const openTopics = new SvelteSet<string>();

	const filters = $derived<SheetFilters>({
		query: searchQuery,
		difficulty: selectedDifficulty,
		status: selectedStatus
	});
	const visibleSteps = $derived(filterSheet(dsaSteps, filters, solved.slugs, attempted.slugs));
	const visibleCount = $derived(
		visibleSteps.reduce(
			(sum, step) => sum + step.topics.reduce((n, topic) => n + topic.questions.length, 0),
			0
		)
	);
	const filtering = $derived(
		Boolean(searchQuery.trim() || selectedDifficulty || selectedStatus !== 'all')
	);
	const overall = $derived(countSolved(dsaQuestions, solved.slugs));
	const next = $derived(nextUnsolved(dsaQuestions, solved.slugs));

	function stepProgress(stepId: string) {
		const step = dsaSteps.find((s) => s.id === stepId);
		const questions = step?.topics.flatMap((topic) => topic.questions) ?? [];
		return countSolved(questions, solved.slugs);
	}

	function toggle(set: SvelteSet<string>, id: string) {
		if (set.has(id)) set.delete(id);
		else set.add(id);
	}

	function resetFilters() {
		searchQuery = '';
		selectedDifficulty = '';
		selectedStatus = 'all';
	}
</script>

<svelte:head>
	<title>DSA Sheet - TrenTorch</title>
	<meta
		name="description"
		content="Free data structures and algorithms practice, with high-quality questions."
	/>
</svelte:head>

<main class="sheet min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px]">
		<h1 class="mb-1 font-mono text-[1.4rem] font-bold">DSA Sheet</h1>
		<p class="mb-6 max-w-[680px] text-sm text-muted-foreground">
			Free practice for data structures and algorithms, with high-quality questions.
		</p>

		<div class="progress-card mb-7">
			<div class="min-w-0 flex-1">
				<p class="mb-1 font-mono text-xs tracking-wider text-muted-foreground uppercase">
					Your progress
				</p>
				<p class="font-mono text-lg font-semibold">
					{overall.solved} <span class="text-muted-foreground">of {overall.total} solved</span>
				</p>
				<div
					class="bar mt-2"
					role="progressbar"
					aria-label="Questions solved"
					aria-valuemin={0}
					aria-valuemax={overall.total}
					aria-valuenow={overall.solved}
				>
					<span style="width: {overall.total ? (overall.solved / overall.total) * 100 : 0}%"></span>
				</div>
			</div>
			{#if next}
				<a href={resolve('/ide/[id]', { id: next.id })} class="continue-button press">
					{overall.solved === 0 ? 'Start' : 'Continue'}: {next.title}
					<ArrowRight class="size-4 shrink-0" aria-hidden="true" />
				</a>
			{:else}
				<p class="font-mono text-sm text-[#3fb950]">All done. Nice work.</p>
			{/if}
		</div>

		<div class="mb-4 flex flex-wrap items-center gap-2">
			<label class="search-field">
				<span class="sr-only">Search questions</span>
				<Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2" />
				<input bind:value={searchQuery} type="search" placeholder="Search questions or tags..." />
			</label>

			<FilterSelect
				bind:value={selectedStatus}
				label="Filter by status"
				icon={CheckCircle2}
				options={statuses}
			/>

			<FilterSelect
				bind:value={selectedDifficulty}
				label="Filter by difficulty"
				icon={Gauge}
				options={[
					{ value: '', label: 'All difficulties' },
					...difficulties.map((d) => ({ value: d, label: d }))
				]}
			/>

			{#if filtering}
				<button type="button" class="clear-button" onclick={resetFilters}>
					<RotateCcw class="size-3.5" />
					Clear
				</button>
			{/if}
		</div>

		<p class="mb-3 text-xs text-muted-foreground" aria-live="polite">
			{visibleCount}
			{visibleCount === 1 ? 'question' : 'questions'}
		</p>

		{#if visibleSteps.length === 0}
			<p class="empty-state">No questions match these filters.</p>
		{:else}
			<div class="flex flex-col gap-4">
				{#each visibleSteps as step (step.id)}
					{@const progress = stepProgress(step.id)}
					{@const open = filtering || openSteps.has(step.id)}
					<section class="step-card" aria-labelledby="step-{step.id}">
						<button
							type="button"
							class="step-head"
							aria-expanded={open}
							aria-controls="step-body-{step.id}"
							onclick={() => toggle(openSteps, step.id)}
						>
							<span class="min-w-0 flex-1 text-left">
								<span id="step-{step.id}" class="step-title">{step.title}</span>
							</span>
							<span
								class="bar step-bar"
								role="progressbar"
								aria-label="{step.title} progress"
								aria-valuemin={0}
								aria-valuemax={progress.total}
								aria-valuenow={progress.solved}
							>
								<span
									style="width: {progress.total ? (progress.solved / progress.total) * 100 : 0}%"
								></span>
							</span>
							<ChevronDown
								class="chevron size-4 shrink-0 {open ? 'open' : ''}"
								aria-hidden="true"
							/>
						</button>

						{#if open}
							<div id="step-body-{step.id}" class="step-body">
								{#each step.topics as topic (topic.id)}
									{@const topicKey = `${step.id}/${topic.id}`}
									{@const topicOpen = filtering || openTopics.has(topicKey)}
									{@const topicProgress = countSolved(topic.questions, solved.slugs)}
									<div class="topic">
										<button
											type="button"
											class="topic-head"
											aria-expanded={topicOpen}
											aria-controls="topic-body-{topicKey}"
											onclick={() => toggle(openTopics, topicKey)}
										>
											<h2 class="topic-title">{topic.title}</h2>
											<span class="topic-count">
												{topicProgress.solved} of {topicProgress.total} solved
											</span>
											<ChevronDown
												class="chevron size-4 shrink-0 {topicOpen ? 'open' : ''}"
												aria-hidden="true"
											/>
										</button>
										{#if topicOpen}
											<div id="topic-body-{topicKey}" class="overflow-x-auto">
												<table class="problem-table">
													<colgroup>
														<col class="col-status" />
														<col class="col-num" />
														<col />
														<col class="col-difficulty" />
													</colgroup>
													<thead>
														<tr>
															<th aria-label="Status"></th>
															<th>#</th>
															<th>Question</th>
															<th>Difficulty</th>
														</tr>
													</thead>
													<tbody>
														{#each topic.questions as question, index (question.id)}
															{@const status = getSheetStatus(
																question.id,
																solved.slugs,
																attempted.slugs
															)}
															<tr>
																<td class="status-cell">
																	{#if status === 'solved'}
																		<Check
																			class="mx-auto size-4 text-[#3fb950]"
																			aria-label="Solved"
																		/>
																	{:else if status === 'attempted'}
																		<span role="img" aria-label="Attempted" class="text-[#d29922]"
																			>●</span
																		>
																	{/if}
																</td>
																<td class="num-cell">{index + 1}</td>
																<td>
																	<a
																		href={resolve('/ide/[id]', { id: question.id })}
																		class="problem-link"
																	>
																		{question.title}
																	</a>
																</td>
																<td>
																	<span class="difficulty-badge {question.difficulty}">
																		{question.difficulty}
																	</span>
																</td>
															</tr>
														{/each}
													</tbody>
												</table>
											</div>
										{/if}
									</div>
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
	.progress-card {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 16px 24px;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--secondary);
		padding: 18px;
	}

	.bar {
		display: block;
		height: 6px;
		overflow: hidden;
		border-radius: 3px;
		background: var(--border);
	}

	.bar span {
		display: block;
		height: 100%;
		border-radius: 3px;
		background: #3fb950;
		transition: width 200ms;
	}

	.continue-button {
		display: inline-flex;
		max-width: 100%;
		align-items: center;
		gap: 8px;
		border-radius: 6px;
		background: var(--primary);
		padding: 10px 16px;
		color: var(--primary-foreground);
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 0.8rem;
		text-decoration: none;
	}

	.continue-button:hover {
		opacity: 0.9;
	}

	/* Three levels, told apart by surface and indent: a step is a raised card,
	   a topic is an inset darker card, a question is plain text. */
	.sheet {
		font-variant-numeric: tabular-nums;
		--level-step: var(--secondary);
		--level-topic: color-mix(in oklab, var(--background) 82%, black);
	}

	:global(html:not(.dark)) .sheet {
		--level-step: var(--secondary);
		--level-topic: color-mix(in oklab, var(--background) 94%, var(--foreground));
	}

	.step-card {
		border: 1px solid var(--border);
		border-radius: 12px;
		background: var(--level-step);
		overflow: hidden;
		transition: border-color 150ms;
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
		color: var(--foreground);
	}

	.step-bar {
		width: 120px;
		flex: 0 0 120px;
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
		gap: 10px;
		padding: 2px 14px 16px 18px;
	}

	.topic {
		overflow: hidden;
		border: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		border-radius: 10px;
		background: var(--level-topic);
	}

	.topic-head {
		display: flex;
		width: 100%;
		align-items: center;
		gap: 12px;
		border: 0;
		background: transparent;
		padding: 12px 14px;
		color: var(--foreground);
		font: inherit;
		text-align: left;
		cursor: pointer;
	}

	.topic-head:hover {
		background: color-mix(in oklab, var(--foreground) 6%, transparent);
	}

	.topic-title {
		display: flex;
		min-width: 0;
		flex: 1;
		align-items: center;
		gap: 10px;
		color: var(--foreground);
		font-family: var(--font-sans, system-ui, sans-serif);
		font-size: 0.9375rem;
		font-weight: 600;
	}

	.topic-count {
		border-radius: 6px;
		background: color-mix(in oklab, var(--foreground) 8%, transparent);
		padding: 2px 9px;
		color: var(--muted-foreground);
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 0.7rem;
		white-space: nowrap;
	}

	.topic .problem-table {
		margin: 0 0 6px;
	}

	.num-cell {
		color: var(--muted-foreground);
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 0.75rem;
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
		table-layout: fixed;
		border-collapse: collapse;
		font-size: 0.85rem;
	}

	.problem-table thead th {
		border-top: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		border-bottom: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		padding: 7px 14px;
		color: var(--muted-foreground);
		font-size: 0.7rem;
		font-weight: 500;
		letter-spacing: 0.06em;
		text-align: left;
		text-transform: uppercase;
	}

	.problem-table tbody tr {
		border-bottom: 1px solid color-mix(in oklab, var(--foreground) 6%, transparent);
	}

	.problem-table tbody tr:hover {
		background: color-mix(in oklab, var(--foreground) 5%, transparent);
	}

	.problem-table tbody tr:last-child {
		border-bottom: 0;
	}

	.problem-table tbody td {
		padding: 11px 10px;
		vertical-align: middle;
	}

	.col-status {
		width: 40px;
	}

	.col-num {
		width: 44px;
	}

	.col-difficulty {
		width: 130px;
	}

	.status-cell {
		text-align: center;
	}

	.problem-link {
		color: color-mix(in oklab, var(--foreground) 88%, transparent);
		text-decoration: none;
	}

	.problem-link:hover {
		text-decoration: underline;
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
		color: color-mix(in srgb, #3fb950 70%, var(--foreground));
	}

	.difficulty-badge.Intermediate {
		background: rgb(210 153 34 / 10%);
		color: color-mix(in srgb, #d29922 70%, var(--foreground));
	}

	.difficulty-badge.Advanced {
		background: rgb(229 83 75 / 10%);
		color: color-mix(in srgb, #e5534b 75%, var(--foreground));
	}

	.empty-state {
		border: 1px solid var(--border);
		border-radius: 6px;
		padding: 48px 12px;
		color: var(--muted-foreground);
		font-size: 0.85rem;
		text-align: center;
	}

	@media (max-width: 640px) {
		.step-bar {
			display: none;
		}

		.num-cell {
			display: none !important;
		}

		.step-body {
			padding: 2px 8px 12px 10px;
		}

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
