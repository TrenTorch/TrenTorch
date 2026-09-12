<script lang="ts">
	import logo from '$lib/assets/trentorch-logo.webp';

	let { class: className = '' }: { class?: string } = $props();
</script>

<!-- 192px WebP (~2.6 KB, down from a 47 KB 1075px JPEG). Solid black
     background, no transparency, so it's cropped into a circular badge --
     reads as an intentional icon in both themes; a plain square would be a
     stark black box on the light theme. Only used on the home hero, at
     144px, so 192px covers retina. width/height set to reserve layout box
     and avoid a shift on load. -->
<img
	src={logo}
	alt="TrenTorch"
	width="192"
	height="192"
	class="rounded-full object-cover {className}"
/>
