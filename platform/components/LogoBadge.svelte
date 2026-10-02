<script lang="ts">
	import LogoMark from './LogoMark.svelte';

	let { class: className = '' }: { class?: string } = $props();
</script>

<!-- The brand mark, sized by whatever `class` the caller passes -- the
     navbar and hero both use this at two different sizes. LogoMark's own
     default `rounded-full` crop is kept (not overridden here): the source
     artwork is a solid black square with no transparency, and a circular
     crop is what keeps it reading as a deliberate badge rather than a
     stark black square, in both themes. -->
<span class="inline-flex shrink-0 items-center justify-center {className}">
	<LogoMark class="size-full" />
</span>
