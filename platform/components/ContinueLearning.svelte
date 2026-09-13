<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowRight } from '@lucide/svelte';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import { findQuestionBySlug } from '$lib/data/questions';
	import { solved } from '$lib/stores/solved.svelte';
	import { attempted } from '$lib/stores/attempted.svelte';

	const MAX_ITEMS = 6;

	// attempted is additive-only and never drops a slug once solved, so
	// "in progress" is the set difference against solved, not attempted on
	// its own. Set iteration order is insertion order (oldest first);
	// reversed so the most recently attempted question surfaces first --
	// that's the one actually worth resuming.
	const items = $derived(
		[...attempted.slugs]
			.filter((slug) => !solved.isSolved(slug))
			.reverse()
			.map((slug) => findQuestionBySlug(slug))
			.filter((item) => item !== undefined)
			.slice(0, MAX_ITEMS)
	);
</script>

{#if items.length > 0}
	<div class="space-y-1">
		{#each items as item (item.question.slug)}
			<a
				href={resolve('/ide/[id]', { id: item.question.slug })}
				class="group flex items-center justify-between gap-3 rounded px-2 py-2 transition-colors hover:bg-secondary"
			>
				<div class="min-w-0">
					<p class="truncate font-mono text-sm">{item.question.title}</p>
					<p class="truncate text-xs text-muted-foreground">
						{item.partTitle} &middot; {item.trackName}
					</p>
				</div>
				<div class="flex shrink-0 items-center gap-2">
					<DifficultyBadge difficulty={item.question.difficulty} />
					<ArrowRight
						class="size-4 text-muted-foreground transition-transform group-hover:translate-x-0.5"
					/>
				</div>
			</a>
		{/each}
	</div>
{:else}
	<p class="text-sm text-muted-foreground">
		Nothing in progress yet. <a href={resolve('/questions')} class="underline hover:text-foreground"
			>Pick a question</a
		> to get started.
	</p>
{/if}
