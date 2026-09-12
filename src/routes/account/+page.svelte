<script lang="ts">
	import ProfileCard from '$lib/components/ProfileCard.svelte';
	import StatTile from '$lib/components/StatTile.svelte';
	import ContinueLearning from '$lib/components/ContinueLearning.svelte';
	import PartsChart from '$lib/components/PartsChart.svelte';
	import DifficultyChart from '$lib/components/DifficultyChart.svelte';
	import { getProgressStats, getInProgressCount } from '$lib/data/questions';
	import { solved } from '$lib/stores/solved.svelte';
	import { attempted } from '$lib/stores/attempted.svelte';

	const stats = $derived(getProgressStats(solved.slugs));
	const percent = $derived(
		stats.total === 0 ? 0 : Math.round((stats.completed / stats.total) * 100)
	);
	const inProgress = $derived(getInProgressCount(solved.slugs, attempted.slugs));
	const notStarted = $derived(stats.total - stats.completed - inProgress);
</script>

<svelte:head>
	<title>Account</title>
	<meta name="description" content="Your TrenTorch account and progress." />
</svelte:head>

<div class="container max-w-5xl space-y-8 px-4 py-12 md:px-6">
	<div
		class="flex flex-col gap-6 rounded-md border border-border p-6 sm:flex-row sm:items-center sm:justify-between"
	>
		<div class="space-y-2">
			<ProfileCard name="Student" />
			<p class="max-w-md text-sm text-muted-foreground">
				Real accounts and sign-in are coming once auth is wired up. Progress below is real, stored
				in this browser, not synced across devices yet.
			</p>
		</div>
		<div class="text-right">
			<p class="font-mono text-5xl font-bold tabular-nums">{percent}%</p>
			<p class="mt-1 text-xs text-muted-foreground">of the curriculum solved</p>
		</div>
	</div>

	<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
		<StatTile label="Solved" value={stats.completed} tone="positive" />
		<StatTile label="In progress" value={inProgress} />
		<StatTile label="Not started" value={notStarted} />
		<StatTile label="Total questions" value={stats.total} />
	</div>

	<div class="rounded-md border border-border p-6">
		<h2 class="mb-4 font-mono font-semibold">Continue where you left off</h2>
		<ContinueLearning />
	</div>

	<div class="rounded-md border border-border p-6">
		<h2 class="mb-4 font-mono font-semibold">Progress by Part</h2>
		<PartsChart />
	</div>

	<div class="rounded-md border border-border p-6">
		<h2 class="mb-4 font-mono font-semibold">Progress by difficulty</h2>
		<DifficultyChart />
	</div>
</div>
