<script lang="ts">
	import { Progress } from '$lib/components/ui/progress';

	let { completed, total }: { completed: number; total: number } = $props();

	const percent = $derived(total === 0 ? 0 : Math.round((completed / total) * 100));
</script>

<div class="space-y-2">
	<div class="flex items-baseline justify-between font-mono text-sm">
		<span class="text-muted-foreground">Progress</span>
		<span>{completed} / {total}</span>
	</div>
	<Progress value={percent} />
</div>
