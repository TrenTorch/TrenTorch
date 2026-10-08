<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { SvelteDate } from 'svelte/reactivity';
	import { ArrowRight } from '@lucide/svelte';
	import Button from './Button.svelte';
	import { localDateString } from '$processes/potd/local-date-string';
	import { getPotdForDate } from '$processes/potd/get-potd-for-date';
	import { formatTopic } from '$processes/potd/format-topic';
	import type { PotdSummary } from '$processes/potd/potd-summary';

	let {
		onDayChange,
		potdSummaries = []
	}: { onDayChange?: (today: string) => void; potdSummaries?: PotdSummary[] } = $props();
	let timeUntilMidnight = $state('');
	let lastPotdDate = '';
	// "Today" only exists in the visitor's browser (the page is prerendered), so
	// it is set from the countdown tick; until then, and on a day with nothing
	// scheduled, the card falls back to its generic text.
	let today = $state('');
	const potd = $derived(today ? getPotdForDate(potdSummaries, today) : undefined);
	const topic = $derived(potd?.tags[0] ? formatTopic(potd.tags[0]) : '');

	function updateCountdown() {
		const now = new SvelteDate();
		const date = localDateString(now);
		if (date !== lastPotdDate) {
			lastPotdDate = date;
			today = date;
			onDayChange?.(date);
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
	<h2 id="potd-heading">{potd ? potd.title : "Today's featured problem"}</h2>
	<div class="potd-meta">
		{#if potd && topic}
			<span class="topic-pill">{topic}</span>
		{:else if !potd}
			<span class="topic-pill">Today's challenge</span>
		{/if}
		<p class="countdown">
			Resets in <span>{timeUntilMidnight || '--:--:--'}</span>
		</p>
	</div>
	<Button
		href={potd ? resolve('/ide/[id]?src=potd', { id: potd.id }) : resolve('/potd')}
		class="mt-4"
	>
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
		margin-bottom: 16px;
		font-size: 1.125rem;
		font-weight: 700;
	}

	.countdown {
		color: var(--muted-foreground);
		font-size: 0.875rem;
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
