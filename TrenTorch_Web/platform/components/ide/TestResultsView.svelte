<script lang="ts">
	import type { SubmissionResult } from '$data/curriculum/types';
	import { parseTestFailure } from '$processes/code-execution/parse-test-failure';
	import { ArrowRight, Check, X } from '@lucide/svelte';

	let {
		results = null,
		ratingFeedback = null,
		nextHref = null
	} = $props<{
		results: SubmissionResult | null;
		ratingFeedback: {
			message: string;
			tone: 'success' | 'warning' | 'neutral';
		} | null;
		/** Where "Next question" goes, when there is a next question. */
		nextHref?: string | null;
	}>();

	// Which check's details are open. Defaults to the first failing one, else the first.
	let picked = $state<string | null>(null);
	$effect(() => {
		void results;
		picked = null;
	});
	const selected = $derived(
		results
			? (results.results.find((test: { name: string }) => test.name === picked) ??
					results.results.find((test: { passed: boolean }) => !test.passed) ??
					results.results[0])
			: undefined
	);
	const failure = $derived(
		selected && !selected.passed && selected.error ? parseTestFailure(selected.error) : null
	);

	// A run that could not start at all (a syntax error, a missing function).
	const startError = $derived(
		results?.error && results.totalTests === 0 ? parseTestFailure(results.error) : null
	);

	// "test_07_case_3" -> "case_3": the number prefix is just the run order.
	function shortName(name: string): string {
		return name.replace(/^test_\d+_/, '');
	}
</script>

<div class="flex h-full min-h-0 flex-col bg-background text-[13px] text-foreground">
	{#if results}
		<div class="flex h-9 shrink-0 items-center justify-between border-b border-border px-4 text-xs">
			<span class="text-muted-foreground">
				{results.isSample ? 'Sample run' : 'Full test suite'}
			</span>
			<span class="tabular-nums">
				<span class={results.allPassed ? 'text-(--ide-ok)' : 'text-(--ide-bad)'}>
					{results.passedTests}/{results.totalTests} passed
				</span>
				<span class="ml-2 text-muted-foreground">{results.totalDurationMs} ms</span>
			</span>
		</div>
	{/if}

	<div class="min-h-0 flex-1 overflow-y-auto p-4">
		{#if results}
			<!-- The verdict: one line, no box -->
			{#if results.allPassed}
				<div class="mb-4 flex items-start gap-3">
					<Check class="mt-0.5 size-5 shrink-0 text-(--ide-ok)" />
					<div class="min-w-0 flex-1">
						<h3 class="text-base font-medium text-(--ide-ok)">
							{results.isSample ? 'Sample checks passed' : 'All tests passed'}
						</h3>
						<p class="mt-0.5 text-xs text-muted-foreground">
							{#if results.isSample}
								This ran the first {results.totalTests} check{results.totalTests === 1 ? '' : 's'}.
								Submit runs the full hidden suite and marks the question solved.
							{:else}
								Your code passes every check.
							{/if}
						</p>
					</div>
					{#if !results.isSample && nextHref}
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- nextHref comes from resolve() in the page -->
						<a href={nextHref} class="next-link">
							Next question
							<ArrowRight class="size-3.5" />
						</a>
					{/if}
				</div>
			{:else if startError}
				<div class="mb-4 flex items-start gap-3">
					<X class="mt-0.5 size-5 shrink-0 text-(--ide-bad)" />
					<div class="min-w-0">
						<h3 class="text-base font-medium text-(--ide-bad)">Your code did not run</h3>
						<p class="mt-0.5 text-xs text-muted-foreground">
							No tests ran. Fix this before submitting.
						</p>
						<pre class="detail-pre mt-3">{results.error}</pre>
					</div>
				</div>
			{:else if results.totalTests === 0}
				<div class="mb-4">
					<h3 class="text-base font-medium">No tests ran</h3>
					<p class="mt-0.5 text-xs text-muted-foreground">
						The test runner did not find any checks for this question.
					</p>
				</div>
			{:else}
				<div class="mb-4 flex items-start gap-3">
					<X class="mt-0.5 size-5 shrink-0 text-(--ide-bad)" />
					<div>
						<h3 class="text-base font-medium text-(--ide-bad)">
							{results.failedTests} of {results.totalTests} failed
						</h3>
						<p class="mt-0.5 text-xs text-muted-foreground">Pick a check below to see why.</p>
					</div>
				</div>
			{/if}

			{#if ratingFeedback}
				<p role="status" class="mb-4 border-l-2 border-border pl-3 text-xs text-muted-foreground">
					<span class="text-foreground">Today's POTD rating.</span>
					{ratingFeedback.message}
				</p>
			{/if}

			{#if results.error && results.totalTests > 0}
				<pre class="detail-pre mb-4">{results.error}</pre>
			{/if}

			{#if results.results.length > 0}
				<div class="flex flex-wrap gap-1.5" role="tablist" aria-label="Checks">
					{#each results.results as test (test.name)}
						<button
							type="button"
							role="tab"
							aria-selected={selected?.name === test.name}
							title={test.name}
							class="chip {test.passed ? 'chip-ok' : 'chip-bad'} {selected?.name === test.name
								? 'chip-selected'
								: ''}"
							onclick={() => (picked = test.name)}
						>
							<span class="chip-dot" aria-hidden="true"></span>
							{shortName(test.name)}
						</button>
					{/each}
				</div>

				{#if selected}
					<div class="detail mt-3">
						<div class="flex items-baseline justify-between gap-3">
							<span class="truncate font-mono text-xs text-muted-foreground">{selected.name}</span>
							<span
								class="font-mono text-[11px] whitespace-nowrap text-muted-foreground tabular-nums"
								>{selected.durationMs} ms</span
							>
						</div>

						{#if failure}
							<h4 class="mt-2 text-sm font-medium text-(--ide-bad)">{failure.title}</h4>
							{#if failure.facts.length > 0}
								<dl class="facts mt-3">
									{#each failure.facts as fact (fact.label)}
										<dt>{fact.label}</dt>
										<dd><code>{fact.value}</code></dd>
									{/each}
								</dl>
							{/if}
							{#if failure.note}
								<p class="mt-3 text-xs text-muted-foreground">{failure.note}</p>
							{/if}
							{#if failure.trace}
								<details class="mt-3">
									<summary class="cursor-pointer text-xs text-muted-foreground"
										>Full traceback</summary
									>
									<pre class="detail-pre mt-2">{failure.trace}</pre>
								</details>
							{/if}
						{:else if selected.passed}
							<p class="mt-2 text-xs text-muted-foreground">Passed.</p>
						{/if}
					</div>
				{/if}
			{/if}
		{:else}
			<div
				class="flex h-full flex-col items-center justify-center px-6 text-center text-muted-foreground"
			>
				<p class="font-medium text-foreground">No results yet</p>
				<p class="mt-1 text-xs">
					Run your code to check it against the examples, or submit to run every test.
				</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.next-link {
		display: inline-flex;
		flex-shrink: 0;
		align-items: center;
		gap: 6px;
		border-radius: 6px;
		background: var(--muted);
		padding: 6px 11px;
		color: var(--ide-ok);
		font-size: 12px;
		font-weight: 500;
		text-decoration: none;
		transition: background 120ms;
	}
	.next-link:hover {
		background: color-mix(in oklab, var(--foreground) 15%, transparent);
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 7px;
		border: 1px solid var(--border);
		border-radius: 4px;
		background: transparent;
		padding: 3px 9px 3px 8px;
		color: var(--muted-foreground);
		font-family: var(--ide-mono);
		font-size: 11.5px;
		cursor: pointer;
		transition:
			background 120ms,
			color 120ms;
	}
	.chip:hover {
		color: var(--foreground);
		background: var(--secondary);
	}
	.chip-dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
	}
	.chip-ok .chip-dot {
		background: var(--ide-ok);
	}
	.chip-bad {
		color: var(--foreground);
	}
	.chip-bad .chip-dot {
		background: var(--ide-bad);
	}
	.chip-selected {
		border-color: color-mix(in oklab, var(--foreground) 40%, transparent);
		background: var(--secondary);
		color: var(--foreground);
	}

	.detail {
		border: 1px solid var(--border);
		border-radius: 6px;
		padding: 12px 14px;
	}

	.facts {
		display: grid;
		grid-template-columns: max-content 1fr;
		gap: 8px 16px;
		font-size: 12px;
	}
	.facts dt {
		padding-top: 2px;
		color: var(--muted-foreground);
	}
	.facts dd {
		margin: 0;
		min-width: 0;
	}
	.facts code {
		display: block;
		border-radius: 4px;
		background: var(--secondary);
		padding: 3px 8px;
		font-family: var(--ide-mono);
		font-size: 12px;
		white-space: pre-wrap;
		word-break: break-word;
	}

	.detail-pre {
		border: 1px solid var(--border);
		border-radius: 4px;
		background: var(--secondary);
		padding: 10px 12px;
		font-family: var(--ide-mono);
		font-size: 11.5px;
		line-height: 1.6;
		white-space: pre-wrap;
		word-break: break-word;
	}
</style>
