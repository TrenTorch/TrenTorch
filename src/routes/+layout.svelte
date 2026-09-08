<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>TrenTorch-Web</title>
	<meta
		name="description"
		content="TrenTorch-Web: the browser front for TrenTorch, an educational ML framework you build by hand."
	/>
</svelte:head>

<div class="relative mx-auto flex min-h-screen max-w-7xl flex-col">
	<Navbar />
	<div class="w-full flex-1">
		{@render children()}
	</div>
	<Footer />
</div>
