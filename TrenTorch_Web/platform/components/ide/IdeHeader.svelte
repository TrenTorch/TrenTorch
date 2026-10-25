<script lang="ts">
	import { resolve } from '$app/paths';
	import type { QuestionContent, RuntimeState } from '$data/curriculum/types';
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
			: fromPotd
				? fromPage
					? resolve(`/potd?page=${fromPage}`)
					: resolve('/potd')
				: fromPage
					? resolve(`/questions?page=${fromPage}`)
					: resolve('/questions')
	);
	const backLabel = $derived(
		content.metadata.kind === 'dsa'
			? 'Back to DSA Sheet'
			: fromPotd
				? 'Back to Problem of the Day'
				: 'Back to Module'
	);
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
		content.metadata.kind === 'dsa' ? 'DSA Sheet' : fromPotd ? 'Problem of the Day' : 'Questions'
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
		<a
			href={backHref}
			class="hidden min-w-0 items-center gap-2 rounded-md px-2 py-1.5 transition-colors hover:bg-muted sm:flex"
		>
			<ListChecks class="size-4 shrink-0 text-muted-foreground" />
			<span class="shrink-0 text-muted-foreground">{crumb}</span>
			<span class="text-muted-foreground/60" aria-hidden="true">/</span>
			<span class="truncate font-medium">{place ? place.step : content.metadata.title}</span>
		</a>

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
