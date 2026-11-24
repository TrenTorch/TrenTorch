<script lang="ts">
	// The tiny drawing for each silo of the Software Engineering domain.
	import ArtSheet from '$components/ArtSheet.svelte';
	let { id }: { id: string } = $props();

	const CODE: Record<string, string> = {
		foundations: 'O(n log n)',
		'data-structures': 'node.next',
		algorithms: 'sort(a)',
		'strings-and-design': 'LRU(cap)'
	};
	const code = $derived(CODE[id] ?? 'solve()');
	const range = (n: number) => Array.from({ length: n }, (_, i) => i);
	const BARS = [26, 40, 18, 34, 46, 12, 30];
	const BITS = [1, 0, 1, 1, 0, 1, 0, 0];
</script>

<ArtSheet {code}>
	{#if id === 'foundations'}
		<path d="M14 88 H146 M14 88 V38" class="line faint" />
		<path d="M16 84 Q70 80 144 42" class="line" />
		<path d="M16 84 Q60 82 100 58 T144 40" class="line acc draw" pathLength="1" />
		<circle cx="144" cy="40" r="3.6" class="dot on" />
		{#each range(8) as i (i)}
			<rect
				x={14 + 8 * i}
				y="40"
				width="6"
				height="6"
				rx="1"
				class={BITS[i] ? 'cell on' : 'cell'}
			/>
		{/each}
	{:else if id === 'data-structures'}
		{#each range(4) as i (i)}
			<rect
				x={12 + 36 * i}
				y="42"
				width="26"
				height="14"
				rx="4"
				class={i === 2 ? 'chip on' : 'chip'}
			/>
			{#if i < 3}<path d="M{38 + 36 * i} 49 H{48 + 36 * i}" class="line" />{/if}
		{/each}
		<path d="M80 62 L50 74 M80 62 L110 74" class="line faint" />
		<path d="M80 62 L110 74" class="line acc draw" pathLength="1" />
		{#each [[80, 62], [50, 74], [110, 74], [36, 86], [64, 86]] as [x, y], i (i)}
			<circle cx={x} cy={y} r="4.5" class={i === 0 || i === 2 ? 'dot on' : 'dot'} />
		{/each}
	{:else if id === 'algorithms'}
		{#each range(7) as i (i)}
			<rect
				x={16 + 18 * i}
				y={88 - BARS[i]}
				width="12"
				height={BARS[i]}
				rx="2"
				class={i === 4 ? 'bar on' : 'bar'}
			/>
		{/each}
		<path d="M20 44 H132" class="line faint dash" />
	{:else if id === 'strings-and-design'}
		{#each range(8) as i (i)}
			<rect
				x={14 + 16 * i}
				y="42"
				width="16"
				height="16"
				class={i >= 2 && i <= 4 ? 'cell on' : 'cell'}
			/>
		{/each}
		<path d="M46 38 H94 M46 38 V40 M94 38 V40" class="line acc draw" pathLength="1" />
		{#each range(4) as i (i)}
			<rect
				x={12 + 36 * i}
				y="68"
				width="26"
				height="14"
				rx="4"
				class={i === 0 ? 'chip on' : 'chip'}
			/>
			{#if i < 3}<path d="M{38 + 36 * i} 75 H{48 + 36 * i}" class="line" />{/if}
		{/each}
	{:else}
		<rect x="14" y="42" width="90" height="6" rx="3" class="bar" />
		<rect x="14" y="56" width="124" height="6" rx="3" class="bar" />
		<rect x="14" y="70" width="64" height="6" rx="3" class="bar on" />
	{/if}
</ArtSheet>
