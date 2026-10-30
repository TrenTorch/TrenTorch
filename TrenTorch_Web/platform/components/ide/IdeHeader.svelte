<script lang="ts">
	import { resolve } from '$app/paths';
	import type { QuestionContent, RuntimeState } from '$data/curriculum/types';
	import type { TrackQuestions } from '$processes/ide-content/get-track-questions';
	import SolvedMark from '$components/SolvedMark.svelte';
	import * as Dialog from '$components/ui/dialog';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import {
		ArrowLeft,
		ChevronLeft,
		ChevronRight,
		ListChecks,
		Play,
		CloudUpload,
		RotateCcw,
		RefreshCcw,
		Maximize,
		Minimize,
		Loader2,
		Ellipsis
	} from '@lucide/svelte';
	import ThemePicker from './ThemePicker.svelte';
	import { dsaSteps } from '$data/dsa-sheet';
	import LogoBadge from '$components/LogoBadge.svelte';
	import AccountButton from '$components/AccountButton.svelte';

	let {
		content,
		fromPage = null,
		fromPotd = false,
		fromProblemset = false,
		fromProblemsetPage = null,
		trackQuestions = { partId: null, track: null, questions: [] },
		runtimeState = 'ready',
		isRunning = false,
		isFullscreen = false,
		prevHref = null,
		nextHref = null,
		fontSize = 14,
		onFontSize = () => {},
		onResetCode = () => {},
		onReattempt = () => {},
		onRunCode = () => {},
		onRunTests = () => {},
		onToggleFullscreen = () => {}
	} = $props<{
		content: QuestionContent;
		fromPage?: string | null;
		fromPotd?: boolean;
		fromProblemset?: boolean;
		fromProblemsetPage?: string | null;
		trackQuestions?: TrackQuestions;
		runtimeState: RuntimeState;
		isRunning: boolean;
		isFullscreen?: boolean;
		prevHref?: string | null;
		nextHref?: string | null;
		fontSize?: number;
		onFontSize?: (size: number) => void;
		onResetCode?: () => void;
		onReattempt?: () => void;
		onRunCode?: () => void;
		onRunTests?: () => void;
		onToggleFullscreen?: () => void;
	}>();

	// The "more" menu holds the occasional actions, so the bar stays light.
	let menuOpen = $state(false);
	let menuRoot: HTMLDivElement | undefined = $state();

	function onWindowPointerDown(event: PointerEvent) {
		if (menuOpen && menuRoot && !menuRoot.contains(event.target as Node)) menuOpen = false;
	}

	function onWindowKeydown(event: KeyboardEvent) {
		if (menuOpen && event.key === 'Escape') menuOpen = false;
	}

	function choose(action: () => void) {
		menuOpen = false;
		action();
	}

	let isBusy = $derived(
		isRunning || runtimeState === 'loading_runtime' || runtimeState === 'loading_packages'
	);

	// See +page.svelte's fromPage comment -- ?from=N carries the Questions
	// page a student came from back through here.
	let backHref = $derived(
		content.metadata.kind === 'dsa'
			? resolve('/dsa')
			: fromProblemset
				? resolve(fromProblemsetPage ? `/problemset?page=${fromProblemsetPage}` : '/problemset')
			: fromPotd
				? fromPage
					? resolve(`/potd?page=${fromPage}`)
					: resolve('/potd')
				: fromPage
					? resolve(`/questions?page=${fromPage}`)
					: trackQuestions.partId
						? resolve('/questions/[partId]', { partId: trackQuestions.partId })
						: resolve('/questions')
	);
	const backLabel = $derived(
		content.metadata.kind === 'dsa'
			? 'Back to DSA Sheet'
			: fromProblemset
				? 'Back to Problemset'
			: fromPotd
				? 'Back to Problem of the Day'
				: 'Back to Module'
	);

	let isNavOpen = $state(false);

	// Same ?from=N handling as GuidePane's prev/next links.
	function questionHref(id: string) {
		return fromPage ? resolve(`/ide/[id]?from=${fromPage}`, { id }) : resolve('/ide/[id]', { id });
	}
	// A DSA sheet question shows where it sits ("DSA Sheet / Hashing", and "3 / 6" between the
	// arrows) instead of repeating its own title, which is the heading right below.
	const place = $derived.by(() => {
		if (content.metadata.kind !== 'dsa') return null;
		for (const step of dsaSteps) {
			for (const topic of step.topics) {
				const index = topic.questions.findIndex((q) => q.id === content.id);
				if (index >= 0)
					return { step: step.title, position: index + 1, total: topic.questions.length };
			}
		}
		return null;
	});
	const crumb = $derived(
		content.metadata.kind === 'dsa' ? 'DSA Sheet' : fromPotd ? 'Problem of the Day' : fromProblemset ? 'Problemset' : 'Questions'
	);
</script>

<header
	class="grid h-14 w-full grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center px-3 text-sm text-foreground sm:px-4"
>
	<!-- Left: back to where the student came from, with the question's place in the list -->
	<div class="flex w-full min-w-0 items-center gap-1.5 justify-self-start">
		<a
			href={resolve('/')}
			class="flex items-center rounded-md p-1 transition-opacity hover:opacity-80"
			title="TrenTorch home"
			aria-label="TrenTorch home"
		>
			<LogoBadge class="size-8" />
		</a>
		<span class="h-5 w-px bg-border" aria-hidden="true"></span>
		<a
			href={backHref}
			class="flex items-center rounded-md p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
			title={backLabel}
			aria-label={backLabel}
		>
			<ArrowLeft class="size-4" />
		</a>
		{#if content.metadata.kind === 'dsa'}
			<a
				href={backHref}
				class="hidden min-w-0 items-center gap-2 rounded-md px-2 py-1.5 transition-colors hover:bg-muted sm:flex"
			>
				<ListChecks class="size-4 shrink-0 text-muted-foreground" />
				<span class="shrink-0 text-muted-foreground">{crumb}</span>
				<span class="text-muted-foreground/60" aria-hidden="true">/</span>
				<span class="truncate font-medium">{place ? place.step : content.metadata.title}</span>
			</a>
		{:else}
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
							<Dialog.Description class="text-muted-foreground">
								{trackQuestions.track}
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
								class="flex items-center gap-3 border-l-2 px-4 py-2 transition-colors hover:bg-secondary {isCurrent
									? 'border-yellow-500 bg-secondary font-medium text-foreground dark:border-yellow-400'
									: 'border-transparent text-muted-foreground hover:text-foreground'}"
							>
								<span class="w-5 shrink-0 text-right tabular-nums opacity-60">{i + 1}</span>
								<SolvedMark {isSolved} questionTitle={question.title} />
								<span class="truncate">{question.title}</span>
								{#if isCurrent}
									<span
										class="ml-auto size-2.5 shrink-0 rounded-full bg-yellow-500 dark:bg-yellow-400"
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
		{/if}

		<!-- Previous / next question, right beside the question's name -->
		<!-- eslint-disable svelte/no-navigation-without-resolve -- both hrefs come from resolve() in the page -->
		<div class="ml-1 hidden shrink-0 items-center sm:flex">
			<a
				href={prevHref ?? undefined}
				title="Previous question"
				aria-label="Previous question"
				aria-disabled={!prevHref}
				tabindex={prevHref ? 0 : -1}
				class="flex items-center rounded-md p-1.5 text-muted-foreground transition-colors {prevHref
					? 'hover:bg-muted hover:text-foreground'
					: 'pointer-events-none opacity-30'}"
			>
				<ChevronLeft class="size-4" />
			</a>
			{#if place}
				<span class="px-1 text-xs text-muted-foreground tabular-nums"
					>{place.position} / {place.total}</span
				>
			{/if}
			<a
				href={nextHref ?? undefined}
				title="Next question"
				aria-label="Next question"
				aria-disabled={!nextHref}
				tabindex={nextHref ? 0 : -1}
				class="flex items-center rounded-md p-1.5 text-muted-foreground transition-colors {nextHref
					? 'hover:bg-muted hover:text-foreground'
					: 'pointer-events-none opacity-30'}"
			>
				<ChevronRight class="size-4" />
			</a>
		</div>
		<!-- eslint-enable svelte/no-navigation-without-resolve -->
	</div>

	<!-- Center: Run / Submit -->
	<div class="flex items-center gap-2 justify-self-center">
		<button
			type="button"
			class="press flex h-9 items-center gap-2 rounded-md bg-muted px-4 text-sm font-medium text-foreground hover:bg-foreground/15 disabled:pointer-events-none disabled:opacity-40"
			disabled={isBusy}
			onclick={onRunCode}
			title="Run code (Shift+Enter)"
		>
			{#if isBusy}
				<Loader2 class="size-4 animate-spin" />
			{:else}
				<Play class="size-3.5 fill-current" />
			{/if}
			<span>Run</span>
		</button>

		<button
			type="button"
			class="press flex h-9 items-center gap-2 rounded-md bg-muted px-4 text-sm font-semibold text-(--ide-ok) hover:bg-foreground/15 disabled:pointer-events-none disabled:opacity-40"
			disabled={isBusy}
			onclick={onRunTests}
			title="Run the test suite and submit"
		>
			<CloudUpload class="size-4" />
			<span>Submit</span>
		</button>
	</div>

	<!-- Right: Re-attempt / Reset / Fullscreen -->
	<div class="flex items-center gap-1 justify-self-end">
		<ThemePicker {fontSize} {onFontSize} />
		<div class="relative" bind:this={menuRoot}>
			<button
				type="button"
				class="flex items-center rounded-md p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground {menuOpen
					? 'bg-muted text-foreground'
					: ''}"
				aria-haspopup="menu"
				aria-expanded={menuOpen}
				title="More"
				aria-label="More actions"
				onclick={() => (menuOpen = !menuOpen)}
			>
				<Ellipsis class="size-4" />
			</button>
			{#if menuOpen}
				<div
					role="menu"
					class="more-menu absolute top-full right-0 z-50 mt-2 w-64 rounded-lg border border-border bg-background p-1.5 shadow-2xl"
				>
					<button
						type="button"
						role="menuitem"
						class="menu-item"
						onclick={() => choose(onToggleFullscreen)}
					>
						{#if isFullscreen}
							<Minimize class="size-4 shrink-0" />
						{:else}
							<Maximize class="size-4 shrink-0" />
						{/if}
						<span>{isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}</span>
					</button>
					<button
						type="button"
						role="menuitem"
						class="menu-item"
						onclick={() => choose(onResetCode)}
					>
						<RotateCcw class="size-4 shrink-0" />
						<span class="flex flex-col">
							<span>Reset code</span>
							<span class="menu-hint">Back to the starter code</span>
						</span>
					</button>
					<button
						type="button"
						role="menuitem"
						class="menu-item menu-item-danger"
						onclick={() => choose(onReattempt)}
					>
						<RefreshCcw class="size-4 shrink-0" />
						<span class="flex flex-col">
							<span>Re-attempt question</span>
							<span class="menu-hint">Reset the code and mark it unsolved</span>
						</span>
					</button>
				</div>
			{/if}
		</div>
		<span class="mx-1 h-5 w-px bg-border" aria-hidden="true"></span>
		<AccountButton />
	</div>
</header>

<svelte:window onpointerdown={onWindowPointerDown} onkeydown={onWindowKeydown} />

<style>
	.more-menu {
		animation: menu-in 120ms ease-out;
		transform-origin: top right;
	}

	.menu-item {
		display: flex;
		width: 100%;
		align-items: center;
		gap: 10px;
		border-radius: 6px;
		padding: 8px 10px;
		color: var(--foreground);
		font-size: 13px;
		text-align: left;
		transition: background 100ms;
	}

	.menu-item:hover,
	.menu-item:focus-visible {
		background: var(--muted);
		outline: none;
	}

	.menu-item-danger {
		color: var(--ide-bad);
	}

	.menu-item-danger:hover,
	.menu-item-danger:focus-visible {
		background: color-mix(in oklab, var(--ide-bad) 12%, transparent);
	}

	.menu-hint {
		color: var(--muted-foreground);
		font-size: 11px;
	}

	@keyframes menu-in {
		from {
			opacity: 0;
			transform: translateY(-4px) scale(0.98);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.more-menu {
			animation: none;
		}
	}
</style>
