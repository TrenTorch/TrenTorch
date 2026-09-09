<script lang="ts">
	import { resolve } from '$app/paths';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import { solved } from '$lib/stores/solved.svelte';
	import type { Question } from '$lib/data/questions';

	let { question }: { question: Question } = $props();

	const isSolved = $derived(solved.isSolved(question.slug));
</script>

<div
	class="flex items-center gap-3 border-b border-border px-3 py-2 text-sm transition-colors last:border-0 hover:bg-secondary"
>
	<Checkbox
		checked={isSolved}
		onCheckedChange={() => solved.toggle(question.slug)}
		aria-label="Mark '{question.title}' as solved"
	/>
	<!-- The question's slug doubles as its IDE content id: Maanas authors
	     src/lib/data/ide-content/{slug}.json per question as the curriculum
	     content lands, and /ide/[id] already renders whatever it finds (or
	     a "not published yet" state if it doesn't). -->
	<a
		href={resolve('/ide/[id]', { id: question.slug })}
		class="flex flex-1 items-center justify-between"
	>
		<span class="font-mono {isSolved ? 'text-muted-foreground line-through' : ''}">
			{question.title}
		</span>
		<DifficultyBadge difficulty={question.difficulty} />
	</a>
</div>
