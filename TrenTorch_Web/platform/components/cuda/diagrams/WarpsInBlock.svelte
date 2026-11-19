<script lang="ts">
	import './diagram.css';
	const warps = [0, 1, 2, 3];
	const cls = ['a', 'b', 'c', 'a'];
</script>

<figure class="dg">
	<svg
		viewBox="0 0 720 300"
		role="img"
		aria-label="A block of 128 threads is cut into four warps of 32 consecutive threads, each executing in lockstep"
	>
		<text class="t h" x="20" y="22">One block of 128 threads (blockDim.x = 128)</text>
		{#each warps as w (w)}
			<text class="t s" x="20" y={52 + w * 56}>warp {w}</text>
			<text class="t s" x="20" y={66 + w * 56}>threads {w * 32}..{w * 32 + 31}</text>
			{#each Array.from({ length: 32 }, (_, i) => i) as l (l)}
				<rect class={cls[w]} x={120 + l * 18.5} y={38 + w * 56} width="15" height="34" rx="3" />
			{/each}
		{/each}
		<path class="ln" d="M120 270H712" />
		<text class="t s" x="120" y="288">lane 0</text>
		<text class="t s" x="712" y="288" text-anchor="end">lane 31</text>
		<text class="t" x="416" y="262" text-anchor="middle"
			>32 lanes execute one instruction together</text
		>
	</svg>
	<figcaption>
		The block is cut into warps by consecutive thread id. A warp is the real unit the scheduler
		issues, so a block of 100 threads still occupies 4 warps.
	</figcaption>
</figure>
