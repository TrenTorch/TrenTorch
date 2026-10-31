<script lang="ts">
	import QuestionRow from './QuestionRow.svelte';
	import type { Part } from '$data/questions';

	let { part }: { part: Part } = $props();

	const questionCount = $derived(
		part.tracks.reduce((sum, track) => sum + track.questions.length, 0)
	);
</script>

<!-- The archive of past Problems of the Day: always open, never collapsible. Each track is a date, shown at
     the end of its row. -->
<section
	class="overflow-hidden rounded-2xl border border-border [contain-intrinsic-size:auto_600px] [content-visibility:auto]"
>
	<div class="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
		<h3 class="font-mono text-sm font-semibold">{part.title}</h3>
		<span class="rounded-md bg-secondary/70 px-2 py-0.5 font-mono text-xs text-muted-foreground">
			{questionCount}
		</span>
	</div>
	{#each part.tracks as track (track.name)}
		<div class="border-t border-border px-4 py-3 first:border-t-0">
			{#each track.questions as question (question.slug)}
				<QuestionRow {question} meta={track.name} wrap />
			{/each}
		</div>
	{/each}
</section>
