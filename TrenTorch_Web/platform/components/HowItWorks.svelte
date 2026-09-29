<script lang="ts">
	// A real, literal sequence (theory before code, code before Submit), not
	// decoration -- rendered as a plain numbered list rather than icon
	// circles so the number itself reads as "step order," with the brand
	// accent spent on exactly that number and nothing else in the row.
	const STEPS = [
		{
			title: 'Read the theory',
			body: 'First principles, then the real math: a deep dive that builds intuition before rigor, with hints if you get stuck.'
		},
		{
			title: 'Implement the real signature',
			body: 'The exact function torch.nn.functional actually exposes: real shapes, real defaults, no simplified stand-in.'
		},
		{
			title: 'Submit against hidden tests',
			body: "An exhaustive suite: edge cases, mutation tests, some checked against real offline PyTorch output. Pass everything, it's solved."
		}
	];
</script>

<div class="mx-auto grid max-w-4xl gap-4 text-left sm:grid-cols-3">
	{#each STEPS as step, i (step.title)}
		<div
			class="rounded-2xl border border-border p-6 transition-[border-color,transform,box-shadow] duration-300 hover:-translate-y-1 hover:border-primary hover:shadow-[0_0_0_1px_var(--primary)] motion-reduce:transition-none motion-reduce:hover:translate-y-0"
		>
			<span class="font-mono text-sm font-bold text-primary">{String(i + 1).padStart(2, '0')}</span>
			<h3 class="mt-2 mb-2 font-semibold">{step.title}</h3>
			<p class="text-sm text-muted-foreground">{step.body}</p>
		</div>
	{/each}
</div>
