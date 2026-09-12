<script lang="ts">
	import { Terminal, Trash2, Copy, Check } from '@lucide/svelte';

	let { output = '', onClear = () => {} } = $props<{
		output: string;
		onClear?: () => void;
	}>();

	let copied = $state(false);

	async function copyOutput() {
		if (!output) return;
		try {
			await navigator.clipboard.writeText(output);
			copied = true;
			setTimeout(() => (copied = false), 2000);
		} catch (e) {
			console.error('Failed to copy', e);
		}
	}
</script>

<div class="flex h-full flex-col bg-background font-mono text-xs text-foreground">
	<!-- Console Header -->
	<div class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3">
		<div
			class="flex items-center gap-1.5 text-[11px] tracking-wider text-muted-foreground uppercase"
		>
			<Terminal class="size-3" />
			<span>Console Output</span>
		</div>
		<div class="flex items-center gap-1">
			<button
				type="button"
				class="flex size-6 items-center justify-center text-muted-foreground transition-colors hover:text-foreground"
				title="Copy Output"
				onclick={copyOutput}
			>
				{#if copied}
					<Check class="size-3 text-foreground" />
				{:else}
					<Copy class="size-3" />
				{/if}
			</button>
			<button
				type="button"
				class="flex size-6 items-center justify-center text-muted-foreground transition-colors hover:text-foreground"
				title="Clear Console"
				onclick={onClear}
			>
				<Trash2 class="size-3" />
			</button>
		</div>
	</div>

	<!-- Output Body -->
	<div class="flex-1 overflow-auto p-3 text-xs leading-relaxed">
		{#if output}
			<pre class="font-mono whitespace-pre-wrap text-foreground/80 select-text">{output}</pre>
		{:else}
			<div class="flex h-full items-center justify-center text-muted-foreground italic">
				Click "Run Code" or press Shift+Enter to execute
			</div>
		{/if}
	</div>
</div>
