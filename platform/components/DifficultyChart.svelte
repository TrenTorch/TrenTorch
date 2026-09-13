<script lang="ts">
	import { getDifficultyProgress } from '$lib/data/questions';
	import { solved } from '$lib/stores/solved.svelte';
	import type { Difficulty } from '$lib/data/questions';

	const rows = $derived(getDifficultyProgress(solved.slugs));

	// Difficulty is a severity scale (Easy = good, Medium = warning, Hard =
	// critical), not an arbitrary categorical identity, so this reuses the
	// same green/yellow/red mapping DifficultyBadge.svelte carries -- one
	// semantic color system for "difficulty" across the app, not two.
	const barClass: Record<Difficulty, string> = {
		Easy: 'bg-green-600 dark:bg-green-400',
		Medium: 'bg-yellow-600 dark:bg-yellow-400',
		Hard: 'bg-red-600 dark:bg-red-400'
	};
</script>

<div class="space-y-3">
	{#each rows as row (row.difficulty)}
		{@const percent = row.total === 0 ? 0 : Math.round((row.solved / row.total) * 100)}
		<div class="flex items-center gap-3">
			<span class="w-16 shrink-0 font-mono text-xs text-muted-foreground">{row.difficulty}</span>
			<div class="flex flex-1 items-center gap-2">
				<div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary">
					<div
						class="h-full rounded-sm transition-all {barClass[row.difficulty]}"
						style="width: {percent}%"
					></div>
				</div>
				<span class="w-14 shrink-0 text-right font-mono text-xs text-muted-foreground tabular-nums">
					{row.solved}/{row.total}
				</span>
			</div>
		</div>
	{/each}
</div>
