<script lang="ts">
	import { onDestroy } from 'svelte';
	// play / pause / step / back / reset / speed. With "reduce motion" on, playing is replaced by single steps.
	let { index = $bindable(0), count }: { index?: number; count: number } = $props();
	let playing = $state(false);
	let speed = $state(1);
	let timer: ReturnType<typeof setInterval> | undefined;
	const reduced =
		typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches;

	function stop() {
		playing = false;
		if (timer) clearInterval(timer);
		timer = undefined;
	}
	function play() {
		if (reduced) return;
		if (index >= count - 1) index = 0;
		playing = true;
		timer = setInterval(() => {
			if (index >= count - 1) stop();
			else index += 1;
		}, 900 / speed);
	}
	$effect(() => {
		void speed;
		if (playing) {
			stop();
			play();
		}
	});
	$effect(() => {
		if (index > count - 1) index = Math.max(0, count - 1);
	});
	onDestroy(stop);
</script>

<div class="stepper" role="group" aria-label="Step controls">
	<button
		type="button"
		onclick={() => {
			stop();
			index = 0;
		}}
		aria-label="Reset to the first step">⏮</button
	>
	<button
		type="button"
		onclick={() => {
			stop();
			index = Math.max(0, index - 1);
		}}
		disabled={index === 0}
		aria-label="Previous step">◀</button
	>
	{#if reduced}
		<span class="hint">Reduced motion: use the step buttons</span>
	{:else}
		<button type="button" onclick={() => (playing ? stop() : play())} aria-pressed={playing}
			>{playing ? '⏸ Pause' : '▶ Play'}</button
		>
	{/if}
	<button
		type="button"
		onclick={() => {
			stop();
			index = Math.min(count - 1, index + 1);
		}}
		disabled={index >= count - 1}
		aria-label="Next step">▶|</button
	>
	<span class="pos" aria-hidden="true">step {index + 1} / {count}</span>
	{#if !reduced}
		<label class="speed"
			>Speed
			<input type="range" min="0.25" max="4" step="0.25" bind:value={speed} aria-label="Speed" />
		</label>
	{/if}
</div>

<style>
	.stepper {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.4rem;
	}
	button {
		padding: 0.25rem 0.6rem;
		border: 1px solid var(--border);
		border-radius: 0.4rem;
		background: var(--card);
		font-size: 0.8rem;
	}
	button:hover:not(:disabled) {
		background: var(--secondary);
	}
	button:disabled {
		opacity: 0.45;
	}
	.pos,
	.hint {
		font-size: 0.75rem;
		color: var(--muted-foreground);
	}
	.speed {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		font-size: 0.75rem;
		color: var(--muted-foreground);
	}
</style>
