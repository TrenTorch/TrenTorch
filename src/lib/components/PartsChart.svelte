<script lang="ts">
	import { curriculum } from '$lib/data/questions';

	const rows = curriculum.map((part) => ({
		title: part.title,
		count: part.tracks.reduce((sum, t) => sum + t.questions.length, 0)
	}));

	const max = Math.max(...rows.map((r) => r.count));
</script>

<!--
	Magnitude bar chart, one bar per curriculum Part, ranked by question
	count. Every bar shares one color (the theme's --primary token) rather
	than a distinct categorical hue per Part: bar length is the only thing
	being compared here (a Part's own color carries no meaning anywhere
	else on the page), and a fixed 5-slot categorical palette stopped
	covering every row once the curriculum grew past 5 Parts. A single,
	theme-aware accent scales to any number of rows for free.
-->
<div class="chart space-y-3">
	{#each rows as row (row.title)}
		<div class="flex items-center gap-3">
			<span
				class="w-56 shrink-0 truncate font-mono text-xs text-muted-foreground"
				title={row.title}
			>
				{row.title}
			</span>
			<div class="flex flex-1 items-center gap-2">
				<div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary">
					<div
						class="h-full rounded-sm bg-primary transition-all"
						style="width: {(row.count / max) * 100}%"
					></div>
				</div>
				<span class="w-6 shrink-0 text-right font-mono text-xs tabular-nums">{row.count}</span>
			</div>
		</div>
	{/each}
</div>
