<script lang="ts">
	import { goto } from '$app/navigation';
	import { session } from '$processes/auth/session.svelte';
	import { takeAfterSignInDestination } from '$processes/auth/after-sign-in-destination';

	// A signed-out visitor who clicked Questions or the Problem of the Day was
	// asked to sign in first. Once a session exists (including after an OAuth
	// round trip that returns to /account), send them where they were going.
	$effect(() => {
		if (!session.user) return;
		const destination = takeAfterSignInDestination();
		// The destination came from resolve() when the click was gated, and
		// takeAfterSignInDestination() only returns same-site paths.
		// eslint-disable-next-line svelte/no-navigation-without-resolve
		if (destination) void goto(destination);
	});
</script>
