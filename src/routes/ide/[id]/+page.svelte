<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import type { QuestionContent } from '$lib/curriculum/types';
	import { pyodideService } from '$lib/runtime/pyodideService';
	import {
		loadUserCode,
		saveUserCode,
		resetUserCode,
		loadIdeLayout,
		saveIdeLayout,
		type IdeLayout
	} from '$lib/runtime/storage';
	import { solved } from '$lib/stores/solved.svelte';
	import IdeHeader from '$lib/components/ide/IdeHeader.svelte';
	import GuidePane from '$lib/components/ide/GuidePane.svelte';
	import CodeEditor from '$lib/components/ide/CodeEditor.svelte';
	import OutputConsole from '$lib/components/ide/OutputConsole.svelte';
	import TestResultsView from '$lib/components/ide/TestResultsView.svelte';
	import PaneResizer from '$lib/components/ide/PaneResizer.svelte';
	import { BookOpen, Code2, Terminal, ShieldCheck, ArrowLeft } from '@lucide/svelte';
	import type { PageData } from './$types';

	const DEFAULT_LAYOUT: IdeLayout = { leftPanePercent: 38, bottomPanePercent: 42 };
	const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

	let { data } = $props<{ data: PageData }>();

	// Most ids don't have content yet -- curriculum content is authored
	// question by question, separately from this IDE. That's an expected,
	// common state here, not an error page.
	let content = $derived<QuestionContent | null>(data.content);
	let userCode = $state('');
	let activeRightTab = $state<'console' | 'tests'>('tests');
	let mobileActiveTab = $state<'guide' | 'editor' | 'output'>('editor');

	// Plain references to the service's stores, not $state -- wrapping a
	// legacy svelte/store writable in $state() proxies the store object
	// itself instead of tracking its value, which silently breaks the
	// $storeName auto-subscription below (Run/Submit would appear to do
	// nothing: the store updates, but this component never re-renders).
	const runtimeState = pyodideService.runtimeState;
	const consoleOutput = pyodideService.consoleOutput;
	const testResults = pyodideService.testResults;
	const isRunning = pyodideService.isRunning;

	let ideRoot: HTMLDivElement | undefined = $state();
	let isFullscreen = $state(false);
	let cursorPos = $state({ line: 1, col: 1 });
	let lastSavedAt = $state<number | null>(null);

	// Resizable panes: left guide/code split, and code/console split within
	// the right column. Sizes are shared across every question and
	// persisted, same as LeetCode remembering how you last dragged its panes.
	let mainAreaEl: HTMLDivElement | undefined = $state();
	let rightColumnEl: HTMLDivElement | undefined = $state();
	let leftPanePercent = $state(DEFAULT_LAYOUT.leftPanePercent);
	let bottomPanePercent = $state(DEFAULT_LAYOUT.bottomPanePercent);

	function handleLeftResize(deltaPx: number) {
		if (!mainAreaEl || mainAreaEl.clientWidth === 0) return;
		leftPanePercent = clamp(leftPanePercent + (deltaPx / mainAreaEl.clientWidth) * 100, 20, 60);
		saveIdeLayout({ leftPanePercent, bottomPanePercent });
	}

	function handleBottomResize(deltaPx: number) {
		if (!rightColumnEl || rightColumnEl.clientHeight === 0) return;
		// The divider sits above the bottom pane: dragging it down grows the
		// editor and shrinks the bottom pane, so this is a subtraction.
		bottomPanePercent = clamp(
			bottomPanePercent - (deltaPx / rightColumnEl.clientHeight) * 100,
			15,
			75
		);
		saveIdeLayout({ leftPanePercent, bottomPanePercent });
	}

	onMount(() => {
		const layout = loadIdeLayout(DEFAULT_LAYOUT);
		leftPanePercent = layout.leftPanePercent;
		bottomPanePercent = layout.bottomPanePercent;

		// Only spin up the Pyodide worker (a multi-MB download) when there's
		// actually content to run it against, not on a "not published" page.
		if (content) {
			pyodideService.init();
		}

		const onFullscreenChange = () => {
			isFullscreen = document.fullscreenElement === ideRoot;
		};
		document.addEventListener('fullscreenchange', onFullscreenChange);
		return () => document.removeEventListener('fullscreenchange', onFullscreenChange);
	});

	$effect(() => {
		if (content) {
			userCode = loadUserCode(content.id, content.starterCode);
			pyodideService.testResults.set(null);
			lastSavedAt = Date.now();
		}
	});

	function handleCodeChange(newCode: string) {
		if (!content) return;
		userCode = newCode;
		saveUserCode(content.id, newCode);
		lastSavedAt = Date.now();
	}

	function handleResetCode() {
		if (!content) return;
		if (confirm('Reset code to the original starter template for this question?')) {
			resetUserCode(content.id);
			userCode = content.starterCode;
			lastSavedAt = Date.now();
		}
	}

	async function handleRunCode() {
		activeRightTab = 'console';
		mobileActiveTab = 'output';
		try {
			await pyodideService.runCode(userCode);
		} catch (e) {
			console.error('Run failed', e);
			// Surface the failure where the student can actually see it --
			// a devtools-only error looks identical to nothing happening.
			consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
		}
	}

	async function handleRunTests() {
		if (!content) return;
		activeRightTab = 'tests';
		mobileActiveTab = 'output';
		try {
			const result = await pyodideService.runTests(userCode, content.testHarnessCode, content.id);
			// Passing every hidden test marks the question solved -- in the
			// same store the Questions page's checkbox reads, so this shows
			// up there too, not just as a badge inside the IDE.
			if (result.allPassed) {
				solved.markSolved(content.id);
			}
		} catch (e) {
			console.error('Test run failed', e);
			consoleOutput.set(`[Submit failed]: ${e instanceof Error ? e.message : String(e)}`);
		}
	}

	let runtimeStatusText = $derived.by(() => {
		switch ($runtimeState) {
			case 'loading_runtime':
				return 'Loading Python runtime…';
			case 'loading_packages':
				return 'Loading NumPy…';
			case 'running':
				return 'Executing…';
			case 'testing':
				return 'Running tests…';
			case 'error':
				return 'Runtime error';
			default:
				return 'Python 3.10 • Shift+Enter to run';
		}
	});

	async function handleToggleFullscreen() {
		try {
			if (document.fullscreenElement) {
				await document.exitFullscreen();
			} else {
				await ideRoot?.requestFullscreen();
			}
		} catch (e) {
			console.error('Fullscreen toggle failed', e);
		}
	}
</script>

<svelte:head>
	<title>{content ? content.metadata.title : data.id} | TrenTorch Web IDE</title>
	<meta
		name="description"
		content="Build deep learning framework primitives in Python directly in your browser with TrenTorch Web IDE."
	/>
	{#if content}
		<!-- Warm the connection to Pyodide's CDN as soon as we know we'll need
		     it, instead of waiting for the worker to open the request cold. -->
		<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin="anonymous" />
	{/if}
</svelte:head>

{#if !content}
	<div
		class="flex h-[calc(100vh-3.5rem)] w-full flex-col items-center justify-center gap-4 bg-background px-6 text-center"
	>
		<p class="font-mono text-sm text-muted-foreground">
			No IDE content published yet for <span class="text-foreground">{data.id}</span>.
		</p>
		<a
			href={resolve('/questions')}
			class="flex items-center gap-1.5 border border-border bg-secondary px-3 py-1.5 font-mono text-xs text-foreground transition-colors hover:border-foreground/30 hover:bg-muted"
		>
			<ArrowLeft class="size-3" />
			Back to Questions
		</a>
	</div>
{:else}
	<div
		bind:this={ideRoot}
		class="ide-shell flex h-[calc(100vh-3.5rem)] w-full flex-col overflow-hidden bg-black font-mono text-white"
	>
		<!-- IDE Top Header -->
		<IdeHeader
			{content}
			runtimeState={$runtimeState}
			isRunning={$isRunning}
			{isFullscreen}
			onResetCode={handleResetCode}
			onRunCode={handleRunCode}
			onRunTests={handleRunTests}
			onToggleFullscreen={handleToggleFullscreen}
		/>

		<!-- Mobile Tab Switcher -->
		<div class="flex border-b border-border bg-neutral-950 text-xs md:hidden">
			<button
				type="button"
				class="flex flex-1 items-center justify-center gap-1.5 py-2 {mobileActiveTab === 'guide'
					? 'border-b-2 border-white bg-black font-bold text-white'
					: 'text-neutral-400'}"
				onclick={() => (mobileActiveTab = 'guide')}
			>
				<BookOpen class="size-3.5" />
				<span>Guide</span>
			</button>
			<button
				type="button"
				class="flex flex-1 items-center justify-center gap-1.5 py-2 {mobileActiveTab === 'editor'
					? 'border-b-2 border-white bg-black font-bold text-white'
					: 'text-neutral-400'}"
				onclick={() => (mobileActiveTab = 'editor')}
			>
				<Code2 class="size-3.5" />
				<span>Editor</span>
			</button>
			<button
				type="button"
				class="flex flex-1 items-center justify-center gap-1.5 py-2 {mobileActiveTab === 'output'
					? 'border-b-2 border-white bg-black font-bold text-white'
					: 'text-neutral-400'}"
				onclick={() => (mobileActiveTab = 'output')}
			>
				<Terminal class="size-3.5" />
				<span>Output</span>
			</button>
		</div>

		<!-- Main Multi-Pane Area -->
		<div bind:this={mainAreaEl} class="flex flex-1 overflow-hidden">
			<!-- Left Pane: Guide -->
			<div
				class="ide-left-pane h-full shrink-0 overflow-hidden border-r border-border {mobileActiveTab ===
				'guide'
					? 'block w-full'
					: 'hidden md:block'}"
				style="--ide-left-pane-percent: {leftPanePercent}%"
			>
				<GuidePane {content} isCompleted={solved.isSolved(content.id)} />
			</div>

			<PaneResizer
				axis="x"
				onResize={handleLeftResize}
				valueNow={leftPanePercent}
				valueMin={20}
				valueMax={60}
				class="hidden md:block"
			/>

			<!-- Right Column: Code Editor (Top) + Terminal & Test Suite (Bottom) -->
			<div
				bind:this={rightColumnEl}
				class="flex h-full flex-1 flex-col overflow-hidden {mobileActiveTab === 'guide'
					? 'hidden md:flex'
					: 'flex w-full'}"
			>
				<!-- Top Section: Editor -->
				<div
					class="flex min-h-[40%] flex-1 flex-col overflow-hidden border-b border-border {mobileActiveTab ===
					'output'
						? 'hidden md:flex'
						: 'flex w-full'}"
				>
					<div
						class="flex h-8 items-center justify-between border-b border-border bg-neutral-950/80 px-3 text-[11px] text-neutral-400"
					>
						<div class="flex items-center gap-1.5">
							<Code2 class="size-3" />
							<span>{content.id}.py</span>
						</div>
						<div
							class="flex items-center gap-1.5 text-[10px] {$runtimeState === 'loading_runtime' ||
							$runtimeState === 'loading_packages'
								? 'text-amber-500'
								: $runtimeState === 'error'
									? 'text-red-400'
									: 'text-neutral-500'}"
						>
							{#if $runtimeState === 'loading_runtime' || $runtimeState === 'loading_packages'}
								<span class="size-1.5 animate-pulse rounded-full bg-amber-500" aria-hidden="true"
								></span>
							{/if}
							{runtimeStatusText}
						</div>
					</div>
					<div class="flex-1 overflow-hidden">
						<CodeEditor
							value={userCode}
							onRun={handleRunCode}
							onChange={handleCodeChange}
							onCursorChange={(pos) => (cursorPos = pos)}
						/>
					</div>
					<!-- Editor status bar -->
					<div
						class="flex h-6 shrink-0 items-center justify-between border-t border-border bg-neutral-950/80 px-3 text-[10px] text-neutral-500"
					>
						<span>{lastSavedAt ? 'Saved' : ''}</span>
						<span class="tabular-nums">Ln {cursorPos.line}, Col {cursorPos.col}</span>
					</div>
				</div>

				<PaneResizer
					axis="y"
					onResize={handleBottomResize}
					valueNow={bottomPanePercent}
					valueMin={15}
					valueMax={75}
					class="hidden md:block"
				/>

				<!-- Bottom Section: Terminal & Test Results -->
				<div
					class="ide-bottom-pane flex min-h-[180px] shrink-0 flex-col overflow-hidden {mobileActiveTab ===
					'editor'
						? 'hidden md:flex'
						: 'flex h-[42%] w-full'}"
					style="--ide-bottom-pane-percent: {bottomPanePercent}%"
				>
					<!-- Tabs Bar -->
					<div class="flex h-8 items-center border-b border-border bg-neutral-950 px-1 text-xs">
						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors {activeRightTab ===
							'tests'
								? 'border-t-2 border-white bg-black font-bold text-white'
								: 'text-neutral-500 hover:text-neutral-300'}"
							onclick={() => (activeRightTab = 'tests')}
						>
							<ShieldCheck class="size-3" />
							<span>Test Result</span>
						</button>
						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors {activeRightTab ===
							'console'
								? 'border-t-2 border-white bg-black font-bold text-white'
								: 'text-neutral-500 hover:text-neutral-300'}"
							onclick={() => (activeRightTab = 'console')}
						>
							<Terminal class="size-3" />
							<span>Console</span>
						</button>
					</div>

					<!-- Tab Contents -->
					<div class="flex-1 overflow-hidden">
						{#if activeRightTab === 'tests'}
							<TestResultsView results={$testResults} />
						{:else}
							<OutputConsole
								output={$consoleOutput}
								onClear={() => pyodideService.consoleOutput.set('')}
							/>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	/* The resizer handles only exist at md+ (mobile uses full-width tabs
	   instead), so the dynamic sizes only need to apply there too -- below
	   md, the plain w-full / h-[42%] utility classes in the markup stand. */
	@media (min-width: 768px) {
		.ide-left-pane {
			width: var(--ide-left-pane-percent);
		}
		.ide-bottom-pane {
			height: var(--ide-bottom-pane-percent);
		}
	}

	/* The IDE always renders on a black background regardless of the
	   site's light/dark toggle, so its scrollbars need their own fixed
	   dark coloring instead of the theme-driven --border/--muted-foreground
	   the rest of the site uses (which would go near-invisible here in
	   light mode). */
	:global(.ide-shell) {
		scrollbar-color: #333333 transparent;
	}
	:global(.ide-shell *)::-webkit-scrollbar-thumb {
		background-color: #333333;
	}
	:global(.ide-shell *)::-webkit-scrollbar-thumb:hover {
		background-color: #525252;
	}
</style>
