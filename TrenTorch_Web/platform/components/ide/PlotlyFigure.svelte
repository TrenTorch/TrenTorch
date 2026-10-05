<script lang="ts">
	import { onMount } from 'svelte';
	import { loadPlotly } from '$processes/code-execution/load-plotly';

	let { json } = $props<{ json: string }>();

	let container: HTMLDivElement | undefined = $state();
	let failed = $state(false);
	let plotly: { purge: (el: HTMLElement) => void } | null = null;

	// Draws the figure whenever the container or the JSON changes, and removes it again on the way out.
	$effect(() => {
		const element = container;
		const figure = JSON.parse(json);
		if (!element) return;
		let cancelled = false;
		loadPlotly()
			.then((Plotly) => {
				if (cancelled) return;
				plotly = Plotly;
				// A learner's figure may set its own size; make it fit the pane instead.
				const layout = { ...figure.layout, autosize: true, width: undefined, height: 360 };
				return Plotly.newPlot(element, figure.data, layout, {
					responsive: true,
					displaylogo: false
				});
			})
			.catch(() => (failed = true));
		return () => {
			cancelled = true;
			plotly?.purge(element);
		};
	});

	onMount(() => () => plotly?.purge(container as HTMLElement));
</script>

{#if failed}
	<p class="text-red-700 dark:text-red-300">Could not load the chart viewer (plotly.js).</p>
{:else}
	<div bind:this={container} class="plotly-figure min-h-[360px] w-full"></div>
{/if}
