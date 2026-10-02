<script lang="ts">
	import Folder from './Folder.svelte';
	import QuestionRow from './QuestionRow.svelte';
	import type { Part, Question, Track } from '$data/questions';

	let { part, forceOpen = false }: { part: Part; forceOpen?: boolean } = $props();

	// Parts built outside composePart (e.g. the POTD list) have no sections:
	// treat their tracks as one section.
	const sections = $derived(
		part.sections ?? [
			{
				name: part.title,
				tracks: part.tracks,
				questions: part.tracks.flatMap((t) => t.questions)
			}
		]
	);

	// A section named like its root has no folder, so its sub-sections are listed
	// first, above every folder; below them they would look like they belong to
	// the last folder. The other sections keep their order.
	const ordered = $derived([
		...sections.filter((section) => section.name === part.title),
		...sections.filter((section) => section.name !== part.title)
	]);
</script>

<!-- A level that adds no information is skipped: its content is shown
     directly. So a root with one section shows that section's sub-sections,
     a section with one sub-section shows its questions, and a section named
     exactly like its root (Reinforcement Learning -> Reinforcement Learning)
     shows its sub-sections, at the very top, without a folder of its own. -->
{#snippet questionList(questions: Question[])}
	<div class="px-4 py-2">
		{#each questions as question (question.slug)}
			<QuestionRow {question} />
		{/each}
	</div>
{/snippet}

{#snippet trackList(tracks: Track[])}
	{#if tracks.length > 1}
		{#each tracks as track (track.name)}
			<div class="border-t border-border px-4 py-2 first:border-t-0">
				<h5 class="mb-1 font-mono text-xs tracking-wider text-muted-foreground uppercase">
					{track.name}
				</h5>
				{#each track.questions as question (question.slug)}
					<QuestionRow {question} />
				{/each}
			</div>
		{/each}
	{:else}
		{@render questionList(tracks.flatMap((t) => t.questions))}
	{/if}
{/snippet}

{#if sections.length > 1}
	{#each ordered as section (section.name)}
		{#if section.name === part.title}
			{@render trackList(section.tracks)}
		{:else}
			<Folder
				id={`${part.id}/${section.name}`}
				title={section.name}
				count={section.questions.length}
				level={1}
				{forceOpen}
			>
				{@render trackList(section.tracks)}
			</Folder>
		{/if}
	{/each}
{:else if sections[0]}
	{@render trackList(sections[0].tracks)}
{/if}
