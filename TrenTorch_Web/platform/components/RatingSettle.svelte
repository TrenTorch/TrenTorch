<script lang="ts">
	import { session } from '$processes/auth/session.svelte';
	import { settlePastPotdOutcomes } from '$processes/rating/settle-past-potd';
	import { ratingStore } from '$processes/rating/rating-store.svelte';

	// Same shape as ProgressSync.svelte: runs once per distinct signed-in
	// user, settling any POTD the user attempted but never solved before its
	// day passed (spec §5.1/§5.4 -- the "failed" outcome only applies once
	// the day is over, and this app has no server/cron to fire that
	// automatically, see settle-past-potd.ts), then loads the resulting
	// rating into ratingStore for the account page's badge.
	let settledForUserId: string | null = null;

	$effect(() => {
		const userId = session.user?.id ?? null;
		if (userId && userId !== settledForUserId) {
			settledForUserId = userId;
			void settlePastPotdOutcomes(userId).finally(() => ratingStore.refresh(userId));
		} else if (!userId) {
			settledForUserId = null;
			ratingStore.clear();
		}
	});
</script>
