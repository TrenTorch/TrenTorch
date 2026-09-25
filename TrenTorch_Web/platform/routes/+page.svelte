<script lang="ts">
	import { resolve } from '$app/paths';
	import LogoBadge from '$components/LogoBadge.svelte';
	import Button from '$components/Button.svelte';
	import StatTile from '$components/StatTile.svelte';
	import HowItWorks from '$components/HowItWorks.svelte';
	import Testimonials from '$components/Testimonials.svelte';
	import { BookOpen, Heart, CalendarCheck, ArrowRight } from '@lucide/svelte';
	import Github from '$components/GithubIcon.svelte';
	import SEO from '$components/SEO.svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import { curriculum, getProgressStats } from '$data/questions';
	import { buildSiteJsonLd } from '$processes/seo/build-site-json-ld';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';
	import { browser } from '$app/environment';
	import { getTodaysPotd } from '$processes/potd/get-todays-potd';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();

	// Client-only, same as /potd's own "today" resolution: there is no real
	// visitor "now" at prerender time (see get-todays-potd.ts).
	const todaysProblem = $derived(browser ? getTodaysPotd(data.potdSummaries) : undefined);

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch';
	const SUPPORT_URL = 'https://github.com/sponsors/Shashank-Tripathi-07';

	const totalQuestions = getProgressStats().total;
	const totalParts = curriculum.length;

	// Organisations seen in signup email domains (aggregate only, no individuals).
	// Institutions are kept general (IITs, NITs, IIITs, BITS) rather than naming one campus.
	// Keep in sync with the DB. The matching disclaimer lives in Footer.svelte.
	const LEARNER_ORGS = [
		'xAI',
		'OpenAI',
		'Anthropic',
		'Stanford',
		'Harvard',
		'IITs',
		'IISc',
		'NITs',
		'IIITs',
		'BITS'
	];
	// Duplicated once so the marquee loops seamlessly.
	const MARQUEE_ITEMS = [...LEARNER_ORGS, ...LEARNER_ORGS];

	const DO_LIST = [
		'Learn the theory behind each concept',
		'Follow step-by-step implementation examples',
		'Solve coding challenges based on what you just learned',
		'Implement everything from scratch, from foundational ML to inference and kernels',
		'Practice in a Codeforces-style environment with instant grading',
		'Take on a new Problem of the Day, with ratings'
	];

	const FEATURES = [
		{
			title: 'Real PyTorch, not a stand-in',
			body: 'Functions mirror torch.nn.functional exactly: real signatures, real shape conventions, real bias=None and reduction semantics. What you implement is what the library actually does.'
		},
		{
			title: 'Tests that actually catch bugs',
			body: 'Every Submit runs an exhaustive hidden suite: edge cases, array hygiene, targeted mutation tests, some checked against real offline PyTorch output.'
		},
		{
			title: 'Linear algebra to LLM post-training',
			body: `${totalQuestions} questions across ${totalParts} tracks: classical ML, deep learning foundations, transformers, vision, and production ML engineering, all built from scratch.`
		},
		{
			title: 'Open source, same team',
			body: 'Built by the same maintainers, under the same governance and Code of Conduct as the TrenTorch CLI itself.'
		}
	];
</script>

<SEO
	title="TrenTorch | Free ML practice problems: build PyTorch from scratch"
	description={`${totalQuestions} free machine learning practice problems. Build PyTorch from scratch in Python and run the tests in your browser: classical ML, deep learning, transformers, inference, and more.`}
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
	<!-- Hero -->
	<section class="container flex flex-col items-center px-4 pt-10 pb-10 text-center sm:px-6 sm:pt-12 sm:pb-12 lg:px-8 lg:pt-14 lg:pb-14">
		{#if todaysProblem}
			<a
				href={resolve('/ide/[id]', { id: todaysProblem.question.slug })}
				class="mb-8 flex max-w-full flex-wrap items-center justify-center gap-x-2 gap-y-1 rounded-2xl border border-foreground bg-secondary/50 px-3 py-2.5 font-mono text-[11px] transition-colors hover:bg-secondary sm:w-fit sm:flex-nowrap sm:gap-3 sm:rounded-full sm:px-4 sm:text-xs"
			>
				<CalendarCheck class="size-3.5 text-primary" />
				<span class="text-muted-foreground">Today's Problem:</span>
				<span class="font-semibold">{todaysProblem.question.title}</span>
				<DifficultyBadge difficulty={todaysProblem.question.difficulty} />
				<ArrowRight class="size-3.5" />
			</a>
		{/if}
		<LogoBadge class="mb-7 size-28 sm:mb-8 sm:size-36" />
		<h1
			class="glitch-heading mb-4 font-mono text-4xl font-bold tracking-[0.02em] sm:text-6xl lg:text-7xl"
			data-text="TrenTorch"
		>
			TrenTorch
		</h1>
		<p class="display mb-4 max-w-3xl text-3xl text-balance sm:text-4xl md:text-5xl">
			Don't memorize ML. Understand it from first principles.
		</p>
		<p class="mb-4 max-w-2xl text-base text-muted-foreground sm:text-lg">
			Write every algorithm from scratch, from linear regression, neural networks, RL and inference
			to kernels, and see exactly what your code does at every step. {totalQuestions}+ problems with
			theory and practical explanation.
		</p>
		<p class="mb-8 max-w-xl font-mono text-xs text-muted-foreground sm:text-sm">
			Free. No subscriptions. Powered by sponsors and donations.
		</p>
		<div class="flex w-full flex-col items-stretch justify-center gap-3 sm:w-auto sm:flex-row sm:items-center">
			<Button size="lg" class="rounded-xl!" href={resolve('/questions')} onclick={gateBehindSignIn}>
				<BookOpen class="size-4" />
				Questions
			</Button>
			<Button
				size="lg"
				class="rounded-xl!"
				variant="outline"
				href={GITHUB_URL}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Github class="size-4" />
				View on GitHub
			</Button>
		</div>
	</section>

	<!-- Stats -->
	<section class="container px-4 py-10 sm:px-6 sm:py-12 lg:px-8">
		<div class="mx-auto grid max-w-md grid-cols-2 gap-3 sm:gap-4">
			<StatTile label="Questions" value={totalQuestions} tone="positive" />
			<StatTile label="Tracks" value={totalParts} tone="positive" />
		</div>
	</section>

	<!-- Learners from: aggregate signup email domains, scrolling marquee.
	     Disclaimer is in the footer. -->
	<section class="container px-4 py-10 text-center sm:px-6 sm:py-12 lg:px-8">
		<h2 class="display mb-6 text-3xl text-balance sm:text-4xl">
			Learners signing up from
			<span
				class="mt-2 block font-mono text-base font-normal tracking-normal text-muted-foreground sm:text-lg"
			>
				top companies and campuses
			</span>
		</h2>
		<div class="marquee mx-auto max-w-4xl" aria-label="Organizations learners signed up from">
			<div class="marquee-track">
				{#each MARQUEE_ITEMS as org, i (i)}
					<span class="marquee-chip" aria-hidden={i >= LEARNER_ORGS.length}>{org}</span>
				{/each}
			</div>
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

	<!-- How it works -->
	<section class="screen container px-4 sm:px-6 lg:px-8">
		<h2
			class="mb-10 text-center font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
		>
			How it works
		</h2>
		<HowItWorks />
	</section>

	<!-- What you'll do -->
	<section class="screen container px-4 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-3xl">
			<h2 class="mb-3 text-center text-2xl font-semibold sm:text-3xl">Don't just watch. Build.</h2>
			<p class="mb-10 text-center text-muted-foreground">
				Lectures and theory only get you so far. On TrenTorch you write the code yourself.
			</p>
			<ul
				class="grid gap-px overflow-hidden rounded-2xl border border-foreground bg-foreground sm:grid-cols-2"
			>
				{#each DO_LIST as item (item)}
					<li class="bg-background p-4 text-sm">{item}</li>
				{/each}
			</ul>
			<p class="mt-10 text-center text-lg font-medium text-balance">
				The goal isn't just to teach you how to write the code. It's to help you understand what
				your code is actually doing underneath.
			</p>
		</div>
	</section>

	<!-- Features -->
	<section class="screen container px-4 sm:px-6 lg:px-8">
		<div
			class="mx-auto grid max-w-4xl gap-px overflow-hidden rounded-2xl border border-foreground bg-foreground sm:grid-cols-2"
		>
			{#each FEATURES as feature (feature.title)}
				<div class="bg-background p-6">
					<h3 class="mb-2 font-mono font-semibold">{feature.title}</h3>
					<p class="text-sm text-muted-foreground">{feature.body}</p>
				</div>
			{/each}
		</div>
	</section>

	<!-- Sponsor -->
	<section class="container px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
		<div
			class="mx-auto flex w-full max-w-3xl flex-col items-center gap-2 rounded-2xl border border-foreground/15 bg-secondary/40 px-5 py-7 text-center sm:px-8 sm:py-9"
		>
			<p class="font-mono text-[10px] font-semibold tracking-[0.2em] text-muted-foreground uppercase">
				Proudly sponsored by
			</p>
			<a
				href="https://wensity.com/"
				target="_blank"
				rel="noopener noreferrer"
				aria-label="Wensity, opens in a new tab"
				class="font-signature text-5xl leading-tight font-semibold text-primary transition-colors hover:text-primary/80 focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-primary sm:text-6xl"
			>
				Wensity
			</a>
			<p class="max-w-lg text-sm text-muted-foreground sm:text-base">
				Thanks to Wensity for supporting free, hands-on machine learning education.
			</p>
		</div>
	</section>

	<!-- Free, and why -->
	<section class="screen container px-4 sm:px-6 lg:px-8" style="margin-bottom: 3rem">
		<div class="mx-auto max-w-3xl rounded-2xl border border-foreground p-8 text-center">
			<h2
				class="mb-3 font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
			>
				Free, and here's why
			</h2>
			<p class="mb-3 text-2xl font-semibold text-balance">
				Money shouldn't be the barrier to learning ML.
			</p>
			<p class="mb-3 text-muted-foreground">
				Advanced ML and inference education is often locked behind expensive monthly subscriptions.
				TrenTorch is a free alternative built for students.
			</p>
			<p class="mb-6 text-muted-foreground">
				We don't charge users and we don't sell your data. TrenTorch runs entirely on sponsorships
				and donations. If it helps you, consider supporting it so it stays free for the next
				learner.
			</p>
			{#if SUPPORT_URL}
				<Button class="rounded-xl!" href={SUPPORT_URL} target="_blank" rel="noopener noreferrer">
					<Heart class="size-4" />
					Support TrenTorch
				</Button>
			{/if}
		</div>
	</section>
</div>

<style>
	/* One section per screen on desktop: each block gets a viewport-tall
	   slot (minus the 3.5rem navbar) with its content centered, so a single
	   component holds the reader's attention at a time. Children are set to
	   full width so their own mx-auto/max-w-* still center and cap them
	   inside the flex column. On phones it is just generous vertical padding. */
	.screen {
		padding-block: clamp(3rem, 7vw, 5rem);
	}
	.screen > :global(*) {
		width: 100%;
	}
	@media (min-width: 768px) {
		.screen {
			min-height: min(calc(100svh - 4rem), 30rem);
			padding-block: clamp(3rem, 6vw, 5rem);
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

	/* Learners marquee: a slow, seamless horizontal scroll inside a bordered
	   strip with faded edges. Pauses on hover. */
	.marquee {
		position: relative;
		overflow: hidden;
		border-radius: 0.75rem;
		border: 1px solid var(--foreground);
		-webkit-mask-image: linear-gradient(to right, transparent, #000 12%, #000 88%, transparent);
		mask-image: linear-gradient(to right, transparent, #000 12%, #000 88%, transparent);
	}
	.marquee-track {
		display: flex;
		width: max-content;
		animation: marquee-scroll 28s linear infinite;
	}
	.marquee:hover .marquee-track {
		animation-play-state: paused;
	}
	.marquee-chip {
		flex: none;
		padding: 0.9rem 2rem;
		font-family: var(--font-mono, ui-monospace, monospace);
		font-size: 1.05rem;
		white-space: nowrap;
	}
	@keyframes marquee-scroll {
		to {
			transform: translateX(-50%);
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.marquee-track {
			animation: none;
			flex-wrap: wrap;
			justify-content: center;
			width: auto;
		}
		.marquee-chip[aria-hidden='true'] {
			display: none;
		}
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
