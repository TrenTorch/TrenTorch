<script lang="ts">
	import { resolve } from '$app/paths';
	import LogoBadge from '$components/LogoBadge.svelte';
	import Button from '$components/Button.svelte';
	import StatTile from '$components/StatTile.svelte';
	import HowItWorks from '$components/HowItWorks.svelte';
	import Testimonials from '$components/Testimonials.svelte';
	import { BookOpen, CalendarCheck, ArrowRight } from '@lucide/svelte';
	import Github from '$components/GithubIcon.svelte';
	import SEO from '$components/SEO.svelte';
	import DifficultyBadge from '$components/DifficultyBadge.svelte';
	import { curriculum, getProgressStats } from '$data/questions';
	import { buildSiteJsonLd } from '$processes/seo/build-site-json-ld';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';
	import { browser } from '$app/environment';
	import { getTodaysPotd } from '$processes/potd/get-todays-potd';

	// Client-only, same as /potd's own "today" resolution: there is no real
	// visitor "now" at prerender time (see get-todays-potd.ts).
	const todaysProblem = $derived(browser ? getTodaysPotd() : undefined);

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch';

	const totalQuestions = getProgressStats().total;
	const totalParts = curriculum.length;

	// Organisations seen in signup email domains (aggregate only, no individuals).
	// Institutions are kept general (IITs, NITs, VIT) rather than naming one campus.
	// Keep in sync with the DB. The matching disclaimer lives in Footer.svelte.
	const LEARNER_ORGS = ['xAI', 'Uber', 'BITS Hyderabad', 'IITs', 'NITs', 'VIT', 'and more'];
	// Duplicated once so the marquee loops seamlessly.
	const MARQUEE_ITEMS = [...LEARNER_ORGS, ...LEARNER_ORGS];

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

<div>
	<!-- Hero -->
	<section class="container flex flex-col items-center px-4 pt-24 pb-16 text-center md:px-6">
		{#if todaysProblem}
			<a
				href={resolve('/ide/[id]', { id: todaysProblem.question.slug })}
				class="mb-6 flex w-fit items-center gap-3 rounded-full border border-border bg-secondary/50 px-4 py-2 font-mono text-xs transition-colors hover:border-foreground/30 hover:bg-secondary"
			>
				<CalendarCheck class="size-3.5 text-primary" />
				<span class="text-muted-foreground">Today's Problem:</span>
				<span class="font-semibold">{todaysProblem.question.title}</span>
				<DifficultyBadge difficulty={todaysProblem.question.difficulty} />
				<ArrowRight class="size-3.5" />
			</a>
		{/if}
		<LogoBadge class="mb-8 size-36" />
		<h1
			class="glitch-heading mb-4 font-mono text-4xl font-bold tracking-[0.02em] sm:text-6xl"
			data-text="TrenTorch"
		>
			TrenTorch
		</h1>
		<p class="mb-2 max-w-2xl text-2xl font-semibold sm:text-3xl">Learn ML by building it.</p>
		<p class="mb-8 max-w-2xl text-lg text-muted-foreground">
			Linear regression to transformers, coded from scratch, graded instantly. No terminal, no
			setup, just your browser.
		</p>
		<div class="flex flex-wrap items-center justify-center gap-3">
			<Button size="lg" href={resolve('/questions')} onclick={gateBehindSignIn}>
				<BookOpen class="size-4" />
				Questions
			</Button>
			<Button
				size="lg"
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
	<section class="container px-4 pb-16 md:px-6">
		<div class="mx-auto grid max-w-md grid-cols-2 gap-4">
			<StatTile label="Questions" value={totalQuestions} tone="positive" />
			<StatTile label="Tracks" value={totalParts} tone="positive" />
		</div>
	</section>

	<!-- Learners from: aggregate signup email domains, scrolling marquee.
	     Disclaimer is in the footer. -->
	<section class="container px-4 pb-16 text-center md:px-6">
		<h2 class="mb-6 text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
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
	<section class="pb-16">
		<Testimonials />
	</section>

	<!-- How it works -->
	<section class="container px-4 pb-16 md:px-6">
		<h2
			class="mb-8 text-center font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase"
		>
			How it works
		</h2>
		<HowItWorks />
	</section>

	<!-- Features -->
	<section class="container px-4 pb-24 md:px-6">
		<div class="mx-auto grid max-w-4xl gap-px border bg-border sm:grid-cols-2">
			{#each FEATURES as feature (feature.title)}
				<div class="bg-background p-6">
					<h3 class="mb-2 font-mono font-semibold">{feature.title}</h3>
					<p class="text-sm text-muted-foreground">{feature.body}</p>
				</div>
			{/each}
		</div>
	</section>
</div>

<style>
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
	   strip with a faint dot texture and faded edges. Pauses on hover. */
	.marquee {
		position: relative;
		overflow: hidden;
		border: 1px solid var(--border);
		background-image: radial-gradient(
			color-mix(in oklab, var(--muted-foreground) 22%, transparent) 1px,
			transparent 1px
		);
		background-size: 12px 12px;
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
		border-right: 1px solid var(--border);
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
</style>
