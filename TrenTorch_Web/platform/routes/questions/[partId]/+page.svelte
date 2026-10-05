<script lang="ts">
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import { page } from '$app/state';
	import { ArrowLeft } from '@lucide/svelte';
	import PartTree from '$components/PartTree.svelte';
	import { getPartIcon } from '$data/part-icons';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import SEO from '$components/SEO.svelte';
	import { buildPartSeo } from '$processes/seo/build-part-seo';
	import type { Part } from '$data/questions';
	import type { PageData } from './$types';

	let { data } = $props<{ data: PageData }>();
	const part: Part = $derived(data.part);
	const seo = $derived(buildPartSeo(part));

	const Icon = $derived(getPartIcon(part.id));
	const selectedTopic = $derived(browser ? page.url.searchParams.get('topic') : null);
	// The ?topic= filter (linked from the Problemset) keeps only the sub-sections
	// tagged with that topic, and drops any section or folder left empty.
	const visiblePart: Part = $derived.by(() => {
		if (!selectedTopic) return part;
		const sections = (part.sections ?? [])
			.map((section) => {
				const tracks = section.tracks.filter((track) =>
					track.questions.some((question) => question.topics.includes(selectedTopic))
				);
				return { ...section, tracks, questions: tracks.flatMap((track) => track.questions) };
			})
			.filter((section) => section.tracks.length > 0);
		return { ...part, sections, tracks: sections.flatMap((section) => section.tracks) };
	});
	const allQuestions = $derived(visiblePart.tracks.flatMap((track) => track.questions));
	const totalQuestions = $derived(allQuestions.length);
	const solvedCount = $derived(
		allQuestions.filter((question) => solved.isSolved(question.slug)).length
	);
</script>

<SEO {...seo} />

<div class="container flex flex-col gap-6 px-4 py-12 md:px-6">
	<div>
		<a
			href={resolve('/questions')}
			class="mb-4 inline-flex items-center gap-1.5 font-mono text-xs tracking-wider text-muted-foreground uppercase transition-colors hover:text-primary"
		>
			<ArrowLeft class="size-3.5" />
			All tracks
		</a>
		<div class="flex items-center gap-4">
			<span
				class="flex size-11 shrink-0 items-center justify-center rounded-md border border-border bg-secondary"
			>
				<Icon class="size-5 text-foreground/80" aria-hidden="true" />
			</span>
			<div>
				<h1 class="text-2xl font-bold">{part.title}</h1>
				<p class="text-sm text-muted-foreground">
					{totalQuestions} questions{solvedCount > 0 ? ` · ${solvedCount} done` : ''}
				</p>
			</div>
		</div>
		{#if selectedTopic}
			<div class="mt-4 flex flex-wrap items-center gap-2 text-sm">
				<p class="text-muted-foreground">
					Filtered by topic: <span class="font-medium text-foreground">{selectedTopic}</span>
				</p>
				<a
					href={resolve('/questions/[partId]', { partId: part.id })}
					class="font-medium text-primary hover:underline"
				>
					Clear filter
				</a>
			</div>
		{/if}
	</div>

	{#if selectedTopic && visiblePart.tracks.length === 0}
		<p class="rounded-md border border-border p-4 text-sm text-muted-foreground">
			No learning questions are tagged with this topic.
		</p>
	{:else}
		<div class="overflow-hidden rounded-md border border-border">
			<PartTree part={visiblePart} forceOpen={selectedTopic !== null} />
		</div>
	{/if}
</div>
