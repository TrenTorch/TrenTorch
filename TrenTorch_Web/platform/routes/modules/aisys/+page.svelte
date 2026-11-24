<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import Fuse from 'fuse.js';
	import ModuleArt from '$components/ModuleArt.svelte';
	import ModuleAccordion, { startPage } from '$components/ModuleAccordion.svelte';
	import PartTree from '$components/PartTree.svelte';
	import FilterBar from '$components/FilterBar.svelte';
	import PagePill from '$components/PagePill.svelte';
	import StatTile from '$components/StatTile.svelte';
	import ProblemsetPotdBanner from '$components/ProblemsetPotdBanner.svelte';
	import { aiSystemsParts as curriculum } from '$data/domains';
	import { getPartIcon } from '$data/part-icons';
	import type { Part } from '$data/questions';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { recent } from '$processes/progress-tracking/recent.svelte';
	import { dsaResume, RESUME_LABEL } from '$processes/dsa-sheet/dsa-resume';
	import SEO from '$components/SEO.svelte';
	import { buildBreadcrumbJsonLd } from '$processes/seo/build-breadcrumb-json-ld';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const questionsOf = (part: Part) => part.tracks.flatMap((track) => track.questions);
	const allQuestions = curriculum.flatMap(questionsOf);

	// Green on the pill: the question they left half-done, else the first one for a newcomer, else the next
	// unsolved one (the same rule as the DSA sheet).
	const moduleQuestions = allQuestions.map((question) => ({
		id: question.slug,
		title: question.title
	}));
	const moduleGreen = $derived.by(() => {
		const next = dsaResume(moduleQuestions, solved.slugs, recent.get('module'));
		return next
			? { label: RESUME_LABEL[next.kind], href: resolve('/ide/[id]', { id: next.question.id }) }
			: null;
	});

	const partRows = $derived(
		curriculum.map((part) => {
			const ids = questionsOf(part).map((question) => question.slug);
			return { part, count: ids.length, done: ids.filter((id) => solved.isSolved(id)).length };
		})
	);
	const totalQuestions = allQuestions.length;
	const solvedTotal = $derived(partRows.reduce((sum, row) => sum + row.done, 0));
	// A module is complete when every question in it is solved.
	const completedModules = $derived(
		partRows.filter((row) => row.count > 0 && row.done === row.count).length
	);

	// Links from the Problemset and the IDE arrive as ?part=<id>&topic=<tag>: the
	// module opens, and the topic filter is applied.
	const linkedPart = browser ? page.url.searchParams.get('part') : null;
	const initialOpen = curriculum.some((part) => part.id === linkedPart) ? linkedPart : null;

	let searchQuery = $state('');
	let solvedFilter = $state<'all' | 'solved' | 'unsolved'>('all');
	// '' is no topic chosen, which is what FilterBar means by it too.
	let topicFilter = $state(browser ? (page.url.searchParams.get('topic') ?? '') : '');

	const isFiltering = $derived(
		searchQuery.trim() !== '' || solvedFilter !== 'all' || topicFilter !== ''
	);

	const statuses = [
		{ value: 'all', label: 'All questions' },
		{ value: 'solved', label: 'Solved' },
		{ value: 'unsolved', label: 'Unsolved' }
	];

	const allTopics = allQuestions
		.flatMap((question) => question.topics)
		.filter((topic, i, arr) => arr.indexOf(topic) === i)
		.sort();
	const topicChoices = allTopics.map((topic) => ({
		value: topic,
		label: topic,
		count: allQuestions.filter((question) => question.topics.includes(topic)).length
	}));

	// Fuse tolerates typos and partial words ("gradint dsc" finds "Gradient
	// Descent"); topics are searched at a lower weight than titles.
	const searchIndex = new Fuse(allQuestions, {
		keys: [
			{ name: 'title', weight: 2 },
			{ name: 'topics', weight: 1 }
		],
		threshold: 0.35,
		ignoreLocation: true
	});
	const matchingSlugs = $derived.by(() => {
		const query = searchQuery.trim();
		if (!query) return null;
		return new Set(searchIndex.search(query).map((result) => result.item.slug));
	});

	// The same Part -> Track -> Question shape PartTree expects: a track with every
	// question filtered out drops, and so does a part left with no tracks.
	const filteredCurriculum = $derived.by(() =>
		curriculum
			.map((part) => {
				const keep = (question: Part['tracks'][number]['questions'][number]) => {
					if (matchingSlugs && !matchingSlugs.has(question.slug)) return false;
					if (solvedFilter === 'solved' && !solved.isSolved(question.slug)) return false;
					if (solvedFilter === 'unsolved' && solved.isSolved(question.slug)) return false;
					if (topicFilter !== '' && !question.topics.includes(topicFilter)) return false;
					return true;
				};
				const filterTracks = (tracks: Part['tracks']) =>
					tracks
						.map((track) => ({ ...track, questions: track.questions.filter(keep) }))
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
			.filter((part) => part.tracks.length > 0)
	);

	const matchingQuestionCount = $derived(
		filteredCurriculum.reduce((sum, part) => sum + questionsOf(part).length, 0)
	);
	// What the accordion lists: every module, or only those with a matching question.
	const shown = $derived(isFiltering ? filteredCurriculum : curriculum);
	const rows = $derived(
		shown.map((part) => ({
			id: part.id,
			title: part.title,
			icon: getPartIcon(part.id),
			count: questionsOf(part).length,
			solved: partRows.find((row) => row.part.id === part.id)?.done ?? 0
		}))
	);

	// A topic link starts on page 1 of the matches; otherwise the page holding the linked module.
	let currentPage = $state(startPage(topicFilter ? [] : curriculum, initialOpen));
	// Any filter edit changes what "page 2" means, so it returns to page 1; the first run
	// is skipped so a shared link keeps the page it came in with.
	let mounted = false;
	$effect(() => {
		void searchQuery;
		void solvedFilter;
		void topicFilter;
		if (mounted) currentPage = 1;
		mounted = true;
	});
</script>

<SEO
	title={withSiteName('AI systems practice questions')}
	description={`Browse ${totalQuestions} free machine learning practice questions across ${curriculum.length} modules, from math foundations to transformers, inference, and production ML. Run the tests in your browser.`}
	path="/modules/aisys"
	jsonLd={buildBreadcrumbJsonLd([
		{ name: 'Home', path: '/' },
		{ name: 'Modules', path: '/modules' },
		{ name: 'AI Systems', path: '/modules/aisys' }
	])}
/>

<div class="px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px] space-y-8">
		<header class="dot-texture">
			<PagePill
				slug="modules/aisys/"
				area="module"
				resume={moduleGreen}
				up={{ label: 'all domains', href: resolve('/modules') }}
			/>
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">AI Systems</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				Python to production ML, one subsystem at a time
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
					value={totalQuestions}
					tone="positive"
					progress={{ done: solvedTotal, total: totalQuestions }}
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
			total={totalQuestions}
			placeholder="Search questions..."
			noun="question"
		/>

		{#if isFiltering && filteredCurriculum.length === 0}
			<p class="py-12 text-center text-sm text-muted-foreground">
				No questions match {searchQuery ? `"${searchQuery}"` : 'these filters'}.
			</p>
		{:else}
			<!-- keyed on the filter so each filtered view starts from its own open state -->
			{#key isFiltering}
				<ModuleAccordion
					items={rows}
					forceOpen={isFiltering}
					{initialOpen}
					hue="#d28b7a"
					bind:page={currentPage}
				>
					{#snippet art(item)}<ModuleArt id={item.id} />{/snippet}
					{#snippet children(item)}
						{@const part = shown.find((candidate) => candidate.id === item.id)}
						{#if part}<PartTree {part} forceOpen={isFiltering} />{/if}
					{/snippet}
				</ModuleAccordion>
			{/key}
		{/if}
	</div>
</div>
