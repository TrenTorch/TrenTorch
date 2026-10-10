<script lang="ts">
	import { resolve } from '$app/paths';
	import Button from '$components/Button.svelte';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';
	import StatTile from '$components/StatTile.svelte';
	import ProductTour from '$components/ProductTour.svelte';
	import Testimonials from '$components/Testimonials.svelte';
	import InfiniteMarquee from '$components/InfiniteMarquee.svelte';
	import {
		BookOpen,
		Heart,
		CalendarCheck,
		ArrowRight,
		Lightbulb,
		ListChecks,
		Terminal,
		Cpu,
		Trophy,
		FlaskConical,
		Bug,
		Layers,
		Users
	} from '@lucide/svelte';
	import SEO from '$components/SEO.svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import { Play } from '@lucide/svelte';
	import { curriculum, getProgressStats, getDifficultyProgress } from '$data/questions';
	import { buildSiteJsonLd } from '$processes/seo/build-site-json-ld';
	import { browser } from '$app/environment';
	import { getTodaysPotd } from '$processes/potd/get-todays-potd';
	import { problemsetProblems } from '$data/problemset';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();

	// Client-only, same as /potd's own "today" resolution: there is no real
	// visitor "now" at prerender time (see get-todays-potd.ts).
	const todaysProblem = $derived(browser ? getTodaysPotd(data.potdSummaries) : undefined);

	const SUPPORT_URL = 'https://github.com/sponsors/Shashank-Tripathi-07';

	// A real question's slug (Part 2, DL core mechanics -- see data/questions.ts),
	// shown as a static preview on the right of the hero. Not an interactive
	// editor: the real one pulls in CodeMirror + Pyodide, far too heavy to ship
	// on the landing page just to fill the hero's right column.
	const HERO_DEMO_SLUG = 'dl-core-softmax';

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

	const DO_LIST = [
		{ icon: Lightbulb, title: 'Learn the theory', body: 'Behind each concept, before any code' },
		{
			icon: ListChecks,
			title: 'Follow worked examples',
			body: 'Step-by-step implementation walkthroughs'
		},
		{
			icon: Terminal,
			title: 'Solve coding challenges',
			body: 'Hands-on, with instant feedback on every run'
		},
		{
			icon: Cpu,
			title: 'Build everything from scratch',
			body: 'ML to inference & kernels, Codeforces-style grading'
		},
		{
			icon: Trophy,
			title: 'Earn ratings',
			body: 'Take on the Problem of the Day, build a streak'
		}
	];

	const FEATURES = [
		{
			icon: FlaskConical,
			title: 'Real PyTorch, not a stand-in',
			body: 'What you implement is what the library actually does'
		},
		{
			icon: Bug,
			title: 'Tests that actually catch bugs',
			body: 'Every Submit runs an exhaustive hidden test suite'
		},
		{
			icon: Layers,
			title: 'Linear algebra to LLM post-training',
			body: `${totalProblems} problems across ${totalParts} learning modules: Classical ML to Production Systems, all built from scratch`
		},
		{
			icon: Users,
			title: 'Open source, same team',
			body: 'Built by the same maintainers, under the governance and Code of Conduct of TrenTorch CLI'
		}
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
				{#if todaysProblem}
					<a
						href={resolve('/ide/[id]', { id: todaysProblem.question.slug })}
						class="mb-5 flex w-fit items-center gap-3 rounded-full border border-border bg-secondary/50 px-4 py-2 font-mono text-xs transition-colors hover:bg-secondary"
					>
						<CalendarCheck class="size-3.5 text-primary" />
						<span class="text-muted-foreground">Today's Problem:</span>
						<span class="font-semibold">{todaysProblem.question.title}</span>
						<DifficultyBadge difficulty={todaysProblem.question.difficulty} />
						<ArrowRight class="size-3.5" />
					</a>
				{/if}
				<h1
					class="glitch-heading mb-3 font-mono text-3xl font-bold tracking-[0.02em] sm:text-5xl"
					data-text="TrenTorch"
				>
					TrenTorch
				</h1>
				<p class="display mb-4 max-w-xl text-3xl text-balance sm:text-4xl">
					Don't memorize ML. Understand it from first principles.
				</p>
				<p class="mb-3 max-w-xl text-lg text-muted-foreground">
					Write every algorithm from scratch, from linear regression, neural networks, RL and
					inference to kernels, and see exactly what your code does at every step. {totalProblems}+
					problems with theory and practical explanation.
				</p>
				<p class="mb-7 font-mono text-sm text-muted-foreground">
					Free. No subscriptions. Powered by sponsors and donations.
				</p>
				<div class="flex flex-wrap items-center justify-center gap-3 lg:justify-start">
					<Button size="lg" class="rounded-xl!" href={resolve('/problemset')}>
						<BookOpen class="size-4" />
						Problemset
					</Button>
					<Button
						size="lg"
						class="rounded-xl!"
						variant="outline"
						href={resolve('/questions')}
						onclick={gateBehindSignIn}
					>
						<Layers class="size-4" />
						Module
					</Button>
				</div>
				<div class="mt-8 grid grid-cols-2 gap-4">
					<StatTile label="Problems" value={totalProblems} tone="positive" />
					<StatTile label="Learning modules" value={totalParts} tone="positive" />
				</div>
				<!-- Real per-difficulty split, not a marketing round number: the
				     exact Easy/Medium/Hard totals the curriculum data actually has. -->
				<p class="mt-4 max-w-xl font-mono text-xs text-muted-foreground">
					{difficultyTotals[0].total} easy &middot; {difficultyTotals[1].total} medium &middot; {difficultyTotals[2]
						.total} hard. Most of it is past where a tutorial would have stopped.
				</p>
			</div>

			<!-- Static preview of a real question, styled like an editor window.
			     Fills the column an interactive demo would fill, without
			     pulling CodeMirror/Pyodide into the landing page bundle. -->
			<div class="w-full max-w-md shrink-0 lg:max-w-lg">
				<a
					href={resolve('/ide/[id]', { id: HERO_DEMO_SLUG })}
					class="group block overflow-hidden rounded-2xl border border-border bg-secondary/30 text-left shadow-sm transition-colors hover:border-primary/40"
				>
					<div class="flex items-center justify-between border-b border-border px-4 py-2.5">
						<div class="flex items-center gap-3">
							<span class="flex gap-1.5" aria-hidden="true">
								<span class="size-2.5 rounded-full bg-red-500/70"></span>
								<span class="size-2.5 rounded-full bg-yellow-500/70"></span>
								<span class="size-2.5 rounded-full bg-green-500/70"></span>
							</span>
							<span class="font-mono text-xs text-muted-foreground">softmax.py</span>
						</div>
						<DifficultyBadge difficulty="Medium" />
					</div>
					<pre class="overflow-x-auto px-4 py-4 font-mono text-[13px] leading-relaxed"><code
							><span class="text-sky-500 dark:text-sky-400">import</span> numpy <span
								class="text-sky-500 dark:text-sky-400">as</span
							> np

<span class="text-sky-500 dark:text-sky-400">def</span> <span
								class="text-amber-600 dark:text-amber-300">softmax</span
							>(x):
    <span class="text-muted-foreground"># subtract the row max first -- same result,</span>
    <span class="text-muted-foreground"># keeps exp() from overflowing on large logits</span>
    shifted = x - np.<span class="text-amber-600 dark:text-amber-300">max</span>(x, axis=-<span
								class="text-emerald-600 dark:text-emerald-400">1</span
							>, keepdims=<span class="text-sky-500 dark:text-sky-400">True</span>)
    exp_x = np.exp(shifted)
    <span class="text-sky-500 dark:text-sky-400">return</span> exp_x / exp_x.sum(
        axis=-<span class="text-emerald-600 dark:text-emerald-400">1</span>, keepdims=<span
								class="text-sky-500 dark:text-sky-400">True</span
							>
    )</code
						></pre>
					<div
						class="flex items-center justify-between border-t border-border px-4 py-2.5 font-mono text-xs text-muted-foreground"
					>
						<span>Softmax fwd/bwd &middot; Deep Learning: Core Mechanics</span>
						<span
							class="flex items-center gap-1.5 text-primary transition-transform group-hover:translate-x-0.5"
						>
							<Play class="size-3" />
							Try it
						</span>
					</div>
				</a>
			</div>
		</div>
	</section>

	<!-- Learners from: aggregate signup email domains, scrolling marquee.
	     Disclaimer is in the footer. -->
	<section class="container px-4 py-8 text-center md:px-6 md:py-10">
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

	<!-- How it works: a numbered tour, each step paired with a mockup of the
	     real surface it happens on (same editor-window treatment as the hero)
	     instead of describing the workflow in prose alone. -->
	<section class="screen container px-4 md:px-6">
		<h2 class="mb-10 text-center text-2xl font-semibold sm:text-3xl">How it works</h2>
		<ProductTour />
	</section>

	<!-- What you'll do -->
	<section class="screen container px-4 md:px-6">
		<div class="mx-auto max-w-3xl">
			<h2 class="mb-3 text-center text-2xl font-semibold sm:text-3xl">Don't just watch. Build.</h2>
			<p class="mb-10 text-center text-muted-foreground">
				Lectures and theory only get you so far. On TrenTorch you write the code yourself.
			</p>
			<!-- A card grid, one icon per step, instead of a plain bordered list:
			     each card names the action and the one line of payoff it has,
			     readable at a glance instead of as a wall of sentences. -->
			<ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
				{#each DO_LIST as item (item.title)}
					<li
						class="rounded-2xl border border-border p-6 text-left transition-[border-color,transform,box-shadow] duration-300 hover:-translate-y-1 hover:border-primary hover:shadow-[0_0_0_1px_var(--primary)] motion-reduce:transition-none motion-reduce:hover:translate-y-0"
					>
						<item.icon class="mb-3 size-5 text-primary" aria-hidden="true" />
						<h3 class="mb-1.5 font-semibold">{item.title}</h3>
						<p class="text-sm text-muted-foreground">{item.body}</p>
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
		<!-- A 2x2 icon card grid, same treatment as the "Don't just watch, build"
		     grid above -- these four are independent reasons to use the site,
		     not rows in a comparison table. -->
		<ul class="mx-auto grid max-w-3xl grid-cols-1 gap-4 sm:grid-cols-2">
			{#each FEATURES as feature (feature.title)}
				<li
					class="rounded-2xl border border-border p-6 text-left transition-[border-color,transform,box-shadow] duration-300 hover:-translate-y-1 hover:border-primary hover:shadow-[0_0_0_1px_var(--primary)] motion-reduce:transition-none motion-reduce:hover:translate-y-0"
				>
					<feature.icon class="mb-3 size-5 text-primary" aria-hidden="true" />
					<h3 class="mb-1.5 font-mono font-semibold">{feature.title}</h3>
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
				<svg
					viewBox="0 0 74 76"
					aria-hidden="true"
					class="wensity-sponsor-mark size-8 shrink-0 sm:size-9"
				>
					<use href="/wensity.svg#wensity-mark" />
				</svg>
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
	   same idea as a textured hero background, without
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
	.wensity-sponsor-mark {
		--wensity-back: #171717;
		--wensity-front: #d71920;
	}

	:global(.dark) .wensity-sponsor-mark {
		--wensity-back: #fff;
		--wensity-front: #d71920;
	}

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
