<script lang="ts">
	type Tone = 'neutral' | 'positive';

	let {
		label,
		value,
		tone = 'neutral'
	}: {
		label: string;
		value: string | number;
		/** 'positive' reuses the brand accent color -- spent only on the stat
		 * that's actually good news, never on a neutral count. */
		tone?: Tone;
	} = $props();

	const toneClass: Record<Tone, string> = {
		neutral: 'text-foreground',
		positive: 'text-primary'
	};
</script>

<div class="rounded-xl border border-border p-4">
	<p class="font-mono text-3xl font-bold tabular-nums {toneClass[tone]}">
		{value}
	</p>
	<p class="mt-1 text-xs text-foreground">{label}</p>
</div>
