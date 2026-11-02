<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { ArrowRight, Check, Clock } from '@lucide/svelte';
	import DifficultyBadge from './DifficultyBadge.svelte';
	import WindowDots from './WindowDots.svelte';
	import { formatTopic } from '$processes/potd/format-topic';
	import { createPotdCountdown } from '$processes/potd/potd-countdown.svelte';
	import { solved } from '$processes/progress-tracking/solved.svelte';
	import type { Part } from '$data/questions';

	// Today's Part: one track, named after the date, holding the one question.
	let { part }: { part: Part } = $props();

	const track = $derived(part.tracks[0]);
	const question = $derived(track?.questions[0]);
	const isSolved = $derived(question ? solved.isSolved(question.slug) : false);

	const countdown = createPotdCountdown();
	onMount(() => countdown.start());
</script>

{#if question}
	<section
		class="overflow-hidden rounded-2xl border border-border bg-secondary/30 shadow-sm"
		aria-labelledby="potd-today"
	>
		<div class="flex items-center justify-between border-b border-border px-4 py-2.5">
			<div class="flex items-center gap-3">
				<WindowDots />
				<span class="font-mono text-xs text-muted-foreground">potd / {track.name}</span>
			</div>
			<DifficultyBadge difficulty={question.difficulty} />
		</div>

		<div class="px-5 pt-6 pb-5 sm:px-7">
			<p class="mb-2 font-mono text-xs tracking-wider text-primary uppercase">Today's problem</p>
			<h2
				id="potd-today"
				class="font-mono text-2xl leading-tight font-bold tracking-tight text-balance sm:text-3xl"
			>
				{question.title}
			</h2>
			{#if question.topics.length}
				<ul class="mt-4 flex flex-wrap gap-2" aria-label="Topics">
					{#each question.topics.slice(0, 4) as topic (topic)}
						<li
							class="rounded-md border border-border bg-secondary/60 px-2.5 py-1 font-mono text-xs text-muted-foreground"
						>
							{formatTopic(topic)}
						</li>
					{/each}
				</ul>
			{/if}
		</div>

		<div
			class="flex flex-wrap items-center justify-between gap-3 border-t border-border px-5 py-3 sm:px-7"
		>
			<p class="flex items-center gap-2 font-mono text-xs text-muted-foreground">
				<Clock class="size-3.5" aria-hidden="true" />
				resets in
				<span class="text-foreground tabular-nums">{countdown.time || '--:--:--'}</span>
			</p>
			<a
				href={resolve('/ide/[id]?src=potd', { id: question.slug })}
				class="press inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90 focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:outline-none"
			>
				{#if isSolved}
					<Check class="size-4" aria-hidden="true" />
					Solved. Open it again
				{:else}
					Solve
					<ArrowRight class="size-4" aria-hidden="true" />
				{/if}
			</a>
		</div>
	</section>
{/if}
