<script lang="ts">
	import CellBox from './CellBox.svelte';
	import type { Cell } from '$processes/cuda/viz/types';
	// 32 lanes in one strip: an active lane is a filled orange square, a masked lane is hollow and hatched.
	let { lanes, size = 18 }: { lanes: Cell[]; size?: number } = $props();
</script>

<div class="strip" role="group" aria-label="32 lanes of a warp">
	{#each lanes as cell, i (i)}
		<CellBox cell={{ title: `lane ${i}: ${cell.state ?? 'idle'}`, ...cell }} {size} />
	{/each}
</div>

<style>
	.strip {
		display: grid;
		grid-template-columns: repeat(16, auto);
		gap: 2px;
		width: max-content;
		max-width: 100%;
	}
	@media (min-width: 900px) {
		.strip {
			grid-template-columns: repeat(32, auto);
		}
	}
</style>
