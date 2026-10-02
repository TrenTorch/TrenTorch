<script lang="ts">
	/* eslint-disable svelte/prefer-svelte-reactivity -- throwaway Dates for calendar math, never stored in state */
	import { session } from '$processes/auth/session.svelte';
	import { fetchSolvedDates } from '$processes/progress-tracking/supabase-solved-store';
	import * as Card from '$components/ui/card';

	const WEEKS = 53;
	const CELL = 11;
	const GAP = 3;
	const STEP = CELL + GAP;
	const LEFT = 28;
	const TOP = 16;

	let dates = $state<string[] | null>(null);
	let loading = $state(true);
	let hovered = $state<{ key: string; count: number } | null>(null);

	// A public profile passes the person being viewed; otherwise it is the signed-in user.
	let { userId: viewedId }: { userId?: string } = $props();
	const userId = $derived(viewedId ?? session.user?.id ?? null);

	// Local calendar day, so a solve at 11pm lands on the day the person saw.
	const dayKey = (d: Date) =>
		`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

	$effect(() => {
		const id = userId;
		if (!id) return;
		loading = true;
		fetchSolvedDates(id).then((rows) => {
			if (userId !== id) return;
			dates = rows;
			loading = false;
		});
	});

	const counts = $derived.by(() => {
		const map = new Map<string, number>();
		for (const iso of dates ?? []) {
			const key = dayKey(new Date(iso));
			map.set(key, (map.get(key) ?? 0) + 1);
		}
		return map;
	});

	// Columns are weeks (Sunday first), the last column ends on today.
	const grid = $derived.by(() => {
		const today = new Date();
		today.setHours(0, 0, 0, 0);
		const start = new Date(today);
		start.setDate(today.getDate() - today.getDay() - (WEEKS - 1) * 7);
		const cells: { key: string; count: number; week: number; day: number; future: boolean }[] = [];
		for (let week = 0; week < WEEKS; week++) {
			for (let day = 0; day < 7; day++) {
				const d = new Date(start);
				d.setDate(start.getDate() + week * 7 + day);
				const key = dayKey(d);
				cells.push({ key, count: counts.get(key) ?? 0, week, day, future: d > today });
			}
		}
		const months: { label: string; week: number }[] = [];
		let lastMonth = -1;
		for (let week = 0; week < WEEKS; week++) {
			const d = new Date(start);
			d.setDate(start.getDate() + week * 7);
			if (d.getMonth() !== lastMonth && (week === 0 || d.getDate() <= 7)) {
				months.push({ label: d.toLocaleDateString('en', { month: 'short' }), week });
				lastMonth = d.getMonth();
			}
		}
		return { cells, months };
	});

	const shownCells = $derived(grid.cells.filter((c) => !c.future));
	const total = $derived(shownCells.reduce((sum, c) => sum + c.count, 0));
	const activeDays = $derived(shownCells.filter((c) => c.count > 0).length);
	const longestStreak = $derived.by(() => {
		let best = 0;
		let run = 0;
		for (const c of shownCells) {
			run = c.count > 0 ? run + 1 : 0;
			best = Math.max(best, run);
		}
		return best;
	});

	const level = (count: number) =>
		count === 0 ? 0 : count === 1 ? 1 : count <= 3 ? 2 : count <= 5 ? 3 : 4;
	const fill = [
		'var(--muted)',
		...[30, 50, 75, 100].map((p) => `color-mix(in oklab, var(--primary) ${p}%, transparent)`)
	];

	const width = LEFT + WEEKS * STEP;
	const height = TOP + 7 * STEP;

	const formatDay = (key: string) =>
		new Date(key + 'T00:00:00').toLocaleDateString('en', {
			weekday: 'short',
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		});
</script>

{#if userId}
	<Card.Root class="rounded-2xl border border-border bg-transparent p-0 ring-0">
		<Card.Header class="px-6 pt-6">
			<Card.Title class="font-mono font-semibold">Activity</Card.Title>
			<Card.Description>Questions you solved each day over the past year.</Card.Description>
		</Card.Header>
		<Card.Content class="px-6 pb-6">
			{#if loading}
				<p class="text-sm text-muted-foreground">Loading your activity...</p>
			{:else if dates === null}
				<p class="text-sm text-muted-foreground">Activity is not available right now.</p>
			{:else}
				<div class="mb-3 flex flex-wrap gap-x-6 gap-y-1 font-mono text-xs text-muted-foreground">
					<span>Solved <b class="text-foreground tabular-nums">{total}</b></span>
					<span>Active days <b class="text-foreground tabular-nums">{activeDays}</b></span>
					<span>Longest streak <b class="text-foreground tabular-nums">{longestStreak}</b></span>
				</div>

				<svg
					viewBox="0 0 {width} {height}"
					class="h-auto w-full"
					role="img"
					aria-label="Contribution graph: {total} questions solved in the past year on {activeDays} days"
					onpointerleave={() => (hovered = null)}
				>
					{#each grid.months as month (month.week)}
						<text
							x={LEFT + month.week * STEP}
							y={9}
							font-size="9"
							fill="currentColor"
							fill-opacity="0.6">{month.label}</text
						>
					{/each}
					{#each [1, 3, 5] as day (day)}
						<text
							x={0}
							y={TOP + day * STEP + CELL - 1}
							font-size="9"
							fill="currentColor"
							fill-opacity="0.6">{['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][day]}</text
						>
					{/each}
					{#each shownCells as cell (cell.key)}
						<rect
							x={LEFT + cell.week * STEP}
							y={TOP + cell.day * STEP}
							width={CELL}
							height={CELL}
							rx="2.5"
							fill={fill[level(cell.count)]}
							stroke={hovered?.key === cell.key ? 'currentColor' : 'none'}
							role="presentation"
							onpointerenter={() => (hovered = { key: cell.key, count: cell.count })}
						/>
					{/each}
				</svg>

				<div class="mt-2 flex items-center justify-between gap-4">
					<p class="min-h-5 font-mono text-xs text-muted-foreground" aria-live="polite">
						{#if hovered}
							<span class="text-foreground tabular-nums">{hovered.count}</span>
							{hovered.count === 1 ? 'question' : 'questions'} on {formatDay(hovered.key)}
						{:else}
							Hover a square to see that day.
						{/if}
					</p>
					<div class="flex items-center gap-1 font-mono text-xs text-muted-foreground">
						Less
						{#each fill as color, i (i)}
							<span class="size-2.5 rounded-[3px]" style="background: {color}"></span>
						{/each}
						More
					</div>
				</div>
			{/if}
		</Card.Content>
	</Card.Root>
{/if}
