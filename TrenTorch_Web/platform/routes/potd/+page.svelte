<script lang="ts">
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { CalendarCheck } from '@lucide/svelte';
	import ProfileCard from '$components/ProfileCard.svelte';
	import ProgressSummary from '$components/ProgressSummary.svelte';
	import PotdSection from '$components/PotdSection.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import PotdHero from '$components/PotdHero.svelte';
	import Pagination from '$components/Pagination.svelte';
	import { getProgressStats } from '$data/questions';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { getTodaysPotdPart, getPastPotdPart } from '$processes/potd/get-potd-part';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const stats = $derived(getProgressStats(solved.slugs));

	// Real "today" only exists client-side on a fully prerendered static
	// build -- same guard used everywhere else in this codebase that reads
	// the current date/URL (see e.g. the Questions page's own ?page= read).
	const todayPart = $derived(browser ? getTodaysPotdPart(data.potdSummaries) : []);
	const pastPotdCurriculum = $derived(browser ? getPastPotdPart(data.potdSummaries) : []);

	const PARTS_PER_PAGE = 4;

	let searchQuery = $state('');
	let solvedFilter = $state<'all' | 'solved' | 'unsolved'>('all');
	// '' is no topic chosen, which is what FilterBar means by it too.
	let topicFilter = $state('');
	let currentPage = $state(browser ? Number(page.url.searchParams.get('page')) || 1 : 1);

	// Filters only ever act on the Past Problems list -- Today's Problem is
	// a single, always-relevant entry, the same way the hero card above
	// never gets filtered away either.
	const allTopics = $derived(
		[...todayPart, ...pastPotdCurriculum]
			.flatMap((part) => part.tracks.flatMap((track) => track.questions.flatMap((q) => q.topics)))
			.filter((topic, i, arr) => arr.indexOf(topic) === i)
			.sort()
	);

	const statuses = [
		{ value: 'all', label: 'All problems' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'unsolved', label: 'Unsolved' }
	];
	const pastQuestions = $derived(
		pastPotdCurriculum.flatMap((part) => part.tracks.flatMap((track) => track.questions))
	);
	const topicChoices = $derived(
		allTopics.map((topic) => ({
			value: topic,
			label: topic,
			count: pastQuestions.filter((question) => question.topics.includes(topic)).length
		}))
	);

	const filteredCurriculum = $derived.by(() => {
		const query = searchQuery.trim().toLowerCase();
		return pastPotdCurriculum
			.map((part) => ({
				...part,
				tracks: part.tracks
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
					.filter((track) => track.questions.length > 0)
			}))
			.filter((part) => part.tracks.length > 0);
	});

	const matchingCount = $derived(
		filteredCurriculum.reduce(
			(sum, part) => sum + part.tracks.reduce((n, track) => n + track.questions.length, 0),
			0
		)
	);

	const totalPages = $derived(Math.max(1, Math.ceil(filteredCurriculum.length / PARTS_PER_PAGE)));

	const pagedCurriculum = $derived(
		filteredCurriculum.slice((currentPage - 1) * PARTS_PER_PAGE, currentPage * PARTS_PER_PAGE)
	);

	function goToPage(n: number) {
		currentPage = Math.min(Math.max(1, n), totalPages);
		const url = new URL(window.location.href);
		url.searchParams.set('page', String(currentPage));
		history.replaceState(history.state, '', url);
	}

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
	<title>Problem of the Day - TrenTorch</title>
	<meta name="description" content="A new TrenTorch curriculum question, featured every day." />
</svelte:head>

<div class="container flex flex-col gap-8 px-4 py-12 md:flex-row md:px-6">
	<aside
		class="w-full shrink-0 space-y-6 rounded-md border border-border p-4 md:sticky md:top-20 md:h-fit md:w-64"
	>
		<ProfileCard name="Student" />
		<ProgressSummary completed={stats.completed} total={stats.total} />
	</aside>

	<div class="min-w-0 flex-1 space-y-6">
		<header class="dot-texture">
			<p
				class="mb-3 flex items-center gap-2 font-mono text-xs tracking-wider text-muted-foreground uppercase"
			>
				<CalendarCheck class="size-3.5 text-primary" aria-hidden="true" />
				Problem of the Day
			</p>
			<h1 class="mb-2 font-mono text-3xl font-bold tracking-tight sm:text-4xl">
				One problem, Every day!
			</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				Solve today's to earn rating. Earlier ones wait below.
			</p>
		</header>

		{#each todayPart as part (part.id)}
			<PotdHero {part} />
		{:else}
			<p class="text-sm text-muted-foreground">
				No problem is featured today yet, check back soon.
			</p>
		{/each}

		{#if pastQuestions.length > 0}
			<FilterBar
				bind:query={searchQuery}
				bind:topic={topicFilter}
				bind:status={solvedFilter}
				topics={topicChoices}
				difficulties={[]}
				{statuses}
				resultCount={matchingCount}
				total={pastQuestions.length}
				placeholder="Search past problems..."
				noun="problem"
			/>
		{/if}

		{#if filteredCurriculum.length === 0}
			<p class="py-12 text-center text-sm text-muted-foreground">
				{#if pastPotdCurriculum.length === 0}
					No past Problems of the Day yet, check back soon.
				{:else}
					No problems match {searchQuery ? `"${searchQuery}"` : 'these filters'}.
				{/if}
			</p>
		{:else}
			<div class="space-y-3">
				{#each pagedCurriculum as part (part.id)}
					<PotdSection {part} />
				{/each}
			</div>

			<Pagination {currentPage} {totalPages} onPageChange={goToPage} />
		{/if}
	</div>
</div>
