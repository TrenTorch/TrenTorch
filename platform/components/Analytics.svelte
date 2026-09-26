<script lang="ts">
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import { loadGoogleTag, trackPageView } from '$processes/analytics/google-tag';

	// Loads after hydration so it never delays first paint. afterNavigate fires
	// for the first page ('enter') and for every client side navigation, and its
	// own onMount is registered after this one, so the tag is already loaded.
	onMount(loadGoogleTag);

	afterNavigate(() => trackPageView(location.pathname + location.search));
</script>
