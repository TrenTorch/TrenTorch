<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowLeft } from '@lucide/svelte';
	import QuestionRow from '$components/QuestionRow.svelte';
	import { getPartIcon } from '$data/part-icons';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import type { Part } from '$data/questions';
	import type { PageData } from './$types';

	let { data } = $props<{ data: PageData }>();
	const part: Part = $derived(data.part);

	const Icon = $derived(getPartIcon(part.id));
	const totalQuestions = $derived(part.tracks.reduce((sum, t) => sum + t.questions.length, 0));
	const solvedCount = $derived(
		part.tracks.flatMap((t) => t.questions).filter((q) => solved.isSolved(q.slug)).length
	);
</script>

<svelte:head>
	<title>{part.title} | TrenTorch</title>
</svelte:head>

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
	</div>

	<div class="space-y-6">
		{#each part.tracks as track (track.name)}
			<section class="overflow-hidden rounded-md border border-border">
				<div
					class="flex items-center justify-between gap-3 border-b border-l-2 border-border border-l-primary bg-secondary/40 px-4 py-3"
				>
					<h2 class="font-semibold">{track.name}</h2>
					<span class="text-xs text-muted-foreground">{track.questions.length} questions</span>
				</div>
				{#each track.questions as question (question.slug)}
					<QuestionRow {question} />
				{/each}
			</section>
		{/each}
	</div>
</div>
