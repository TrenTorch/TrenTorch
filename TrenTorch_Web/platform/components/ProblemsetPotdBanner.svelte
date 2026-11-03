<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { resolve } from '$app/paths';
	import { ArrowRight, CalendarCheck } from '@lucide/svelte';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import { getTodaysPotd } from '$processes/potd/get-todays-potd';
	import type { PotdSummary } from '$processes/potd/potd-summary';
	import { createPotdCountdown } from '$processes/potd/potd-countdown.svelte';

	let {
		summaries = [],
		onDayChange
	}: { summaries?: PotdSummary[]; onDayChange?: (today: string) => void } = $props();

	const countdown = createPotdCountdown((day) => onDayChange?.(day));

	// No visitor "now" exists when the page is prerendered, so today's problem is only known in the browser.
	// It is looked up from the countdown's day, so the pill changes by itself when the day rolls over.
	const today = $derived(browser && countdown.day ? getTodaysPotd(summaries) : undefined);

	onMount(() => countdown.start());
</script>

<!-- One quiet line, like the pill on the home page, with the clock added. It says what it is and where it
     goes, and nothing more. -->
<a
	href={today ? resolve('/ide/[id]?src=potd', { id: today.question.slug }) : resolve('/potd')}
	class="potd-pill group"
	class:has-title={Boolean(today)}
	aria-label={today
		? `Problem of the Day: ${today.question.title}. Resets in ${countdown.time}`
		: 'Problem of the Day'}
>
	<CalendarCheck class="size-3.5 shrink-0 text-primary" aria-hidden="true" />
	<span class="label">Problem of the Day</span>
	{#if today}
		<span class="title">{today.question.title}</span>
		<DifficultyBadge difficulty={today.question.difficulty} />
	{/if}
	<span class="clock" aria-hidden="true">
		<span class="clock-label">resets in</span>
		<span class="clock-time">{countdown.time || '--:--:--'}</span>
	</span>
	<ArrowRight
		class="size-3.5 shrink-0 transition-transform group-hover:translate-x-0.5"
		aria-hidden="true"
	/>
</a>

<style>
	.potd-pill {
		display: flex;
		width: fit-content;
		max-width: 100%;
		align-items: center;
		gap: 10px;
		border: 1px solid var(--border);
		border-radius: 999px;
		background: color-mix(in srgb, var(--secondary) 55%, transparent);
		padding: 7px 14px;
		color: var(--foreground);
		font-family: var(--font-mono);
		font-size: 0.75rem;
		transition:
			background-color 150ms,
			border-color 150ms;
	}

	.potd-pill:hover {
		border-color: color-mix(in srgb, var(--primary) 45%, var(--border));
		background: var(--secondary);
	}

	.label {
		flex: none;
		color: var(--muted-foreground);
	}

	/* Said once: the label up front, then only the problem. */
	.title {
		min-width: 0;
		overflow: hidden;
		font-weight: 600;
		text-overflow: ellipsis;
		text-transform: uppercase;
		white-space: nowrap;
	}

	.clock {
		display: inline-flex;
		flex: none;
		align-items: baseline;
		gap: 6px;
		border-left: 1px solid var(--border);
		padding-left: 10px;
		color: var(--muted-foreground);
	}

	.clock-time {
		color: var(--foreground);
		font-variant-numeric: tabular-nums;
	}

	@media (max-width: 640px) {
		.potd-pill {
			gap: 8px;
			padding: 7px 12px;
		}

		/* With the problem's name showing there is no room for the label, and the calendar says it. */
		.has-title .label {
			display: none;
		}

		.clock-label {
			display: none;
		}
	}
</style>
