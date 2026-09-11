<script lang="ts">
	import { page } from '$app/state';
	import ProfileCard from '$lib/components/ProfileCard.svelte';
	import ProgressSummary from '$lib/components/ProgressSummary.svelte';
	import ModuleSection from '$lib/components/ModuleSection.svelte';
	import QuestionFilters from '$lib/components/QuestionFilters.svelte';
	import Pagination from '$lib/components/Pagination.svelte';
	import { curriculum, getProgressStats } from '$lib/data/questions';
	import { solved } from '$lib/stores/solved.svelte';

	const stats = getProgressStats();

	// 14 Parts and 337 questions is too much DOM to mount at once on first
	// load -- paginating the (possibly filtered) Parts list, not individual
	// questions, keeps each Part's tracks together instead of splitting one
	// mid-list across two pages.
	const PARTS_PER_PAGE = 4;

	let searchQuery = $state('');
	let solvedFilter = $state<'all' | 'solved' | 'unsolved'>('all');
	let topicFilter = $state('all');

	// Page number lives in the URL (?page=N), not just component state, so
	// a reload or a shared link lands back on the same page instead of
	// always snapping to page 1.
	let currentPage = $state(Number(page.url.searchParams.get('page')) || 1);

	const allTopics = curriculum
		.flatMap((part) => part.tracks.flatMap((track) => track.questions.flatMap((q) => q.topics)))
		.filter((topic, i, arr) => arr.indexOf(topic) === i)
		.sort();

	// Filters the same Part -> Track -> Question shape ModuleSection already
	// expects, so ModuleSection itself needs no changes: a Track with every
	// question filtered out drops entirely, and so does a Part left with no
	// Tracks, rather than rendering an empty section.
	const filteredCurriculum = $derived.by(() => {
		const query = searchQuery.trim().toLowerCase();
		return curriculum
			.map((part) => ({
				...part,
				tracks: part.tracks
					.map((track) => ({
						...track,
						questions: track.questions.filter((question) => {
							if (query && !question.title.toLowerCase().includes(query)) return false;
							if (solvedFilter === 'solved' && !solved.isSolved(question.slug)) return false;
							if (solvedFilter === 'unsolved' && solved.isSolved(question.slug)) return false;
							if (topicFilter !== 'all' && !question.topics.includes(topicFilter)) return false;
							return true;
						})
					}))
					.filter((track) => track.questions.length > 0)
			}))
			.filter((part) => part.tracks.length > 0);
	});

	const totalPages = $derived(Math.max(1, Math.ceil(filteredCurriculum.length / PARTS_PER_PAGE)));

	const pagedCurriculum = $derived(
		filteredCurriculum.slice((currentPage - 1) * PARTS_PER_PAGE, currentPage * PARTS_PER_PAGE)
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

<svelte:head>
	<title>Questions</title>
	<meta name="description" content="Every TrenTorch curriculum question, in one place." />
</svelte:head>

<div class="container flex flex-col gap-8 px-4 py-12 md:flex-row md:px-6">
	<aside
		class="w-full shrink-0 space-y-6 rounded-md border border-border p-4 md:sticky md:top-20 md:h-fit md:w-64"
	>
		<ProfileCard name="Student" />
		<ProgressSummary completed={stats.completed} total={stats.total} />
	</aside>

	<div class="flex-1 space-y-6">
		<QuestionFilters bind:searchQuery bind:solvedFilter bind:topicFilter topics={allTopics} />

		{#if filteredCurriculum.length === 0}
			<p class="py-12 text-center text-sm text-muted-foreground">
				No questions match {searchQuery ? `"${searchQuery}"` : 'these filters'}.
			</p>
		{:else}
			<div class="space-y-3">
				{#each pagedCurriculum as part (part.id)}
					<ModuleSection {part} />
				{/each}
			</div>

			<Pagination {currentPage} {totalPages} onPageChange={goToPage} />
		{/if}
	</div>
</div>
