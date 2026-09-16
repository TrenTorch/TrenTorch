<script lang="ts">
	import { Check } from '@lucide/svelte';
	import { curriculum } from '$data/questions';
	import type { RoadmapPartEntry } from '$processes/roadmap/active-roadmap.svelte';

	let {
		title,
		parts,
		mastered
	}: {
		title: string;
		parts: RoadmapPartEntry[];
		mastered: boolean;
	} = $props();

	const partTitle = (partId: string) => curriculum.find((p) => p.id === partId)?.title ?? partId;
	const partCount = (partId: string) => {
		const part = curriculum.find((p) => p.id === partId);
		return part ? part.tracks.reduce((sum, t) => sum + t.questions.length, 0) : 0;
	};

	// The first non-skipped Part is where the student actually starts.
	const firstActiveIndex = $derived(parts.findIndex((p) => !p.skipped));
</script>

<div>
	<p class="mb-1 text-xs text-muted-foreground uppercase">Your roadmap</p>
	<h2 class="mb-1 text-xl font-bold">{title}</h2>
	<p class="mb-6 text-sm text-muted-foreground">
		Built from your quiz results and what you selected.
		{#if mastered}
			Starting past Math &amp; Statistics for ML since your placement quiz showed mastery.
		{/if}
	</p>

	<div class="space-y-1">
		{#each parts as part, i (part.partId)}
			<div class="flex items-center gap-3 py-2">
				<span
					class="flex size-7 shrink-0 items-center justify-center rounded-full text-xs font-semibold {part.skipped
						? 'border border-border bg-secondary text-muted-foreground'
						: i === firstActiveIndex
							? 'bg-primary text-primary-foreground'
							: 'border border-border bg-secondary text-muted-foreground'}"
				>
					{#if part.skipped}
						<Check class="size-3.5" />
					{:else}
						{i + 1}
					{/if}
				</span>
				<span class="text-sm font-medium">{partTitle(part.partId)}</span>
				<span class="text-xs text-muted-foreground">
					{#if part.skipped}
						&middot; skipped, quiz showed mastery
					{:else}
						&middot; {partCount(part.partId)} questions{i === firstActiveIndex
							? ' · start here'
							: ''}
					{/if}
				</span>
			</div>
		{/each}
	</div>
</div>
