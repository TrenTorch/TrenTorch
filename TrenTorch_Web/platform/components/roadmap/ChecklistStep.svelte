<script lang="ts">
	let {
		items,
		noneLabel,
		checked,
		onToggle
	}: {
		items: string[];
		noneLabel: string;
		checked: Set<string>;
		onToggle: (item: string) => void;
	} = $props();
</script>

<div class="flex flex-col gap-2">
	{#each items as item (item)}
		<button
			type="button"
			onclick={() => onToggle(item)}
			aria-pressed={checked.has(item)}
			class="flex items-center gap-3 rounded-md border px-4 py-2.5 text-left text-sm transition-colors {checked.has(
				item
			)
				? 'border-primary bg-primary/5'
				: 'border-border hover:border-foreground/30'}"
		>
			<span
				class="flex size-4 shrink-0 items-center justify-center rounded-[4px] border {checked.has(
					item
				)
					? 'border-primary bg-primary text-primary-foreground'
					: 'border-input'}"
			>
				{#if checked.has(item)}&check;{/if}
			</span>
			{item}
		</button>
	{/each}
	<button
		type="button"
		onclick={() => onToggle(noneLabel)}
		aria-pressed={checked.has(noneLabel)}
		class="rounded-md border border-dashed px-4 py-2.5 text-left text-sm text-muted-foreground transition-colors {checked.has(
			noneLabel
		)
			? 'border-solid border-primary bg-primary/5 text-foreground'
			: 'border-border hover:border-foreground/30'}"
	>
		{noneLabel}
	</button>
</div>
