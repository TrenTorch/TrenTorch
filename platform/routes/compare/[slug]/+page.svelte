<script lang="ts">
	import { resolve } from '$app/paths';
	import SEO from '$components/SEO.svelte';
	import type { CompetitorCapabilityField } from '$data/competitors';
	import { CLAIMS } from '$processes/seo/claims';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	const competitor = $derived(data.competitor);

	type ComparisonRow = {
		label: string;
		trentorch: string;
		other: string;
		capabilityKey?: CompetitorCapabilityField;
	};

	const rows = $derived([
		{
			label: 'ML from scratch',
			trentorch: CLAIMS.fromScratch.text,
			other: competitor.coversFromScratchML,
			capabilityKey: 'coversFromScratchML'
		},
		{
			label: 'PyTorch',
			trentorch: CLAIMS.pytorchStyleImplementations.text,
			other: competitor.coversPyTorch,
			capabilityKey: 'coversPyTorch'
		},
		{
			label: 'CUDA / Triton',
			trentorch: CLAIMS.cudaTritonConcepts.text,
			other: competitor.coversCudaTriton,
			capabilityKey: 'coversCudaTriton'
		},
		{
			label: 'Inference / serving',
			trentorch: CLAIMS.inferenceSystems.text,
			other: competitor.coversInferenceServing,
			capabilityKey: 'coversInferenceServing'
		},
		{
			label: 'Instant / hidden-test grading',
			trentorch: CLAIMS.hiddenTestGrading.text,
			other: competitor.hasInstantGrading,
			capabilityKey: 'hasInstantGrading'
		},
		{
			label: 'Problem of the Day / rating',
			trentorch: CLAIMS.dailyRatedProblem.text,
			other: competitor.hasDailyProblemAndRating,
			capabilityKey: 'hasDailyProblemAndRating'
		},
		{
			label: 'Interactive visualizations',
			trentorch: CLAIMS.selectedVisualizations.text,
			other: competitor.hasInteractiveVisualizations,
			capabilityKey: 'hasInteractiveVisualizations'
		},
		{
			label: 'Research-paper implementations',
			trentorch: CLAIMS.researchPaperImplementations.live
				? CLAIMS.researchPaperImplementations.text
				: 'Not currently offered',
			other: competitor.hasResearchPaperImplementations,
			capabilityKey: 'hasResearchPaperImplementations'
		},
		{
			label: 'Pricing',
			trentorch: CLAIMS.freePractice.text,
			other: competitor.pricing
		}
	] satisfies ComparisonRow[]);

	function competitorCapability(value: string, note?: string): string {
		if (value === 'yes') return 'Listed on the official site';
		if (value === 'partial')
			return note ?? 'Part of this capability is listed; other details are unconfirmed';
		if (value === 'unverified') return 'Not confirmed in the official pages reviewed';
		return value;
	}

	function pricingLabel(value: string): string {
		if (value === 'freemium') return 'Free access and paid plans listed';
		if (value === 'paid') return 'Paid';
		return 'Free';
	}
</script>

<SEO {...data.seo} />

<main class="container max-w-4xl px-4 py-12 md:px-6">
	<a
		href={resolve('/')}
		class="mb-6 inline-flex font-mono text-xs tracking-wider text-muted-foreground uppercase hover:text-primary"
	>
		TrenTorch home
	</a>
	<h1 class="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
		{competitor.name} Alternative: TrenTorch vs {competitor.name}
	</h1>
	<p class="mb-8 max-w-3xl text-muted-foreground">
		TrenTorch is {CLAIMS.freePractice.text}. Learners can {CLAIMS.fromScratch.text}.
		{competitor.summary} If you are exploring alternatives for machine-learning practice, compare the
		currently listed capabilities below and follow the official links to decide what fits your needs.
	</p>

	<section class="mb-10 overflow-x-auto rounded-xl border border-border">
		<h2 class="px-5 pt-5 font-mono text-xl font-semibold">Capability overview</h2>
		<table class="w-full min-w-[44rem] border-collapse text-left text-sm">
			<thead>
				<tr class="border-b border-border">
					<th scope="col" class="p-4 font-semibold">Capability</th>
					<th scope="col" class="p-4 font-semibold">TrenTorch</th>
					<th scope="col" class="p-4 font-semibold">{competitor.name}</th>
				</tr>
			</thead>
			<tbody>
				{#each rows as row (row.label)}
					<tr class="border-b border-border last:border-0">
						<th scope="row" class="p-4 font-medium">{row.label}</th>
						<td class="p-4 text-muted-foreground">{row.trentorch}</td>
						<td class="p-4 text-muted-foreground">
							{row.label === 'Pricing'
								? pricingLabel(row.other)
								: competitorCapability(
										row.other,
										row.capabilityKey ? competitor.capabilityNotes[row.capabilityKey] : undefined
									)}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</section>

	<section class="mb-10">
		<h2 class="mb-4 font-mono text-xl font-semibold">When TrenTorch may fit</h2>
		<ul class="list-disc space-y-2 pl-5 text-sm leading-relaxed text-muted-foreground">
			<li>{CLAIMS.freePractice.text}</li>
			<li>{CLAIMS.fromScratch.text}</li>
			<li>{CLAIMS.dailyRatedProblem.text}</li>
			<li>{CLAIMS.appliedPotdScenarios.text}</li>
			<li>{CLAIMS.inferenceSystems.text}</li>
		</ul>
	</section>

	<section class="mb-10 rounded-xl border border-border p-6">
		<h2 class="mb-3 font-mono text-xl font-semibold">About {competitor.name}</h2>
		<p class="mb-4 text-sm leading-relaxed text-muted-foreground">
			{competitor.summary} Information was checked on {competitor.verifiedOn}; capabilities not
			confirmed on the linked pages are labeled accordingly, not treated as unavailable.
		</p>
		<ul class="list-disc space-y-1 pl-5 text-sm">
			{#each competitor.sources as source (source.url)}
				<li>
					<!-- These are external URLs from the verified competitor registry. -->
					<!-- eslint-disable svelte/no-navigation-without-resolve -->
					<a
						href={source.url}
						target="_blank"
						rel="noopener noreferrer"
						class="underline underline-offset-4 hover:text-primary"
					>
						{source.label}
					</a>
					<!-- eslint-enable svelte/no-navigation-without-resolve -->
				</li>
			{/each}
		</ul>
	</section>

	<section class="mb-10">
		<h2 class="mb-4 font-mono text-xl font-semibold">Explore TrenTorch curriculum</h2>
		<ul class="grid gap-3 sm:grid-cols-2">
			{#each data.parts as part (part.id)}
				<li class="rounded-lg border border-border p-4">
					<a
						href={resolve('/questions/[partId]', { partId: part.id })}
						class="font-medium underline underline-offset-4 hover:text-primary"
					>
						{part.title}
					</a>
					<div class="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted-foreground">
						{#each part.tracks.flatMap( (track) => track.questions.slice(0, 2) ) as question (question.slug)}
							<a
								href={resolve('/ide/[id]', { id: question.slug })}
								class="underline underline-offset-4 hover:text-primary"
							>
								{question.title}
							</a>
						{/each}
					</div>
				</li>
			{/each}
		</ul>
	</section>

	<section class="mb-10 rounded-xl border border-border p-6">
		<h2 class="mb-4 font-mono text-xl font-semibold">Frequently asked questions</h2>
		{#each data.faqs as faq (faq.question)}
			<div class="mb-4 last:mb-0">
				<h3 class="mb-1 font-semibold">{faq.question}</h3>
				<p class="text-sm leading-relaxed text-muted-foreground">{faq.answer}</p>
			</div>
		{/each}
	</section>

	<nav aria-label="Related TrenTorch pages" class="flex flex-wrap gap-x-5 gap-y-2 text-sm">
		<a href={resolve('/compare')} class="underline underline-offset-4 hover:text-primary"
			>All alternatives</a
		>
		<a href={resolve('/faq')} class="underline underline-offset-4 hover:text-primary">FAQ</a>
		<a href={resolve('/questions')} class="underline underline-offset-4 hover:text-primary"
			>All curriculum sections</a
		>
		<a
			href={resolve('/[slug]', { slug: 'machine-learning-coding-practice' })}
			class="underline underline-offset-4 hover:text-primary">Machine-learning practice guide</a
		>
		{#each data.landingPages.filter((page) => page.slug !== 'machine-learning-coding-practice') as page (page.slug)}
			<a
				href={resolve('/[slug]', { slug: page.slug })}
				class="underline underline-offset-4 hover:text-primary"
			>
				{page.title}
			</a>
		{/each}
		{#each data.otherComparisons as other (other.slug)}
			<a
				href={resolve('/compare/[slug]', { slug: other.slug })}
				class="underline underline-offset-4 hover:text-primary"
			>
				{other.name} alternative
			</a>
		{/each}
	</nav>
</main>
