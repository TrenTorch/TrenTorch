<script lang="ts">
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import ModuleSection from '$components/ModuleSection.svelte';
	import PartCard from '$components/PartCard.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import PagePill from '$components/PagePill.svelte';
	import StatTile from '$components/StatTile.svelte';
	import Pagination from '$components/Pagination.svelte';
	import ProblemsetPotdBanner from '$components/ProblemsetPotdBanner.svelte';
	import { curriculum, getProgressStats, getPartProgress } from '$data/questions';
	import { getPartIcon } from '$data/part-icons';
	import type { PageProps } from './$types';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import SEO from '$components/SEO.svelte';
	import { buildBreadcrumbJsonLd } from '$processes/seo/build-breadcrumb-json-ld';
	import { withSiteName } from '$processes/seo/with-site-name';

	const stats = $derived(getProgressStats(solved.slugs));
	const partProgress = $derived(getPartProgress(solved.slugs));
	// A module is complete when every question in it is solved.
	const completedModules = $derived(
		partProgress.filter((part) => part.total > 0 && part.solved === part.total).length
	);

	// 14 Parts and 337+ questions is too much DOM to mount at once on first
	// load -- paginating the (possibly filtered) Parts list, not individual
	// questions, keeps each Part's tracks together instead of splitting one
	// mid-list across two pages.
	const PARTS_PER_PAGE = 4;
	// The default "pick a track" card grid paginates separately, at its own
	// page size -- a card is far cheaper to mount than a fully expanded
	// question list, but 15 tracks in one column is still a long scroll.
	let { data }: PageProps = $props();

	const CARDS_PER_PAGE = 6;

	let searchQuery = $state('');
	let solvedFilter = $state<'all' | 'solved' | 'unsolved'>('all');
	// '' is no topic chosen, which is what FilterBar means by it too.
	let topicFilter = $state('');

	// The track-picker grid is the default landing view (matches "pick a
	// track" from a fresh visit); touching any filter switches to a flat,
	// filtered question list instead, since "which track has a question
	// matching X" isn't a question the card grid can answer on its own.
	const isFiltering = $derived(
		searchQuery.trim() !== '' || solvedFilter !== 'all' || topicFilter !== ''
	);

	// Page number lives in the URL (?page=N), not just component state, so
	// a reload or a shared link lands back on the same page instead of
	// always snapping to page 1. Guarded by `browser`: reading
	// page.url.searchParams during the static-site prerendering pass (no
	// real query string exists then) throws, so the prerendered HTML
	// always starts from page 1 and the real page number is picked up
	// once this runs in an actual browser.
	let currentPage = $state(browser ? Number(page.url.searchParams.get('page')) || 1 : 1);

	const statuses = [
		{ value: 'all', label: 'All questions' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'unsolved', label: 'Unsolved' }
	];

	const allTopics = curriculum
		.flatMap((part) => part.tracks.flatMap((track) => track.questions.flatMap((q) => q.topics)))
		.filter((topic, i, arr) => arr.indexOf(topic) === i)
		.sort();

	const topicChoices = allTopics.map((topic) => ({
		value: topic,
		label: topic,
		count: curriculum.reduce(
			(sum, part) =>
				sum +
				part.tracks.reduce(
					(n, track) => n + track.questions.filter((q) => q.topics.includes(topic)).length,
					0
				),
			0
		)
	}));

	// Filters the same Part -> Track -> Question shape ModuleSection already
	// expects, so ModuleSection itself needs no changes: a Track with every
	// question filtered out drops entirely, and so does a Part left with no
	// Tracks, rather than rendering an empty section.
	const filteredCurriculum = $derived.by(() => {
		const query = searchQuery.trim().toLowerCase();
		return curriculum
			.map((part) => {
				const filterTracks = (tracks: typeof part.tracks) =>
					tracks
						.map((track) => ({
							...track,
							questions: track.questions.filter((question) => {
								if (query && !question.title.toLowerCase().includes(query)) return false;
								if (solvedFilter === 'solved' && !solved.isSolved(question.slug)) return false;
								if (solvedFilter === 'unsolved' && solved.isSolved(question.slug)) return false;
								if (topicFilter !== '' && !question.topics.includes(topicFilter)) return false;
								return true;
							})
						}))
						.filter((track) => track.questions.length > 0);
				return {
					...part,
					tracks: filterTracks(part.tracks),
					sections: part.sections
						?.map((section) => {
							const tracks = filterTracks(section.tracks);
							return { ...section, tracks, questions: tracks.flatMap((t) => t.questions) };
						})
						.filter((section) => section.tracks.length > 0)
				};
			})
			.filter((part) => part.tracks.length > 0);
	});

	const matchingQuestionCount = $derived(
		filteredCurriculum.reduce(
			(sum, part) => sum + part.tracks.reduce((n, track) => n + track.questions.length, 0),
			0
		)
	);

	const totalPages = $derived(
		isFiltering
			? Math.max(1, Math.ceil(filteredCurriculum.length / PARTS_PER_PAGE))
			: Math.max(1, Math.ceil(curriculum.length / CARDS_PER_PAGE))
	);

	const pagedCurriculum = $derived(
		filteredCurriculum.slice((currentPage - 1) * PARTS_PER_PAGE, currentPage * PARTS_PER_PAGE)
	);

	const pagedParts = $derived(
		curriculum.slice((currentPage - 1) * CARDS_PER_PAGE, currentPage * CARDS_PER_PAGE)
	);

	// Plain history.replaceState (not SvelteKit's goto/pushState/replaceState)
	// on purpose: this only needs the URL bar to reflect the current page
	// for reload/share, not a real SvelteKit navigation with its
	// invalidation lifecycle -- the page itself never actually changes
	// route, only which slice of already-loaded data is shown.
	function goToPage(n: number) {
		currentPage = Math.min(Math.max(1, n), totalPages);
		const url = new URL(window.location.href);
		url.searchParams.set('page', String(currentPage));
		history.replaceState(history.state, '', url);
	}

	// Any filter/search edit changes what "page 2" even means, so it jumps
	// back to page 1 -- guarded to skip the very first run (mount), which
	// would otherwise stomp the page number a reload/shared link came in
	// with before the user has touched a filter at all.
	let mounted = false;
	$effect(() => {
		void searchQuery;
		void solvedFilter;
		void topicFilter;
		if (mounted) goToPage(1);
		mounted = true;
	});
</script>

<SEO
	title={withSiteName('Machine learning practice questions')}
	description={`Browse ${stats.total} free machine learning practice questions across ${curriculum.length} sections, from math foundations to transformers, inference, and production ML. Run the tests in your browser.`}
	path="/questions"
	jsonLd={buildBreadcrumbJsonLd([
		{ name: 'Home', path: '/' },
		{ name: 'Module', path: '/questions' }
	])}
/>

<div class="px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px] space-y-8">
		<header class="dot-texture">
			<PagePill slug="questions/" />
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">Modules</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				From Python basics to production ML, one module at a time.
			</p>
			<div class="mt-6 grid max-w-md grid-cols-2 gap-3 sm:gap-4">
				<StatTile
					label="Modules"
					value={curriculum.length}
					tone="positive"
					progress={{ done: completedModules, total: curriculum.length }}
					progressLabel="complete"
				/>
				<StatTile
					label="Questions"
					value={stats.total}
					tone="positive"
					progress={{ done: stats.completed, total: stats.total }}
				/>
			</div>
		</header>

		<ProblemsetPotdBanner summaries={data.potdSummaries} />

		<FilterBar
			bind:query={searchQuery}
			bind:topic={topicFilter}
			bind:status={solvedFilter}
			topics={topicChoices}
			difficulties={[]}
			{statuses}
			resultCount={matchingQuestionCount}
			total={stats.total}
			placeholder="Search questions..."
			noun="question"
		/>

		{#if isFiltering}
			{#if filteredCurriculum.length === 0}
				<p class="py-12 text-center text-sm text-muted-foreground">
					No questions match {searchQuery ? `"${searchQuery}"` : 'these filters'}.
				</p>
			{:else}
				<div class="space-y-3">
					{#each pagedCurriculum as part (part.id)}
						<ModuleSection {part} forceOpen />
					{/each}
				</div>

				<Pagination {currentPage} {totalPages} onPageChange={goToPage} />
			{/if}
		{:else}
			<div class="grid gap-3">
				{#each pagedParts as part (part.id)}
					{@const progress = partProgress.find((p) => p.id === part.id)}
					<PartCard
						id={part.id}
						title={part.title}
						icon={getPartIcon(part.id)}
						questionCount={part.tracks.reduce((sum, t) => sum + t.questions.length, 0)}
						solved={progress?.solved ?? 0}
						total={progress?.total ?? 0}
					/>
				{/each}
			</div>

			<Pagination {currentPage} {totalPages} onPageChange={goToPage} />
		{/if}
	</div>
</div>
