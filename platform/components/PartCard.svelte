<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowRight, type LucideIcon } from '@lucide/svelte';
	import { Progress } from '$components/ui/progress';

	let {
		id,
		title,
		icon: Icon,
		questionCount,
		solved,
		total
	}: {
		id: string;
		title: string;
		icon: LucideIcon;
		questionCount: number;
		/** Real solved/total for THIS part, used to decide the in-progress
		 * highlight -- omit (or leave both 0) when there's no signed-in
		 * student progress to show yet. */
		solved: number;
		total: number;
	} = $props();

	// "In progress" (not just started, not finished either) is the one state
	// worth visually calling out on a track-picker: it's the part a
	// returning student most likely wants to jump straight back into.
	const inProgress = $derived(solved > 0 && solved < total);
</script>

<a
	href={resolve('/questions/[partId]', { partId: id })}
	class="group flex items-center gap-4 rounded-md border px-5 py-4 transition-colors {inProgress
		? 'border-primary/60'
		: 'border-border hover:border-foreground/30'}"
>
	<span
		class="flex size-10 shrink-0 items-center justify-center rounded-md border border-border bg-secondary"
	>
		<Icon class="size-4.5 text-foreground/80" aria-hidden="true" />
	</span>
	<span class="min-w-0 flex-1">
		<span class="block font-semibold">{title}</span>
		<span class="block text-xs text-muted-foreground">
			{questionCount} question{questionCount === 1 ? '' : 's'}
			{#if solved > 0}
				&middot; {solved} done
			{/if}
		</span>
		{#if inProgress}
			<Progress value={solved} max={total} class="mt-2 h-1 max-w-52" />
		{/if}
	</span>
	<ArrowRight
		class="size-4 shrink-0 text-muted-foreground transition-transform group-hover:translate-x-0.5 group-hover:text-primary"
		aria-hidden="true"
	/>
</a>
