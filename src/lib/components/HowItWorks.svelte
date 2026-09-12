<script lang="ts">
	import { BookOpen, Code2, CloudUpload } from '@lucide/svelte';

	// Numbered because it's a real, literal sequence (theory before code,
	// code before Submit), not decoration -- the same three icons the IDE
	// itself uses (Submit's CloudUpload especially), so this reads as a
	// preview of the actual product, not an abstract diagram of it.
	const STEPS = [
		{
			icon: BookOpen,
			title: 'Read the theory',
			body: 'First principles, then the real math: a deep dive that builds intuition before rigor, with hints if you get stuck.'
		},
		{
			icon: Code2,
			title: 'Implement the real signature',
			body: 'The exact function torch.nn.functional actually exposes: real shapes, real defaults, no simplified stand-in.'
		},
		{
			icon: CloudUpload,
			title: 'Submit against hidden tests',
			body: "An exhaustive suite: edge cases, mutation tests, some checked against real offline PyTorch output. Pass everything, it's solved."
		}
	];
</script>

<div class="mx-auto grid max-w-4xl gap-8 sm:grid-cols-3">
	{#each STEPS as step, i (step.title)}
		<div class="relative flex flex-col items-center text-center">
			<div
				class="mb-4 flex size-12 items-center justify-center rounded-full border border-border bg-secondary"
			>
				<step.icon class="size-5 text-foreground" aria-hidden="true" />
			</div>
			<span class="mb-1 font-mono text-xs text-muted-foreground">Step {i + 1}</span>
			<h3 class="mb-2 font-mono font-semibold">{step.title}</h3>
			<p class="text-sm text-muted-foreground">{step.body}</p>
		</div>
	{/each}
</div>
