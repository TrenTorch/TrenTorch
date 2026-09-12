<script lang="ts">
	import { getPartProgress } from '$lib/data/questions';
	import { solved } from '$lib/stores/solved.svelte';

	// Solved out of that Part's own total, not just a raw question count --
	// the useful question on an account page is "how far along is this
	// Part," not "how big is this Part."
	const rows = $derived(getPartProgress(solved.slugs));
</script>

<!--
	Progress bars, one per curriculum Part: the solved fraction fills in
	--primary (the theme's monochrome accent, same token the Questions page's
	own progress bar uses), the rest of the track stays --secondary. Every
	row carries its own "solved / total" label rather than relying on bar
	length alone to be legible.
-->
<div class="space-y-3">
	{#each rows as row (row.id)}
		{@const percent = row.total === 0 ? 0 : Math.round((row.solved / row.total) * 100)}
		<div class="flex items-center gap-3">
			<span
				class="w-56 shrink-0 truncate font-mono text-xs text-muted-foreground"
				title={row.title}
			>
				{row.title}
			</span>
			<div class="flex flex-1 items-center gap-2">
				<div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary">
					<div class="h-full rounded-sm bg-primary transition-all" style="width: {percent}%"></div>
				</div>
				<span class="w-14 shrink-0 text-right font-mono text-xs text-muted-foreground tabular-nums">
					{row.solved}/{row.total}
				</span>
			</div>
		</div>
	{/each}
</div>
