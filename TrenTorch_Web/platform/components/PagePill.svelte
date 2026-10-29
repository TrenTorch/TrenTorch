<script lang="ts">
	import WindowDots from './WindowDots.svelte';

	// The small editor-window label at the top of a page's header: the three dots and where you are, as a
	// folder ("papers/"). It says what the page is without a second heading.
	let { slug }: { slug: string } = $props();
</script>

<div
	class="mb-4 inline-flex items-center gap-3 rounded-full border border-border bg-secondary/50 py-1.5 pr-4 pl-3 font-mono text-xs text-muted-foreground"
>
	<WindowDots />
	{slug}
</div>
