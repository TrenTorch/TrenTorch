<script lang="ts">
	import MarkdownPage from '$lib/components/MarkdownPage.svelte';

	let { data }: { data: { html: string } } = $props();
</script>

<svelte:head>
	<title>TrenTorch-Web Docs</title>
	<meta
		name="description"
		content="The full TrenTorch-Web README: what it is, how to run it, and how to contribute."
	/>
</svelte:head>

<div class="container max-w-4xl px-4 py-12 md:px-6">
	<MarkdownPage html={data.html} />
</div>
