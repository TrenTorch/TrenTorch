<script lang="ts">
	import type { SubmissionResult } from '$lib/curriculum/types';
	import { CheckCircle2, XCircle, ShieldCheck, AlertCircle } from '@lucide/svelte';

	let { results = null } = $props<{
		results: SubmissionResult | null;
	}>();
</script>

<div class="flex h-full flex-col bg-background font-mono text-xs text-foreground">
	<!-- Results Header -->
	<div class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3">
		<div
			class="flex items-center gap-1.5 text-[11px] tracking-wider text-muted-foreground uppercase"
		>
			<ShieldCheck class="size-3" />
			<span>{results?.isSample ? 'Sample Run' : 'Test Verification Suite'}</span>
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
	<div class="flex-1 overflow-auto p-4">
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
					class="mb-4 flex items-center gap-2 border border-border bg-secondary p-3 text-foreground/80"
				>
					<XCircle class="size-4 shrink-0 text-muted-foreground" />
					<span class="text-xs">
						Your code crashed before any check could run. See the exception below.
					</span>
				</div>
			{:else}
				<div
					class="mb-4 flex items-center gap-2 border border-border bg-secondary p-3 text-foreground/80"
				>
					<AlertCircle class="size-4 shrink-0 text-muted-foreground" />
					<span class="text-xs">
						{results.failedTests} test{results.failedTests === 1 ? '' : 's'} failing. Check assertions
						below.
					</span>
				</div>
			{/if}

			<!-- Execution Error if any -->
			{#if results.error}
				<div class="mb-4 border border-border bg-secondary p-3 text-foreground/80">
					<div class="mb-1 flex items-center gap-1.5 text-xs font-bold text-foreground">
						<XCircle class="size-3.5 text-muted-foreground" />
						<span>Execution Exception</span>
					</div>
					<pre
						class="font-mono text-[11px] whitespace-pre-wrap text-muted-foreground">{results.error}</pre>
				</div>
			{/if}

			<!-- Test list -->
			<div class="space-y-2">
				{#each results.results as test (test.name)}
					<div
						class="border p-3 transition-colors {test.passed
							? 'border-border bg-secondary/40'
							: 'border-border bg-secondary'}"
					>
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								{#if test.passed}
									<CheckCircle2 class="size-3.5 text-green-600 dark:text-green-400" />
									<span class="font-bold text-foreground/80">{test.name}</span>
								{:else}
									<XCircle class="size-3.5 text-muted-foreground" />
									<span class="font-bold text-foreground">{test.name}</span>
								{/if}
							</div>
							<span class="font-mono text-[11px] text-muted-foreground">{test.durationMs}ms</span>
						</div>

						{#if !test.passed && test.error}
							<div
								class="mt-2 border-t border-border pt-2 font-mono text-[11px] text-muted-foreground"
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
