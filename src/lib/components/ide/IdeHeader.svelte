<script lang="ts">
	import { resolve } from '$app/paths';
	import type { QuestionContent, RuntimeState } from '$lib/curriculum/types';
	import {
		ArrowLeft,
		ListChecks,
		Play,
		CloudUpload,
		RotateCcw,
		RefreshCcw,
		Maximize,
		Minimize,
		Loader2
	} from '@lucide/svelte';

	let {
		content,
		runtimeState = 'ready',
		isRunning = false,
		isFullscreen = false,
		onResetCode = () => {},
		onReattempt = () => {},
		onRunCode = () => {},
		onRunTests = () => {},
		onToggleFullscreen = () => {}
	} = $props<{
		content: QuestionContent;
		runtimeState: RuntimeState;
		isRunning: boolean;
		isFullscreen?: boolean;
		onResetCode?: () => void;
		onReattempt?: () => void;
		onRunCode?: () => void;
		onRunTests?: () => void;
		onToggleFullscreen?: () => void;
	}>();

	let isBusy = $derived(
		isRunning || runtimeState === 'loading_runtime' || runtimeState === 'loading_packages'
	);
</script>

<header
	class="grid h-12 w-full grid-cols-[1fr_auto_1fr] items-center border-b border-border bg-background px-2 font-mono text-xs text-foreground"
>
	<!-- Left: back to Questions -->
	<div class="flex items-center gap-1 justify-self-start">
		<a
			href={resolve('/questions')}
			class="flex items-center gap-1.5 rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
			title="Back to Questions"
		>
			<ArrowLeft class="size-4" />
		</a>
		<div class="h-4 w-px bg-border"></div>
		<a
			href={resolve('/questions')}
			class="flex items-center gap-1.5 rounded px-2 py-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
		>
			<ListChecks class="size-3.5" />
			<span class="hidden truncate sm:inline">{content.metadata.title}</span>
		</a>
	</div>

	<!-- Center: Run / Submit -->
	<div class="flex items-center gap-2 justify-self-center">
		<button
			type="button"
			class="flex items-center gap-1.5 rounded-full border border-border bg-secondary px-3.5 py-1.5 font-medium text-foreground transition-colors hover:border-foreground/30 hover:bg-muted disabled:pointer-events-none disabled:opacity-40"
			disabled={isRunning}
			onclick={onRunCode}
			title="Run code (Shift+Enter)"
		>
			{#if isBusy}
				<Loader2 class="size-3.5 animate-spin" />
			{:else}
				<Play class="size-3 fill-current" />
			{/if}
			<span>Run</span>
		</button>

		<button
			type="button"
			class="flex items-center gap-1.5 rounded-full bg-emerald-600 px-3.5 py-1.5 font-medium text-white shadow-sm transition-colors hover:bg-emerald-500 disabled:pointer-events-none disabled:opacity-40 dark:bg-emerald-500 dark:hover:bg-emerald-400"
			disabled={isRunning}
			onclick={onRunTests}
			title="Run the test suite and submit"
		>
			<CloudUpload class="size-3.5" />
			<span>Submit</span>
		</button>
	</div>

	<!-- Right: Re-attempt / Reset / Fullscreen -->
	<div class="flex items-center gap-1 justify-self-end">
		<button
			type="button"
			class="flex items-center rounded border border-red-500/30 p-1.5 text-red-600 transition-colors hover:bg-red-500/10 dark:text-red-400"
			onclick={onReattempt}
			title="Re-attempt this question: reset to the starter code and mark it unsolved again"
			aria-label="Re-attempt this question"
		>
			<RefreshCcw class="size-3.5" />
		</button>
		<button
			type="button"
			class="rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
			onclick={onResetCode}
			title="Reset code to the original starter template"
		>
			<RotateCcw class="size-3.5" />
		</button>
		<button
			type="button"
			class="rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
			onclick={onToggleFullscreen}
			title={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
		>
			{#if isFullscreen}
				<Minimize class="size-3.5" />
			{:else}
				<Maximize class="size-3.5" />
			{/if}
		</button>
	</div>
</header>
