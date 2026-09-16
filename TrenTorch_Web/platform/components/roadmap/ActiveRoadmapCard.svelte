<script lang="ts">
	import { resolve } from '$app/paths';
	import Button from '$components/Button.svelte';
	import { Progress } from '$components/ui/progress';
	import { curriculum } from '$data/questions';
	import { domainDefs } from '$data/roadmap-domains';
	import { activeRoadmap, getRoadmapProgress } from '$processes/roadmap/active-roadmap.svelte';

	const roadmap = $derived(activeRoadmap.value);
	const progress = $derived(getRoadmapProgress());
	const percent = $derived(
		progress && progress.totalCount > 0
			? Math.round((progress.totalSolved / progress.totalCount) * 100)
			: 0
	);
	const title = $derived(
		roadmap
			? roadmap.domainIds
					.map((id) => domainDefs.find((d) => d.id === id)?.name)
					.filter((n): n is string => Boolean(n))
					.join(' + ')
			: ''
	);

	function reset() {
		if (confirm("Reset your roadmap? Questions you've already solved stay solved.")) {
			activeRoadmap.reset();
		}
	}

	const partTitle = (partId: string) => curriculum.find((p) => p.id === partId)?.title ?? partId;
</script>

<div class="rounded-md border border-border p-6">
	<h2 class="mb-4 font-mono font-semibold">Your roadmap</h2>

	{#if !roadmap || !progress}
		<p class="mb-4 text-sm text-muted-foreground">You're not following a roadmap yet.</p>
		<Button href={resolve('/roadmap')}>Build a roadmap</Button>
	{:else}
		<p class="mb-1 font-medium">{title}</p>
		<p class="mb-3 text-sm text-muted-foreground">
			{progress.totalSolved} of {progress.totalCount} questions solved
		</p>
		<Progress value={percent} class="mb-5 h-2" />

		<div class="space-y-3">
			{#each progress.rows as row (row.partId)}
				<div class="flex items-center gap-4 {row.skipped ? 'opacity-50' : ''}">
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-medium">{partTitle(row.partId)}</p>
						<p class="text-xs text-muted-foreground">
							{row.skipped ? 'Skipped — quiz showed mastery' : `${row.solved} / ${row.total} done`}
						</p>
					</div>
					{#if !row.skipped}
						<Progress value={row.solved} max={row.total} class="h-1.5 max-w-40 flex-1" />
					{/if}
				</div>
			{/each}
		</div>

		<button
			type="button"
			onclick={reset}
			class="mt-5 rounded-md border border-border px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:border-destructive hover:text-destructive"
		>
			Reset roadmap
		</button>
	{/if}
</div>
