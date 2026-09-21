<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import type { QuestionContent } from '$data/curriculum/types';
	import { pyodideService } from '$processes/code-execution/pyodide-service';
	import { loadUserCode } from '$processes/code-execution/load-user-code';
	import { saveUserCode } from '$processes/code-execution/save-user-code';
	import { resetUserCode } from '$processes/code-execution/reset-user-code';
	import { loadIdeLayout } from '$processes/code-execution/load-ide-layout';
	import { saveIdeLayout } from '$processes/code-execution/save-ide-layout';
	import type { IdeLayout } from '$processes/code-execution/ide-layout-key';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { session } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import { potdEntries } from '$data/potd';
	import { localDateString } from '$processes/potd/local-date-string';
	import IdeHeader from '$components/ide/IdeHeader.svelte';
	import GuidePane from '$components/ide/GuidePane.svelte';
	import CodeEditor from '$components/ide/CodeEditor.svelte';
	import OutputConsole from '$components/ide/OutputConsole.svelte';
	import TestResultsView from '$components/ide/TestResultsView.svelte';
	import PaneResizer from '$components/ide/PaneResizer.svelte';
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

	// QuestionRow.svelte carries the Questions page's own current page
	// number in as ?from=N when linking here, so "Back to Questions" can
	// return to that page instead of always landing on page 1 -- passed
	// down to IdeHeader, which builds its own resolve()'d href from it
	// (a pre-built href string can't be verified by eslint's
	// svelte/no-navigation-without-resolve rule the way a direct
	// resolve() call in the component that renders the <a> can).
	let fromPage = $derived(browser ? page.url.searchParams.get('from') : null);
	let backHref = $derived(
		fromPage ? resolve(`/questions?page=${fromPage}`) : resolve('/questions')
	);

	// Prev/next in the same curriculum order /questions lists them in, so
	// the guide pane's arrows step through in the exact order a student
	// would encounter these questions from the menu. GuidePane turns these
	// ids into hrefs itself (via resolve).
	let adjacentQuestions = $derived({ prevId: data.prevId, nextId: data.nextId });

	// Problem of the Day questions get a reduced guide: today's featured
	// question -- and any question scheduled for a FUTURE date, reachable
	// by a student who already knows/guesses its id -- shows only
	// Description (no Theory or Solution -- nothing that would take the
	// edge off the daily challenge, or spoil a day that hasn't happened
	// yet); Theory only comes back once the entry's own date is strictly
	// in the past. Solution stays off for every POTD question regardless
	// of date -- a POTD is meant to be worked out, not read. Regular
	// (non-POTD) questions are unaffected. Browser-guarded like every
	// other "what day is it" read in this codebase: there's no real
	// visitor "now" at prerender time, so this defaults to the full tab
	// set until hydration can compute it for real.
	let guideTabs = $derived.by<('description' | 'theory' | 'solution')[]>(() => {
		if (!content || !browser) return ['description', 'theory', 'solution'];
		const entry = potdEntries.find((e) => e.questionId === content.id);
		if (!entry) return ['description', 'theory', 'solution'];
		const today = localDateString(new Date());
		return entry.date < today ? ['description', 'theory'] : ['description'];
	});

	// "Run" checks the code against just this many of the visible test
	// cases (LeetCode-style), for a fast sanity pass. "Submit" runs the
	// whole hidden suite and is what actually marks the question solved.
	const SAMPLE_TEST_COUNT = 2;
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

		const onFullscreenChange = () => {
			isFullscreen = document.fullscreenElement === ideRoot;
		};
		document.addEventListener('fullscreenchange', onFullscreenChange);
		return () => document.removeEventListener('fullscreenchange', onFullscreenChange);
	});

	$effect(() => {
		if (content) {
			// init() is idempotent (no-ops once the worker exists), so this
			// covers both the normal first-load case and navigating here
			// (prev/next arrows, or back into another question) from a page
			// that never had content to init for in the first place -- an
			// onMount-only call would miss that second case entirely, since
			// SvelteKit reuses this component across /ide/[id] param changes
			// rather than remounting it.
			pyodideService.init();
			userCode = loadUserCode(content.id, content.starterCode);
			pyodideService.testResults.set(null);
			// Also clear the console: otherwise the previous question's Run/
			// Submit output stays on screen, now sitting under a different
			// question's title -- easy to misread as this question's result.
			pyodideService.consoleOutput.set('');
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
			// Whatever Run/Submit showed was for the code that just got
			// discarded -- leaving it up would read as still describing the
			// (now reset) editor content.
			pyodideService.testResults.set(null);
			pyodideService.consoleOutput.set('');
		}
	}

	// Full reset, not just the editor: starter code back, and the question
	// dropped from both the solved and attempted stores so /questions shows
	// it as untouched again.
	function handleReattemptQuestion() {
		if (!content) return;
		if (
			confirm(
				'Re-attempt this question? This restores the starter code and marks the question unsolved again.'
			)
		) {
			resetUserCode(content.id);
			userCode = content.starterCode;
			lastSavedAt = Date.now();
			solved.unmarkSolved(content.id);
			attempted.unmarkAttempted(content.id);
			// Same as Reset: an old "All Tests Passed" left on screen would
			// directly contradict "marked unsolved again" happening right above it.
			pyodideService.testResults.set(null);
			pyodideService.consoleOutput.set('');
		}
	}

	async function handleRunCode() {
		if (!session.user) {
			signInPrompt.open();
			return;
		}
		mobileActiveTab = 'output';

		// No question loaded (an id with no published content): nothing to
		// check against, so just exec and print, same as before.
		if (!content) {
			activeRightTab = 'console';
			try {
				await pyodideService.runCode(userCode);
			} catch (e) {
				console.error('Run failed', e);
				consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
			}
			return;
		}

		// LeetCode-style Run: execute the code against the first couple of
		// visible checks and show pass/fail, without marking the question
		// attempted or solved -- that's Submit's job.
		activeRightTab = 'tests';
		try {
			const result = await pyodideService.runTests(
				userCode,
				content.testHarnessCode,
				content.id,
				SAMPLE_TEST_COUNT
			);
			// Surface the student's own print() output in the Console tab too.
			consoleOutput.set(result.rawOutput?.trim() || '(no output)');
		} catch (e) {
			console.error('Run failed', e);
			// Surface the failure where the student can actually see it --
			// a devtools-only error looks identical to nothing happening.
			consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
		}
	}

	async function handleRunTests() {
		if (!session.user) {
			signInPrompt.open();
			return;
		}
		if (!content) return;
		activeRightTab = 'tests';
		mobileActiveTab = 'output';
		try {
			const result = await pyodideService.runTests(userCode, content.testHarnessCode, content.id);
			// Getting here means the hidden tests actually ran: mark the
			// question attempted regardless of the outcome, then solved on top
			// of that if every test passed. Both feed the same stores the
			// Questions page reads, so a Submit here ticks the row there too.
			//
			// Use result.contentId, not content.id: `content` is a $derived
			// that tracks the *currently shown* question, and the student can
			// navigate to a different one (prev/next arrows, or Back to
			// Questions and into another) while this await is still pending --
			// content.id read here would then mark the *new* question solved
			// based on the *old* question's test results. result.contentId is
			// the id that was actually sent to the worker, unaffected by any
			// navigation that happened while it was running.
			attempted.markAttempted(result.contentId);
			if (result.allPassed) {
				solved.markSolved(result.contentId);
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
				return 'Python 3.12 • Shift+Enter to run';
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
	<meta
		name="description"
		content="Build deep learning framework primitives in Python directly in your browser with TrenTorch."
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
			href={backHref}
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
			{fromPage}
			runtimeState={$runtimeState}
			isRunning={$isRunning}
			{isFullscreen}
			onResetCode={handleResetCode}
			onReattempt={handleReattemptQuestion}
			onRunCode={handleRunCode}
			onRunTests={handleRunTests}
			onToggleFullscreen={handleToggleFullscreen}
		/>

		<!-- Mobile Tab Switcher -->
		<div class="flex border-b border-border bg-secondary text-xs md:hidden">
			<button
				type="button"
				class="flex flex-1 items-center justify-center gap-1.5 py-2 {mobileActiveTab === 'guide'
					? 'border-b-2 border-primary bg-primary font-bold text-primary-foreground'
					: 'text-muted-foreground'}"
				onclick={() => (mobileActiveTab = 'guide')}
			>
				<BookOpen class="size-3.5" />
				<span>Guide</span>
			</button>
			<button
				type="button"
				class="flex flex-1 items-center justify-center gap-1.5 py-2 {mobileActiveTab === 'editor'
					? 'border-b-2 border-primary bg-primary font-bold text-primary-foreground'
					: 'text-muted-foreground'}"
				onclick={() => (mobileActiveTab = 'editor')}
			>
				<Code2 class="size-3.5" />
				<span>Editor</span>
			</button>
			<button
				type="button"
				class="flex flex-1 items-center justify-center gap-1.5 py-2 {mobileActiveTab === 'output'
					? 'border-b-2 border-primary bg-primary font-bold text-primary-foreground'
					: 'text-muted-foreground'}"
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
				<GuidePane
					{content}
					isCompleted={solved.isSolved(content.id)}
					prevId={adjacentQuestions.prevId}
					nextId={adjacentQuestions.nextId}
					visibleTabs={guideTabs}
				/>
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
						class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3 text-[11px] text-muted-foreground"
					>
						<div class="flex items-center gap-1.5">
							<Code2 class="size-3" />
							<span>{content.id}.py</span>
						</div>
						<div
							class="flex items-center gap-1.5 text-[10px] {$runtimeState === 'loading_runtime' ||
							$runtimeState === 'loading_packages'
								? 'text-amber-600 dark:text-amber-500'
								: $runtimeState === 'error'
									? 'text-red-600 dark:text-red-400'
									: 'text-muted-foreground'}"
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
						class="flex h-6 shrink-0 items-center justify-between border-t border-border bg-secondary px-3 text-[10px] text-muted-foreground"
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
					<div class="flex h-8 items-center border-b border-border bg-secondary px-1 text-xs">
						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors {activeRightTab ===
							'tests'
								? 'border-t-2 border-primary bg-primary font-bold text-primary-foreground'
								: 'text-muted-foreground hover:text-foreground'}"
							onclick={() => (activeRightTab = 'tests')}
						>
							<ShieldCheck class="size-3" />
							<span>Test Result</span>
						</button>
						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors {activeRightTab ===
							'console'
								? 'border-t-2 border-primary bg-primary font-bold text-primary-foreground'
								: 'text-muted-foreground hover:text-foreground'}"
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
