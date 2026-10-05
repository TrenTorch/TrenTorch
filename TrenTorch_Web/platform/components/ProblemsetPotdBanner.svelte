<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { SvelteDate } from 'svelte/reactivity';
	import { ArrowRight } from '@lucide/svelte';
	import Button from './Button.svelte';
	import { localDateString } from '$processes/potd/local-date-string';

	let { onDayChange }: { onDayChange?: (today: string) => void } = $props();
	let timeUntilMidnight = $state('');
	let lastPotdDate = '';

	function updateCountdown() {
		const now = new SvelteDate();
		const today = localDateString(now);
		if (today !== lastPotdDate) {
			lastPotdDate = today;
			onDayChange?.(today);
		}

		const nextMidnight = new SvelteDate(now);
		nextMidnight.setHours(24, 0, 0, 0);
		const seconds = Math.max(0, Math.floor((nextMidnight.getTime() - now.getTime()) / 1000));
		const hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
		const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
		timeUntilMidnight = `${hours}:${minutes}:${String(seconds % 60).padStart(2, '0')}`;
	}

	onMount(() => {
		updateCountdown();
		const timer = window.setInterval(updateCountdown, 1000);
		return () => window.clearInterval(timer);
	});
</script>

<section class="potd-card" aria-labelledby="potd-heading">
	<p class="potd-eyebrow">Problem of the Day</p>
	<h2 id="potd-heading">Today's featured problem</h2>
	<p class="potd-description">A new challenge every day</p>
	<div class="potd-meta">
		<span class="topic-pill">Today's challenge</span>
		<p class="countdown">
			Resets in <span>{timeUntilMidnight || '--:--:--'}</span>
		</p>
	</div>
	<Button href={resolve('/potd')} class="mt-4">
		Solve
		<ArrowRight class="size-4" />
	</Button>
</section>

<style>
	.potd-card {
		border: 1px solid var(--border);
		border-radius: 10px;
		background: linear-gradient(
			180deg,
			color-mix(in srgb, var(--primary) 8%, var(--secondary)),
			var(--secondary)
		);
		padding: 22px 26px;
		color: var(--foreground);
	}

	.potd-eyebrow {
		margin-bottom: 8px;
		color: var(--muted-foreground);
		font-size: 0.7rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	h2 {
		margin-bottom: 4px;
		font-size: 1.125rem;
		font-weight: 700;
	}

	.potd-description,
	.countdown {
		color: var(--muted-foreground);
		font-size: 0.875rem;
	}

	.potd-description {
		margin-bottom: 16px;
	}

	.potd-meta {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 8px;
	}

	.topic-pill {
		border: 1px solid color-mix(in srgb, var(--primary) 35%, var(--border));
		border-radius: 999px;
		background: color-mix(in srgb, var(--primary) 12%, var(--background));
		padding: 5px 10px;
		color: color-mix(in srgb, var(--primary) 55%, var(--foreground));
		font-size: 0.72rem;
	}

	.countdown {
		margin-left: auto;
		font-size: 0.75rem;
	}

	.countdown span {
		color: var(--foreground);
		font-family: 'Geist Mono', ui-monospace, monospace;
		font-variant-numeric: tabular-nums;
	}

	@media (max-width: 640px) {
		.potd-card {
			padding: 18px;
		}
	}
</style>
