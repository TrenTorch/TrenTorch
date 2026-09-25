<script lang="ts">
	import { session } from '$processes/auth/session.svelte';
	import {
		fetchRatingHistory,
		type RatingHistoryPoint
	} from '$processes/rating/supabase-rating-store';
	import { LineChart, Spline } from 'layerchart';
	import * as Chart from '$components/ui/chart';
	import type { ChartConfig } from '$components/ui/chart';
	import * as Card from '$components/ui/card';
	import { RATING_TIERS } from '$processes/rating/rating-math';

	let history = $state<RatingHistoryPoint[] | null>(null);
	let loading = $state(true);

	// A public profile passes the person being viewed; otherwise it is the signed-in user.
	let { userId: viewedId }: { userId?: string } = $props();
	const userId = $derived(viewedId ?? session.user?.id ?? null);

	$effect(() => {
		const id = userId;
		if (!id) return;
		loading = true;
		fetchRatingHistory(id).then((rows) => {
			if (userId !== id) return;
			history = rows;
			loading = false;
		});
	});

	// Same hues as RatingBadge, drawn as faint background bands.
	const bandColor: Record<string, string> = {
		'Hello World': '#64748b',
		'Segfault Survivor': '#16a34a',
		'Knight of the Kernel': '#2563eb',
		'Ace of Attention': '#9333ea',
		'Conqueror of CUDA': '#ea580c',
		Singularity: '#dc2626'
	};

	// Codeforces-style axis: every tier gets the same height, so the chart is
	// drawn in "tier units" (whole number = a tier floor) and mapped back to
	// ratings for labels and the tooltip.
	const SINGULARITY_SPAN = 500;
	const tierPos = (rating: number) => {
		const k = RATING_TIERS.findLastIndex((t) => rating >= t.min);
		const tier = RATING_TIERS[Math.max(k, 0)];
		const span = (tier.max ?? tier.min + SINGULARITY_SPAN) - tier.min;
		return Math.max(k, 0) + Math.min((rating - tier.min) / span, 0.999);
	};

	const points = $derived.by(() => {
		if (!history || history.length === 0) return [];
		return [
			{ i: 0, rating: history[0].ratingBefore, event: undefined as RatingHistoryPoint | undefined },
			...history.map((event, n) => ({ i: n + 1, rating: event.ratingAfter, event }))
		].map((p) => ({ ...p, pos: tierPos(p.rating) }));
	});

	const tierRange = $derived.by(() => {
		const positions = points.map((p) => p.pos);
		const lo = Math.floor(Math.min(...positions));
		const hi = Math.min(Math.floor(Math.max(...positions)) + 2, RATING_TIERS.length);
		return { lo, hi };
	});

	const visibleTiers = $derived(
		RATING_TIERS.slice(tierRange.lo, tierRange.hi).map((tier, n) => ({
			...tier,
			low: tierRange.lo + n,
			high: tierRange.lo + n + 1
		}))
	);
	const tierTicks = $derived(
		Array.from({ length: tierRange.hi - tierRange.lo + 1 }, (_, n) => tierRange.lo + n)
	);

	const chartConfig = {
		rating: { label: 'Rating', color: '#e9b93a' }
	} satisfies ChartConfig;

	const chartProps = $derived({
		xAxis: {
			ticks: [0, points.length - 1],
			format: (v: number) => (v === 0 ? '' : formatDate(history?.[v - 1]?.date ?? ''))
		},
		yAxis: {
			ticks: tierTicks,
			format: (v: number) => String(RATING_TIERS[v]?.min ?? '')
		}
	});

	const tipLabel = (v: unknown) => {
		const event = history?.[Number(v) - 1];
		return event
			? `${event.ratingAfter} (${event.delta >= 0 ? '+' : ''}${event.delta}) ${formatDate(event.date)}`
			: 'Start';
	};

	const formatDate = (iso: string) =>
		new Date(iso + 'T00:00:00').toLocaleDateString('en', { month: 'short', day: 'numeric' });

	const last = $derived(history?.[history.length - 1]);
	const peak = $derived(history ? Math.max(...history.map((h) => h.ratingAfter)) : 0);
</script>

{#if userId}
	<Card.Root class="rounded-2xl border border-foreground bg-transparent p-0 ring-0">
		<Card.Header class="px-6 pt-6">
			<Card.Title class="font-mono font-semibold">Rating history</Card.Title>
			<Card.Description>
				Every Problem of the Day you finish moves your rating. Bands are the rating tiers.
			</Card.Description>
		</Card.Header>
		<Card.Content class="px-6 pb-6">
			{#if loading}
				<p class="text-sm text-muted-foreground">Loading your rating history...</p>
			{:else if history === null}
				<p class="text-sm text-muted-foreground">Rating history is not available right now.</p>
			{:else if history.length === 0}
				<p class="text-sm text-muted-foreground">
					No rated Problem of the Day yet. Solve the daily problem and your graph starts here.
				</p>
			{:else}
				<div class="mb-3 flex flex-wrap gap-x-6 gap-y-1 font-mono text-xs text-muted-foreground">
					<span>Current <b class="text-foreground tabular-nums">{last?.ratingAfter}</b></span>
					<span>Peak <b class="text-foreground tabular-nums">{peak}</b></span>
					<span>Rated days <b class="text-foreground tabular-nums">{history.length}</b></span>
				</div>
				<Chart.Container config={chartConfig} class="aspect-auto h-44 w-full">
					<LineChart
						data={points}
						x="i"
						xDomain={[0, points.length - 1]}
						y="pos"
						yDomain={[tierRange.lo, tierRange.hi]}
						series={[{ key: 'pos', label: 'Rating', color: '#e9b93a' }]}
						padding={{ left: 36, right: 8, top: 6, bottom: 18 }}
						props={chartProps}
					>
						{#snippet marks({ context })}
							{#each visibleTiers as tier (tier.name)}
								<rect
									x={0}
									y={context.yScale(tier.high)}
									width={context.width}
									height={context.yScale(tier.low) - context.yScale(tier.high)}
									fill={bandColor[tier.name]}
									fill-opacity="0.45"
								/>
								<text
									x={context.width - 6}
									y={context.yScale(tier.high) + 11}
									text-anchor="end"
									font-size="9"
									fill="currentColor"
									fill-opacity="0.75">{tier.name}</text
								>
							{/each}
							<Spline seriesKey="pos" />
							{#each points as point (point.i)}
								<circle
									cx={context.xScale(point.i)}
									cy={context.yScale(point.pos)}
									r="2.5"
									fill="#e9b93a"
									stroke="white"
									stroke-width="1.25"
								/>
							{/each}
						{/snippet}
						{#snippet tooltip()}
							<Chart.Tooltip labelFormatter={tipLabel} hideIndicator>
								{#snippet formatter({ value })}
									<span class="text-muted-foreground">
										{RATING_TIERS[Math.floor(Number(value))]?.name}
									</span>
								{/snippet}
							</Chart.Tooltip>
						{/snippet}
					</LineChart>
				</Chart.Container>
			{/if}
		</Card.Content>
	</Card.Root>
{/if}
