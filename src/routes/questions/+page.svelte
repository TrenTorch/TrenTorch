<script lang="ts">
	import ProfileCard from '$lib/components/ProfileCard.svelte';
	import ProgressSummary from '$lib/components/ProgressSummary.svelte';
	import ModuleSection from '$lib/components/ModuleSection.svelte';
	import QuestionFilters from '$lib/components/QuestionFilters.svelte';
	import { curriculum, getProgressStats } from '$lib/data/questions';
	import { solved } from '$lib/stores/solved.svelte';

	const stats = getProgressStats();

	let searchQuery = $state('');
	let solvedFilter = $state<'all' | 'solved' | 'unsolved'>('all');
	let topicFilter = $state('all');

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
				{#each filteredCurriculum as part (part.id)}
					<ModuleSection {part} />
				{/each}
			</div>
		{/if}
	</div>
</div>
