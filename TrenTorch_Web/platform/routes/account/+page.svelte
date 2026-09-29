<script lang="ts">
	import ProfileSidebar from '$components/ProfileSidebar.svelte';
	import StatTile from '$components/StatTile.svelte';
	import PartsChart from '$components/PartsChart.svelte';
	import DifficultyChart from '$components/DifficultyChart.svelte';
	import DeleteAccountCard from '$components/DeleteAccountCard.svelte';
	import ProfileSection from '$components/ProfileSection.svelte';
	import RatingHistory from '$components/RatingHistory.svelte';
	import ContributionGraph from '$components/ContributionGraph.svelte';
	import SEO from '$components/SEO.svelte';
	import { withSiteName } from '$processes/seo/with-site-name';
	import { getProgressStats, getInProgressCount } from '$data/questions';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';

	const stats = $derived(getProgressStats(solved.slugs));
	const inProgress = $derived(getInProgressCount(solved.slugs, attempted.slugs));
	const notStarted = $derived(stats.total - stats.completed - inProgress);
</script>

<SEO
	title={withSiteName('Your account')}
	description="Your TrenTorch account and progress."
	path="/account"
	noindex
/>

<div class="container max-w-5xl px-4 py-12 md:px-6">
	<div class="grid gap-6 lg:grid-cols-[1fr_320px] lg:items-start">
		<!-- Right on desktop: identity card. Sign-in itself is the shared SignInDialog
		     (mounted once in the root layout), so there is exactly one sign-in
		     surface in the app. -->
		<div class="lg:col-start-2 lg:row-start-1 lg:self-stretch">
			<ProfileSidebar solvedCount={stats.completed} total={stats.total} />
		</div>

		<!-- Left on desktop: stats and graphs -->
		<div class="space-y-8 lg:col-start-1 lg:row-start-1">
			<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
				<StatTile label="Solved" value={stats.completed} tone="positive" />
				<StatTile label="In progress" value={inProgress} />
				<StatTile label="Not started" value={notStarted} />
				<StatTile label="Total questions" value={stats.total} />
			</div>

			<ProfileSection />
			<RatingHistory />
			<ContributionGraph />

			<div class="rounded-md border border-border p-6">
				<h2 class="mb-4 font-mono font-semibold">Progress by difficulty</h2>
				<DifficultyChart />
			</div>

			<div class="rounded-md border border-border p-6">
				<h2 class="mb-4 font-mono font-semibold">Progress by Part</h2>
				<PartsChart />
			</div>

			<DeleteAccountCard />
		</div>
	</div>
</div>
