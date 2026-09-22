<script lang="ts">
	import { Badge } from '$components/ui/badge';
	import { tierForRating, type RatingTier } from '$processes/rating/rating-math';

	let { rating }: { rating: number } = $props();

	let tier = $derived<RatingTier>(tierForRating(rating));

	// Placeholder colors only -- potd-rating-system-spec.md §6 explicitly
	// scopes the real badge/ring visual design (colors, shape, share-card)
	// out of this spec as "a separate design task." This is just enough to
	// make the tiers visually distinct today.
	const colorClass: Record<string, string> = {
		'Hello World': 'text-slate-600 dark:text-slate-400 border-slate-600/30',
		'Segfault Survivor': 'text-green-600 dark:text-green-400 border-green-600/30',
		'Knight of the Kernel': 'text-blue-600 dark:text-blue-400 border-blue-600/30',
		'Ace of Attention': 'text-purple-600 dark:text-purple-400 border-purple-600/30',
		'Conqueror of CUDA': 'text-orange-600 dark:text-orange-400 border-orange-600/30',
		Singularity: 'text-red-600 dark:text-red-400 border-red-600/30'
	};
</script>

<div class="flex items-center gap-2">
	<span class="font-mono text-2xl font-bold tabular-nums">{rating}</span>
	<Badge variant="outline" class="font-mono text-xs {colorClass[tier.name]}">
		{tier.name}
	</Badge>
</div>
