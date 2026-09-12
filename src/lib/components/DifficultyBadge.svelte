<script lang="ts">
	import { Badge } from '$lib/components/ui/badge';
	import type { Difficulty } from '$lib/data/questions';

	let { difficulty }: { difficulty: Difficulty } = $props();

	const colorClass: Record<Difficulty, string> = {
		Easy: 'text-green-600 dark:text-green-400 border-green-600/30',
		Medium: 'text-yellow-600 dark:text-yellow-400 border-yellow-600/30',
		Hard: 'text-red-600 dark:text-red-400 border-red-600/30'
	};
</script>

<Badge variant="outline" class="font-mono text-xs {colorClass[difficulty]}">
	{difficulty}
</Badge>
