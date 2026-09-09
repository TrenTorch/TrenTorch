<script lang="ts">
	import logo from '$lib/assets/trentorch-logo.jpg';

	let { class: className = '' }: { class?: string } = $props();
</script>

<!-- The source JPG has a solid black background (no transparency), so it's
     cropped into a circular badge here rather than shown as a square -- that
     reads as an intentional icon in both light and dark mode, a plain square
     would show as a stark black box on the light theme. -->
<img src={logo} alt="TrenTorch" class="rounded-full object-cover {className}" />
