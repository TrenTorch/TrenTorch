<script lang="ts">
	import { Badge } from '$components/ui/badge';
	import { Building2 } from '@lucide/svelte';
	import type { CompanyTag } from '$data/questions';

	let { companies }: { companies: CompanyTag } = $props();

	// Keeps the row compact -- the full list (and the role context) is
	// always available via the title tooltip, this is just a preview.
	const PREVIEW_COUNT = 2;
	const previewNames = $derived(companies.names.slice(0, PREVIEW_COUNT).join(', '));
	const remainingCount = $derived(companies.names.length - PREVIEW_COUNT);
	const tooltip = $derived(`${companies.names.join(', ')} — ${companies.roles}`);
</script>

<Badge
	variant="outline"
	class="inline-flex items-center gap-1 font-mono text-xs text-sky-600 dark:text-sky-400 border-sky-600/30"
	title={tooltip}
>
	<Building2 class="size-3" />
	{previewNames}{#if remainingCount > 0}
		+{remainingCount}
	{/if}
</Badge>
