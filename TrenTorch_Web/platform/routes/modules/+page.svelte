<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowRight } from '@lucide/svelte';
	import DomainArt from '$components/DomainArt.svelte';
	import PagePill from '$components/PagePill.svelte';
	import SEO from '$components/SEO.svelte';
	import { Badge } from '$components/ui/badge';
	import { Progress } from '$components/ui/progress';
	import { aiSystemsParts, domains, type DomainId } from '$data/domains';
	import { dsaQuestions, dsaSteps } from '$data/dsa-sheet';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';
	import { signInSkipped } from '$processes/auth/preview-mode';
	import { session } from '$processes/auth/session.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import { buildBreadcrumbJsonLd } from '$processes/seo/build-breadcrumb-json-ld';
	import { withSiteName } from '$processes/seo/with-site-name';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const aiIds = aiSystemsParts.flatMap((part) =>
		part.tracks.flatMap((track) => track.questions.map((question) => question.slug))
	);
	const dsaIds = dsaQuestions.map((question) => question.id);

	// What each live domain's card shows: a count line and how much is solved.
	const facts = $derived.by<Partial<Record<DomainId, { line: string; ids: string[] }>>>(() => ({
		aisys: { line: `${aiSystemsParts.length} modules · ${aiIds.length} questions`, ids: aiIds },
		gpu: {
			line: `${data.cudaChapters} chapters · ${data.cudaIds.length} problems`,
			ids: data.cudaIds
		},
		software: { line: `${dsaSteps.length} steps · ${dsaIds.length} questions`, ids: dsaIds }
	}));
	const doneIn = (ids: string[]) => ids.filter((id) => solved.isSolved(id)).length;

	// Each card's tint, mixed into the page background so it works in both themes.
	const HUES: Record<DomainId, string> = {
		aisys: '#d28b7a',
		gpu: '#7fb59a',
		software: '#a597d1',
		'system-design': '#c9a86a',
		robotics: '#7fa7c9'
	};
	// The last word of a two-word title is set in italics.
	const split = (title: string) => {
		const at = title.lastIndexOf(' ');
		return at < 0 ? [title, ''] : [title.slice(0, at), title.slice(at + 1)];
	};

	// Cards fill their row whatever the count: three to a row on wide screens
	// and two on medium ones, with the last row's cards stretched to the full width.
	const lgSpan = (index: number, total: number) => {
		const left = total % 3;
		if (index < total - left) return 'lg:col-span-2';
		return left === 1 ? 'lg:col-span-6' : 'lg:col-span-3';
	};
	const mdSpan = (index: number, total: number) =>
		total % 2 === 1 && index === total - 1 ? 'md:col-span-2' : '';
	// A card that spans a whole row lays its drawing beside its text.
	const wideAt = (index: number, total: number) => {
		const lg = total % 3 === 1 && index === total - 1;
		const md = total % 2 === 1 && index === total - 1;
		return [md ? 'md:flex-row' : '', md && !lg ? 'lg:flex-col' : ''].join(' ');
	};

	// Guests browse this page freely; opening a domain asks them to sign in.
	const showSignIn = $derived(!session.isLoading && !session.user && !signInSkipped());
</script>

<SEO
	title={withSiteName('Modules')}
	description="Structured paths of theory and hands-on problems, in AI systems, GPU programming and software engineering. Run the tests in your browser."
	path="/modules"
	jsonLd={buildBreadcrumbJsonLd([
		{ name: 'Home', path: '/' },
		{ name: 'Modules', path: '/modules' }
	])}
/>

<div class="px-4 pt-7 pb-12 sm:px-5 md:px-6">
	<div class="mx-auto w-full max-w-[1180px] space-y-8">
		<header class="dot-texture">
			<PagePill slug="modules/" area="module" />
			<h1 class="mb-3 font-mono text-3xl font-bold tracking-tight sm:text-4xl">Modules</h1>
			<p class="max-w-xl text-lg text-muted-foreground">
				Pick a domain. Each one is a structured path of theory and problems that run in your
				browser.
			</p>
		</header>

		<ul class="grid gap-5 md:grid-cols-2 lg:grid-cols-6">
			{#each domains as domain, index (domain.id)}
				{@const fact = facts[domain.id]}
				{@const [lead, last] = split(domain.title)}
				{@const live = Boolean(domain.href && fact)}
				<li
					class="domain-card relative isolate flex flex-col overflow-hidden rounded-3xl border border-border shadow-sm transition-[transform,box-shadow] duration-500 {lgSpan(
						index,
						domains.length
					)} {mdSpan(index, domains.length)} {wideAt(index, domains.length)} {live
						? 'hover:-translate-y-0.5 hover:shadow-xl'
						: ''}"
					style="--hue: {HUES[
						domain.id
					]}; background-color: color-mix(in oklab, var(--hue) 22%, var(--background));"
				>
					<!-- a soft dotted texture, blurred and faded out beneath the art so the text stays clear -->
					<div
						class="pointer-events-none absolute inset-0 -z-10 blur-[1.2px]"
						style="background-image: radial-gradient(color-mix(in oklab, var(--foreground) 7%, transparent) 1px, transparent 1.4px); background-size: 5px 5px; mask-image: linear-gradient(to bottom, black 35%, transparent 60%);"
						aria-hidden="true"
					></div>
					<div class="px-4 pt-4 md:flex-1 {live ? '' : 'opacity-60 saturate-50'}">
						<DomainArt id={domain.id} {live} />
					</div>
					<div class="flex flex-1 flex-col gap-4 px-6 pt-3 pb-6">
						<div>
							<h2 class="font-mono text-2xl leading-tight font-bold tracking-tight">
								{lead}{#if last}&nbsp;<i class="font-medium">{last}</i>{/if}
							</h2>
							<p class="mt-2 text-sm text-foreground/70">{domain.blurb}</p>
						</div>
						<div class="mt-auto flex flex-wrap items-center justify-between gap-3">
							{#if live && fact && domain.href}
								{@const done = doneIn(fact.ids)}
								<div class="min-w-0">
									<p class="font-mono text-xs text-foreground/80">{fact.line}</p>
									{#if done > 0}
										<Progress value={done} max={fact.ids.length} class="mt-2 h-1 w-40" />
									{/if}
								</div>
								<a
									href={resolve(domain.href as '/')}
									onclick={gateBehindSignIn}
									aria-label="{showSignIn ? 'Sign in to open' : 'Open'} {domain.title}"
									class="group inline-flex h-11 items-center gap-2 rounded-xl bg-foreground px-5 text-sm font-medium whitespace-nowrap text-background shadow-md after:absolute after:inset-0 after:content-[''] focus-visible:outline-none"
								>
									{showSignIn ? 'Sign in to open' : 'Open'}
									<ArrowRight
										class="size-4 transition-transform group-hover:translate-x-0.5"
										aria-hidden="true"
									/>
								</a>
							{:else}
								<Badge
									variant="outline"
									class="h-6 rounded-full border-foreground/30 px-3 text-xs text-foreground/70"
									>soon</Badge
								>
							{/if}
						</div>
					</div>
				</li>
			{/each}
		</ul>
	</div>
</div>
