<script lang="ts">
	import './layout.css';
	import 'katex/dist/katex.min.css';
	import { page } from '$app/state';
	import favicon from '$assets/trentorch-logo.webp';
	import Navbar from '$components/Navbar.svelte';
	import Footer from '$components/Footer.svelte';
	import SignInDialog from '$components/SignInDialog.svelte';
	import ProgressSync from '$components/ProgressSync.svelte';
	import RatingSettle from '$components/RatingSettle.svelte';
	import AfterSignInRedirect from '$components/AfterSignInRedirect.svelte';

	let { children } = $props();

	// Footer only appears on the homepage. It was previously shown on every
	// route except /ide, but a long, scrollable list page (Questions,
	// Account) doesn't want a footer competing with pagination for "the
	// bottom of the content" -- the homepage is the one place it's meant to
	// be a page-ending element.
	let showFooter = $derived(page.url.pathname === '/');
</script>

<svelte:head>
	<link rel="icon" type="image/webp" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&display=swap"
	/>
</svelte:head>

<!-- No max-width here: the navbar and footer bars go full-bleed edge to
     edge on any screen size, and each page's own sections cap their
     content at a readable width via the shared .container class instead. -->
<div class="relative flex min-h-screen flex-col">
	<Navbar />
	<div class="w-full flex-1">
		{@render children()}
	</div>
	{#if showFooter}
		<Footer />
	{/if}
</div>
<SignInDialog />
<ProgressSync />
<RatingSettle />
<AfterSignInRedirect />
