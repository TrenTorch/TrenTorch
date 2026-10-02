<script lang="ts">
	import { resolve } from '$app/paths';
	import SEO from '$components/SEO.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<SEO {...data.seo} />

<main class="container max-w-4xl px-4 py-12 md:px-6">
	<a
		href={resolve('/')}
		class="mb-6 inline-flex font-mono text-xs tracking-wider text-muted-foreground uppercase hover:text-primary"
	>
		TrenTorch home
	</a>
	<h1 class="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">{data.page.title}</h1>
	<p class="mb-8 max-w-3xl text-lg text-muted-foreground">
		This guide groups relevant parts of the real TrenTorch curriculum for {data.page.primaryIntent}.
		Use the section and problem links below to explore the material.
	</p>

	<section class="mb-10 rounded-xl border border-border p-6">
		<h2 class="mb-4 font-mono text-lg font-semibold">What TrenTorch offers</h2>
		<ul class="list-disc space-y-2 pl-5 text-sm leading-relaxed">
			{#each data.claims as claim (claim)}
				<li>{claim}</li>
			{/each}
		</ul>
	</section>

	<section class="mb-10">
		<h2 class="mb-5 font-mono text-xl font-semibold">Explore the curriculum</h2>
		<div class="space-y-5">
			{#each data.parts as part (part.id)}
				<article class="rounded-xl border border-border p-5">
					<h3 class="mb-3 text-lg font-semibold">
						<a
							href={resolve('/questions/[partId]', { partId: part.id })}
							class="hover:text-primary"
						>
							{part.title}
						</a>
					</h3>
					{#each part.tracks as track (track.name)}
						<div class="mb-3 last:mb-0">
							<h4 class="mb-1 text-sm font-medium">{track.name}</h4>
							<ul class="flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted-foreground">
								{#each track.questions as question (question.slug)}
									<li>
										<a
											href={resolve('/ide/[id]', { id: question.slug })}
											class="underline underline-offset-4 hover:text-primary"
										>
											{question.title}
										</a>
									</li>
								{/each}
							</ul>
						</div>
					{/each}
				</article>
			{/each}
		</div>
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

	<p class="text-sm text-muted-foreground">
		Explore all <a
			class="underline underline-offset-4 hover:text-primary"
			href={resolve('/questions')}>curriculum sections</a
		>
		or read the
		<a class="underline underline-offset-4 hover:text-primary" href={resolve('/faq')}>FAQ</a>.
	</p>
</main>
