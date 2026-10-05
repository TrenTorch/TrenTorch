<script lang="ts">
	import { Terminal, Trash2, Copy, Check } from '@lucide/svelte';
	import type { PreviewFigure, SingleTestResult, SubmissionResult } from '$data/curriculum/types';
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

<div class="flex h-full min-h-0 flex-col bg-background font-mono text-xs text-foreground">
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
	<div class="min-h-0 flex-1 overflow-y-auto p-3 text-xs leading-relaxed">
		{#if results}
			<section
				class="mb-3 rounded border p-3 {results.error || results.failedTests > 0
					? 'border-red-500/40 bg-red-500/5 text-red-700 dark:text-red-300'
					: results.totalTests === 0
						? 'border-amber-500/40 bg-amber-500/5 text-amber-700 dark:text-amber-300'
						: 'border-emerald-500/30 bg-emerald-500/5 text-emerald-700 dark:text-emerald-300'}"
			>
				<p class="font-bold">
					{#if results.error}
						{results.error.includes('SyntaxError') || results.error.includes('IndentationError')
							? 'Python syntax error — tests could not start.'
							: 'Execution error — tests could not start.'}
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
					<ul class="mt-2 space-y-2">
						{#each results.results.filter((test: SingleTestResult) => !test.passed) as test (test.name)}
							<li>
								<p class="font-semibold">{test.name}</p>
								{#if test.error}<pre class="mt-0.5 whitespace-pre-wrap">{test.error}</pre>{/if}
							</li>
						{/each}
					</ul>
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
					? 'text-red-700 dark:text-red-300'
					: 'text-foreground/80'}">{output}</pre>
		{:else if figures.length === 0}
			<div class="flex h-full items-center justify-center text-muted-foreground italic">
				Click "Run Code" or press Shift+Enter to execute
			</div>
		{/if}
	</div>
</div>
