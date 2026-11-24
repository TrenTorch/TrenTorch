<script lang="ts">
	// The tiny drawing for each part of the GPU Programming domain (parts A to G).
	import ArtSheet from '$components/ArtSheet.svelte';
	let { id }: { id: string } = $props();

	const CODE: Record<string, string> = {
		A: 'sm_80',
		B: '<<<g, b>>>',
		C: 'if (tid < n)',
		D: 'a[tid]',
		E: 'scan(x)',
		F: 'stream[i]',
		G: 'W / BW',
		'1': 'c[i]=a[i]+b[i]',
		'2': 'sum(x)',
		'3': 'softmax(row)',
		'4': 'x[i-1..i+1]',
		'5': 'hist[bin]++',
		'6': 'C = A @ B',
		'7': 'nccl.allreduce'
	};
	const code = $derived(CODE[id] ?? 'kernel()');
	const range = (n: number) => Array.from({ length: n }, (_, i) => i);
	// reduction tree: 8 inputs halve each level
	const LEVELS = [8, 4, 2, 1];
	const treeX = (level: number, i: number) => 22 + (i + 0.5) * (116 / LEVELS[level]);
	const treeY = (level: number) => 84 - level * 15;
</script>

<ArtSheet {code}>
	{#if id === 'A'}
		{#each range(2) as row (row)}
			{#each range(4) as col (col)}
				<rect
					x={14 + 34 * col}
					y={38 + 17 * row}
					width="30"
					height="13"
					rx="3"
					class={row === 0 && col === 1 ? 'cell on' : 'cell'}
				/>
			{/each}
		{/each}
		<rect x="14" y="76" width="132" height="12" rx="3" class="cell fill" />
		<path d="M45 64 V76 M79 64 V76" class="line faint" />
	{:else if id === 'B'}
		{#each range(3) as block (block)}
			<rect x={12 + 46 * block} y="38" width="42" height="50" rx="5" class="cell" />
			{#each range(4) as t (t)}
				<rect
					x={17 + 46 * block + 9 * t}
					y={block === 1 ? 52 : 58}
					width="7"
					height={block === 1 ? 24 : 18}
					rx="2"
					class={block === 1 && t === 2 ? 'bar on' : 'bar'}
				/>
			{/each}
		{/each}
	{:else if id === 'C'}
		{#each range(8) as lane (lane)}
			<rect
				x={14 + 17 * lane}
				y="38"
				width="14"
				height="10"
				rx="2.5"
				class={lane < 4 ? 'cell on' : 'cell'}
			/>
		{/each}
		<path d="M45 52 V66 M45 66 H31 M45 66 H59" class="line acc draw" pathLength="1" />
		<path d="M113 52 V66 M113 66 H99 M113 66 H127" class="line faint" />
		<rect x="14" y="74" width="62" height="12" rx="3" class="cell on" />
		<rect x="84" y="74" width="62" height="12" rx="3" class="cell fill" />
	{:else if id === 'D'}
		{#each range(8) as lane (lane)}
			<circle cx={22 + 16 * lane} cy="44" r="4" class={lane === 3 ? 'dot on' : 'dot'} />
			<path d="M{22 + 16 * lane} 49 V70" class="line faint" />
			<rect
				x={14 + 16 * lane}
				y="70"
				width="16"
				height="16"
				class={lane === 3 ? 'cell on' : 'cell fill'}
			/>
		{/each}
	{:else if id === 'E'}
		{#each range(3) as level (level)}
			{#each range(LEVELS[level]) as i (i)}
				<path
					d="M{treeX(level, i)} {treeY(level)} L{treeX(level + 1, Math.floor(i / 2))} {treeY(
						level + 1
					)}"
					class={i === 0 || (level === 1 && i === 1) ? 'line acc draw' : 'line faint'}
					pathLength="1"
				/>
			{/each}
		{/each}
		{#each range(4) as level (level)}
			{#each range(LEVELS[level]) as i (i)}
				<circle
					cx={treeX(level, i)}
					cy={treeY(level)}
					r={level === 3 ? 5 : 4}
					class={level === 3 ? 'dot on' : 'dot'}
				/>
			{/each}
		{/each}
	{:else if id === 'F'}
		{#each [[14, 40, 0], [40, 56, 1], [68, 72, 2]] as [x, y], i (i)}
			<rect {x} {y} width="46" height="10" rx="4" class={i === 1 ? 'bar on' : 'bar'} />
			<rect x={x + 52} {y} width="40" height="10" rx="4" class="bar" />
		{/each}
		<path d="M14 36 V90 M14 90 H146" class="line faint" />
	{:else if id === 'G'}
		<path d="M14 88 H146 M14 88 V38" class="line faint" />
		<path d="M18 84 L84 48 H142" class="line acc draw" pathLength="1" />
		<circle cx="84" cy="48" r="4" class="dot on" />
		<circle cx="52" cy="66" r="3" class="dot" />
		<circle cx="118" cy="48" r="3" class="dot" />
	{:else if id === '1'}
		{#each range(8) as i (i)}
			<rect x={14 + 17 * i} y="40" width="14" height="10" rx="2.5" class="cell" />
			<rect x={14 + 17 * i} y="55" width="14" height="10" rx="2.5" class="cell" />
			<rect
				x={14 + 17 * i}
				y="76"
				width="14"
				height="10"
				rx="2.5"
				class={i === 3 ? 'cell on' : 'cell fill'}
			/>
		{/each}
		<path d="M21 70 H139" class="line faint" />
	{:else if id === '2'}
		{#each range(8) as i (i)}
			<rect x={14 + 17 * i} y="40" width="14" height="10" rx="2.5" class="cell" />
		{/each}
		<path
			d="M21 50 L35 66 M38 50 L35 66 M55 50 L69 66 M72 50 L69 66 M89 50 L103 66 M106 50 L103 66 M123 50 L137 66 M140 50 L137 66"
			class="line faint"
		/>
		<path d="M35 66 L52 82 M69 66 L52 82" class="line acc draw" pathLength="1" />
		<circle cx="52" cy="82" r="4.5" class="dot on" />
		<circle cx="120" cy="82" r="4.5" class="dot" />
		<path d="M103 66 L120 82 M137 66 L120 82" class="line faint" />
	{:else if id === '3'}
		{#each [[90, 60], [50, 100], [70, 80]] as [w], i (i)}
			<rect x="14" y={40 + 16 * i} width="132" height="11" rx="4" class="bar" />
			<rect
				x="14"
				y={40 + 16 * i}
				width={w}
				height="11"
				rx="4"
				class={i === 1 ? 'bar on' : 'bar fill'}
			/>
		{/each}
	{:else if id === '4'}
		{#each range(9) as i (i)}
			<rect
				x={12 + 14.5 * i}
				y="54"
				width="14.5"
				height="18"
				class={i >= 3 && i <= 5 ? 'cell fill' : 'cell'}
			/>
		{/each}
		<rect x="55.5" y="50" width="43.5" height="26" rx="4" class="window" />
		<path d="M77 78 V88" class="line acc" />
		<rect x="70" y="86" width="14.5" height="6" rx="2" class="bar on" />
	{:else if id === '5'}
		{#each [18, 34, 12, 40, 26, 8, 22] as h, i (i)}
			<rect
				x={16 + 18 * i}
				y={88 - h}
				width="13"
				height={h}
				rx="2"
				class={i === 3 ? 'bar on' : 'bar'}
			/>
		{/each}
	{:else if id === '6'}
		{#each range(3) as r (r)}
			{#each range(3) as c (c)}
				<rect
					x={14 + 14 * c}
					y={50 + 12 * r}
					width="12"
					height="10"
					rx="2"
					class={r === 1 ? 'cell on' : 'cell'}
				/>
				<rect
					x={62 + 14 * c}
					y={50 + 12 * r}
					width="12"
					height="10"
					rx="2"
					class={c === 1 ? 'cell on' : 'cell'}
				/>
				<rect
					x={110 + 12 * c}
					y={50 + 12 * r}
					width="10"
					height="10"
					rx="2"
					class={r === 1 && c === 1 ? 'cell on' : 'cell fill'}
				/>
			{/each}
		{/each}
		<text x="56" y="62" font-size="9" fill="var(--ink)">×</text>
		<text x="102" y="62" font-size="9" fill="var(--ink)">=</text>
	{:else if id === '7'}
		<path d="M44 48 H116 M124 56 V72 M116 80 H44 M36 72 V56" class="line acc draw" pathLength="1" />
		{#each [[36, 48], [124, 48], [124, 80], [36, 80]] as [x, y], i (i)}
			<rect
				x={x - 11}
				y={y - 8}
				width="22"
				height="16"
				rx="4"
				class={i === 0 ? 'chip on' : 'chip'}
			/>
		{/each}
	{:else}
		<rect x="14" y="42" width="90" height="6" rx="3" class="bar" />
		<rect x="14" y="56" width="124" height="6" rx="3" class="bar" />
		<rect x="14" y="70" width="64" height="6" rx="3" class="bar on" />
	{/if}
</ArtSheet>
