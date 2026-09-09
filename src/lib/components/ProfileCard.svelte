<script lang="ts">
	import * as Avatar from '$lib/components/ui/avatar';

	let { name, avatarUrl }: { name: string; avatarUrl?: string } = $props();

	const initials = $derived(
		name
			.split(' ')
			.map((part) => part[0])
			.join('')
			.slice(0, 2)
			.toUpperCase()
	);
</script>

<div class="flex items-center gap-3">
	<Avatar.Root>
		{#if avatarUrl}
			<Avatar.Image src={avatarUrl} alt={name} />
		{/if}
		<Avatar.Fallback class="font-mono">{initials}</Avatar.Fallback>
	</Avatar.Root>
	<span class="font-mono font-medium">{name}</span>
</div>
