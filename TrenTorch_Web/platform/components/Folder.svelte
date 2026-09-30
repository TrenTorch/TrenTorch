<script lang="ts">
	import type { Snippet } from 'svelte';
	import { ChevronDown } from '@lucide/svelte';
	import { collapsedSections } from '$processes/progress-tracking/collapsed-sections.svelte';

	let {
		id,
		title,
		count,
		level,
		defaultOpen = false,
		forceOpen = false,
		children
	}: {
		id: string;
		title: string;
		count: number;
		/** 0 = root, 1 = section: only changes the styling. */
		level: 0 | 1;
		defaultOpen?: boolean;
		/** Keeps the folder open regardless of the saved state (used while filtering). */
		forceOpen?: boolean;
		children: Snippet;
	} = $props();

	const open = $derived(forceOpen || collapsedSections.isOpen(id, defaultOpen));
</script>

<div
	class={level === 0 ? 'overflow-hidden rounded-md border border-border' : 'border-t border-border'}
>
	<button
		type="button"
		onclick={() => collapsedSections.toggle(id)}
		class="flex w-full items-center justify-between px-4 text-left transition-colors hover:bg-secondary {level ===
		0
			? 'py-3'
			: 'bg-secondary/40 py-2.5'}"
		aria-expanded={open}
	>
		{#if level === 0}
			<h3 class="font-mono font-semibold">{title}</h3>
		{:else}
			<h4 class="font-mono text-sm font-semibold">{title}</h4>
		{/if}
		<span class="flex items-center gap-2 text-xs text-muted-foreground">
			{count} questions
			<ChevronDown class="size-4 transition-transform {open ? '' : '-rotate-90'}" />
		</span>
	</button>
	{#if open}
		{@render children()}
	{/if}
</div>
