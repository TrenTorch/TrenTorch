<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import type { QuestionContent } from '$data/curriculum/types';
	import { unifiedExecutor } from '$processes/code-execution/unified-executor';
	import { detectLanguage } from '$processes/code-execution/detect-language';
	import { loadUserCode } from '$processes/code-execution/load-user-code';
	import { saveUserCode } from '$processes/code-execution/save-user-code';
	import { draftSync } from '$processes/code-execution/draft-sync.svelte';
	import { resetUserCode } from '$processes/code-execution/reset-user-code';
	import { loadIdeLayout } from '$processes/code-execution/load-ide-layout';
	import { saveIdeLayout } from '$processes/code-execution/save-ide-layout';
	import type { IdeLayout } from '$processes/code-execution/ide-layout-key';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { attempted } from '$processes/progress-tracking/attempted.svelte';
	import { recordPotdAttempt as recordPotdAttemptHistory } from '$processes/progress-tracking/supabase-potd-attempts-store';
	import { isPotdQuestion } from '$processes/potd/is-potd-question';
	import { session } from '$processes/auth/session.svelte';
	import { signInSkipped } from '$processes/auth/preview-mode';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import { potdEntries } from '$data/potd';
	import { utcDateString } from '$processes/potd/utc-date-string';
	import { isCurrentPotd } from '$processes/rating/is-current-potd';
	import { recordPotdOutcome } from '$processes/rating/supabase-rating-store';
	import { ratingStore } from '$processes/rating/rating-store.svelte';
	import SEO from '$components/SEO.svelte';
	import IdeHeader from '$components/ide/IdeHeader.svelte';
	import GuidePane from '$components/ide/GuidePane.svelte';
	import CodeEditor from '$components/ide/CodeEditor.svelte';
	import OutputConsole from '$components/ide/OutputConsole.svelte';
	import TestResultsView from '$components/ide/TestResultsView.svelte';
	import CustomRunPanel from '$components/ide/CustomRunPanel.svelte';
	import PaneResizer from '$components/ide/PaneResizer.svelte';
	import {
		BookOpen,
		Code2,
		Terminal,
		ShieldCheck,
		ArrowLeft,
		IndentIncrease
	} from '@lucide/svelte';
	import type { PageData } from './$types';

	const DEFAULT_LAYOUT: IdeLayout = { leftPanePercent: 38, bottomPanePercent: 42 };
	const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

	let { data } = $props<{ data: PageData }>();
	const seo = $derived(data.seo);

	// Most ids don't have content yet -- curriculum content is authored
	// question by question, separately from this IDE. That's an expected,
	// common state here, not an error page.
	let content = $derived<QuestionContent | null>(data.content);
	let customFunctionNames = $derived(
		content
			? Array.from(
					content.starterCode.matchAll(/^\s*def\s+([A-Za-z_]\w*)\s*\(/gm),
					(match) => match[1] ?? ''
				)
			: []
	);
	let userCode = $state('');

	// QuestionRow.svelte carries the Questions page's own current page
	// number in as ?from=N when linking here, so "Back to Questions" can
	// return to that page instead of always landing on page 1 -- passed
	// down to IdeHeader, which builds its own resolve()'d href from it
	// (a pre-built href string can't be verified by eslint's
	// svelte/no-navigation-without-resolve rule the way a direct
	// resolve() call in the component that renders the <a> can).
	let fromPage = $derived(browser ? page.url.searchParams.get('from') : null);
	let fromPotd = $derived(browser ? page.url.searchParams.get('src') === 'potd' : false);
	let backHref = $derived(
		fromPotd
			? fromPage
				? resolve(`/potd?page=${fromPage}`)
				: resolve('/potd')
			: fromPage
				? resolve(`/questions?page=${fromPage}`)
				: resolve('/questions')
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
	let guideTabs = $derived.by<('description' | 'theory' | 'solution' | 'discussion')[]>(() => {
		if (!content || !browser) return ['description', 'theory', 'solution'];
		const entry = potdEntries.find((e) => e.questionId === content.id);
		if (!entry) return ['description', 'theory', 'solution'];
		const today = utcDateString(new Date());
		return entry.date < today
			? ['description', 'theory', 'discussion']
			: ['description', 'discussion'];
	});

	// "Run" checks the code against just this many of the visible test
	// cases (LeetCode-style), for a fast sanity pass. "Submit" runs the
	// whole hidden suite and is what actually marks the question solved.
	const SAMPLE_TEST_COUNT = 2;
	let activeRightTab = $state<'console' | 'tests' | 'custom'>('tests');
	let mobileActiveTab = $state<'guide' | 'editor' | 'output'>('editor');
	let ratingFeedback = $state<{
		questionId: string;
		message: string;
		tone: 'success' | 'warning' | 'neutral';
	} | null>(null);
	let visibleRatingFeedback = $derived(
		ratingFeedback?.questionId === content?.id ? ratingFeedback : null
	);

	// Keep the local sign-in bypass available for automated/manual development
	// runs. Custom runs are separate from progress tracking and are available
	// while signed out.
	function canRunWhileSignedOut(): boolean {
		return signInSkipped();
	}

	// Plain references to the service's stores, not $state -- wrapping a
	// legacy svelte/store writable in $state() proxies the store object
	// itself instead of tracking its value, which silently breaks the
	// $storeName auto-subscription below (Run/Submit would appear to do
	// nothing: the store updates, but this component never re-renders).
	const runtimeState = unifiedExecutor.runtimeState;
	const consoleOutput = unifiedExecutor.consoleOutput;
	const consoleError = unifiedExecutor.consoleError;
	const testResults = unifiedExecutor.testResults;
	const isRunning = unifiedExecutor.isRunning;

	let ideRoot: HTMLDivElement | undefined = $state();
	let isFullscreen = $state(false);
	let cursorPos = $state({ line: 1, col: 1 });
	let reindentCode = $state<() => void>(() => {});
	let language = $derived(content ? detectLanguage(content) : 'python');
	let isSql = $derived(language === 'sql');
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
		const onIdeKeydown = (event: KeyboardEvent) => {
			if (
				event.key !== 'F5' ||
				event.repeat ||
				event.shiftKey ||
				event.altKey ||
				event.ctrlKey ||
				event.metaKey
			) {
				return;
			}
			event.preventDefault();
			void handleRunCode();
		};
		document.addEventListener('fullscreenchange', onFullscreenChange);
		document.addEventListener('keydown', onIdeKeydown);
		return () => {
			document.removeEventListener('fullscreenchange', onFullscreenChange);
			document.removeEventListener('keydown', onIdeKeydown);
		};
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
			unifiedExecutor.init(content);
			userCode = loadUserCode(content.id, content.starterCode);
			editedSinceLoad = false;
			unifiedExecutor.testResults.set(null);
			unifiedExecutor.consoleError.set(false);
			// Also clear the console: otherwise the previous question's Run/
			// Submit output stays on screen, now sitting under a different
			// question's title -- easy to misread as this question's result.
			unifiedExecutor.consoleOutput.set('');
			lastSavedAt = Date.now();
		}
	});

	// Set once the student types, so a sync landing mid-edit never swaps code
	// out from under them; before that, newer code from another device is loaded.
	let editedSinceLoad = false;

	$effect(() => {
		void draftSync.version;
		if (!content || editedSinceLoad || !draftSync.wasPulled(content.id)) return;
		userCode = loadUserCode(content.id, content.starterCode);
	});

	function handleCodeChange(newCode: string) {
		if (!content) return;
		editedSinceLoad = true;
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
			unifiedExecutor.testResults.set(null);
			unifiedExecutor.consoleOutput.set('');
			unifiedExecutor.consoleError.set(false);
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
			unifiedExecutor.testResults.set(null);
			unifiedExecutor.consoleOutput.set('');
			unifiedExecutor.consoleError.set(false);
		}
	}

	async function handleRunCode() {
		if (!session.user && !canRunWhileSignedOut()) {
			signInPrompt.open();
			return;
		}
		activeRightTab = 'console';
		mobileActiveTab = 'output';

		// No question loaded (an id with no published content): nothing to
		// check against, so just exec and print, same as before.
		if (!content) {
			try {
				await unifiedExecutor.runCode(userCode);
			} catch (e) {
				console.error('Run failed', e);
				consoleError.set(true);
				consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
			}
			return;
		}

		// SQL Run behaves like a SQL console: execute the script and show the
		// result table (or SQLite's own error) -- the tests are Submit's job.
		if (isSql) {
			try {
				await unifiedExecutor.runCode(userCode, content.dbSchema);
			} catch (e) {
				console.error('Run failed', e);
				consoleError.set(true);
				consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
			}
			return;
		}

		// LeetCode-style Run: execute the code against the first couple of
		// visible checks and show pass/fail in the Console, without marking
		// the question attempted or solved -- that's Submit's job.
		try {
			const result = await unifiedExecutor.runTests(
				userCode,
				content.testHarnessCode,
				content.id,
				SAMPLE_TEST_COUNT
			);
			// Surface the student's own print() output in the Console tab too.
			consoleOutput.set(result.rawOutput?.trim() || '(no output)');
		} catch (e) {
			console.error('Run failed', e);
			consoleError.set(true);
			// Surface the failure where the student can actually see it --
			// a devtools-only error looks identical to nothing happening.
			consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
		}
	}

	async function handleRunTests() {
		if (!session.user && !canRunWhileSignedOut()) {
			signInPrompt.open();
			return;
		}
		if (!content) return;
		activeRightTab = 'tests';
		mobileActiveTab = 'output';
		ratingFeedback = null;
		// Snapshot what is actually being tested. The student can keep typing or
		// switch question while the tests run, and the GitHub save below must
		// commit the exact code that passed, for the question that passed.
		const submitted = content;
		const submittedCode = userCode;
		try {
			const result = await unifiedExecutor.runTests(
				submittedCode,
				submitted.testHarnessCode,
				submitted.id,
				undefined,
				submitted.dbSchema
			);
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
			if (isPotdQuestion(result.contentId)) {
				if (!isCurrentPotd(result.contentId)) {
					if (result.allPassed) {
						ratingFeedback = {
							questionId: result.contentId,
							tone: 'neutral',
							message: 'Past POTDs do not change your rating. Your solve is still recorded locally.'
						};
					}
					return;
				}

				if (!session.user) {
					ratingFeedback = {
						questionId: result.contentId,
						tone: 'warning',
						message:
							'Sign in to save this attempt and receive a rating update. This run was only recorded locally.'
					};
					return;
				}

				// Persist the attempt before requesting a solve rating: the database
				// validates the rating against this durable solved-attempt record.
				const attemptSaved = await recordPotdAttemptHistory(
					result.contentId,
					result.passedTests,
					result.totalTests,
					result.allPassed
				);
				if (!attemptSaved) {
					ratingFeedback = {
						questionId: result.contentId,
						tone: 'warning',
						message:
							'Your attempt could not be saved, so no rating update was confirmed. Please try again.'
					};
					return;
				}

				if (!result.allPassed) {
					ratingFeedback = {
						questionId: result.contentId,
						tone: 'neutral',
						message:
							'No rating changes on failed submits today. An unsuccessful attempt may be settled after the POTD day ends if it remains unsolved.'
					};
					return;
				}

				const outcome = await recordPotdOutcome(result.contentId, 'solved');
				if (!outcome) {
					ratingFeedback = {
						questionId: result.contentId,
						tone: 'warning',
						message:
							'Your solve was recorded, but the rating update could not be confirmed. Refresh your profile before retrying.'
					};
					return;
				}

				ratingStore.setRating(outcome.ratingAfter);
				const amount = Math.abs(outcome.delta);
				const signedAmount = outcome.delta > 0 ? `+${amount}` : `${outcome.delta}`;
				const reason = outcome.alreadyRecorded
					? outcome.delta < 0
						? `This POTD was already settled as unsuccessful: ${signedAmount} was applied previously. A later solve does not reverse a settled rating.`
						: `This POTD was already rated: ${signedAmount} was applied previously; this submit made no additional change.`
					: outcome.delta > 0
						? `Rating change: ${signedAmount}.`
						: 'No rating change: the solve reward rounded to zero at your current rating.';
				ratingFeedback = {
					questionId: result.contentId,
					tone: outcome.delta < 0 ? 'warning' : 'success',
					message: `${reason} Your rating is now ${outcome.ratingAfter}.`
				};
			}
		} catch (e) {
			console.error('Test run failed', e);
			consoleError.set(true);
			consoleOutput.set(`[Submit failed]: ${e instanceof Error ? e.message : String(e)}`);
		}
	}

	async function handleRunCustom(
		functionName: string,
		argumentsJson: string,
		expectedJson: string
	) {
		if (!content) return;
		activeRightTab = 'console';
		mobileActiveTab = 'output';
		unifiedExecutor.testResults.set(null);
		unifiedExecutor.consoleError.set(false);
		try {
			await unifiedExecutor.runCustomTest(
				userCode,
				content.testHarnessCode,
				content.id,
				functionName,
				argumentsJson,
				expectedJson
			);
		} catch (error) {
			console.error('Custom run failed', error);
			consoleError.set(true);
			consoleOutput.set(
				`[Custom run failed]: ${error instanceof Error ? error.message : String(error)}`
			);
		}
	}

	let runtimeStatusText = $derived.by(() => {
		switch ($runtimeState) {
			case 'loading_runtime':
				return isSql ? 'Loading SQLite…' : 'Loading Python runtime…';
			case 'loading_packages':
				return isSql ? 'Loading SQLite…' : 'Loading libraries…';
			case 'running':
				return 'Executing…';
			case 'testing':
				return 'Running tests…';
			case 'error':
				return 'Runtime error';
			default:
				return isSql ? 'SQLite 3.39 • Ctrl/Cmd+Enter to run' : 'Python 3.12 • Shift+Enter to run';
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

<SEO
	title={seo.title}
	description={seo.description}
	path={seo.path}
	type="article"
	noindex={!seo.indexable}
	jsonLd={seo.jsonLd}
/>

<svelte:head>
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
			{fromPotd ? 'Back to Problem of the Day' : 'Back to Questions'}
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
			{fromPotd}
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
					companies={data.companies}
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
							<span>{content.id}{isSql ? '.sql' : '.py'}</span>
						</div>
						<div class="flex items-center gap-2">
							{#if !isSql}
								<button
									type="button"
									class="flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] text-amber-600 transition-colors hover:bg-amber-500/10 hover:text-amber-700 dark:text-amber-400 dark:hover:text-amber-300"
									onclick={() => reindentCode()}
									title="Fix indentation for the entire file"
									aria-label="Fix indentation"
								>
									<IndentIncrease class="size-3" />
									<span class="hidden sm:inline">Fix indent</span>
								</button>
							{/if}
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
					</div>
					<div class="min-h-0 flex-1 overflow-hidden">
						{#key language}
							<CodeEditor
								{language}
								value={userCode}
								onRun={handleRunCode}
								onChange={handleCodeChange}
								onCursorChange={(pos) => (cursorPos = pos)}
								bind:reindent={reindentCode}
							/>
						{/key}
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
						{#if !isSql}
							<button
								type="button"
								class="flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors {activeRightTab ===
								'custom'
									? 'border-t-2 border-primary bg-primary font-bold text-primary-foreground'
									: 'text-muted-foreground hover:text-foreground'}"
								onclick={() => (activeRightTab = 'custom')}
							>
								<span>Custom Run</span>
							</button>
						{/if}
					</div>

					<!-- Tab Contents -->
					<div class="flex-1 overflow-hidden">
						{#if activeRightTab === 'tests'}
							<TestResultsView results={$testResults} ratingFeedback={visibleRatingFeedback} />
						{:else if activeRightTab === 'console'}
							<OutputConsole
								output={$consoleOutput}
								results={$testResults}
								hasError={$consoleError}
								onClear={() => unifiedExecutor.consoleOutput.set('')}
							/>
						{:else if content}
							{#key content.id}
								<CustomRunPanel
									functionNames={customFunctionNames}
									isRunning={$isRunning}
									output={$consoleOutput}
									hasError={$consoleError}
									onRun={handleRunCustom}
								/>
							{/key}
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
