<script lang="ts">
	import './layout.css';
	import { page } from '$app/state';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();

	// The IDE fills the exact remaining viewport height below the navbar
	// (h-[calc(100vh-3.5rem)]) with its own internal panes -- a footer
	// below it would just get squeezed off-screen behind a scrollbar, and
	// the page doesn't want one anyway.
	let showFooter = $derived(!page.url.pathname.startsWith('/ide'));
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
