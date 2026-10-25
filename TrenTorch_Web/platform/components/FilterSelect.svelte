<script lang="ts">
	import type { Component } from 'svelte';
	import * as Select from '$components/ui/select';

	type Option = { value: string; label: string };

	// An empty string is "no filter" on the pages that use this; the list itself needs a real value.
	const NONE = '__none__';

	let {
		value = $bindable(''),
		options,
		label,
		icon: Icon,
		class: className = ''
	}: {
		value: string;
		options: Option[];
		label: string;
		icon?: Component<{ class?: string }>;
		class?: string;
	} = $props();

	const shown = $derived(options.find((option) => option.value === value)?.label ?? '');
</script>

<Select.Root
	type="single"
	value={value === '' ? NONE : value}
	onValueChange={(next) => (value = next === NONE ? '' : next)}
>
	<Select.Trigger
		aria-label={label}
		class="press h-[38px] w-auto gap-2 rounded-md border-border bg-secondary px-3 text-[0.78rem] hover:bg-muted dark:bg-secondary dark:hover:bg-muted {className}"
	>
		<span class="flex items-center gap-2">
			{#if Icon}<Icon class="size-4 text-muted-foreground" />{/if}
			{shown}
		</span>
	</Select.Trigger>
	<Select.Content class="min-w-(--bits-select-anchor-width)">
		{#each options as option (option.value)}
			<Select.Item value={option.value === '' ? NONE : option.value} label={option.label} />
		{/each}
	</Select.Content>
</Select.Root>
