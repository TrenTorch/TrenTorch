<script lang="ts">
	// `html` is only ever generated from this repo's own README.md, never
	// from user input, so rendering it raw here is safe.
	let { html }: { html: string } = $props();
</script>

<article
	class="prose max-w-none prose-neutral dark:prose-invert prose-headings:font-mono prose-a:text-primary prose-code:font-mono prose-code:text-foreground prose-pre:border prose-pre:border-border prose-pre:bg-secondary prose-pre:text-foreground prose-table:text-sm prose-img:rounded-none"
>
	<!-- html is only ever generated server-side from this repo's own README.md
	     (see +page.server.ts), never from user input, so this is safe. -->
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html html}
</article>
