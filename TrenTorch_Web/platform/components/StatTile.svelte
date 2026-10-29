<script lang="ts">
	type Tone = 'neutral' | 'positive';

	let {
		label,
		value,
		tone = 'neutral',
		progress,
		progressLabel = 'solved'
	}: {
		label: string;
		value: string | number;
		/** 'positive' reuses the brand accent color -- spent only on the stat
		 * that's actually good news, never on a neutral count. */
		tone?: Tone;
		/**
		 * How many of `total` are solved. Shown as a bar and "N solved" once there is at least one, and not
		 * at all before that, so a fresh account just sees the count.
		 */
		progress?: { done: number; total: number };
		/** What the bar counts, after the number: "45 solved", "2 complete". */
		progressLabel?: string;
	} = $props();

	const toneClass: Record<Tone, string> = {
		neutral: 'text-foreground',
		positive: 'text-primary'
	};
</script>

<div class="h-full rounded-xl border border-border p-4">
	<p class="font-mono text-3xl font-bold tabular-nums {toneClass[tone]}">
		{value}
	</p>
	<p class="mt-1 text-xs text-foreground">{label}</p>
	{#if progress && progress.done > 0}
		<div
			class="mt-3 h-1.5 overflow-hidden rounded-full bg-border"
			role="progressbar"
			aria-label="{label} {progressLabel}"
			aria-valuemin={0}
			aria-valuemax={progress.total}
			aria-valuenow={progress.done}
		>
			<span
				class="block h-full rounded-full bg-[#3fb950] transition-[width] duration-200"
				style="width: {progress.total ? (progress.done / progress.total) * 100 : 0}%"
			></span>
		</div>
		<p class="mt-1.5 font-mono text-[11px] text-muted-foreground tabular-nums">
			{progress.done}
			{progressLabel}
		</p>
	{/if}
</div>
