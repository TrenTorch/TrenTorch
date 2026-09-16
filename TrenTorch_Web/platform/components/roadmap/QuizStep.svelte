<script lang="ts">
	import type { QuizQuestion } from '$data/roadmap-quiz';

	let {
		question,
		pickedIndex,
		onPick
	}: {
		question: QuizQuestion;
		pickedIndex: number | null;
		onPick: (index: number) => void;
	} = $props();
</script>

<div class="rounded-md border border-border p-5">
	<p class="mb-3 text-xs text-muted-foreground">From: {question.sourceTitle}</p>
	<p class="mb-4 text-base font-medium">{question.prompt}</p>
	<div class="flex flex-col gap-2">
		{#each question.options as option, i (option)}
			<button
				type="button"
				onclick={() => onPick(i)}
				aria-pressed={pickedIndex === i}
				class="rounded-md border px-4 py-2.5 text-left text-sm transition-colors {pickedIndex === i
					? 'border-primary bg-primary/5'
					: 'border-border hover:border-foreground/30'}"
			>
				{option}
			</button>
		{/each}
	</div>
</div>
