<script lang="ts">
	import './diagram.css';
	const bx = [0, 1, 2, 3];
	const by = [0, 1];
</script>

<figure class="dg">
	<svg
		viewBox="0 0 720 330"
		role="img"
		aria-label="A grid of 4 by 2 thread blocks; block (2,1) is expanded into a grid of threads"
	>
		<text class="t h" x="20" y="22">Grid (gridDim = 4 x 2)</text>
		{#each by as y (y)}
			{#each bx as x (x)}
				<rect
					class={x === 2 && y === 1 ? 'a' : 'box'}
					x={20 + x * 78}
					y={36 + y * 78}
					width="70"
					height="70"
					rx="8"
				/>
				<text class="t s" x={55 + x * 78} y={76 + y * 78} text-anchor="middle">({x},{y})</text>
			{/each}
		{/each}
		<text class="t s" x="20" y="212">blockIdx.x = 0..3, blockIdx.y = 0..1</text>
		<path class="ln" d="M176 192L400 120" stroke-dasharray="5 4" />
		<text class="t h" x="410" y="22">Block (2,1) (blockDim = 8 x 4)</text>
		<rect class="box" x="410" y="36" width="290" height="160" rx="10" />
		{#each [0, 1, 2, 3] as ty (ty)}
			{#each [0, 1, 2, 3, 4, 5, 6, 7] as tx (tx)}
				<rect class="a" x={422 + tx * 34} y={48 + ty * 36} width="28" height="28" rx="5" />
			{/each}
		{/each}
		<text class="t s" x="422" y="214">threadIdx.x = 0..7, threadIdx.y = 0..3</text>
		<text class="t" x="20" y="262">Global column = blockIdx.x * blockDim.x + threadIdx.x</text>
		<text class="t" x="20" y="286">Global row = blockIdx.y * blockDim.y + threadIdx.y</text>
		<text class="t s" x="20" y="310"
			>Every thread runs the same kernel and uses these indices to pick its own data.</text
		>
	</svg>
	<figcaption>
		A grid is a 2D arrangement of blocks, and each block is itself a 2D arrangement of threads.
	</figcaption>
</figure>
