<script lang="ts">
	import { Check, Copy } from '@lucide/svelte';

	let { text, class: className = '' }: { text: string; class?: string } = $props();
	let copied = $state(false);

	async function handleCopy() {
		try {
			await navigator.clipboard.writeText(text);
			copied = true;
			setTimeout(() => (copied = false), 1500);
		} catch {
			// Clipboard API unavailable (non-HTTPS, permission denied, etc.):
			// fail quietly rather than throw in the UI.
		}
	}
</script>

<button
	type="button"
	onclick={handleCopy}
	aria-label={copied ? 'Copied' : 'Copy to clipboard'}
	class="inline-flex h-7 w-7 items-center justify-center rounded-sm border border-border bg-background/80 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground {className}"
>
	{#if copied}
		<Check class="size-3.5" />
	{:else}
		<Copy class="size-3.5" />
	{/if}
</button>
