<script lang="ts">
	import DifficultyBadge from '$components/DifficultyBadge.svelte';

	// Three real steps of the actual workflow, each paired with a mockup of
	// the real surface it happens on (styled like the hero's editor-window
	// preview) instead of an icon or a generic illustration. Grounded in one
	// real question (Cross-Entropy, Deep Learning: Core Mechanics) throughout,
	// so the three panels read as one continuous example, not three unrelated
	// screenshots.
	const STEPS = [
		{
			n: '01',
			title: 'Read the theory',
			body: 'First principles, then the real math: a deep dive that builds intuition before rigor, with hints if you get stuck.',
			kind: 'theory'
		},
		{
			n: '02',
			title: 'Implement the real signature',
			body: 'The exact function torch.nn.functional actually exposes: real shapes, real defaults, no simplified stand-in.',
			kind: 'code'
		},
		{
			n: '03',
			title: 'Submit against hidden tests',
			body: "An exhaustive suite: edge cases, mutation tests, some checked against real offline PyTorch output. Pass everything, it's solved.",
			kind: 'tests'
		}
	] as const;
</script>

<div class="mx-auto flex max-w-4xl flex-col gap-10 text-left sm:gap-14">
	{#each STEPS as step, i (step.n)}
		<div
			class="flex flex-col items-center gap-6 sm:gap-10 {i % 2 === 1
				? 'sm:flex-row-reverse'
				: 'sm:flex-row'}"
		>
			<div class="flex-1">
				<span class="font-mono text-sm font-bold text-primary">{step.n}</span>
				<h3 class="mt-2 mb-2 text-lg font-semibold">{step.title}</h3>
				<p class="text-sm text-muted-foreground">{step.body}</p>
			</div>

			<div class="w-full flex-1">
				{#if step.kind === 'theory'}
					<div class="overflow-hidden rounded-2xl border border-border bg-secondary/30 text-left">
						<div
							class="flex items-center gap-2 border-b border-border px-4 py-2.5 font-mono text-xs text-muted-foreground"
						>
							<span class="flex gap-1.5" aria-hidden="true">
								<span class="size-2.5 rounded-full bg-red-500/70"></span>
								<span class="size-2.5 rounded-full bg-yellow-500/70"></span>
								<span class="size-2.5 rounded-full bg-green-500/70"></span>
							</span>
							trentorch.com/learn/cross-entropy
						</div>
						<div class="space-y-3 px-5 py-5">
							<p class="font-mono text-sm font-semibold">Cross-Entropy Loss</p>
							<p class="text-sm text-muted-foreground">
								Measures how far a predicted distribution is from the true one. For a one-hot
								target, it collapses to <span class="font-mono text-foreground"
									>-log(p_correct)</span
								>: the model is only penalized for how little probability it assigned the right
								class.
							</p>
							<p class="font-mono text-xs text-muted-foreground">
								L = -&Sigma; y<sub>i</sub> log(p<sub>i</sub>)
							</p>
						</div>
					</div>
				{:else if step.kind === 'code'}
					<div class="overflow-hidden rounded-2xl border border-border bg-secondary/30 text-left">
						<div class="flex items-center justify-between border-b border-border px-4 py-2.5">
							<div class="flex items-center gap-3">
								<span class="flex gap-1.5" aria-hidden="true">
									<span class="size-2.5 rounded-full bg-red-500/70"></span>
									<span class="size-2.5 rounded-full bg-yellow-500/70"></span>
									<span class="size-2.5 rounded-full bg-green-500/70"></span>
								</span>
								<span class="font-mono text-xs text-muted-foreground">cross_entropy.py</span>
							</div>
							<DifficultyBadge difficulty="Medium" />
						</div>
						<pre class="overflow-x-auto px-4 py-4 font-mono text-[13px] leading-relaxed"><code
								><span class="text-sky-500 dark:text-sky-400">def</span> <span
									class="text-amber-600 dark:text-amber-300">cross_entropy</span
								>(logits, target):
    log_probs = log_softmax(logits, dim=-<span class="text-emerald-600 dark:text-emerald-400"
									>1</span
								>)
    <span class="text-sky-500 dark:text-sky-400">return</span
								> -log_probs[range(len(target)), target].mean()</code
							></pre>
					</div>
				{:else}
					<div class="overflow-hidden rounded-2xl border border-border bg-secondary/30 text-left">
						<div
							class="flex items-center justify-between border-b border-border px-4 py-2.5 font-mono text-xs text-muted-foreground"
						>
							<span>Submit &middot; hidden tests</span>
							<span class="font-semibold text-emerald-600 dark:text-emerald-400"
								>12 / 12 passed</span
							>
						</div>
						<ul class="divide-y divide-border px-4 py-1 font-mono text-[13px]">
							{#each ['matches torch.nn.functional.cross_entropy', 'uneven class probabilities', 'batch of 1', 'logits with large magnitude (no overflow)', 'gradient matches finite-difference check'] as t (t)}
								<li class="flex items-center gap-2.5 py-2">
									<span class="text-emerald-600 dark:text-emerald-400" aria-hidden="true"
										>&check;</span
									>
									<span class="text-muted-foreground">{t}</span>
								</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>
		</div>
	{/each}
</div>
