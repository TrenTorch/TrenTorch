<script lang="ts">
	import { resolve } from '$app/paths';
	import { goto } from '$app/navigation';
	import { SvelteSet } from 'svelte/reactivity';
	import Button from '$components/Button.svelte';
	import DomainStep from '$components/roadmap/DomainStep.svelte';
	import QuizStep from '$components/roadmap/QuizStep.svelte';
	import ChecklistStep from '$components/roadmap/ChecklistStep.svelte';
	import ResultStep from '$components/roadmap/ResultStep.svelte';
	import { domainDefs } from '$data/roadmap-domains';
	import { assembleQuiz } from '$data/roadmap-quiz';
	import { activeRoadmap, type RoadmapState } from '$processes/roadmap/active-roadmap.svelte';

	type Step = 'domains' | 'quiz' | 'tools' | 'concepts' | 'result';
	const STEP_ORDER: Step[] = ['domains', 'quiz', 'tools', 'concepts', 'result'];

	const NONE_TOOLS = "I haven't used any of these — I'm brand new";
	const NONE_CONCEPTS = "I don't know any of these yet";
	const TOOLS = ['Python', 'NumPy', 'pandas', 'scikit-learn', 'PyTorch', 'CUDA basics'];
	const CONCEPTS = [
		'Gradient descent',
		'Backpropagation',
		'Bias-variance tradeoff',
		'Cross-validation',
		'Attention mechanism',
		'Bootstrapping'
	];

	let step = $state<Step>('domains');
	// SvelteSet is reactive on its own (mutations are tracked directly) --
	// no $state wrapper needed, and toggling mutates in place rather than
	// replacing the whole set, same pattern as the existing solved/
	// collapsed-sections stores elsewhere in this codebase.
	const selectedDomainIds = new SvelteSet<string>();

	let quiz = $state<ReturnType<typeof assembleQuiz>>([]);
	let quizIndex = $state(0);
	let quizAnswers = $state<(number | null)[]>([]);

	const toolsKnown = new SvelteSet<string>();
	const conceptsKnown = new SvelteSet<string>();

	let builtRoadmap = $state<RoadmapState | null>(null);

	const stepIndex = $derived(STEP_ORDER.indexOf(step));

	function toggleDomain(id: string) {
		if (selectedDomainIds.has(id)) selectedDomainIds.delete(id);
		else selectedDomainIds.add(id);
	}

	// Selecting the "none of these" sentinel clears any other pick and
	// becomes the sole selection, and vice versa -- matches the spec's
	// explicit "none" handling for both checklist steps.
	function toggleChecklistItem(set: SvelteSet<string>, item: string, noneValue: string) {
		if (item === noneValue) {
			set.clear();
			set.add(item);
		} else {
			set.delete(noneValue);
			if (set.has(item)) set.delete(item);
			else set.add(item);
		}
	}

	function startQuiz() {
		quiz = assembleQuiz([...selectedDomainIds]);
		quizIndex = 0;
		quizAnswers = new Array(quiz.length).fill(null);
		step = 'quiz';
	}

	function nextQuizQuestion() {
		if (quizIndex < quiz.length - 1) {
			quizIndex++;
		} else {
			step = 'tools';
		}
	}

	function buildAndShowResult() {
		const correct = quiz.filter((q, i) => quizAnswers[i] === q.correctIndex).length;
		builtRoadmap = activeRoadmap.build(
			[...selectedDomainIds],
			{ correct, total: quiz.length },
			[...toolsKnown],
			[...conceptsKnown]
		);
		step = 'result';
	}

	function startNow() {
		if (!builtRoadmap) return;
		activeRoadmap.activate(builtRoadmap);
		goto(resolve('/account'));
	}

	const domainNames = $derived(
		[...selectedDomainIds]
			.map((id) => domainDefs.find((d) => d.id === id)?.name)
			.filter((n): n is string => Boolean(n))
			.join(' + ')
	);

	const mastered = $derived(
		builtRoadmap
			? builtRoadmap.quizScore.correct >= Math.ceil(builtRoadmap.quizScore.total * 0.66)
			: false
	);
</script>

<svelte:head>
	<title>Build a roadmap | TrenTorch</title>
	<meta
		name="description"
		content="A personalized, ordered path through the TrenTorch curriculum."
	/>
</svelte:head>

<div class="container max-w-2xl px-4 py-12 md:px-6">
	{#if step !== 'result'}
		<div class="mb-6 flex items-center justify-between">
			<span class="text-xs text-muted-foreground uppercase">
				Step {stepIndex + 1} of {STEP_ORDER.length - 1}
			</span>
			<div class="flex gap-1">
				{#each STEP_ORDER.slice(0, -1) as s, i (s)}
					<span class="h-1 w-6 rounded-full {i <= stepIndex ? 'bg-primary' : 'bg-secondary'}"
					></span>
				{/each}
			</div>
		</div>
	{/if}

	{#if step === 'domains'}
		<h1 class="mb-1 text-xl font-bold">What do you want to learn?</h1>
		<p class="mb-6 text-sm text-muted-foreground">
			Pick as many as you want — we'll combine them into one path.
		</p>
		<DomainStep selectedIds={selectedDomainIds} onToggle={toggleDomain} />
		<div class="mt-6 flex justify-end">
			<Button disabled={selectedDomainIds.size === 0} onclick={startQuiz}>Continue</Button>
		</div>
	{:else if step === 'quiz'}
		<h1 class="mb-1 text-xl font-bold">Quick placement check</h1>
		<p class="mb-6 text-sm text-muted-foreground">
			{quiz.length} short questions, not graded — just tells us where to start you. Pulled straight from
			the question bank.
		</p>
		<QuizStep
			question={quiz[quizIndex]}
			pickedIndex={quizAnswers[quizIndex]}
			onPick={(i) => (quizAnswers[quizIndex] = i)}
		/>
		<div class="mt-6 flex justify-between">
			<Button variant="outline" onclick={() => (step = 'domains')}>Back</Button>
			<Button disabled={quizAnswers[quizIndex] === null} onclick={nextQuizQuestion}>
				{quizIndex === quiz.length - 1 ? 'Continue' : 'Next'}
			</Button>
		</div>
	{:else if step === 'tools'}
		<h1 class="mb-1 text-xl font-bold">What have you already used?</h1>
		<p class="mb-6 text-sm text-muted-foreground">
			Tools &amp; libraries — this just tags familiar topics in your roadmap, it doesn't skip
			anything by itself.
		</p>
		<ChecklistStep
			items={TOOLS}
			noneLabel={NONE_TOOLS}
			checked={toolsKnown}
			onToggle={(item) => toggleChecklistItem(toolsKnown, item, NONE_TOOLS)}
		/>
		<div class="mt-6 flex justify-between">
			<Button variant="outline" onclick={() => (step = 'quiz')}>Back</Button>
			<Button onclick={() => (step = 'concepts')}>Continue</Button>
		</div>
	{:else if step === 'concepts'}
		<h1 class="mb-1 text-xl font-bold">Which concepts do you already know?</h1>
		<p class="mb-6 text-sm text-muted-foreground">
			Same as tools — tags your roadmap, doesn't change what's skipped. Only the quiz decides that.
		</p>
		<ChecklistStep
			items={CONCEPTS}
			noneLabel={NONE_CONCEPTS}
			checked={conceptsKnown}
			onToggle={(item) => toggleChecklistItem(conceptsKnown, item, NONE_CONCEPTS)}
		/>
		<div class="mt-6 flex justify-between">
			<Button variant="outline" onclick={() => (step = 'tools')}>Back</Button>
			<Button onclick={buildAndShowResult}>Build my roadmap</Button>
		</div>
	{:else if step === 'result' && builtRoadmap}
		<ResultStep title={domainNames} parts={builtRoadmap.parts} {mastered} />
		<Button class="mt-6" onclick={startNow}>Start now</Button>
	{/if}
</div>
