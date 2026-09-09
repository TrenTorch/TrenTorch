<script lang="ts">
	import { curriculum } from '$lib/data/questions';

	const rows = curriculum.map((part, i) => ({
		title: part.title,
		count: part.tracks.reduce((sum, t) => sum + t.questions.length, 0),
		slot: i + 1
	}));

	const max = Math.max(...rows.map((r) => r.count));
</script>

<!--
	Categorical bar chart, one bar per curriculum Part. Colors are the
	dataviz skill's validated default categorical palette, slots 1-5 in
	fixed order (never reassigned/cycled), validated against this repo's
	actual surfaces:
	  node scripts/validate_palette.js "#2a78d6,#eb6834,#1baf7a,#eda100,#e87ba4" --mode light
	    -> ALL CHECKS PASS (3 slots WARN sub-3:1 contrast, relief required)
	  node scripts/validate_palette.js "#3987e5,#d95926,#199e70,#c98500,#d55181" --mode dark --surface "#000000"
	    -> ALL CHECKS PASS, no warnings
	The light-mode WARN is why every bar carries a direct value label rather
	than relying on the fill color alone.
-->
<div class="chart space-y-3">
	{#each rows as row (row.title)}
		<div class="flex items-center gap-3">
			<span class="w-40 shrink-0 truncate font-mono text-xs text-muted-foreground">
				{row.title}
			</span>
			<div class="flex flex-1 items-center gap-2">
				<div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary">
					<div
						class="slot-{row.slot} h-full rounded-sm transition-all"
						style="width: {(row.count / max) * 100}%"
					></div>
				</div>
				<span class="w-6 shrink-0 text-right font-mono text-xs tabular-nums">{row.count}</span>
			</div>
		</div>
	{/each}
</div>

<style>
	.chart {
		--slot-1: #2a78d6;
		--slot-2: #eb6834;
		--slot-3: #1baf7a;
		--slot-4: #eda100;
		--slot-5: #e87ba4;
	}
	:global(.dark) .chart {
		--slot-1: #3987e5;
		--slot-2: #d95926;
		--slot-3: #199e70;
		--slot-4: #c98500;
		--slot-5: #d55181;
	}
	.slot-1 {
		background: var(--slot-1);
	}
	.slot-2 {
		background: var(--slot-2);
	}
	.slot-3 {
		background: var(--slot-3);
	}
	.slot-4 {
		background: var(--slot-4);
	}
	.slot-5 {
		background: var(--slot-5);
	}
</style>
