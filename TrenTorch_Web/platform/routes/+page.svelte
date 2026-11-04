<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import Button from '$components/Button.svelte';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';
	import StatTile from '$components/StatTile.svelte';
	import Testimonials from '$components/Testimonials.svelte';
	import InfiniteMarquee from '$components/InfiniteMarquee.svelte';
	import { BookOpen, Heart, ArrowRight, CalendarCheck, Layers } from '@lucide/svelte';
	import SEO from '$components/SEO.svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import { ArrowUp, ChevronUp, Code2, Play } from '@lucide/svelte';
	import { curriculum, getProgressStats, getDifficultyProgress } from '$data/questions';
	import { buildSiteJsonLd } from '$processes/seo/build-site-json-ld';
	import { createPotdCountdown } from '$processes/potd/potd-countdown.svelte';
	import { dsaResume, type DsaResumeQuestion } from '$processes/dsa-sheet/dsa-resume';
	import { recent } from '$processes/progress-tracking/recent.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { resetUserCode } from '$processes/code-execution/reset-user-code';
	import WindowDots from '$components/WindowDots.svelte';
	import { highlightPython, type TokenKind } from '$processes/potd/highlight-python';
	import { pickPreview, previewParts } from '$processes/potd/home-preview';
	import {
		affectedRange,
		blocksEdit,
		exceedsLines,
		MAX_WINDOW_LINES,
		MIN_WINDOW_LINES,
		windowGrowth,
		editForKey,
		SIGNATURE_LINE
	} from '$processes/potd/editor-keys';
	import { loadUserCode } from '$processes/code-execution/load-user-code';
	import { saveHomeDraft, stripHint } from '$processes/potd/home-draft';
	import { istDateString } from '$processes/potd/ist-date-string';
	import { problemsetProblems } from '$data/problemset';
	import { dsaSteps } from '$data/dsa-sheet';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();

	let learnerCount = $state(0);
	let learnerCountElement: HTMLElement;

	onMount(() => {
		const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		const observer = new IntersectionObserver(
			([entry]) => {
				if (!entry.isIntersecting) return;
				observer.disconnect();
				if (reduceMotion) {
					learnerCount = 6000;
					return;
				}
				const duration = 1600;
				const start = performance.now();
				const animate = (now: number) => {
					const progress = Math.min((now - start) / duration, 1);
					const eased = 1 - Math.pow(1 - progress, 4);
					learnerCount = Math.round(6000 * eased);
					if (progress < 1) requestAnimationFrame(animate);
				};
				requestAnimationFrame(animate);
			},
			{ threshold: 0.35 }
		);
		if (learnerCountElement) observer.observe(learnerCountElement);
		return () => observer.disconnect();
	});

	// The code window shows the Problem of the Day. The prerendered page is drawn for the day it was built;
	// once in the browser it moves to the visitor's own IST day (the same "today" the Problem of the Day
	// page uses), which is the same day except for a page that has been cached for a while.
	let day = $state<string | null>(null);
	onMount(() => (day = istDateString(new Date())));
	const preview = $derived(pickPreview(data.potdPreviews, day ?? data.buildDay));
	// A day with nothing scheduled shows the latest one that ran, and says so.
	const isToday = $derived(preview?.date === (day ?? data.buildDay));
	// The window is a real text field: a transparent textarea over the coloured code. What is typed is kept as a
	// draft for the IDE (see home-draft.ts), and "Continue in IDE" fades in once there is anything to continue.
	let typed = $state<{ id: string; text: string } | null>(null);
	// A visitor who already has code for this problem in the IDE sees that, not the starter: otherwise what
	// they type here could not be carried back without overwriting it. `full` is that saved code in whole
	// (the window only shows the start of it); the draft is only applied while the IDE still holds exactly it.
	let saved = $state<{
		id: string;
		code: string;
		lines: number;
		full: string;
		changed: boolean;
	} | null>(null);
	$effect(() => {
		const id = preview?.id;
		const full = id ? loadUserCode(id, '', 'python') : '';
		// Shown as its own, longer window only once the student has changed something: a different length or a
		// different start. Its `full` text is kept either way, as what the draft is made on top of.
		const changed =
			previewParts(full).code !== preview?.code ||
			full.replace(/\s+$/, '').split('\n').length !== preview?.total;
		saved =
			id && full.trim()
				? { id, ...previewParts(full, changed ? MAX_WINDOW_LINES - 14 : 0), full, changed }
				: null;
	});
	const base = $derived(
		saved && saved.id === preview?.id
			? saved
			: preview
				? { code: preview.code, lines: preview.lines, full: null }
				: null
	);
	const shown = $derived(typed && typed.id === preview?.id ? typed.text : (base?.code ?? ''));
	// Once something has been typed the way on stays open, even if the text is later put back as it was.
	let hasTyped = $state(false);
	const isEdited = $derived(
		Boolean(preview) && (hasTyped || Boolean(saved?.changed && saved.id === preview?.id))
	);
	const codeLines = $derived(highlightPython(shown));
	let codeScroller = $state<HTMLElement>();

	// The window's dots. Red clears the preview back to the starter (asking first when that would also wipe code
	// the student saved in the IDE), yellow folds the window into the capsule below it, green opens the IDE with
	// whatever is typed (it is already kept as the draft).
	const HOME_COLLAPSED_KEY = 'trentorch_home_preview_collapsed';
	let collapsed = $state(false);
	onMount(() => {
		try {
			collapsed = localStorage.getItem(HOME_COLLAPSED_KEY) === '1';
		} catch {
			// Storage blocked: the window just starts open each visit.
		}
	});
	function setCollapsed(next: boolean) {
		collapsed = next;
		try {
			localStorage.setItem(HOME_COLLAPSED_KEY, next ? '1' : '0');
		} catch {
			// As above.
		}
	}
	function clearPreview() {
		if (!preview) return;
		if (saved?.changed) {
			const sure = confirm(
				'Clear the preview? This also removes the code you saved for this problem in the IDE.'
			);
			if (!sure) return;
			resetUserCode(preview.id, 'python');
			saved = null;
		}
		typed = null;
		hasTyped = false;
		saveHomeDraft(null);
	}

	// The capsule shows how long today's problem has left once the window is folded into it.
	const countdown = createPotdCountdown();
	onMount(() => countdown.start());
	// What the folded preview's two cards say: the DSA sheet's way in, and the newest paper.
	// The sheet's question list is only fetched once the window is folded, so the page does not carry it
	// for everyone who never folds it.
	let dsaList = $state<readonly DsaResumeQuestion[]>([]);
	$effect(() => {
		if (collapsed && !dsaList.length)
			void import('$data/dsa-sheet').then((m) => (dsaList = m.dsaQuestions));
	});
	const dsaNext = $derived(dsaResume(dsaList, solved.slugs, recent.get('dsa')));
	const DSA_VERB = { continue: 'Continue', start: 'Start with', next: 'Up next' } as const;

	// The function signature is part of the preview, not of the exercise: shown, but not editable.
	const lockedLine = $derived(base?.code.split('\n').find((l) => SIGNATURE_LINE.test(l)) ?? null);
	const lockedIndex = $derived(lockedLine === null ? -1 : shown.split('\n').indexOf(lockedLine));
	let overLocked = $state(false);

	function onBeforeInput(event: InputEvent & { currentTarget: HTMLTextAreaElement }) {
		const area = event.currentTarget;
		const type = event.inputType;
		if (type.startsWith('history')) return;
		const [from, to] = affectedRange(area.value, area.selectionStart, area.selectionEnd, type);
		const insert =
			event.data ??
			event.dataTransfer?.getData('text/plain') ??
			(type === 'insertLineBreak' || type === 'insertParagraph' ? '\n' : '');
		// A drop lands wherever the pointer is, not at the selection, so it is never allowed to.
		if (
			type === 'insertFromDrop' ||
			blocksEdit(area.value, lockedLine, from, to, insert) ||
			exceedsLines(area.value, from, to, insert)
		) {
			event.preventDefault();
		}
	}
	function onPointerMove(event: MouseEvent & { currentTarget: HTMLTextAreaElement }) {
		const lineHeight = parseFloat(getComputedStyle(event.currentTarget).lineHeight);
		overLocked = lockedIndex >= 0 && Math.floor(event.offsetY / lineHeight) === lockedIndex;
	}

	function onType(event: Event & { currentTarget: HTMLTextAreaElement }) {
		if (!preview || !base) return;
		typed = { id: preview.id, text: event.currentTarget.value };
		hasTyped = true;
		saveHomeDraft(
			event.currentTarget.value === base.code
				? null
				: {
						id: preview.id,
						text: stripHint(event.currentTarget.value),
						shownLines: base.lines,
						base: base.full ?? undefined
					}
		);
	}
	// Tab indents rather than leaving the field; Escape hands Tab back so the keyboard is never trapped.
	let tabLeaves = false;
	function onKey(event: KeyboardEvent & { currentTarget: HTMLTextAreaElement }) {
		const area = event.currentTarget;
		if (event.key === 'Escape') {
			tabLeaves = true;
			return;
		}
		const key = event.key;
		if ((key !== 'Tab' && key !== 'Enter') || event.isComposing) return;
		if (key === 'Tab' && tabLeaves) {
			tabLeaves = false;
			return;
		}
		tabLeaves = false;
		const edit = editForKey(
			area.value,
			area.selectionStart,
			area.selectionEnd,
			key,
			event.shiftKey
		);
		if (!edit) return;
		event.preventDefault();
		if (
			blocksEdit(area.value, lockedLine, edit.from, edit.to, edit.insert) ||
			exceedsLines(area.value, edit.from, edit.to, edit.insert)
		)
			return;
		// execCommand keeps the browser's undo history; the fallback is for browsers that refuse it.
		area.setSelectionRange(edit.from, edit.to);
		if (!document.execCommand('insertText', false, edit.insert)) {
			area.setRangeText(edit.insert, edit.from, edit.to, 'end');
			area.dispatchEvent(new Event('input', { bubbles: true }));
		}
		area.setSelectionRange(edit.selStart, edit.selEnd);
	}
	// Keep the coloured layer under the text as a long line scrolls sideways.
	function syncScroll(event: Event & { currentTarget: HTMLTextAreaElement }) {
		if (codeScroller) codeScroller.scrollLeft = event.currentTarget.scrollLeft;
	}

	const TOKEN_CLASS: Record<TokenKind, string> = {
		keyword: 'text-sky-500 dark:text-sky-400',
		function: 'text-amber-600 dark:text-amber-300',
		number: 'text-emerald-600 dark:text-emerald-400',
		string: 'text-emerald-600 dark:text-emerald-400',
		comment: 'text-muted-foreground',
		plain: ''
	};

	const SUPPORT_URL = 'https://github.com/sponsors/Shashank-Tripathi-07';

	const DSA_PREVIEW_TOPICS = [
		'Number Theory',
		'Dynamic Programming',
		'Range Queries',
		'Design and Data Structures'
	];
	const dsaPreview = $derived(
		DSA_PREVIEW_TOPICS.flatMap((label) => {
			const match = dsaSteps
				.flatMap((step) => step.topics.map((topic) => ({ step, topic })))
				.find(({ step, topic }) =>
					`${step.title} ${topic.title}`.toLowerCase().includes(label.toLowerCase())
				);
			return match
				? [{ label, stepId: match.step.id, questions: match.topic.questions.slice(0, 2) }]
				: [];
		})
	);

	const totalQuestions = getProgressStats().total;
	const totalProblems = totalQuestions + problemsetProblems.length;
	const totalParts = curriculum.length;

	// Real per-difficulty totals (no solved set passed in, so `total` is all
	// that's used here) for the hero's "weighted past the basics" line.
	const difficultyTotals = getDifficultyProgress();

	// Organisations seen in signup email domains (aggregate only, no individuals).
	// Keep in sync with the DB. The matching disclaimer lives in Footer.svelte.
	type LearnerOrg = {
		name: string;
		/** Path under /static for the logo, absent for text-only entries. */
		logo?: string;
		/** Mask box in px: CSS masks have no intrinsic size, so each logo's
		 * size is declared explicitly and w tracks the asset's aspect ratio
		 * so it never distorts. */
		w?: number;
		h?: number;
		/** Render `name` beside the mark; omitted for wordmark logos, where
		 * the logo already reads as the name. */
		withName?: boolean;
	};
	const LEARNER_ORGS: LearnerOrg[] = [
		{ name: 'xAI', logo: '/logos/xai.svg', w: 25, h: 28, withName: true },
		{ name: 'SpaceX', logo: '/logos/spacex.svg', w: 28, h: 28, withName: true },
		{ name: 'OpenAI', logo: '/logos/openai.svg', w: 89, h: 24 },
		{ name: 'Anthropic', logo: '/logos/anthropic.svg', w: 214, h: 24 },
		{ name: 'Harvard', logo: '/logos/harvard.png', w: 87, h: 24 },
		{ name: 'Stanford', logo: '/logos/stanford.svg', w: 115, h: 24 },
		{ name: 'IIT Bombay', logo: '/logos/iit-bombay.svg', w: 33, h: 32, withName: true },
		{ name: 'BITS Pilani', logo: '/logos/bits-pilani.png', w: 32, h: 32, withName: true },
		{ name: 'IISc', logo: '/logos/iisc.svg', w: 36, h: 32, withName: true },
		{ name: 'NITs' },
		{ name: 'IIITs' }
	];
</script>

<SEO
	title="TrenTorch | Free ML practice problems: build PyTorch from scratch"
	description={`${totalProblems} free machine learning practice problems. Build PyTorch from scratch in Python and run the tests in your browser: classical ML, deep learning, transformers, inference, and more.`}
	path="/"
	jsonLd={buildSiteJsonLd()}
/>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap"
	/>
</svelte:head>

<div>
	<!-- Hero: two columns from lg up (copy + CTA left, a static code preview
	     right) so the section uses the full viewport width instead of a
	     single centered column with empty flanks either side. Below lg it
	     collapses back to one centered column. -->
	<section class="hero-texture container px-4 pt-8 pb-8 md:px-6 md:pt-10 lg:pb-10">
		<div
			class="mx-auto flex max-w-6xl flex-col items-center gap-10 text-center lg:flex-row lg:items-center lg:gap-12 lg:text-left"
		>
			<div class="flex min-w-0 flex-1 flex-col items-center lg:items-start">
				<h1
					class="glitch-heading mb-3 font-mono text-3xl font-bold tracking-[0.02em] sm:text-5xl"
					data-text="TrenTorch"
				>
					TrenTorch
				</h1>
				<p class="display mb-4 max-w-xl text-3xl text-balance sm:text-4xl">
					Learn machine learning by building it.
				</p>
				<p class="mb-3 max-w-xl text-lg text-muted-foreground">
					Don't just read about AI. Write it yourself, one small step at a time, and see exactly
					what your code does. {totalProblems}+ practice problems, each with a clear explanation.
				</p>
				<p class="mb-7 font-mono text-sm text-muted-foreground">
					Free forever. No subscriptions. Supported by sponsors and donations.
				</p>
				<div class="flex flex-wrap items-center justify-center gap-3 lg:justify-start">
					<Button size="lg" class="rounded-xl!" href={resolve('/problemset')}>
						<BookOpen class="size-4" />
						Start practicing
					</Button>
					<Button
						size="lg"
						class="rounded-xl!"
						variant="outline"
						href={resolve('/questions')}
						onclick={gateBehindSignIn}
					>
						<Layers class="size-4" />
						Browse topics
					</Button>
				</div>
				<div class="mt-8 grid grid-cols-2 gap-4">
					<StatTile label="Problems" value={totalProblems} tone="positive" />
					<StatTile label="Topics" value={totalParts} tone="positive" />
				</div>
				<!-- Real per-difficulty split, not a marketing round number: the
				     exact Easy/Medium/Hard totals the curriculum data actually has. -->
				<p class="mt-4 max-w-xl font-mono text-xs text-muted-foreground">
					Start easy, finish hard: {difficultyTotals[0].total} beginner &middot; {difficultyTotals[1]
						.total} intermediate &middot; {difficultyTotals[2].total} advanced problems.
				</p>
			</div>

			<!-- Today's Problem of the Day in a window styled like an editor: the start of its starter code,
			     coloured, and editable in place. It is a plain textarea over a coloured copy, so the landing page
			     ships no CodeMirror or Pyodide. Typing in it is optional; whatever is typed goes with the visitor
			     into the IDE. The capsule below it, with its arrow, is the link. -->
			{#if preview}
				<div
					class="w-full max-w-md shrink-0 lg:w-[calc(32rem+16rem*(var(--grow)-1))] lg:max-w-none"
					style:--grow={windowGrowth(shown.split('\n').length)}
				>
					<!-- Widens half to each side. The half on the left is made room for in the layout (the copy beside
					     it wraps and the gap stays as it was); the half on the right spills out past the column. -->
					<!-- Folding is a slide, not a swap: the window's height eases to nothing while the cards' eases open, so
					     a long draft visibly travels into the capsule. Only the height is clipped, the window still spills right. -->
					<div
						class="grid transition-[grid-template-rows,opacity] duration-1000 ease-in-out motion-reduce:transition-none {collapsed
							? 'grid-rows-[0fr] opacity-0'
							: 'grid-rows-[1fr] opacity-100 delay-100'}"
						inert={collapsed}
					>
						<div class="min-h-0 overflow-y-clip">
							<div class="transition-[margin] duration-300 lg:mr-[calc(-16rem*(var(--grow)-1))]">
								<div
									class="overflow-hidden rounded-2xl border border-border bg-secondary/30 text-left shadow-sm transition-colors focus-within:border-primary/40"
								>
									<div class="flex items-center justify-between border-b border-border px-4 py-2.5">
										<div class="flex items-center gap-3">
											<WindowDots
												red={{ label: 'clear', onclick: clearPreview }}
												yellow={{ label: 'minimise', onclick: () => setCollapsed(true) }}
												green={{
													label: 'open in IDE',
													href: resolve('/ide/[id]', { id: preview.id })
												}}
											/>
											<span class="font-mono text-xs text-muted-foreground">{preview.file}</span>
										</div>
										<DifficultyBadge difficulty={preview.difficulty} />
									</div>
									<!-- Two layers in one grid cell, with identical type metrics: the coloured code underneath
						     sets the size, the textarea above it is transparent apart from its caret. -->
									<div
										class="grid grid-cols-[minmax(0,1fr)] px-4 pt-4 pb-0 font-mono text-[13px] leading-relaxed"
									>
										<div
											bind:this={codeScroller}
											class="pointer-events-none col-start-1 row-start-1 overflow-x-hidden whitespace-pre"
											aria-hidden="true"
										>
											{#each codeLines as line, i (i)}
												<div
													class="min-h-[1.625em] {i === lockedIndex
														? '-mx-4 bg-foreground/[0.045] px-4'
														: ''}"
												>
													{#each line as token, j (j)}{#if token.kind === 'plain'}{token.text}{:else}<span
																class={TOKEN_CLASS[token.kind]}>{token.text}</span
															>{/if}{/each}
												</div>
											{/each}
										</div>
										<textarea
											value={shown}
											onbeforeinput={onBeforeInput}
											oninput={onType}
											onmousemove={onPointerMove}
											onmouseleave={() => (overLocked = false)}
											style:cursor={overLocked ? 'not-allowed' : 'text'}
											onkeydown={onKey}
											onscroll={syncScroll}
											wrap="off"
											spellcheck="false"
											autocomplete="off"
											autocapitalize="off"
											aria-label="Starter code of the {isToday
												? 'featured'
												: 'latest'} problem. Edit it to try your own; the function signature is locked."
											class="col-start-1 row-start-1 m-0 block w-full resize-none [scrollbar-width:none] overflow-x-auto overflow-y-hidden border-0 bg-transparent p-0 font-[inherit] leading-[inherit] whitespace-pre text-transparent caret-foreground outline-none [&::-webkit-scrollbar]:hidden"
										></textarea>
									</div>
									<!-- Rows the window keeps below a short text, so it never gets shorter than 15 lines. They are
							     marked as out of bounds the way the signature is: tinted, and the pointer says no. -->
									{#if shown.split('\n').length < MIN_WINDOW_LINES}
										<div
											class="cursor-not-allowed bg-foreground/[0.03]"
											style:height="{(MIN_WINDOW_LINES - shown.split('\n').length) * 1.625 * 13}px"
											aria-hidden="true"
										></div>
									{/if}
									<div class="h-4"></div>
									<div
										class="flex min-h-12 items-center justify-between gap-3 border-t border-border px-4 py-2.5 font-mono text-xs text-muted-foreground"
									>
										<span class="truncate">{preview.where}</span>
										<!-- Only there once something is typed; until then it is invisible, out of the tab order and
							     out of reach of the pointer, so the empty state is just the window. -->
										<a
											href={resolve('/ide/[id]', { id: preview.id })}
											tabindex={isEdited ? 0 : -1}
											aria-hidden={!isEdited}
											class="flex shrink-0 items-center gap-1.5 rounded-md bg-primary/10 px-2.5 py-1.5 text-primary transition-opacity duration-500 hover:bg-primary/15 {isEdited
												? 'opacity-100'
												: 'pointer-events-none opacity-0'}"
										>
											<Play class="size-3" />
											Continue in IDE
										</a>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div
						class="grid transition-[grid-template-rows,opacity] duration-1000 ease-in-out motion-reduce:transition-none {collapsed
							? 'grid-rows-[1fr] opacity-100 delay-500'
							: 'grid-rows-[0fr] opacity-0'}"
						inert={!collapsed}
					>
						<div class="min-h-0 overflow-y-clip">
							<div class="grid gap-3 text-left sm:grid-cols-2">
								<a
									href={resolve('/dsa')}
									class="group rounded-2xl border border-border bg-secondary/30 p-4 font-mono transition-colors hover:border-primary/40 hover:bg-secondary/50"
								>
									<Code2 class="mb-3 size-4 text-primary" />
									<p class="text-sm font-semibold">Data structures &amp; algorithms</p>
									<p class="mt-1 text-xs text-muted-foreground">{data.dsaTotal} problems</p>
									<p class="mt-3 text-xs text-primary">
										{dsaNext
											? `${DSA_VERB[dsaNext.kind]}: ${dsaNext.question.title}`
											: 'Open the sheet'}
									</p>
								</a>
								<a
									href={resolve('/papers')}
									class="group rounded-2xl border border-border bg-secondary/30 p-4 font-mono transition-colors hover:border-primary/40 hover:bg-secondary/50"
								>
									<BookOpen class="mb-3 size-4 text-primary" />
									<p class="text-sm font-semibold">Research papers</p>
									<p class="mt-1 text-xs text-muted-foreground">Latest</p>
									<p class="mt-3 line-clamp-2 text-xs text-primary">
										{data.latestPaper?.title ?? 'Read and code the classics'}
									</p>
								</a>
							</div>
						</div>
					</div>

					<!-- A plain arrow up from the capsule to the window it names, with room either side. -->
					<div
						class="flex flex-col items-center py-3 transition-[margin] duration-300 lg:mr-[calc(-16rem*(var(--grow)-1))]"
					>
						<ArrowUp
							class="mb-3 size-5 text-primary transition-all duration-300 {collapsed
								? 'mb-0 h-0 opacity-0'
								: ''}"
							aria-hidden="true"
						/>
						<!-- The capsule is the link to the problem. Folded, it grows a second line (what is left of
						     the day) and a button to bring the window back; that button sits beside the link, not in it. -->
						<div
							class="flex w-fit max-w-full items-center rounded-full border border-border bg-secondary/50 font-mono text-xs transition-all duration-300 hover:bg-secondary {collapsed
								? 'py-1.5 pl-1'
								: ''}"
						>
							<a
								href={resolve('/ide/[id]', { id: preview.id })}
								class="flex min-w-0 items-center gap-3 rounded-full px-4 {collapsed
									? 'py-2.5'
									: 'py-2'}"
							>
								<CalendarCheck class="size-3.5 shrink-0 text-primary" />
								<span class="flex min-w-0 flex-col">
									<span class="flex min-w-0 items-center gap-3">
										<span class="shrink-0 text-muted-foreground"
											>{isToday ? "Today's Problem:" : 'Latest Problem:'}</span
										>
										<span class="truncate font-semibold uppercase">{preview.title}</span>
										<DifficultyBadge difficulty={preview.difficulty} />
									</span>
									{#if collapsed && isToday && countdown.time}
										<span class="mt-1 text-[11px] text-muted-foreground"
											>Next problem in {countdown.time}</span
										>
									{/if}
								</span>
							</a>
							{#if collapsed}
								<button
									type="button"
									class="mr-2 grid size-7 shrink-0 place-items-center rounded-full text-muted-foreground transition-colors hover:bg-background hover:text-foreground"
									aria-label="Show the code window"
									title="Show the code window"
									onclick={() => setCollapsed(false)}
								>
									<ChevronUp class="size-4" />
								</button>
							{/if}
						</div>
					</div>
				</div>
			{/if}
		</div>
	</section>

	<!-- Learners from: aggregate signup email domains, scrolling marquee.
	     Disclaimer is in the footer. -->
	<section class="container px-4 py-8 text-center md:px-6 md:py-10">
		<div
			class="mx-auto mb-7 flex w-fit flex-col items-center"
			bind:this={learnerCountElement}
			aria-label="6,000 learners"
		>
			<p class="font-mono text-4xl font-bold tracking-tight text-primary tabular-nums sm:text-5xl">
				{learnerCount.toLocaleString('en-US')}+
			</p>
			<p class="mt-1 text-xs font-medium tracking-[0.16em] text-muted-foreground uppercase">
				Learners and growing
			</p>
		</div>
		<h2 class="display mb-6 text-3xl text-balance sm:text-4xl">
			Learners signing up from
			<span
				class="mt-2 block font-mono text-base font-normal tracking-normal text-muted-foreground sm:text-lg"
			>
				top companies and campuses
			</span>
		</h2>
		<div
			class="mx-auto max-w-4xl rounded-2xl border border-border px-5 py-3.5"
			role="group"
			aria-label="Organizations learners signed up from"
		>
			<InfiniteMarquee speed={30} pauseOnHover gap="gap-10">
				{#each LEARNER_ORGS as org (org.name)}
					<span
						class="inline-flex shrink-0 items-center gap-2.5 font-mono text-sm font-semibold whitespace-nowrap"
						role="img"
						aria-label={org.name}
					>
						{#if org.logo}
							<span
								class="org-logo"
								aria-hidden="true"
								style="--logo: url({org.logo}); width: {org.w}px; height: {org.h}px"
							></span>
						{/if}
						{#if org.withName || !org.logo}
							<span aria-hidden="true">{org.name}</span>
						{/if}
					</span>
				{/each}
			</InfiniteMarquee>
		</div>
		<p class="mt-4 text-xs text-muted-foreground/50">
			Based on signup email domains. Not an endorsement, see footer.
		</p>
	</section>

	<!-- Testimonials: shown early, right after the stats -- a first-time
	     visitor sees what other people think of the project before they've
	     had to read anything else about how it works. -->
	<section class="screen">
		<Testimonials />
	</section>

	<!-- Featured learning paths: editorial rows with real problem previews. -->
	<section class="screen container px-4 md:px-6">
		<div class="mx-auto w-full max-w-6xl">
			<div class="mb-8 max-w-3xl">
				<p class="mb-3 font-mono text-xs font-semibold tracking-[0.2em] text-primary uppercase">
					Explore the curriculum
				</p>
				<h2 class="display text-3xl text-balance sm:text-4xl lg:text-5xl">
					From real-world ML problems to rigorous DSA fundamentals.
				</h2>
				<p class="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground">
					TrenTorch combines hands-on machine learning challenges with a carefully structured data
					structures and algorithms sheet. Learn the reasoning, implement the solution, and
					understand why it works.
				</p>
			</div>

			<section class="learning-row">
				<div class="learning-copy">
					<div class="mb-4">
						<span class="learning-index">01</span><span class="learning-kicker"
							>Applied machine learning</span
						>
					</div>
					<h3 class="display text-3xl sm:text-4xl">Company case studies</h3>
					<p class="mt-4 max-w-lg text-base leading-relaxed text-muted-foreground">
						Go beyond textbook exercises. Work through company-inspired scenarios in recommendation
						systems, experimentation, feature engineering, classification and decision trees. Each
						challenge turns a practical engineering need into a focused implementation problem.
					</p>
					<div class="learning-index-list">
						<a
							href={resolve('/ide/[id]?src=problemset&page=1', {
								id: 'stable-softmax-logits-company-201'
							})}><span>01</span><strong>stable-softmax-logits</strong><small>Netflix</small></a
						>
						<a
							href={resolve('/ide/[id]?src=problemset&page=1', {
								id: 'distance-normalized-features-company-202'
							})}><span>02</span><strong>distance-normalized-features</strong><small>Uber</small></a
						>
						<a
							href={resolve('/ide/[id]?src=problemset&page=1', {
								id: 'entropy-of-clicks-company-203'
							})}><span>03</span><strong>entropy-of-clicks</strong><small>Google</small></a
						>
					</div>
					<a class="learning-link" href={resolve('/problemset?companyCases=true')}
						>Browse all company case studies <ArrowRight class="size-4" /></a
					>
				</div>
				<div class="group/window artifact-window">
					<div class="artifact-chrome">
						<WindowDots decorative /><span>cases / netflix / stable-softmax-logits</span><span
							class="artifact-right">Medium</span
						>
					</div>
					<nav class="artifact-tabs" aria-label="Open this real question in the IDE">
						<a
							class="active"
							href={resolve('/ide/[id]?guide=description', {
								id: 'stable-softmax-logits-company-201'
							})}>Problem</a
						>
						<a href={resolve('/ide/[id]?guide=theory', { id: 'stable-softmax-logits-company-201' })}
							>Theory</a
						>
						<a href={resolve('/ide/[id]?panel=editor', { id: 'stable-softmax-logits-company-201' })}
							>Starter code</a
						>
						<a href={resolve('/ide/[id]?panel=tests', { id: 'stable-softmax-logits-company-201' })}
							>Tests</a
						>
					</nav>
					<div class="artifact-content">
						<h4>Stable softmax for ranking scores</h4>
						<p class="artifact-meta">
							Netflix case <span>·</span> <b>Medium</b> <span>·</span> NumPy
						</p>
						<p class="artifact-statement">
							Convert a model's raw ranking scores into probabilities, even when logits are large
							enough to make a naive exponential overflow.
						</p>
						<pre><code
								><span class="syntax-key">def</span> <span class="syntax-fn">softmax</span>(logits):
    shifted = logits - logits.max(axis=-<span class="syntax-num">1</span>, keepdims=<span
									class="syntax-key">True</span
								>)
    exp = np.exp(shifted)
    <span class="syntax-key">return</span> exp / exp.sum(axis=-<span class="syntax-num">1</span
								>, keepdims=<span class="syntax-key">True</span>)</code
							></pre>
						<div class="artifact-tests"><span>HIDDEN TESTS</span><b>✓ 4 / 4 passed</b></div>
						<div class="artifact-test-row">✓ <span>Large logits — no overflow</span></div>
						<div class="artifact-test-row">✓ <span>Each row sums to one</span></div>
					</div>
				</div>
			</section>

			<section class="learning-row learning-row-flip">
				<div class="learning-copy">
					<div class="mb-4">
						<span class="learning-index">02</span><span class="learning-kicker"
							>Algorithms &amp; problem solving</span
						>
					</div>
					<h3 class="display text-3xl sm:text-4xl">A DSA sheet built around understanding.</h3>
					<p class="mt-4 max-w-lg text-base leading-relaxed text-muted-foreground">
						Prepare with a structured, Google-level data structures and algorithms curriculum. Learn
						the theory, recognize patterns, and practise with real questions from the TrenTorch DSA
						sheet—then track your progress as you improve.
					</p>
					<div class="learning-principles">
						<div>
							<span>01</span>
							<p>
								<strong>Understand the theory</strong><small
									>Build intuition before jumping into implementation.</small
								>
							</p>
						</div>
						<div>
							<span>02</span>
							<p>
								<strong>Recognize reusable patterns</strong><small
									>Connect ideas across algorithms and data structures.</small
								>
							</p>
						</div>
						<div>
							<span>03</span>
							<p>
								<strong>Practise with purpose</strong><small
									>Work through curated questions and difficulty levels.</small
								>
							</p>
						</div>
					</div>
					<a class="learning-link" href={resolve('/dsa')}
						>Explore the complete DSA sheet <ArrowRight class="size-4" /></a
					>
				</div>
				<div class="group/window artifact-window dsa-artifact">
					<div class="artifact-chrome">
						<WindowDots decorative /><span>dsa-sheet</span><span class="artifact-right"
							>Learn the idea. Then solve.</span
						>
					</div>
					<div class="dsa-preview-head">
						<strong>Questions from your sheet</strong><span>Live links · TrenTorch DSA</span>
					</div>
					{#each dsaPreview as group, i (group.label)}
						<div class="dsa-preview-group">
							<div class="dsa-preview-group-head">
								<span>0{i + 1} · {group.label}</span><span>{group.questions.length} selected</span>
							</div>
							{#each group.questions as question (question.id)}
								<a class="dsa-preview-question" href={resolve('/ide/[id]', { id: question.id })}>
									<span class="dsa-status" aria-hidden="true">○</span>
									<strong>{question.title}</strong>
									<span class="dsa-difficulty {question.difficulty.toLowerCase()}"
										>{question.difficulty}</span
									>
									<ArrowRight class="size-3.5 shrink-0" />
								</a>
							{/each}
						</div>
					{/each}
					<div class="dsa-preview-footer">
						<span>Learn → practise → track</span><a href={resolve('/dsa')}
							>Open DSA sheet <ArrowRight class="size-3.5" /></a
						>
					</div>
					<div class="dsa-topic-links" aria-label="Jump to a DSA topic">
						<a href={resolve('/dsa?q=Arrays')}>Arrays</a>
						<a href={resolve('/dsa?q=Trees')}>Trees</a>
						<a href={resolve('/dsa?q=Graphs')}>Graphs</a>
						<a href={resolve('/dsa?q=Dynamic%20Programming')}>DP</a>
					</div>
				</div>
			</section>
			<section class="learning-row research-paper-row">
				<div class="learning-copy">
					<div class="mb-4">
						<span class="learning-index">03</span><span class="learning-kicker"
							>Research papers · Read, annotate, implement</span
						>
					</div>
					<h3 class="display text-3xl sm:text-4xl">Read the paper. Mark it up.</h3>
					<p class="mt-3 max-w-lg text-base leading-relaxed text-muted-foreground">
						Open the original paper in your browser. Highlight the lines that matter, draw on the
						page, and keep notes beside the text. Then implement the paper's ideas yourself, step by
						step.
					</p>
					<p
						class="mt-7 font-mono text-xs font-semibold tracking-[0.16em] text-muted-foreground uppercase"
					>
						Explore papers across every major topic
					</p>
					<div class="learning-index-list research-topic-list">
						<a href={resolve('/papers?track=neural-network-foundations')}
							><span>01</span><strong>Neural Network Foundations</strong><small
								>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=optimization-training')}
							><span>02</span><strong>Optimization &amp; Training</strong><small
								>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=transformers-llms')}
							><span>03</span><strong>Transformers &amp; LLMs</strong><small>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=classical-ml-learning-theory')}
							><span>04</span><strong>Classical ML &amp; Learning Theory</strong><small
								>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=reinforcement-learning-alignment')}
							><span>05</span><strong>Reinforcement Learning &amp; Alignment</strong><small
								>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=unsupervised-representation-learning')}
							><span>06</span><strong>Unsupervised &amp; Representation Learning</strong><small
								>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=computer-vision')}
							><span>07</span><strong>Computer Vision</strong><small>Read &amp; code</small></a
						>
						<a href={resolve('/papers?track=agentic-systems')}
							><span>08</span><strong>Agentic Systems</strong><small>Read &amp; code</small></a
						>
						<a href={resolve('/papers?track=inference-distributed-production')}
							><span>09</span><strong>Inference, Distributed &amp; Production</strong><small
								>Read &amp; code</small
							></a
						>
						<a href={resolve('/papers?track=sequence-models-attention')}
							><span>10</span><strong>Sequence Models &amp; Attention</strong><small
								>Read &amp; code</small
							></a
						>
					</div>
					<a class="learning-link" href={resolve('/papers')}
						>Explore all research papers <ArrowRight class="size-4" /></a
					>
				</div>
				<div class="research-preview-stack">
					<div
						class="group/window paper-reader artifact-window"
						aria-label="Preview of the TrenTorch research paper reader"
					>
						<div class="artifact-chrome">
							<WindowDots decorative /><span>papers / attention-is-all-you-need</span><span
								class="artifact-right">1 / 15</span
							>
						</div>
						<div class="paper-toolbar">
							<span class="paper-tool active">Read</span><span class="paper-tool">Draw</span><span
								class="paper-tool">Highlight</span
							><span class="paper-tool">Text</span><span class="paper-tool">Erase</span>
							<span class="paper-colors" aria-label="Annotation colors"
								><i></i><i></i><i></i><i></i><i></i></span
							>
							<span class="paper-saved">Saved in<br />this browser</span>
						</div>
						<div class="paper-reader-body">
							<div class="paper-page">
								<div class="paper-page-rule"></div>
								<h4>Attention Is All You Need</h4>
								<div class="paper-page-rule thin"></div>
								<div class="paper-lines"><i></i><i></i><i></i><i></i></div>
								<h5>3.2.1&nbsp; Scaled Dot-Product Attention</h5>
								<div class="paper-lines short"><i></i><i></i></div>
								<div class="paper-highlight">Attention(Q, K, V) = softmax(<br />QKᵀ / √dₖ) V</div>
								<p class="paper-annotation">← key idea</p>
								<div class="paper-lines"><i></i><i></i></div>
							</div>
							<aside class="paper-notes">
								<strong>Notes</strong>
								<p>Scaling by √dₖ stops the softmax from saturating when dₖ is large.</p>
								<p class="note-highlight">
									Why not just divide by dₖ? Check the variance argument.
								</p>
								<p>Next: try the question on this section.</p>
							</aside>
						</div>
						<div class="paper-reader-footer">
							<span>Read the original · annotate · understand</span><a
								href={resolve('/papers/attention-is-all-you-need')}
								>Open paper reader <ArrowRight class="size-3.5" /></a
							>
						</div>
					</div>
				</div>
			</section>
			<section class="learning-row learning-row-flip research-code-row">
				<div class="group/window artifact-window research-challenge">
					<div class="artifact-chrome">
						<WindowDots decorative /><span>transformers-llms / scaled-dot-product-attention</span
						><span class="challenge-level">Intermediate</span>
					</div>
					<div class="artifact-content">
						<h4>Attention Is All You Need: Scaled Dot-Product Attention</h4>
						<p class="challenge-eyebrow">The problem, from first principles</p>
						<p class="artifact-statement">
							Attention Is All You Need (Vaswani et al., 2017) drops recurrence entirely. Each
							position builds its output by comparing a query with every key, turning similarities
							into weights, and averaging the values with those weights. Dividing by the square root
							of the key dimension keeps the softmax from saturating.
						</p>
						<p class="challenge-eyebrow">From theory to code</p>
						<p class="artifact-statement">
							Implement <code>scaled_dot_product_attention(Q, K, V)</code>, which returns
							<code>softmax(QK^T / sqrt(d)) V</code> with a row-wise softmax.
						</p>
						<p class="challenge-eyebrow">Constraints</p>
						<ul class="challenge-constraints">
							<li><code>Q</code> and <code>K</code> share the feature dimension <code>d</code>.</li>
						</ul>
						<pre><code
								><span class="syntax-key">def</span> <span class="syntax-fn"
									>scaled_dot_product_attention</span
								>(Q, K, V):
    <span class="text-muted-foreground"># softmax(QK^T / sqrt(d)) V, row-wise softmax</span>
    ...</code
							></pre>
						<div class="challenge-run"><span>hidden tests</span><strong>Run · 0 / 5</strong></div>
					</div>
				</div>
				<div class="learning-copy">
					<div class="mb-4">
						<span class="learning-index">04</span><span class="learning-kicker"
							>Research papers · Code</span
						>
					</div>
					<h3 class="display text-3xl sm:text-4xl">Then code the paper.</h3>
					<p class="mt-4 max-w-lg text-base leading-relaxed text-muted-foreground">
						Every paper comes with questions that start from first principles and end in working
						code. Implement the idea yourself and run it against hidden tests.
					</p>
					<div class="learning-principles research-code-principles">
						<div>
							<span>01</span>
							<p>
								<strong>The problem, from first principles</strong><small
									>What the paper is actually solving, in plain terms</small
								>
							</p>
						</div>
						<div>
							<span>02</span>
							<p>
								<strong>From theory to code</strong><small
									>The exact function to write, with real shapes and defaults</small
								>
							</p>
						</div>
						<div>
							<span>03</span>
							<p>
								<strong>Constraints that matter</strong><small
									>The edge cases the paper assumes, spelled out</small
								>
							</p>
						</div>
						<div>
							<span>04</span>
							<p>
								<strong>Check it against hidden tests</strong><small
									>Pass everything and the paper is yours</small
								>
							</p>
						</div>
					</div>
					<a class="learning-link" href={resolve('/papers/attention-is-all-you-need')}
						>Code the paper <ArrowRight class="size-4" /></a
					>
				</div>
			</section>
		</div>
	</section>

	<section class="screen goal-statement-section container px-4 md:px-6">
		<div class="goal-statement">
			<p class="goal-eyebrow">Beyond writing code</p>
			<h2 class="display">The goal isn't just to teach you how to write the code</h2>
			<p>It's to help you understand what your code is actually doing underneath</p>
		</div>
	</section>

	<!-- Hosting & OSS Support -->
	<section class="container px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
		<div
			class="mx-auto flex w-full max-w-3xl flex-col items-center gap-4 rounded-2xl border border-border/15 bg-secondary/40 px-5 py-7 text-center sm:px-8 sm:py-9"
		>
			<p
				class="font-mono text-[14px] font-semibold tracking-[0.2em] text-muted-foreground uppercase"
			>
				Hosting &amp; OSS support by
			</p>
			<div class="flex flex-wrap items-center justify-center gap-x-8 gap-y-3">
				<a
					href="https://vercel.com/"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="Vercel, opens in a new tab"
					class="flex items-center gap-2 font-mono text-2xl font-bold tracking-tight text-[#171717] transition-colors hover:text-[#999999] focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-primary sm:text-3xl dark:text-[#999999] dark:hover:text-[#fafafa]"
				>
					<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="size-6">
						<path d="m12 1.608 12 20.784H0Z" />
					</svg>
					Vercel
				</a>
				<a
					href="https://mintlify.com/"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="Mintlify, opens in a new tab"
					class="mint-link flex items-center gap-2 font-mono text-2xl font-bold tracking-tight whitespace-nowrap transition-colors focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-primary sm:text-3xl"
				>
					<svg viewBox="0 0 980 980" aria-hidden="true" class="size-6 shrink-0">
						<path
							class="mint-path-a"
							d="M817.701 404.994V202.123C817.701 180.353 800.039 163 778.595 163H575.818C543.966 163 512.43 169.31 483.102 181.299C453.773 193.604 426.968 211.273 404.577 233.989L403 235.567C373.356 265.54 352.227 302.769 341.505 343.785C360.742 338.737 380.609 336.213 400.477 335.898C453.457 335.266 505.493 352.304 547.751 384.17C585.91 412.566 614.922 451.689 630.69 496.806C647.089 542.555 648.981 592.405 636.682 639.415C677.364 628.688 714.893 607.549 744.852 577.892L746.429 576.314C768.819 553.913 786.794 527.095 799.093 497.753C811.392 468.411 817.385 436.86 817.385 404.994H817.701Z"
						/>
						<path
							class="mint-path-b"
							d="M335.451 401.567C335.765 339.332 360.584 279.612 404.255 234.979L235.543 403.767C234.915 404.396 234.286 404.71 233.658 405.339C192.501 446.2 167.682 500.892 163.598 558.726C159.827 612.789 173.965 666.223 204.126 710.856C207.002 715.113 214.808 716.514 219.207 712.427L322.57 609.331C354.929 576.957 364.983 528.866 349.589 485.804C339.849 459.087 335.137 430.484 335.451 401.567Z"
						/>
						<path
							class="mint-path-b"
							d="M745.449 576.328C713.089 608.075 672.56 630.077 628.575 639.82C584.277 649.564 538.408 646.736 495.681 631.648C495.681 631.648 495.366 631.648 495.052 631.648C452.01 616.247 403.942 626.305 371.582 658.365L268.218 761.462C263.82 765.862 264.448 773.091 269.789 776.549C314.401 806.409 367.812 820.868 421.85 817.096C479.658 813.01 534.009 788.179 575.166 747.003L576.737 745.431L745.449 576.643V576.328Z"
						/>
					</svg>
					Mintlify
				</a>
			</div>
			<p class="max-w-lg text-sm text-muted-foreground sm:text-base">
				Thanks to Vercel and Mintlify for providing infrastructure
			</p>
		</div>
	</section>

	<!-- Free, and why: a confident closer (big statement, minimal framing)
	     instead of a boxed card, same restraint as the hero -- the disclosure
	     underneath still carries the full explanation, just smaller. -->
	<section class="screen container px-4 md:px-6" style="margin-bottom: 3rem">
		<div
			class="mx-auto flex max-w-4xl flex-col items-center justify-between gap-6 rounded-2xl border border-border p-6 text-center sm:flex-row sm:text-left"
		>
			<div>
				<h2 class="display mb-2 text-2xl text-balance sm:text-3xl">
					Free. Money shouldn't be the barrier to learning ML.
				</h2>
				<p class="max-w-2xl text-sm leading-relaxed text-muted-foreground">
					We don't charge users and we don't sell your data. TrenTorch runs entirely on sponsorships
					and donations.
				</p>
			</div>
			{#if SUPPORT_URL}
				<Button
					variant="outline"
					class="shrink-0 rounded-xl!"
					href={SUPPORT_URL}
					target="_blank"
					rel="noopener noreferrer"
				>
					<Heart class="size-4" />
					Support TrenTorch
				</Button>
			{/if}
		</div>
	</section>
</div>

<style>
	/* A faint dot-grid behind the hero only, fading out toward the edges via
	   a radial mask -- gives the section some depth instead of flat color,
	   same idea as deep-ml.com/tensortonic.com's textured heroes, without
	   a decorative image asset to ship. currentColor-based dots so they
	   follow the theme automatically. */
	.hero-texture {
		position: relative;
	}
	.hero-texture::before {
		content: '';
		position: absolute;
		inset: -2rem -1rem auto -1rem;
		height: 32rem;
		pointer-events: none;
		z-index: -1;
		background-image: radial-gradient(currentColor 1px, transparent 1px);
		background-size: 22px 22px;
		color: var(--border);
		opacity: 0.5;
		mask-image: radial-gradient(ellipse 70% 60% at 65% 30%, black, transparent 75%);
		-webkit-mask-image: radial-gradient(ellipse 70% 60% at 65% 30%, black, transparent 75%);
	}

	/* One section per screen on desktop: each block gets a viewport-tall
	   slot (minus the 3.5rem navbar) with its content centered, so a single
	   component holds the reader's attention at a time. Children are set to
	   full width so their own mx-auto/max-w-* still center and cap them
	   inside the flex column. On phones it is just generous vertical padding. */

	.mint-link {
		--mint-a: #18e299;
		--mint-b: #0c8c5e;
		color: var(--mint-b);
	}
	.mint-link:hover,
	.mint-link:focus-visible {
		--mint-a: #0c8c5e;
		--mint-b: #18e299;
	}
	.mint-path-a {
		fill: var(--mint-a);
	}
	.mint-path-b {
		fill: var(--mint-b);
	}

	.learning-row {
		display: grid;
		grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
		align-items: center;
		gap: clamp(2rem, 7vw, 5rem);
		padding: clamp(3.5rem, 8vw, 7rem) 0;
		border-top: 1px solid var(--border);
	}

	.research-paper-row {
		grid-template-columns: minmax(0, 0.88fr) minmax(0, 1.12fr);
	}
	.research-topic-list a {
		grid-template-columns: 1.5rem minmax(0, 1fr) auto;
	}
	.research-preview-stack {
		display: grid;
		gap: 1rem;
		min-width: 0;
	}
	.paper-reader {
		background: var(--background);
	}
	.paper-code {
		background: var(--background);
	}
	.paper-code-heading {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.8rem;
		font: 0.78rem var(--font-sans, system-ui, sans-serif);
	}
	.paper-toolbar {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.85rem;
		border-bottom: 1px solid var(--border);
		padding: 0.75rem 1rem;
		color: var(--muted-foreground);
		font: 0.68rem var(--font-sans, system-ui, sans-serif);
	}
	.paper-tool {
		padding: 0.42rem 0.55rem;
		white-space: nowrap;
	}
	.paper-tool.active {
		border-radius: 8px;
		background: var(--foreground);
		color: var(--background);
		font-weight: 600;
	}
	.paper-colors {
		display: inline-flex;
		gap: 0.42rem;
		margin-left: auto;
	}
	.paper-colors i {
		width: 13px;
		height: 13px;
		border: 2px solid #333;
		border-radius: 50%;
		background: #e7444c;
	}
	.paper-colors i:nth-child(2) {
		background: #3987ff;
	}
	.paper-colors i:nth-child(3) {
		background: #21a65b;
	}
	.paper-colors i:nth-child(4) {
		background: #ffd21c;
	}
	.paper-colors i:nth-child(5) {
		background: #18243c;
	}
	.paper-saved {
		color: var(--muted-foreground);
		font: 0.58rem/1.25 var(--font-mono, monospace);
	}
	.paper-reader-body {
		display: grid;
		grid-template-columns: minmax(0, 1.45fr) minmax(10rem, 0.9fr);
		min-height: 27rem;
	}
	.paper-page {
		align-self: stretch;
		margin: 1.2rem;
		padding: 1.5rem 1.45rem;
		border: 1px solid var(--border);
		background: #fff;
		color: #171717;
	}
	:global(.dark) .paper-page {
		background-color: #2c2c2c;
		/* A fine grain over the flat graphite, so the sheet reads as matte stock rather than a screen fill. */
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .14 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
		color: #faf9f6;
	}
	:global(.dark) .paper-page-rule,
	:global(.dark) .paper-lines i {
		background: #faf9f6;
	}
	.paper-page-rule {
		height: 3px;
		margin: 0.15rem 0 0.8rem;
		background: #171717;
	}
	.paper-page-rule.thin {
		height: 1px;
		margin: 0.8rem 0 1.15rem;
	}
	.paper-page h4 {
		margin: 0.8rem 0;
		text-align: center;
		font:
			700 1.1rem Georgia,
			serif;
	}
	.paper-page h5 {
		margin: 1.2rem 0 0.65rem;
		font:
			700 0.88rem Georgia,
			serif;
	}
	.paper-lines {
		display: grid;
		gap: 0.42rem;
		margin: 0.7rem 0;
	}
	.paper-lines i {
		display: block;
		height: 6px;
		background: #3a3a3a;
	}
	.paper-lines i:nth-child(2) {
		width: 94%;
	}
	.paper-lines i:nth-child(3) {
		width: 88%;
	}
	.paper-lines i:nth-child(4) {
		width: 62%;
	}
	.paper-lines.short i {
		width: 94%;
	}
	.paper-lines.short i:nth-child(2) {
		width: 88%;
	}
	.paper-highlight {
		margin: 0.8rem 0;
		background: #ffe16a;
		padding: 0.6rem;
		color: #151515;
		font:
			italic 0.9rem/1.45 Georgia,
			serif;
	}
	.paper-annotation {
		margin: 0.9rem 0;
		color: #d32935;
		font: 0.68rem var(--font-mono, monospace);
	}
	.paper-notes {
		border-left: 1px solid var(--border);
		padding: 1.5rem 1.1rem;
		color: var(--foreground);
		font: 0.82rem/1.6 var(--font-sans, system-ui, sans-serif);
	}
	.paper-notes strong {
		color: var(--foreground);
	}
	.paper-notes p {
		margin-top: 1rem;
	}
	.paper-notes .note-highlight {
		color: var(--warn);
	}
	.paper-reader-footer {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 0.7rem;
		border-top: 1px solid var(--border);
		padding: 0.85rem 1rem;
		color: var(--muted-foreground);
		font: 0.63rem var(--font-mono, monospace);
	}
	.paper-reader-footer a {
		display: inline-flex;
		align-items: center;
		gap: 0.35rem;
		color: #ed454d;
		text-decoration: none;
	}
	.goal-statement-section {
		padding-block: clamp(3rem, 7vw, 6rem);
	}
	.goal-statement {
		max-width: 54rem;
		margin: 0 auto;
		text-align: center;
	}
	.goal-eyebrow {
		margin-bottom: 1.2rem;
		color: var(--primary);
		font: 700 0.7rem var(--font-mono, monospace);
		letter-spacing: 0.18em;
		text-transform: uppercase;
	}
	.goal-statement h2 {
		font-size: clamp(2rem, 5vw, 4rem);
		line-height: 1.08;
	}
	.goal-statement > p:last-child {
		max-width: 43rem;
		margin: 1.3rem auto 0;
		color: var(--muted-foreground);
		font-size: clamp(1.05rem, 2vw, 1.45rem);
		line-height: 1.55;
	}

	.research-code-row {
		grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
	}
	.research-challenge {
		background: var(--secondary);
	}
	.research-challenge .artifact-content {
		padding: 1.15rem;
	}
	.research-challenge h4 {
		margin-bottom: 1.25rem;
		font: 700 1.15rem/1.35 var(--font-sans, system-ui, sans-serif);
	}
	.challenge-level {
		margin-left: auto;
		border: 1px solid color-mix(in srgb, var(--warn) 45%, transparent);
		border-radius: 999px;
		padding: 0.2rem 0.6rem;
		color: var(--warn);
		white-space: nowrap;
	}
	.challenge-eyebrow {
		margin: 1.15rem 0 0.45rem;
		color: var(--muted-foreground);
		font: 0.62rem var(--font-mono, monospace);
		letter-spacing: 0.14em;
		text-transform: uppercase;
	}
	.research-challenge .artifact-statement {
		margin-bottom: 0.75rem;
	}
	.research-challenge .artifact-statement code,
	.challenge-constraints code {
		border-radius: 4px;
		background: color-mix(in srgb, var(--foreground) 9%, transparent);
		padding: 0.1rem 0.3rem;
		color: var(--foreground);
	}
	.challenge-constraints {
		margin: 0.4rem 0 0.75rem;
		padding-left: 1.2rem;
		color: var(--foreground);
		font: 0.78rem/1.6 var(--font-sans, system-ui, sans-serif);
	}
	.challenge-run {
		display: flex;
		justify-content: space-between;
		border-top: 1px solid var(--border);
		margin-top: 0.9rem;
		padding-top: 0.9rem;
		color: var(--muted-foreground);
		font: 0.68rem var(--font-mono, monospace);
	}
	.challenge-run strong {
		color: var(--ok);
	}
	.research-code-principles {
		margin-top: 2rem;
	}
	.research-code-principles > div {
		grid-template-columns: 2rem 1fr;
		padding: 1rem 0;
	}
	.research-code-principles strong {
		font-size: 0.9rem;
	}
	.research-code-principles small {
		font-size: 0.82rem;
	}

	.learning-row-flip {
		grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
	}
	.learning-row-flip .learning-copy {
		order: 2;
	}
	.learning-index {
		color: var(--primary);
		font: 700 0.8rem var(--font-mono, ui-monospace, monospace);
		letter-spacing: 0.08em;
	}
	.learning-kicker {
		margin-left: 0.75rem;
		color: var(--muted-foreground);
		font: 0.7rem var(--font-mono, ui-monospace, monospace);
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}
	.learning-index-list,
	.learning-principles {
		margin-top: 2rem;
		border-top: 1px solid var(--border);
	}
	.learning-index-list a {
		display: grid;
		grid-template-columns: 1.5rem minmax(0, 1fr) auto;
		align-items: baseline;
		gap: 0.7rem;
		padding: 0.9rem 0;
		border-bottom: 1px solid var(--border);
		color: var(--foreground);
		text-decoration: none;
	}
	.learning-index-list a:hover strong {
		color: var(--primary);
	}
	.learning-index-list a > span,
	.learning-principles > div > span {
		color: var(--muted-foreground);
		font: 0.7rem var(--font-mono, ui-monospace, monospace);
	}
	.learning-index-list strong {
		overflow-wrap: anywhere;
		font: 600 0.78rem var(--font-mono, ui-monospace, monospace);
	}
	.learning-index-list small {
		color: var(--muted-foreground);
		font: 0.7rem var(--font-mono, ui-monospace, monospace);
	}
	.learning-link {
		display: inline-flex;
		align-items: center;
		gap: 0.6rem;
		margin-top: 1.7rem;
		color: var(--primary);
		font: 700 0.8rem var(--font-mono, ui-monospace, monospace);
		text-decoration: none;
	}
	.learning-link:hover {
		text-decoration: underline;
	}
	.artifact-window {
		--ok: #1a9a5c;
		--warn: #b9770e;
		--syn-key: #cf222e;
		--syn-fn: #0969da;
		--syn-num: #0550ae;
		min-width: 0;
		overflow: hidden;
		border: 1px solid var(--border);
		border-radius: 11px;
		background: var(--secondary);
		color: var(--foreground);
		box-shadow: 0 18px 55px rgb(0 0 0 / 12%);
		font-family: ui-monospace, 'SF Mono', Menlo, monospace;
	}
	:global(.dark) .artifact-window {
		--ok: #2fd180;
		--warn: #e8b13a;
		--syn-key: #ff7b72;
		--syn-fn: #79c0ff;
		--syn-num: #a5d6ff;
	}
	.artifact-chrome {
		display: flex;
		align-items: center;
		gap: 0.65rem;
		min-height: 42px;
		border-bottom: 1px solid var(--border);
		padding: 0.65rem 0.9rem;
		color: var(--muted-foreground);
		font-size: 0.68rem;
	}
	.artifact-right {
		margin-left: auto;
		white-space: nowrap;
	}
	.artifact-tabs {
		display: flex;
		gap: 1.25rem;
		border-bottom: 1px solid var(--border);
		padding: 0 1rem;
		color: var(--muted-foreground);
		font-size: 0.68rem;
	}
	.artifact-tabs .active {
		border-color: #d93a40;
		color: var(--foreground);
	}
	.artifact-content {
		padding: 1.25rem;
	}
	.artifact-content h4 {
		font: 700 1rem var(--font-sans, system-ui, sans-serif);
	}
	.artifact-meta {
		margin: 0.35rem 0 1rem;
		color: var(--muted-foreground);
		font-size: 0.68rem;
	}
	.artifact-meta b {
		color: var(--warn);
	}
	.artifact-meta span {
		padding: 0 0.2rem;
	}
	.artifact-statement {
		margin-bottom: 1rem;
		color: var(--muted-foreground);
		font: 0.8rem/1.6 var(--font-sans, system-ui, sans-serif);
	}
	.artifact-content pre {
		overflow-x: auto;
		border: 1px solid var(--border);
		border-radius: 7px;
		background: var(--background);
		padding: 0.9rem;
		color: var(--foreground);
		font-size: 0.68rem;
		line-height: 1.7;
	}
	.syntax-key {
		color: var(--syn-key);
	}
	.syntax-fn {
		color: var(--syn-fn);
	}
	.syntax-num {
		color: var(--syn-num);
	}
	.artifact-tests {
		display: flex;
		justify-content: space-between;
		gap: 0.5rem;
		margin-top: 1rem;
		color: var(--muted-foreground);
		font-size: 0.65rem;
	}
	.artifact-tests b {
		color: var(--ok);
	}
	.artifact-test-row {
		border-top: 1px solid var(--border);
		padding: 0.55rem 0;
		color: var(--ok);
		font-size: 0.7rem;
	}
	.artifact-test-row span {
		margin-left: 0.45rem;
		color: var(--muted-foreground);
	}
	.learning-principles > div {
		display: grid;
		grid-template-columns: 1.5rem 1fr;
		gap: 0.65rem;
		padding: 0.9rem 0;
		border-bottom: 1px solid var(--border);
	}
	.learning-principles strong {
		font-size: 0.88rem;
	}
	.learning-principles small {
		display: block;
		margin-top: 0.15rem;
		color: var(--muted-foreground);
		font-size: 0.75rem;
	}
	.dsa-artifact {
		align-self: center;
	}
	.dsa-preview-head {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 1.1rem 1.2rem 0.8rem;
	}
	.dsa-preview-head strong {
		font: 700 0.95rem var(--font-sans, system-ui, sans-serif);
	}
	.dsa-preview-head > span {
		color: var(--muted-foreground);
		font-size: 0.62rem;
	}
	.dsa-preview-group {
		border-top: 1px solid var(--border);
	}
	.dsa-preview-group-head {
		display: flex;
		justify-content: space-between;
		gap: 0.5rem;
		background: color-mix(in srgb, var(--foreground) 4%, transparent);
		padding: 0.55rem 1.2rem;
		color: var(--muted-foreground);
		font-size: 0.62rem;
		letter-spacing: 0.04em;
	}
	.dsa-preview-question {
		display: grid;
		grid-template-columns: 1rem minmax(0, 1fr) auto 0.9rem;
		align-items: center;
		gap: 0.55rem;
		border-bottom: 1px solid var(--border);
		padding: 0.75rem 1.2rem;
		color: var(--foreground);
		text-decoration: none;
	}
	.dsa-preview-question:hover {
		background: color-mix(in srgb, var(--foreground) 5%, transparent);
	}
	.dsa-preview-question strong {
		overflow-wrap: anywhere;
		font: 500 0.72rem var(--font-sans, system-ui, sans-serif);
	}
	.dsa-status {
		color: var(--muted-foreground);
	}
	.dsa-difficulty {
		font-size: 0.62rem;
	}
	.dsa-difficulty.beginner {
		color: var(--ok);
	}
	.dsa-difficulty.intermediate {
		color: var(--warn);
	}
	.dsa-difficulty.advanced {
		color: #d93a40;
	}
	.dsa-preview-footer {
		display: flex;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 0.9rem 1.2rem;
		color: var(--muted-foreground);
		font-size: 0.62rem;
	}
	.dsa-preview-footer a {
		display: inline-flex;
		align-items: center;
		gap: 0.35rem;
		color: #d93a40;
		text-decoration: none;
	}
	.artifact-tabs a {
		padding: 0.7rem 0;
		border-bottom: 2px solid transparent;
		color: var(--muted-foreground);
		text-decoration: none;
		white-space: nowrap;
	}
	.artifact-tabs a:hover {
		color: var(--foreground);
	}
	.artifact-tabs a.active {
		border-color: #d93a40;
		color: var(--foreground);
	}
	.dsa-topic-links {
		display: flex;
		flex-wrap: wrap;
		gap: 0.45rem;
		border-top: 1px solid var(--border);
		padding: 0.8rem 1.2rem 1rem;
	}
	.dsa-topic-links a {
		border: 1px solid var(--border);
		border-radius: 999px;
		padding: 0.28rem 0.65rem;
		color: var(--muted-foreground);
		font-size: 0.65rem;
		text-decoration: none;
	}
	.dsa-topic-links a:hover {
		border-color: #d93a40;
		color: var(--foreground);
	}
	@media (max-width: 767px) {
		.paper-reader-body {
			grid-template-columns: minmax(0, 1fr);
		}
		.paper-notes {
			border-top: 1px solid var(--border);
			border-left: 0;
		}
		.paper-colors {
			margin-left: 0;
		}
		.learning-row,
		.learning-row-flip {
			grid-template-columns: minmax(0, 1fr);
			gap: 2rem;
			padding: 3.5rem 0;
		}
		.learning-row-flip .learning-copy {
			order: 0;
		}
		.learning-index-list a {
			grid-template-columns: 1.2rem minmax(0, 1fr) auto;
		}
		.learning-index-list strong {
			font-size: 0.68rem;
		}
	}

	.screen {
		padding-block: 2.5rem;
	}
	.screen > :global(*) {
		width: 100%;
	}
	@media (min-width: 768px) {
		.screen {
			min-height: min(calc(100svh - 3.5rem), 28rem);
			padding-block: 1.2rem;
			display: flex;
			flex-direction: column;
			justify-content: center;
		}
	}

	/* A restrained CRT/chromatic-aberration flicker on the hero wordmark
	   only -- two color-fringed copies of the same text, offset a couple
	   pixels and animated with a low-duty-cycle step function so it reads
	   as an occasional glitch, not a constant distracting wobble. Built
	   from the element's own text via ::before/::after + the `content`
	   attr() function (data-text), so it never drifts out of sync with an
	   edit to the heading itself. Dark-mode only: on white, a red/cyan
	   fringe reads as a misrendered element rather than a deliberate
	   effect, so light mode just gets the plain heading. */
	:global(.dark) .glitch-heading {
		position: relative;
	}
	:global(.dark) .glitch-heading::before,
	:global(.dark) .glitch-heading::after {
		content: attr(data-text);
		position: absolute;
		inset: 0;
		background: var(--background);
		clip-path: inset(0 0 0 0);
	}
	:global(.dark) .glitch-heading::before {
		color: #ff3b30;
		animation: glitch-shift-1 7s steps(1) infinite;
	}
	:global(.dark) .glitch-heading::after {
		color: #22d3ee;
		animation: glitch-shift-2 7s steps(1) infinite;
	}
	@keyframes glitch-shift-1 {
		0%,
		92%,
		100% {
			transform: translate(0, 0);
			opacity: 0;
			clip-path: inset(0 0 100% 0);
		}
		93% {
			transform: translate(-2px, 1px);
			opacity: 0.7;
			clip-path: inset(10% 0 60% 0);
		}
		95% {
			transform: translate(2px, -1px);
			opacity: 0.7;
			clip-path: inset(55% 0 15% 0);
		}
		97% {
			opacity: 0;
		}
	}
	@keyframes glitch-shift-2 {
		0%,
		94%,
		100% {
			transform: translate(0, 0);
			opacity: 0;
			clip-path: inset(0 0 100% 0);
		}
		95% {
			transform: translate(2px, -1px);
			opacity: 0.6;
			clip-path: inset(20% 0 50% 0);
		}
		96.5% {
			transform: translate(-2px, 1px);
			opacity: 0.6;
			clip-path: inset(65% 0 5% 0);
		}
		98% {
			opacity: 0;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		:global(.dark) .glitch-heading::before,
		:global(.dark) .glitch-heading::after {
			animation: none;
			opacity: 0;
		}
	}

	/* Monochrome logo masks for the learners marquee: the logo silhouette is
	   painted in currentColor, so every mark follows the surrounding text
	   colour in both themes with no per-theme assets needed. */
	.org-logo {
		display: inline-block;
		flex: none;
		background: currentColor;
		-webkit-mask: var(--logo) center / contain no-repeat;
		mask: var(--logo) center / contain no-repeat;
	}

	/* Display face for the two big headlines. Space Grotesk pairs well with the
	   monospace wordmark; falls back to the app's sans if the font is blocked. */
	.display {
		font-family: 'Space Grotesk', var(--font-sans, ui-sans-serif), system-ui, sans-serif;
		font-weight: 700;
		letter-spacing: -0.03em;
		line-height: 1.08;
	}
</style>
