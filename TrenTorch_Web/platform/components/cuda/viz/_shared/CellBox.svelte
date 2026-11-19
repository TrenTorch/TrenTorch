<script lang="ts">
	import type { Cell } from '$processes/cuda/viz/types';
	let { cell, size = 22 }: { cell: Cell; size?: number } = $props();
	const state = $derived(cell.state ?? 'idle');
	// Never colour alone: masked is hatched, stalled shows a clock, an error shows a cross and the word.
	const glyph = $derived(state === 'stalled' ? '⏱' : state === 'error' ? '✕' : '');
	const label = $derived(
		cell.title ?? `${cell.text ?? ''} ${state === 'idle' ? '' : state}`.trim()
	);
</script>

<span
	class="cell {state}"
	class:tinted={cell.tint !== undefined && state === 'idle'}
	style="--s:{size}px; {cell.tint !== undefined ? `--tint: var(--viz-t${cell.tint})` : ''}"
	role="img"
	aria-label={label}
	title={label}
>
	{#if glyph}<span class="glyph" aria-hidden="true">{glyph}</span>{/if}
	{#if cell.text !== undefined}<span class="txt">{cell.text}</span>{/if}
</span>

<style>
	.cell {
		position: relative;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: var(--s);
		height: var(--s);
		padding: 0 3px;
		box-sizing: border-box;
		border: 1px solid var(--border);
		border-radius: 3px;
		font: 600 10px/1 var(--font-mono, ui-monospace, monospace);
		color: var(--foreground);
		background: var(--card);
	}
	.tinted {
		background: color-mix(in oklab, var(--tint) 28%, var(--card));
		border-color: var(--tint);
	}
	.active {
		background: var(--viz-active);
		border-color: var(--viz-active);
		color: #fff;
	}
	.masked {
		color: var(--muted-foreground);
		background: repeating-linear-gradient(
			45deg,
			transparent 0 3px,
			color-mix(in oklab, var(--viz-masked) 55%, transparent) 3px 4px
		);
		border-color: var(--viz-masked);
	}
	.stalled {
		background: color-mix(in oklab, var(--viz-stall) 30%, var(--card));
		border-color: var(--viz-stall);
	}
	.touch {
		outline: 2px solid var(--viz-active);
		outline-offset: 1px;
		background: color-mix(in oklab, var(--viz-active) 18%, var(--card));
	}
	.error {
		background: color-mix(in oklab, var(--viz-error) 24%, var(--card));
		border: 2px solid var(--viz-error);
		color: var(--viz-error);
	}
	.done {
		background: color-mix(in oklab, var(--viz-good) 22%, var(--card));
		border-color: var(--viz-good);
	}
	.glyph {
		margin-right: 2px;
		font-size: 9px;
	}
</style>
