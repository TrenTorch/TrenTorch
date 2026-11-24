<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { SvelteSet } from 'svelte/reactivity';
	import { ArrowRight, BookOpen, Check, ChevronDown, RotateCcw } from '@lucide/svelte';
	import DsaSummit from '$components/DsaSummit.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import ModuleAccordion, { startPage } from '$components/ModuleAccordion.svelte';
	import PagePill from '$components/PagePill.svelte';
	import SEO from '$components/SEO.svelte';
	import SoftwareArt from '$components/SoftwareArt.svelte';
	import StatTile from '$components/StatTile.svelte';
	import { dsaQuestions, dsaSteps } from '$data/dsa-sheet';
	import { softwareSilos } from '$data/software-silos';
	import { Layers } from '@lucide/svelte';
	import {
		countSolved,
		filterSheet,
		getSheetStatus,
		type SheetFilters,
		type SheetStatus
	} from '$processes/dsa-sheet/filter-sheet';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { dsaResume, RESUME_LABEL } from '$processes/dsa-sheet/dsa-resume';
	import { recent } from '$processes/progress-tracking/recent.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { buildBreadcrumbJsonLd } from '$processes/seo/build-breadcrumb-json-ld';
	import { withSiteName } from '$processes/seo/with-site-name';

	const difficulties = ['Beginner', 'Intermediate', 'Advanced'];
	const statuses: { value: SheetStatus; label: string }[] = [
		{ value: 'all', label: 'All Statuses' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'attempted', label: 'Attempted' },
		{ value: 'unsolved', label: 'Unsolved' }
	];

	let searchQuery = $state(browser ? (page.url.searchParams.get('q') ?? '') : '');
	let selectedDifficulty = $state('');
	let selectedStatus = $state<SheetStatus>('all');
	// Topics the visitor opened inside a step; steps themselves are rows of the accordion.
	const openTopics = new SvelteSet<string>();

	const filters = $derived<SheetFilters>({
		query: searchQuery,
		difficulty: selectedDifficulty,
		status: selectedStatus
	});
	const visibleSteps = $derived(filterSheet(dsaSteps, filters, solved.slugs, attempted.slugs));
	const questionsOf = (step: (typeof dsaSteps)[number]) => step.topics.flatMap((t) => t.questions);
	const visibleCount = $derived(
		visibleSteps.reduce((sum, step) => sum + questionsOf(step).length, 0)
	);
	const filtering = $derived(
		Boolean(searchQuery.trim() || selectedDifficulty || selectedStatus !== 'all')
	);
	// Green on the pill: the question they left half-done, else the first one for a newcomer, else the next
	// unsolved one (the same rule as the home page's DSA card).
	const green = $derived.by(() => {
		const next = dsaResume(dsaQuestions, solved.slugs, recent.get('dsa'));
		return next
			? { label: RESUME_LABEL[next.kind], href: resolve('/ide/[id]', { id: next.question.id }) }
			: null;
	});
	const overall = $derived(countSolved(dsaQuestions, solved.slugs));
	// A progression is complete when every question in it is solved.
	const completedSteps = $derived(
		dsaSteps.filter((step) => {
			const { solved: done, total } = countSolved(questionsOf(step), solved.slugs);
			return total > 0 && done === total;
		}).length
	);

	// The silos, each with the steps of it that survive the filters.
	const silos = $derived(
		softwareSilos
			.map((silo) => ({
				...silo,
				visible: silo.steps
					.map((id) => visibleSteps.find((s) => s.id === id))
					.filter((s): s is (typeof dsaSteps)[number] => Boolean(s))
			}))
			.filter((silo) => silo.visible.length > 0)
	);
	const rows = $derived(
		silos.map((silo) => {
			const questions = silo.visible.flatMap(questionsOf);
			return {
				id: silo.id,
				title: silo.title,
				icon: Layers,
				count: questions.length,
				solved: countSolved(questions, solved.slugs).solved
			};
		})
	);

	// A shared ?step= link names a step; its silo is the row to open.
	const stepLink = browser ? page.url.searchParams.get('step') : null;
	const initialOpen = stepLink
		? (softwareSilos.find((silo) => silo.steps.includes(stepLink))?.id ?? null)
		: null;
	if (stepLink) openTopics.add(stepLink);
	let currentPage = $state(startPage(softwareSilos, initialOpen));
	// A filter edit changes what "page 2" means; the first run keeps a shared link's page.
	let mounted = false;
	$effect(() => {
		void searchQuery;
		void selectedDifficulty;
		void selectedStatus;
		if (mounted) currentPage = 1;
		mounted = true;
	});

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

<SEO
	title={withSiteName('Software Engineering')}
	description="Free software engineering practice: data structures and algorithms in four silos, with high-quality questions and theory."
	path="/modules/software"
	jsonLd={buildBreadcrumbJsonLd([
		{ name: 'Home', path: '/' },
		{ name: 'Modules', path: '/modules' },
		{ name: 'Software Engineering', path: '/modules/software' }
	])}
/>

<main class="min-h-screen px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px] space-y-8">
		<header class="dot-texture">
			<PagePill
				slug="modules/software/"
				area="dsa"
				resume={green}
				up={{ label: 'all domains', href: resolve('/modules') }}
			/>
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">
				Software Engineering
			</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				From data structures and algorithms, towards the craft of shipping real software
			</p>
			<div class="mt-6 grid max-w-md grid-cols-2 gap-3 sm:gap-4">
				<StatTile
					label="Questions"
					value={overall.total}
					tone="positive"
					progress={{ done: overall.solved, total: overall.total }}
				/>
				<StatTile
					label="Progressions"
					value={dsaSteps.length}
					tone="positive"
					progress={{ done: completedSteps, total: dsaSteps.length }}
					progressLabel="complete"
				/>
			</div>
		</header>

		<FilterBar
			bind:query={searchQuery}
			bind:difficulty={selectedDifficulty}
			bind:status={selectedStatus}
			{difficulties}
			{statuses}
			resultCount={visibleCount}
			total={dsaQuestions.length}
			placeholder="Search questions or tags..."
			noun="question"
		/>

		{#if rows.length === 0}
			<p class="py-12 text-center text-sm text-muted-foreground">
				No questions match these filters.
				<button
					type="button"
					class="ml-2 inline-flex items-center gap-1 underline"
					onclick={resetFilters}
				>
					<RotateCcw class="size-3.5" aria-hidden="true" />
					Clear filters
				</button>
			</p>
		{:else}
			<!-- keyed on the filter so each filtered view starts from its own open state -->
			{#key filtering}
				<ModuleAccordion
					items={rows}
					forceOpen={filtering}
					{initialOpen}
					hue="#a597d1"
					bind:page={currentPage}
				>
					{#snippet art(item)}<SoftwareArt id={item.id} />{/snippet}
					{#snippet children(item)}
						{@const silo = silos.find((x) => x.id === item.id)}
						<div class="flex flex-col gap-2 p-3">
							{#each silo?.visible ?? [] as step (step.id)}
								{@const stepOpen = filtering || openTopics.has(step.id)}
								{@const stepProgress = countSolved(questionsOf(step), solved.slugs)}
								<div class="topic">
									<button
										type="button"
										class="topic-head"
										aria-expanded={stepOpen}
										aria-controls="step-body-{step.id}"
										onclick={() => toggle(openTopics, step.id)}
									>
										<h3 class="min-w-0 flex-1 text-left font-semibold">{step.title}</h3>
										<span class="muted">{stepProgress.solved} of {stepProgress.total} solved</span>
										<ChevronDown
											class="size-4 shrink-0 text-muted-foreground transition-transform {stepOpen
												? ''
												: '-rotate-90'}"
											aria-hidden="true"
										/>
									</button>
									{#if stepOpen}
										<div id="step-body-{step.id}" class="topic-body flex flex-col gap-2 p-2">
											{#if step.hasTheory}
												<a
													class="row"
													href={resolve('/modules/software/theory/[step]', { step: step.id })}
												>
													<BookOpen class="size-4 shrink-0" aria-hidden="true" />
													<span class="min-w-0 flex-1 font-semibold">{step.title} Theory</span>
													<span class="muted">Read the theory</span>
													<ArrowRight class="size-4 shrink-0" aria-hidden="true" />
												</a>
											{/if}
											{#each step.topics as topic (topic.id)}
												{@const topicKey = `${step.id}/${topic.id}`}
												{@const topicOpen = filtering || openTopics.has(topicKey)}
												{@const progress = countSolved(topic.questions, solved.slugs)}
												<div class="topic">
													<button
														type="button"
														class="topic-head"
														aria-expanded={topicOpen}
														aria-controls="topic-body-{topicKey}"
														onclick={() => toggle(openTopics, topicKey)}
													>
														<h4 class="min-w-0 flex-1 text-left font-semibold">{topic.title}</h4>
														<span class="muted">{progress.solved} of {progress.total} solved</span>
														<ChevronDown
															class="size-4 shrink-0 text-muted-foreground transition-transform {topicOpen
																? ''
																: '-rotate-90'}"
															aria-hidden="true"
														/>
													</button>
													{#if topicOpen}
														<ol id="topic-body-{topicKey}" class="topic-body">
															{#each topic.questions as question, index (question.id)}
																{@const status = getSheetStatus(
																	question.id,
																	solved.slugs,
																	attempted.slugs
																)}
																<li>
																	<a
																		href={resolve('/ide/[id]', { id: question.id })}
																		class="question"
																		onclick={() => recent.note('dsa', question.id)}
																	>
																		<span class="w-5 text-center">
																			{#if status === 'solved'}
																				<Check
																					class="mx-auto size-4 text-[#3fb950]"
																					aria-label="Solved"
																				/>
																			{:else if status === 'attempted'}
																				<span
																					role="img"
																					aria-label="Attempted"
																					class="text-[#d29922]">●</span
																				>
																			{/if}
																		</span>
																		<span class="muted w-6">{index + 1}</span>
																		<span class="min-w-0 flex-1">{question.title}</span>
																		<span class="difficulty-badge {question.difficulty}">
																			{question.difficulty}
																		</span>
																	</a>
																</li>
															{/each}
														</ol>
													{/if}
												</div>
											{/each}
										</div>
									{/if}
								</div>
							{/each}
						</div>
					{/snippet}
				</ModuleAccordion>
			{/key}
		{/if}
	</div>

	<div class="mx-auto mt-12 mb-2 w-full max-w-[1180px]">
		<DsaSummit />
	</div>
</main>

<style>
	.row,
	.topic {
		border: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		border-radius: 10px;
		background: color-mix(in oklab, var(--foreground) 3%, var(--background));
	}
	.row {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 11px 16px;
		color: var(--foreground);
	}
	.row:hover {
		background: color-mix(in oklab, var(--foreground) 7%, var(--background));
	}
	.topic-head {
		display: flex;
		width: 100%;
		align-items: center;
		gap: 12px;
		padding: 11px 16px;
		color: var(--foreground);
	}
	.topic-body {
		border-top: 1px solid color-mix(in oklab, var(--foreground) 9%, transparent);
		padding: 4px 8px 8px;
	}
	.question {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 8px;
		border-radius: 8px;
		color: var(--foreground);
	}
	.question:hover {
		background: color-mix(in oklab, var(--foreground) 6%, transparent);
	}
	.muted {
		font-size: 0.8rem;
		color: var(--muted-foreground);
		white-space: nowrap;
	}
	.difficulty-badge {
		font-size: 0.75rem;
		font-weight: 600;
		padding: 2px 8px;
		border-radius: 999px;
		border: 1px solid currentColor;
	}
	.difficulty-badge.Beginner {
		color: #3fb950;
	}
	.difficulty-badge.Intermediate {
		color: #d29922;
	}
	.difficulty-badge.Advanced {
		color: #f85149;
	}
</style>
