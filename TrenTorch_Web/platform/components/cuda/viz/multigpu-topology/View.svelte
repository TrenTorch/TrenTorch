<script lang="ts">
	import Explorer from '../_shared/Explorer.svelte';
	import { VIZ_BY_ID } from '$processes/cuda/viz';
	let { mode = '', title = '' }: { mode?: string; title?: string } = $props();
</script>

<Explorer config={VIZ_BY_ID['multigpu-topology']} {mode} {title} />
