<script lang="ts">
	import './diagram.css';
	const queue = [0, 1, 2, 3, 4, 5, 6, 7];
	const sms = [
		[0, 4],
		[1, 5],
		[2, 6],
		[3, 7]
	];
	const col = ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b'];
</script>

<figure class="dg">
	<svg
		viewBox="0 0 720 300"
		role="img"
		aria-label="Eight thread blocks waiting in a queue are handed to four streaming multiprocessors, two each"
	>
		<text class="t h" x="20" y="24">Launched grid: 8 blocks</text>
		{#each queue as b (b)}
			<rect class={col[b]} x={20 + b * 56} y="36" width="48" height="44" rx="7" />
			<text class="t" x={44 + b * 56} y="64" text-anchor="middle">B{b}</text>
		{/each}
		<rect class="box hi" x="20" y="108" width="440" height="34" rx="8" />
		<text class="t" x="240" y="130" text-anchor="middle"
			>GigaThread Engine: assigns a block to any SM with room</text
		>
		{#each sms as blocks, i (i)}
			<path class="ln" d="M{100 + i * 118} 142V170" />
			<rect class="box" x={20 + i * 118} y="170" width="108" height="100" rx="10" />
			<text class="t h" x={74 + i * 118} y="192" text-anchor="middle">SM {i}</text>
			{#each blocks as b, j (b)}
				<rect class={col[b]} x={30 + i * 118 + j * 48} y="204" width="42" height="44" rx="6" />
				<text class="t s" x={51 + i * 118 + j * 48} y="231" text-anchor="middle">B{b}</text>
			{/each}
		{/each}
		<text class="t s" x="500" y="190">Blocks never talk to each other.</text>
		<text class="t s" x="500" y="210">An SM keeps a block until it finishes,</text>
		<text class="t s" x="500" y="230">then takes the next waiting one.</text>
		<text class="t s" x="500" y="260">When blocks outnumber SM slots</text>
		<text class="t s" x="500" y="278">they run in waves.</text>
	</svg>
	<figcaption>
		The hardware, not you, decides which SM runs which block and when. The order is not guaranteed.
	</figcaption>
</figure>
