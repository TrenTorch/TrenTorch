<script lang="ts">
	import Folder from './Folder.svelte';
	import PartTree from './PartTree.svelte';
	import type { Part } from '$data/questions';

	let { part, forceOpen = false }: { part: Part; forceOpen?: boolean } = $props();

	const questionCount = $derived(
		part.tracks.reduce((sum, track) => sum + track.questions.length, 0)
	);
</script>

<!-- content-visibility:auto lets the browser skip layout/paint/style work
     for whichever folders are off-screen without changing the markup. -->
<div class="[contain-intrinsic-size:auto_60px] [content-visibility:auto]">
	<Folder id={part.id} title={part.title} count={questionCount} level={0} defaultOpen>
		<PartTree {part} {forceOpen} />
	</Folder>
</div>
