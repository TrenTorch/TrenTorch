<script lang="ts">
	import QuestionRow from './QuestionRow.svelte';
	import type { Part } from '$data/questions';

	let { part }: { part: Part } = $props();

	const questionCount = $derived(
		part.tracks.reduce((sum, track) => sum + track.questions.length, 0)
	);
</script>

<!-- POTD-only section: always expanded, never collapsible. ModuleSection
     stays collapsible for the Questions page; this exists so /potd has no
     dropdowns -- headers centered, content always visible. The count only
     shows when there is more than one question, so Today's Problem (always
     a single question) hides it while Past Problems keeps it. -->
<section
	class="overflow-hidden rounded-md border border-border [contain-intrinsic-size:auto_600px] [content-visibility:auto]"
>
	<div class="grid grid-cols-[1fr_auto_1fr] items-center gap-3 border-b border-border px-4 py-3">
		{#if questionCount > 1}
			<p class="justify-self-start text-xs text-muted-foreground">
				{questionCount} questions
			</p>
		{:else}
			<span aria-hidden="true"></span>
		{/if}
		<h3 class="justify-self-center text-center font-mono font-semibold">{part.title}</h3>
		<span class="justify-self-end" aria-hidden="true"></span>
	</div>
	{#each part.tracks as track (track.name)}
		<div class="border-t border-border px-4 py-3 first:border-t-0">
			{#each track.questions as question (question.slug)}
				<QuestionRow {question} meta={track.name} />
			{/each}
		</div>
	{/each}
</section>
