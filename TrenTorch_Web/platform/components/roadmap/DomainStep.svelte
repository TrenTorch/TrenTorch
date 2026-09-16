<script lang="ts">
	import { domainDefs, comingSoonDomains } from '$data/roadmap-domains';

	let {
		selectedIds,
		onToggle
	}: {
		selectedIds: Set<string>;
		onToggle: (id: string) => void;
	} = $props();
</script>

<div class="grid gap-3 sm:grid-cols-2">
	{#each domainDefs as domain (domain.id)}
		<button
			type="button"
			onclick={() => onToggle(domain.id)}
			aria-pressed={selectedIds.has(domain.id)}
			class="rounded-md border p-4 text-left transition-colors {selectedIds.has(domain.id)
				? 'border-primary bg-primary/5'
				: 'border-border hover:border-foreground/30'}"
		>
			<span class="block font-semibold">{domain.name}</span>
			<span class="block text-sm text-muted-foreground">{domain.description}</span>
		</button>
	{/each}
	{#each comingSoonDomains as domain (domain.name)}
		<div class="cursor-not-allowed rounded-md border border-border p-4 text-left opacity-40">
			<span class="block font-semibold">{domain.name}</span>
			<span class="block text-sm text-muted-foreground">{domain.description}</span>
		</div>
	{/each}
</div>
