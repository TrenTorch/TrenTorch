<script lang="ts">
	import { Badge } from '$components/ui/badge';
	import type { Difficulty } from '$data/questions';
	import type { ProblemsetDifficulty } from '$data/problemset';

	// The Problemset names its levels Beginner, Intermediate and Advanced; they take the colours of the
	// Easy, Medium and Hard they correspond to.
	let { difficulty }: { difficulty: Difficulty | ProblemsetDifficulty } = $props();

	const EASY = 'text-green-600 dark:text-green-400 border-green-600/30';
	const MEDIUM = 'text-yellow-600 dark:text-yellow-400 border-yellow-600/30';
	const HARD = 'text-red-600 dark:text-red-400 border-red-600/30';
	const colorClass: Record<Difficulty | ProblemsetDifficulty, string> = {
		Easy: EASY,
		Medium: MEDIUM,
		Hard: HARD,
		Beginner: EASY,
		Intermediate: MEDIUM,
		Advanced: HARD
	};
</script>

<Badge variant="outline" class="font-mono text-xs {colorClass[difficulty]}">
	{difficulty}
</Badge>
