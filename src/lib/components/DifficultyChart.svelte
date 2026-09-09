<script lang="ts">
	import { curriculum, type Difficulty } from '$lib/data/questions';

	const order: Difficulty[] = ['Easy', 'Medium', 'Hard'];
	const barClass: Record<Difficulty, string> = {
		Easy: 'bg-green-600 dark:bg-green-400',
		Medium: 'bg-yellow-600 dark:bg-yellow-400',
		Hard: 'bg-red-600 dark:bg-red-400'
	};

	const allQuestions = curriculum.flatMap((p) => p.tracks.flatMap((t) => t.questions));
	const rows = order.map((difficulty) => ({
		difficulty,
		count: allQuestions.filter((q) => q.difficulty === difficulty).length
	}));

	const max = Math.max(...rows.map((r) => r.count));
</script>

<!--
	Difficulty is a severity scale (Easy = good, Medium = warning, Hard =
	critical), not an arbitrary categorical identity, so this reuses the same
	green/yellow/red mapping DifficultyBadge.svelte already carries -- one
	semantic color system for "difficulty" across the app, not two.
-->
<div class="space-y-3">
	{#each rows as row (row.difficulty)}
		<div class="flex items-center gap-3">
			<span class="w-16 shrink-0 font-mono text-xs text-muted-foreground">{row.difficulty}</span>
			<div class="flex flex-1 items-center gap-2">
				<div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary">
					<div
						class="h-full rounded-sm transition-all {barClass[row.difficulty]}"
						style="width: {(row.count / max) * 100}%"
					></div>
				</div>
				<span class="w-6 shrink-0 text-right font-mono text-xs tabular-nums">{row.count}</span>
			</div>
		</div>
	{/each}
</div>
