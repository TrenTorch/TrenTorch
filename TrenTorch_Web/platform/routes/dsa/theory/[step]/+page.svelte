<script lang="ts">
	import { resolve } from '$app/paths';
	import TheoryReader from '$components/TheoryReader.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<TheoryReader theory={data.theory} backHref={resolve('/dsa')} backLabel="DSA Sheet" />
