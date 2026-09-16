<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { CalendarCheck, ArrowRight } from '@lucide/svelte';
	import ProfileCard from '$components/ProfileCard.svelte';
	import ProgressSummary from '$components/ProgressSummary.svelte';
	import ModuleSection from '$components/ModuleSection.svelte';
	import QuestionFilters from '$components/QuestionFilters.svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import Button from '$components/Button.svelte';
	import Pagination from '$components/Pagination.svelte';
	import { getProgressStats } from '$data/questions';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { getTodaysPotdPart, getPastPotdPart } from '$processes/potd/get-potd-part';
	import { getTodaysPotd } from '$processes/potd/get-todays-potd';

	const stats = $derived(getProgressStats(solved.slugs));

	// Real "today" only exists client-side on a fully prerendered static
	// build -- same guard used everywhere else in this codebase that reads
	// the current date/URL (see e.g. the Questions page's own ?page= read).
	const todaysProblem = $derived(browser ? getTodaysPotd() : undefined);
	const todayPart = browser ? getTodaysPotdPart() : [];
	const pastPotdCurriculum = browser ? getPastPotdPart() : [];

	const PARTS_PER_PAGE = 4;

	let searchQuery = $state('');
	let solvedFilter = $state<'all' | 'solved' | 'unsolved'>('all');
	let topicFilter = $state('all');
	let currentPage = $state(browser ? Number(page.url.searchParams.get('page')) || 1 : 1);

	// Filters only ever act on the Past Problems list -- Today's Problem is
	// a single, always-relevant entry, the same way the hero card above
	// never gets filtered away either.
	const allTopics = [...todayPart, ...pastPotdCurriculum]
		.flatMap((part) => part.tracks.flatMap((track) => track.questions.flatMap((q) => q.topics)))
		.filter((topic, i, arr) => arr.indexOf(topic) === i)
		.sort();

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

		{#if pastPotdCurriculum[0]}
			<div>
				<p class="mb-2 text-xs font-semibold text-muted-foreground uppercase">Past problems</p>
				<div class="space-y-1">
					{#each pastPotdCurriculum[0].tracks.slice(0, 5) as track (track.name)}
						<a
							href={resolve('/ide/[id]', { id: track.questions[0].slug })}
							class="block rounded-md border border-border px-2.5 py-2 text-xs transition-colors hover:border-foreground/30 hover:bg-secondary"
						>
							<p class="text-muted-foreground">{track.name}</p>
							<p class="truncate font-medium text-foreground">{track.questions[0].title}</p>
						</a>
					{/each}
				</div>
			</div>
		{/if}
	</aside>

	<div class="flex-1 space-y-6">
		<div class="rounded-md border border-border p-5">
			<div class="mb-3 flex items-center gap-2 font-mono text-xs text-muted-foreground uppercase">
				<CalendarCheck class="size-4" />
				Today's Problem
			</div>
			{#if todaysProblem}
				<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
					<div class="min-w-0">
						<h1 class="mb-1 truncate font-mono text-xl font-bold">
							{todaysProblem.question.title}
						</h1>
						<p class="mb-2 truncate text-sm text-muted-foreground">
							{todaysProblem.sectionLabel} &middot; {todaysProblem.trackLabel}
						</p>
						<DifficultyBadge difficulty={todaysProblem.question.difficulty} />
					</div>
					<Button
						size="lg"
						class="shrink-0"
						href={resolve('/ide/[id]', { id: todaysProblem.question.slug })}
					>
						Try Now
						<ArrowRight class="size-4" />
					</Button>
				</div>
			{:else}
				<p class="text-sm text-muted-foreground">
					No problem is featured today yet, check back soon.
				</p>
			{/if}
		</div>

		{#each todayPart as part (part.id)}
			<ModuleSection {part} />
		{/each}

		<QuestionFilters bind:searchQuery bind:solvedFilter bind:topicFilter topics={allTopics} />

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
					<ModuleSection {part} />
				{/each}
			</div>

			<Pagination {currentPage} {totalPages} onPageChange={goToPage} />
		{/if}
	</div>
</div>
