<script lang="ts">
	import { Terminal, Trash2, Copy, Check } from '@lucide/svelte';
	import type { PreviewFigure, SubmissionResult } from '$data/curriculum/types';
	import PlotlyFigure from './PlotlyFigure.svelte';

	let {
		output = '',
		results = null,
		hasError = false,
		figures = [],
		onClear = () => {}
	} = $props<{
		output: string;
		results?: SubmissionResult | null;
		hasError?: boolean;
		figures?: PreviewFigure[];
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

<div class="flex h-full min-h-0 flex-col bg-background text-[13px] text-foreground">
	<!-- Console Header -->
	<div class="flex h-9 shrink-0 items-center justify-between border-b border-border px-4">
		<div class="flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
			<Terminal class="size-3.5" />
			<span>Output</span>
		</div>
		<div class="flex items-center gap-1">
			<button
				type="button"
				class="flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
				title="Copy Output"
				onclick={copyOutput}
			>
				{#if copied}
					<Check class="size-3.5 text-foreground" />
				{:else}
					<Copy class="size-3.5" />
				{/if}
			</button>
			<button
				type="button"
				class="flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
				title="Clear Console"
				onclick={onClear}
			>
				<Trash2 class="size-3.5" />
			</button>
		</div>
	</div>

	<!-- Output Body -->
	<div class="min-h-0 flex-1 overflow-y-auto p-4 text-[13px] leading-relaxed">
		{#if results}
			<section class="mb-3 rounded border border-border p-3">
				<p
					class="font-medium {results.error || results.failedTests > 0
						? 'text-(--ide-bad)'
						: results.totalTests === 0
							? 'text-(--ide-warn)'
							: 'text-(--ide-ok)'}"
				>
					{#if results.error}
						{results.error.includes('SyntaxError') || results.error.includes('IndentationError')
							? 'Python syntax error. The tests could not start.'
							: 'Execution error. The tests could not start.'}
					{:else if results.totalTests === 0}
						No tests ran.
					{:else if results.failedTests > 0}
						{results.passedTests}/{results.totalTests} checks passed; {results.failedTests} failed.
					{:else}
						{results.passedTests}/{results.totalTests}
						{results.isSample ? 'sample checks' : 'checks'} passed.
					{/if}
				</p>
				{#if results.error}
					<pre class="mt-2 whitespace-pre-wrap">{results.error}</pre>
				{:else if results.failedTests > 0}
					<p class="mt-1 text-xs text-muted-foreground">
						Open the Test result tab for the details.
					</p>
				{:else if results.totalTests === 0}
					<p class="mt-1">The test runner did not find any checks for this question.</p>
				{/if}
			</section>
		{/if}
		{#if figures.length > 0}
			<section class="mb-3 space-y-3" aria-label="Preview of your chart">
				{#each figures as figure, index (index)}
					{#if figure.kind === 'png'}
						<img
							src={`data:image/png;base64,${figure.data}`}
							alt={`Preview chart ${index + 1} drawn by your code`}
							class="max-w-full rounded border border-border bg-white"
						/>
					{:else}
						<PlotlyFigure json={figure.json} />
					{/if}
				{/each}
			</section>
		{/if}
		{#if output}
			<pre
				class="font-mono whitespace-pre-wrap select-text {hasError
					? 'text-(--ide-bad)'
					: 'text-foreground/80'}">{output}</pre>
		{:else if figures.length === 0}
			<div class="flex h-full items-center justify-center text-muted-foreground">
				Run your code (Shift+Enter) to see its output here
			</div>
		{/if}
	</div>
</div>
