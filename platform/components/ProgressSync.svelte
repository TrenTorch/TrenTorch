<script lang="ts">
	import { session } from '$processes/auth/session.svelte';
	import { syncSolvedWithSupabase } from '$processes/progress-tracking/sync-solved-with-supabase';
	import { syncAttemptedWithSupabase } from '$processes/progress-tracking/sync-attempted-with-supabase';
	import { syncDrafts } from '$processes/code-execution/draft-sync.svelte';

	// Runs once per distinct signed-in user, not on every reactive re-render
	// (session.user is a new object on each auth event, so tracking it
	// directly would re-sync constantly) -- keyed on user id, which only
	// actually changes on a real sign-in/sign-out/account-switch.
	let syncedForUserId: string | null = null;
	let lastSyncAt = 0;
	const REFOCUS_SYNC_MS = 60_000;

	function syncAll(userId: string) {
		lastSyncAt = Date.now();
		void syncSolvedWithSupabase(userId);
		void syncAttemptedWithSupabase(userId);
		void syncDrafts(userId);
	}

	// Coming back to this tab (or switching from another device) re-syncs, so
	// work done elsewhere shows up without a manual reload.
	function onVisible() {
		const userId = session.user?.id;
		if (
			document.visibilityState === 'visible' &&
			userId &&
			Date.now() - lastSyncAt > REFOCUS_SYNC_MS
		) {
			syncAll(userId);
		}
	}

	$effect(() => {
		const userId = session.user?.id ?? null;
		if (userId && userId !== syncedForUserId) {
			syncedForUserId = userId;
			syncAll(userId);
		} else if (!userId) {
			syncedForUserId = null;
		}
	});
</script>

<svelte:document onvisibilitychange={onVisible} />
