<script lang="ts">
	import './layout.css';
	import { page } from '$app/state';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();

	// Footer only appears on the homepage. It was previously shown on every
	// route except /ide, but a long, scrollable list page (Questions,
	// Account) doesn't want a footer competing with pagination for "the
	// bottom of the content" -- the homepage is the one place it's meant to
	// be a page-ending element.
	let showFooter = $derived(page.url.pathname === '/');
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>TrenTorch-Web</title>
	<meta
		name="description"
		content="TrenTorch-Web: the browser front for TrenTorch, an educational ML framework you build by hand."
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
