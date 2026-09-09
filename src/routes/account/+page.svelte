<script lang="ts">
	import ProfileCard from '$lib/components/ProfileCard.svelte';
	import ProgressSummary from '$lib/components/ProgressSummary.svelte';
	import PartsChart from '$lib/components/PartsChart.svelte';
	import DifficultyChart from '$lib/components/DifficultyChart.svelte';
	import { getProgressStats } from '$lib/data/questions';

	const stats = getProgressStats();
</script>

<svelte:head>
	<title>Account</title>
	<meta name="description" content="Your TrenTorch account and progress." />
</svelte:head>

<div class="container max-w-3xl space-y-8 px-4 py-12 md:px-6">
	<div class="space-y-6 rounded-md border border-border p-6">
		<ProfileCard name="Student" />
		<ProgressSummary completed={stats.completed} total={stats.total} />
		<p class="text-sm text-muted-foreground">
			Real accounts, sign-in, and per-student progress are coming once auth is wired up. Numbers
			below are the real curriculum shape (question counts, difficulty spread), not placeholder
			data, only "questions completed" is a stand-in until progress tracking exists.
		</p>
	</div>

	<div class="rounded-md border border-border p-6">
		<p class="mb-1 font-mono text-5xl font-bold tabular-nums">{stats.total}</p>
		<p class="text-sm text-muted-foreground">questions across the curriculum</p>
	</div>

	<div class="rounded-md border border-border p-6">
		<h2 class="mb-4 font-mono font-semibold">Questions by Part</h2>
		<PartsChart />
	</div>

	<div class="rounded-md border border-border p-6">
		<h2 class="mb-4 font-mono font-semibold">Questions by difficulty</h2>
		<DifficultyChart />
	</div>
</div>
