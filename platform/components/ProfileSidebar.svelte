<script lang="ts">
	import IdentityCard from '$components/IdentityCard.svelte';
	import GithubSyncCard from '$components/GithubSyncCard.svelte';

	let { solvedCount, total }: { solvedCount: number; total: number } = $props();
</script>

<div class="space-y-4 lg:sticky lg:top-20">
	<IdentityCard {solvedCount} {total} />
	<GithubSyncCard />
</div>
