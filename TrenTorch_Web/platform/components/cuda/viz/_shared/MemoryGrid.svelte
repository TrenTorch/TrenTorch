<script lang="ts">
	import CellBox from './CellBox.svelte';
	import type { Cell } from '$processes/cuda/viz/types';
	// Cells with addresses: the memory model used by the coalescing, bank and tiling figures.
	let {
		cells,
		columns = 16,
		size = 24
	}: { cells: Cell[]; columns?: number; size?: number } = $props();
</script>

<div class="grid" style="--cols:{columns}" role="group" aria-label="memory cells">
	{#each cells as cell, i (i)}<CellBox {cell} {size} />{/each}
</div>

<style>
	.grid {
		display: grid;
		grid-template-columns: repeat(var(--cols), auto);
		gap: 2px;
		width: max-content;
		max-width: 100%;
		overflow-x: auto;
	}
</style>
