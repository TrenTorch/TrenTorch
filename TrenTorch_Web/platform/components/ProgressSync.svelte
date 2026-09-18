<script lang="ts">
	import { session } from '$processes/auth/session.svelte';
	import { syncSolvedWithSupabase } from '$processes/progress-tracking/sync-solved-with-supabase';

	// Runs once per distinct signed-in user, not on every reactive re-render
	// (session.user is a new object on each auth event, so tracking it
	// directly would re-sync constantly) -- keyed on user id, which only
	// actually changes on a real sign-in/sign-out/account-switch.
	let syncedForUserId: string | null = null;

	$effect(() => {
		const userId = session.user?.id ?? null;
		if (userId && userId !== syncedForUserId) {
			syncedForUserId = userId;
			void syncSolvedWithSupabase(userId);
		} else if (!userId) {
			syncedForUserId = null;
		}
	});
</script>
