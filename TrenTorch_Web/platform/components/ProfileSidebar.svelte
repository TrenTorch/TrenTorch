<script lang="ts">
	import IdentityCard from '$components/IdentityCard.svelte';
	import type { ViewedProfile } from '$processes/profile/public-profile';

	let {
		solvedCount,
		total,
		viewed
	}: { solvedCount: number; total: number; viewed?: ViewedProfile } = $props();
</script>

<div class="space-y-4 lg:sticky lg:top-20">
	<IdentityCard {solvedCount} {total} {viewed} />
</div>
