<script lang="ts">
	import type { Readout } from '$processes/cuda/viz/types';
	let { readouts }: { readouts: Readout[] } = $props();
</script>

<dl class="bar">
	{#each readouts as r (r.label)}
		<div class="chip {r.tone ?? 'neutral'}" title={r.hint}>
			<dt>{r.label}</dt>
			<dd>{r.value}</dd>
		</div>
	{/each}
</dl>

<style>
	.bar {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin: 0;
	}
	.chip {
		display: flex;
		flex-direction: column;
		padding: 0.35rem 0.6rem;
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		background: var(--card);
		min-width: 6rem;
	}
	dt {
		font-size: 0.68rem;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--muted-foreground);
	}
	dd {
		margin: 0;
		font: 600 0.95rem var(--font-mono, ui-monospace, monospace);
	}
	.good dd {
		color: var(--viz-good);
	}
	.bad dd {
		color: var(--viz-error);
	}
	.bad dt::before {
		content: '⚠ ';
	}
</style>
