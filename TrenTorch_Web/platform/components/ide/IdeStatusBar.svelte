<script lang="ts">
	import type { RuntimeState } from '$data/curriculum/types';

	let {
		runtimeState = 'ready',
		runtimeText = '',
		language = 'Python',
		line = 1,
		col = 1,
		saved = false
	} = $props<{
		runtimeState: RuntimeState;
		runtimeText: string;
		language?: string;
		line?: number;
		col?: number;
		saved?: boolean;
	}>();

	const loading = $derived(
		runtimeState === 'loading_runtime' || runtimeState === 'loading_packages'
	);
</script>

<!-- A thin status line under the workbench, like an editor's: what the runtime is
     doing on the left, where the cursor is on the right. -->
<footer
	class="flex h-7 shrink-0 items-center justify-between gap-4 px-4 text-[11px] text-muted-foreground"
>
	<div class="flex min-w-0 items-center gap-4">
		<span class="flex items-center gap-1.5 whitespace-nowrap">
			<span
				class="size-1.5 rounded-full {loading ? 'animate-pulse' : ''}"
				style:background={runtimeState === 'error'
					? 'var(--ide-bad)'
					: loading
						? 'var(--ide-warn)'
						: 'var(--ide-ok)'}
				aria-hidden="true"
			></span>
			<span class="truncate">{runtimeText}</span>
		</span>
		<span class="hidden whitespace-nowrap sm:inline">{language}</span>
	</div>
	<div class="flex items-center gap-4 whitespace-nowrap">
		<span class="tabular-nums">Ln {line}, Col {col}</span>
		{#if saved}
			<span class="text-(--ide-ok)">Saved</span>
		{/if}
	</div>
</footer>
