<script lang="ts">
	type Tone = 'neutral' | 'positive';

	let {
		label,
		value,
		tone = 'neutral'
	}: {
		label: string;
		value: string | number;
		/** 'positive' reuses the same green DifficultyBadge/DifficultyChart use
		 * for "Easy"/solved -- the one semantic accent this monochrome design
		 * system has, spent only on the stat that's actually good news. */
		tone?: Tone;
	} = $props();

	const toneClass: Record<Tone, string> = {
		neutral: 'text-foreground',
		positive: 'text-green-600 dark:text-green-400'
	};
</script>

<div class="rounded-md border border-border p-4">
	<p class="font-mono text-3xl font-bold tabular-nums {toneClass[tone]}">
		{value}
	</p>
	<p class="mt-1 text-xs text-muted-foreground">{label}</p>
</div>
