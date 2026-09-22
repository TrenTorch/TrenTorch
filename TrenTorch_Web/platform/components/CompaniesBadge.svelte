<script lang="ts">
	import { Badge } from '$components/ui/badge';
	import { Building2 } from '@lucide/svelte';

	// A single company name -- withCompanies (data/questions.ts) hands each
	// question exactly one name from its Part's pool, round-robin, instead
	// of stamping the whole pool onto every question. One specific name per
	// question reads as a real, exclusive-feeling data point; a badge
	// listing "NVIDIA, Meta +6" on every question in a Part reads as "this
	// was asked everywhere," which is both untrue and forgettable.
	let { company }: { company: { name: string; roles: string } } = $props();
	const tooltip = $derived(company.roles);
</script>

<Badge
	variant="outline"
	class="inline-flex items-center gap-1 border-sky-600/30 font-mono text-xs text-sky-600 dark:text-sky-400"
	title={tooltip}
>
	<Building2 class="size-3" />
	{company.name}
</Badge>
