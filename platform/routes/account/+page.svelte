<script lang="ts">
	import ProfileCard from '$components/ProfileCard.svelte';
	import StatTile from '$components/StatTile.svelte';
	import ContinueLearning from '$components/ContinueLearning.svelte';
	import PartsChart from '$components/PartsChart.svelte';
	import DifficultyChart from '$components/DifficultyChart.svelte';
	import Button from '$components/Button.svelte';
	import { LogOut } from '@lucide/svelte';
	import { getProgressStats, getInProgressCount } from '$data/questions';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { session, signOut } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';

	const stats = $derived(getProgressStats(solved.slugs));
	const percent = $derived(
		stats.total === 0 ? 0 : Math.round((stats.completed / stats.total) * 100)
	);
	const inProgress = $derived(getInProgressCount(solved.slugs, attempted.slugs));
	const notStarted = $derived(stats.total - stats.completed - inProgress);
</script>

<svelte:head>
	<meta name="description" content="Your TrenTorch account and progress." />
</svelte:head>

<div class="container max-w-5xl px-4 py-12 md:px-6">
	<div class="grid gap-6 lg:grid-cols-[320px_1fr] lg:items-start">
		<!-- Left: profile + sign-in, the one place account state lives on this
		     page -- the sign-in dialog itself is shared with the IDE's Run/
		     Submit gate (SignInDialog.svelte, mounted once in the root
		     layout), so there is exactly one sign-in surface in the app. -->
		<div class="space-y-5 rounded-md border border-border p-6">
			<ProfileCard name="Student" />
			<p class="text-sm text-muted-foreground">
				Progress is stored in this browser, not synced across devices yet.
			</p>
			<div>
				<p class="font-mono text-4xl font-bold tabular-nums">{percent}%</p>
				<p class="mt-1 text-xs text-muted-foreground">of the curriculum solved</p>
			</div>
			<div class="border-t border-border pt-4">
				{#if session.user}
					<p class="mb-2 truncate text-sm text-muted-foreground">
						Signed in as <span class="font-medium text-foreground">{session.user.email}</span>
					</p>
					<Button variant="outline" size="sm" onclick={signOut}>
						<LogOut class="size-3.5" />
						Sign out
					</Button>
				{:else}
					<Button size="sm" class="w-full" onclick={() => signInPrompt.open()}>
						Sign in / Sign up
					</Button>
				{/if}
			</div>
		</div>

		<!-- Right: stats and graphs -->
		<div class="space-y-8">
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
	</div>
</div>
