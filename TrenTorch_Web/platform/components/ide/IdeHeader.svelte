<script lang="ts">
	import { resolve } from '$app/paths';
	import type { QuestionContent, RuntimeState } from '$data/curriculum/types';
	import type { TrackQuestion } from '$processes/ide-content/get-track-questions';
	import * as Dialog from '$components/ui/dialog';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import {
		ArrowLeft,
		ListChecks,
		Play,
		CloudUpload,
		RotateCcw,
		RefreshCcw,
		Maximize,
		Minimize,
		Loader2,
		Check
	} from '@lucide/svelte';

	let {
		content,
		fromPage = null,
		fromPotd = false,
		trackQuestions = { track: null, questions: [] },
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
		fromPage?: string | null;
		fromPotd?: boolean;
		trackQuestions?: { track: string | null; questions: TrackQuestion[] };
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

	// See +page.svelte's fromPage comment -- ?from=N carries the Questions
	// page a student came from back through here.
	let backHref = $derived(
		fromPotd
			? fromPage
				? resolve(`/potd?page=${fromPage}`)
				: resolve('/potd')
			: fromPage
				? resolve(`/questions?page=${fromPage}`)
				: resolve('/questions')
	);
	const backLabel = $derived(fromPotd ? 'Back to Problem of the Day' : 'Back to Module');

	let isNavOpen = $state(false);

	// Same ?from=N handling as GuidePane's prev/next links.
	function questionHref(id: string) {
		return fromPage ? resolve(`/ide/[id]?from=${fromPage}`, { id }) : resolve('/ide/[id]', { id });
	}
</script>

<header
	class="grid h-12 w-full grid-cols-[1fr_auto_1fr] items-center border-b border-border bg-background px-2 font-mono text-xs text-foreground"
>
	<!-- Left: back to where the student came from -->
	<div class="flex items-center gap-1 justify-self-start">
		<a
			href={backHref}
			class="flex items-center gap-1.5 rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
			title={backLabel}
		>
			<ArrowLeft class="size-4" />
		</a>
		<div class="h-4 w-px bg-border"></div>
		<Dialog.Root bind:open={isNavOpen}>
			<Dialog.Trigger
				class="flex items-center gap-1.5 rounded-md px-2 py-1.5 text-amber-600 transition-colors hover:bg-amber-500/10 hover:text-amber-700 dark:text-amber-400 dark:hover:text-amber-300"
				title="Problem list"
			>
				<ListChecks class="size-3.5" />
				<span class="hidden truncate sm:inline">{content.metadata.title}</span>
			</Dialog.Trigger>
			<!-- Not portaled, so SvelteKit's router handles these links and it shows in fullscreen. -->
			<Dialog.Content
				portalProps={{ disabled: true }}
				class="data-open:slide-in-from-left data-closed:slide-out-to-left data-open:zoom-in-100 data-closed:zoom-out-100 top-0 left-0 flex h-full max-w-sm translate-x-0 translate-y-0 flex-col rounded-none border-y-0 border-l-0 p-0 font-mono text-xs"
			>
				<div class="border-b border-border px-4 py-3">
					<Dialog.Title class="text-sm">Problems</Dialog.Title>
					{#if trackQuestions.track}
						<Dialog.Description class="text-muted-foreground capitalize">
							{trackQuestions.track.replaceAll('-', ' ')}
						</Dialog.Description>
					{/if}
				</div>
				<nav class="flex-1 overflow-y-auto py-1">
					{#each trackQuestions.questions as question, i (question.id)}
						{@const isCurrent = question.id === content.id}
						{@const isSolved = solved.isSolved(question.id)}
						<a
							href={questionHref(question.id)}
							onclick={() => (isNavOpen = false)}
							aria-current={isCurrent ? 'page' : undefined}
							class="flex items-center gap-3 px-4 py-2 transition-colors hover:bg-secondary {isCurrent
								? 'bg-secondary text-foreground'
								: 'text-muted-foreground hover:text-foreground'}"
						>
							<span class="w-5 shrink-0 text-right tabular-nums opacity-60">{i + 1}</span>
							<!-- Same read-only solved indicator as QuestionRow's -->
							<span
								class="flex size-4 shrink-0 items-center justify-center rounded-[4px] border {isSolved
									? 'border-primary bg-primary text-primary-foreground'
									: 'border-input'}"
								role="img"
								aria-label={isSolved
									? `'${question.title}' is solved`
									: `'${question.title}' is not solved yet`}
							>
								{#if isSolved}
									<Check class="size-3.5" />
								{/if}
							</span>
							<span class="truncate">{question.title}</span>
							{#if isCurrent}
								<span
									class="ml-auto size-2 shrink-0 rounded-full bg-yellow-500 dark:bg-yellow-400"
									title="Current problem"
								></span>
							{/if}
						</a>
					{:else}
						<p class="px-4 py-2 text-muted-foreground">No problems listed for this track yet.</p>
					{/each}
				</nav>
			</Dialog.Content>
		</Dialog.Root>
	</div>

	<!-- Center: Run / Submit -->
	<div class="flex items-center gap-2 justify-self-center">
		<button
			type="button"
			class="flex items-center gap-1.5 rounded-full border border-border bg-secondary px-3.5 py-1.5 font-medium text-foreground transition-colors hover:border-foreground/30 hover:bg-muted disabled:pointer-events-none disabled:opacity-40"
			disabled={isBusy}
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
			disabled={isBusy}
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
			class="flex items-center rounded-md border border-red-500/30 p-1.5 text-red-600 transition-colors hover:bg-red-500/10 dark:text-red-400"
			onclick={onReattempt}
			title="Re-attempt this question: reset to the starter code and mark it unsolved again"
			aria-label="Re-attempt this question"
		>
			<RefreshCcw class="size-3.5" />
		</button>
		<button
			type="button"
			class="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
			onclick={onResetCode}
			title="Reset code to the original starter template"
		>
			<RotateCcw class="size-3.5" />
		</button>
		<button
			type="button"
			class="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
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
