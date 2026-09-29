<script lang="ts">
	import { resolve } from '$app/paths';
	import LogoBadge from '$components/LogoBadge.svelte';
	import Button from '$components/Button.svelte';
	import StatTile from '$components/StatTile.svelte';
	import HowItWorks from '$components/HowItWorks.svelte';
	import Testimonials from '$components/Testimonials.svelte';
	import InfiniteMarquee from '$components/InfiniteMarquee.svelte';
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

	const DO_LIST = [
		'Learn the theory behind each concept',
		'Follow step-by-step implementation examples',
		'Solve hands-on coding challenges',
		'Implement everything from scratch, ML to inference & kernels\n(Codeforces-style environment with instant grading)',
		'Take on the Problem of the Day and earn ratings'
	];

	const FEATURES = [
		{
			title: 'Real PyTorch, not a stand-in',
			body: 'What you implement is what the library actually does'
		},
		{
			title: 'Tests that actually catch bugs',
			body: 'Every Submit runs an exhaustive hidden test suite'
		},
		{
			title: 'Linear algebra to LLM post-training',
			body: `${totalQuestions} questions across ${totalParts} tracks: Classical ML to Production Systems, all built from scratch`
		},
		{
			title: 'Open source, same team',
			body: 'Built by the same maintainers, under the governance and Code of Conduct of TrenTorch CLI'
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
	<section class="container flex flex-col items-center px-4 pt-6 pb-8 text-center md:px-6 md:pt-6">
		{#if todaysProblem}
			<a
				href={resolve('/ide/[id]', { id: todaysProblem.question.slug })}
				class="mb-6 flex w-fit items-center gap-3 rounded-full border border-border bg-secondary/50 px-4 py-2 font-mono text-xs transition-colors hover:bg-secondary"
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
			class="glitch-heading mb-4 font-mono text-4xl font-bold tracking-[0.02em] sm:text-6xl"
			data-text="TrenTorch"
		>
			TrenTorch
		</h1>
		<p class="display mb-4 max-w-3xl text-3xl text-balance sm:text-5xl">
			Don't memorize ML. Understand it from first principles.
		</p>
		<p class="mb-3 max-w-2xl text-lg text-muted-foreground">
			Write every algorithm from scratch, from linear regression, neural networks, RL and inference
			to kernels, and see exactly what your code does at every step. {totalQuestions}+ problems with
			theory and practical explanation.
		</p>
		<p class="mb-8 font-mono text-sm text-muted-foreground">
			Free. No subscriptions. Powered by sponsors and donations.
		</p>
		<div class="flex flex-wrap items-center justify-center gap-3">
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
	<section class="container px-4 py-8 md:px-6 md:py-12">
		<div class="mx-auto grid max-w-md grid-cols-2 gap-4">
			<StatTile label="Questions" value={totalQuestions} tone="positive" />
			<StatTile label="Tracks" value={totalParts} tone="positive" />
		</div>
	</section>

	<!-- Learners from: aggregate signup email domains, scrolling marquee.
	     Disclaimer is in the footer. -->
	<section class="container px-4 py-8 text-center md:px-6 md:py-12">
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

	<!-- How it works -->
	<section class="screen container px-4 md:px-6">
		<h2 class="mb-10 text-center text-2xl font-semibold sm:text-3xl">How it works</h2>
		<HowItWorks />
	</section>

	<!-- What you'll do -->
	<section class="screen container px-4 md:px-6">
		<div class="mx-auto max-w-3xl">
			<h2 class="mb-3 text-center text-2xl font-semibold sm:text-3xl">Don't just watch. Build.</h2>
			<p class="mb-10 text-center text-muted-foreground">
				Lectures and theory only get you so far. On TrenTorch you write the code yourself.
			</p>
			<!-- Flattened to a single-column list: the old gap-px grid read as a
			     2x3 comparison table, which implied rows/relationships that aren't
			     there -- these are six independent things you do on the site. -->
			<ul class="mx-auto max-w-3xl divide-y divide-border rounded-2xl border border-border">
				{#each DO_LIST as item (item)}
					<li class="px-6 py-5 text-center text-sm whitespace-pre-line">
						<h3>{item}</h3>
					</li>
				{/each}
			</ul>
			<p class="mt-10 text-center text-lg font-medium text-balance">
				The goal isn't just to teach you how to write the code<br />It's to help you understand what
				your code is actually doing underneath
			</p>
		</div>
	</section>

	<!-- Features -->
	<section class="screen container px-4 md:px-6">
		<!-- Same treatment as the list above: one feature per row instead of
		     a 2x2 table of cells. -->
		<ul class="mx-auto max-w-3xl divide-y divide-border rounded-2xl border border-border">
			{#each FEATURES as feature (feature.title)}
				<li class="px-6 py-7 text-center">
					<h3 class="mb-2 font-mono font-semibold">{feature.title}</h3>
					<p class="text-sm text-muted-foreground">{feature.body}</p>
				</li>
			{/each}
		</ul>
	</section>

	<!-- Sponsor -->
	<section class="container px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
		<div
			class="mx-auto flex w-full max-w-3xl flex-col items-center gap-2 rounded-2xl border border-border/15 bg-secondary/40 px-5 py-7 text-center sm:px-8 sm:py-9"
		>
			<p
				class="font-mono text-[14px] font-semibold tracking-[0.2em] text-muted-foreground uppercase"
			>
				Proudly Sponsored by
			</p>
			<a
				href="https://ui.wensity.com/?utm_source=trentorch&utm_medium=sponsorship&utm_campaign=trentorch_sponsor_2026"
				target="_blank"
				rel="noopener noreferrer"
				aria-label="Wensity, opens in a new tab"
				class="font-signature inline-flex items-center gap-3 text-5xl leading-tight font-semibold text-primary transition-colors hover:text-primary/80 focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-primary sm:text-6xl"
			>
				<img src="/wensity.svg" alt="" class="size-8 shrink-0 sm:size-9" />
				Wensity
			</a>
			<p class="max-w-lg text-sm text-muted-foreground sm:text-base">
				Thanks to Wensity for supporting our mission
			</p>
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

	<!-- Free, and why -->
	<section class="screen container px-4 md:px-6" style="margin-bottom: 3rem">
		<div class="mx-auto max-w-3xl rounded-2xl border border-border p-8 text-center">
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
