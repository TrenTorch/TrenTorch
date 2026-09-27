<script lang="ts">
	import type { SubmissionResult } from '$data/curriculum/types';
	import { CheckCircle2, XCircle, ShieldCheck, AlertCircle } from '@lucide/svelte';

	let { results = null } = $props<{
		results: SubmissionResult | null;
	}>();

	function getErrorSummary(error: string): string {
		return error.trim().split('\n').at(-1)?.trim() || 'Python could not complete this run.';
	}

	function getErrorTitle(error: string): string {
		if (/SyntaxError|IndentationError/.test(error)) return 'Python syntax error';
		if (error.includes('Test harness does not contain')) return 'Test setup error';
		return 'Python execution error';
	}
</script>

<div class="flex h-full min-h-0 flex-col bg-background font-mono text-xs text-foreground">
	<!-- Results Header -->
	<div class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3">
		<div
			class="flex items-center gap-1.5 text-[11px] tracking-wider text-muted-foreground uppercase"
		>
			<ShieldCheck class="size-3" />
			<span>
				{#if !results}
					Test Results
				{:else if results.isSample}
					Sample Run Results
				{:else}
					Full Test Suite Results
				{/if}
			</span>
		</div>
		{#if results}
			<div class="text-[11px]">
				<span class={results.allPassed ? 'font-bold text-foreground' : 'text-muted-foreground'}>
					{results.passedTests}/{results.totalTests} Passed
				</span>
				<span class="ml-1 text-muted-foreground/60">({results.totalDurationMs}ms)</span>
			</div>
		{/if}
	</div>

	<!-- Results Content -->
	<div class="min-h-0 flex-1 overflow-y-auto p-4">
		{#if results}
			<!-- Top status banner -->
			{#if results.allPassed && results.isSample}
				<div class="mb-4 border border-border bg-secondary p-4">
					<div class="flex items-center gap-3">
						<CheckCircle2 class="size-6 text-green-600 dark:text-green-400" />
						<div>
							<h3 class="text-sm font-bold text-foreground">Sample checks passed</h3>
							<p class="text-xs text-muted-foreground">
								This only ran the first {results.totalTests} check{results.totalTests === 1
									? ''
									: 's'}. Hit Submit to run the full hidden suite and mark the question solved.
							</p>
						</div>
					</div>
				</div>
			{:else if results.allPassed}
				<div class="mb-4 border border-border bg-secondary p-4">
					<div class="flex items-center gap-3">
						<CheckCircle2 class="size-6 text-green-600 dark:text-green-400" />
						<div>
							<h3 class="text-sm font-bold text-foreground">All Tests Passed! ⚡</h3>
							<p class="text-xs text-muted-foreground">
								Your implementation conforms to the core TrenTorch specification.
							</p>
						</div>
					</div>
				</div>
			{:else if results.error && results.totalTests === 0}
				<div
					class="mb-4 flex items-start gap-2 border border-red-500/40 bg-red-500/5 p-3 text-red-700 dark:text-red-300"
				>
					<XCircle class="mt-0.5 size-4 shrink-0" />
					<div class="text-xs">
						<p class="font-bold">{getErrorTitle(results.error)}</p>
						<p class="mt-1 break-words">{getErrorSummary(results.error)}</p>
						<p class="mt-1 text-red-700/80 dark:text-red-300/80">
							No tests ran. Fix this error before submitting.
						</p>
					</div>
				</div>
			{:else if results.totalTests === 0}
				<div
					class="mb-4 border border-amber-500/40 bg-amber-500/5 p-3 text-amber-700 dark:text-amber-300"
				>
					<p class="text-xs font-bold">No tests ran</p>
					<p class="mt-1 text-xs">The test runner did not find any checks for this question.</p>
				</div>
			{:else}
				<div
					class="mb-4 flex items-center gap-2 border border-red-500/40 bg-red-500/5 p-3 text-red-700 dark:text-red-300"
				>
					<AlertCircle class="size-4 shrink-0" />
					<span class="text-xs">
						{results.isSample ? 'Sample checks' : 'Test suite'}: {results.failedTests} of
						{results.totalTests} failed. Open each failed check below for its assertion or exception.
					</span>
				</div>
			{/if}

			<!-- Execution Error if any -->
			{#if results.error}
				<div class="mb-4 border border-red-500/40 bg-red-500/5 p-3 text-red-700 dark:text-red-300">
					<div class="mb-1 flex items-center gap-1.5 text-xs font-bold">
						<XCircle class="size-3.5" />
						<span>{getErrorTitle(results.error)}</span>
					</div>
					<pre class="font-mono text-[11px] whitespace-pre-wrap">{results.error}</pre>
				</div>
			{/if}

			<!-- Test list -->
			<div class="space-y-2">
				{#each results.results as test (test.name)}
					<div
						class="border p-3 transition-colors {test.passed
							? 'border-border bg-secondary/40'
							: 'border-red-500/30 bg-red-500/5'}"
					>
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								{#if test.passed}
									<CheckCircle2 class="size-3.5 text-green-600 dark:text-green-400" />
									<span class="font-bold text-foreground/80">{test.name}</span>
								{:else}
									<XCircle class="size-3.5 text-red-600 dark:text-red-400" />
									<span class="font-bold text-red-700 dark:text-red-300">{test.name}</span>
								{/if}
							</div>
							<span class="font-mono text-[11px] text-muted-foreground">{test.durationMs}ms</span>
						</div>

						{#if !test.passed && test.error}
							<div
								class="mt-2 border-t border-red-500/25 pt-2 font-mono text-[11px] text-red-700 dark:text-red-300"
							>
								<p class="whitespace-pre-wrap">{test.error}</p>
							</div>
						{/if}
					</div>
				{/each}
			</div>
		{:else}
			<div
				class="flex h-full flex-col items-center justify-center text-center text-muted-foreground"
			>
				<ShieldCheck class="mb-2 size-8 stroke-[1.5]" />
				<p class="italic">Click "Run Tests" to test your implementation</p>
			</div>
		{/if}
	</div>
</div>
