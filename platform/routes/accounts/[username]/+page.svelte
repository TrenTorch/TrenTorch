<script lang="ts">
	import { page } from '$app/state';
	import ProfileSidebar from '$components/ProfileSidebar.svelte';
	import StatTile from '$components/StatTile.svelte';
	import PartsChart from '$components/PartsChart.svelte';
	import DifficultyChart from '$components/DifficultyChart.svelte';
	import RatingHistory from '$components/RatingHistory.svelte';
	import ContributionGraph from '$components/ContributionGraph.svelte';
	import SEO from '$components/SEO.svelte';
	import { withSiteName } from '$processes/seo/with-site-name';
	import { getProgressStats } from '$data/questions';
	import { fetchPublicProfile, type ViewedProfile } from '$processes/profile/public-profile';
	import { fetchSolvedQuestions } from '$processes/progress-tracking/supabase-solved-store';

	// The path segment is "@name"; the database only answers for public profiles.
	const username = $derived(page.params.username?.replace(/^@/, '').toLowerCase() ?? '');

	type State =
		| { status: 'loading' }
		| { status: 'missing' }
		| { status: 'error' }
		| { status: 'ready'; viewed: ViewedProfile; slugs: Set<string> };
	let state = $state<State>({ status: 'loading' });

	$effect(() => {
		const name = username;
		state = { status: 'loading' };
		(async () => {
			const viewed = await fetchPublicProfile(name);
			if (name !== username) return;
			if (viewed === undefined) return void (state = { status: 'error' });
			if (viewed === null) return void (state = { status: 'missing' });
			const rows = await fetchSolvedQuestions(viewed.id);
			if (name !== username) return;
			state = { status: 'ready', viewed, slugs: new Set(rows.map((row) => row.question_id)) };
		})();
	});

	const stats = $derived(state.status === 'ready' ? getProgressStats(state.slugs) : null);
	const title = $derived(
		state.status === 'ready'
			? `${state.viewed.profile.displayName || `@${state.viewed.profile.username}`} (@${state.viewed.profile.username})`
			: 'Profile'
	);
</script>

<SEO
	title={withSiteName(title)}
	description="A TrenTorch profile and progress."
	path={`/accounts/@${username}`}
	noindex={state.status !== 'ready'}
/>

<div class="container max-w-5xl px-4 py-12 md:px-6">
	{#if state.status === 'ready' && stats}
		<div class="grid gap-6 lg:grid-cols-[1fr_320px] lg:items-start">
			<div class="lg:col-start-2 lg:row-start-1 lg:self-stretch">
				<ProfileSidebar solvedCount={stats.completed} total={stats.total} viewed={state.viewed} />
			</div>

			<div class="space-y-8 lg:col-start-1 lg:row-start-1">
				<div class="grid grid-cols-2 gap-4">
					<StatTile label="Solved" value={stats.completed} tone="positive" />
					<StatTile label="Total questions" value={stats.total} />
				</div>

				<RatingHistory userId={state.viewed.id} />
				<ContributionGraph userId={state.viewed.id} />

				<div class="rounded-md border border-border p-6">
					<h2 class="mb-4 font-mono font-semibold">Progress by difficulty</h2>
					<DifficultyChart slugs={state.slugs} />
				</div>

				<div class="rounded-md border border-border p-6">
					<h2 class="mb-4 font-mono font-semibold">Progress by Part</h2>
					<PartsChart slugs={state.slugs} />
				</div>
			</div>
		</div>
	{:else if state.status === 'loading'}
		<p class="text-sm text-muted-foreground">Loading profile...</p>
	{:else if state.status === 'missing'}
		<h1 class="font-mono text-xl font-semibold">Profile not found</h1>
		<p class="mt-2 text-sm text-muted-foreground">This profile does not exist or is private.</p>
	{:else}
		<h1 class="font-mono text-xl font-semibold">Profile unavailable</h1>
		<p class="mt-2 text-sm text-muted-foreground">
			Could not load this profile. Try again shortly.
		</p>
	{/if}
</div>
