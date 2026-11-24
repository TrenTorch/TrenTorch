<script lang="ts">
	// A module's tiny drawing, in the same cut-open-sheet language as the hub cards:
	// a code line on top, and underneath it a picture of what that module is about.
	// Drawn from theme tokens, so it follows light and dark. Decorative only.
	import ArtSheet from '$components/ArtSheet.svelte';
	let { id }: { id: string } = $props();

	const CODE: Record<string, string> = {
		'part-python': 'def f(x):',
		'part-mathematics': '∇f(x)',
		'part-data-science': 'df.groupby()',
		'part-classical-ml': 'fit(X, y)',
		'part-deep-learning': 'net(x)',
		'part-language-modelling-attention-llms': 'lm("The cat")',
		'part-inference': 'serve(req)',
		'part-reinforcement-learning': 'env.step(a)',
		'part-computer-vision': 'conv(img)',
		'part-agentic-systems': 'agent.run()',
		'part-distributed-systems': 'allreduce(g)',
		'part-production-reliability': 'deploy(v2)'
	};
	const code = $derived(CODE[id] ?? 'run()');

	const range = (n: number) => Array.from({ length: n }, (_, i) => i);
	// deep learning: neurons per layer and where each layer sits
	const LAYERS = [3, 4, 4, 2];
	const layerX = (layer: number) => 26 + 36 * layer;
	const neuronY = (layer: number, i: number) => 62 + (i - (LAYERS[layer] - 1) / 2) * 12;
	// reinforcement learning: grid centres
	const cx = (col: number) => 27 + 26 * col;
	const cy = (row: number) => 46 + 16 * row;
	// language model: how likely each next token is
	const NEXT = [30, 18, 12, 8, 5, 3];
	// computer vision: which pixels are "lit"
	const LIT = new Set([9, 10, 11, 16, 17, 18, 23, 24, 25]);
</script>

<ArtSheet {code}>
	{#if id === 'part-python'}
		{#each [[60, 0], [44, 0], [72, 10], [52, 10], [36, 0]] as [w, indent], i (i)}
			<rect
				x={14 + indent}
				y={40 + 10 * i}
				width={w}
				height="5"
				rx="2.5"
				class={i === 2 ? 'bar on' : 'bar'}
			/>
		{/each}
		<path d="M110 44 V84" class="line faint" />
	{:else if id === 'part-mathematics'}
		<path d="M14 88 H146" class="line faint" />
		<path d="M20 40 Q80 110 140 40" class="line" />
		<path d="M32 52.6 L50 66.3 L68 73.6" class="line acc draw" pathLength="1" />
		{#each [[32, 52.6], [50, 66.3], [68, 73.6]] as [x, y], i (i)}
			<circle cx={x} cy={y} r="3" class="dot" />
		{/each}
		<circle cx="80" cy="75" r="3.6" class="dot on" />
	{:else if id === 'part-data-science'}
		{#each range(4) as col (col)}
			{#each range(4) as row (row)}
				<rect
					x={16 + 32 * col}
					y={39 + 12 * row}
					width="30"
					height="10"
					rx="3"
					class={row === 0 ? 'cell head' : col === 2 ? 'cell on' : 'cell'}
				/>
			{/each}
		{/each}
	{:else if id === 'part-classical-ml'}
		{#each [[30, 52], [38, 62], [26, 68], [42, 48], [34, 78]] as [x, y], i (i)}
			<circle cx={x} cy={y} r="4" class="dot" />
		{/each}
		{#each [[112, 50], [122, 62], [132, 48], [118, 76], [104, 66]] as [x, y], i (i)}
			<circle cx={x} cy={y} r="4" class="dot on" />
		{/each}
		<path d="M90 36 L70 90" class="line acc dash draw" pathLength="1" />
	{:else if id === 'part-deep-learning'}
		{#each range(3) as layer (layer)}
			{#each range(LAYERS[layer]) as a (a)}
				{#each range(LAYERS[layer + 1]) as b (b)}
					<path
						d="M{layerX(layer)} {neuronY(layer, a)} L{layerX(layer + 1)} {neuronY(layer + 1, b)}"
						class="line faint"
					/>
				{/each}
			{/each}
		{/each}
		<path
			d="M{layerX(0)} {neuronY(0, 1)} L{layerX(1)} {neuronY(1, 2)} L{layerX(2)} {neuronY(
				2,
				1
			)} L{layerX(3)} {neuronY(3, 0)}"
			class="line acc draw"
			pathLength="1"
		/>
		{#each range(4) as layer (layer)}
			{#each range(LAYERS[layer]) as i (i)}
				<circle cx={layerX(layer)} cy={neuronY(layer, i)} r="4.2" class="dot" />
			{/each}
		{/each}
	{:else if id === 'part-language-modelling-attention-llms'}
		{#each range(4) as i (i)}
			<rect x={12 + 36 * i} y="38" width="32" height="12" rx="4" class="chip" />
		{/each}
		<path d="M148 44 H152" class="line faint" />
		{#each NEXT as h, i (i)}
			<rect
				x={16 + 22 * i}
				y={90 - h}
				width="16"
				height={h}
				rx="3"
				class={i === 0 ? 'bar on' : 'bar'}
			/>
		{/each}
	{:else if id === 'part-inference'}
		{#each range(3) as row (row)}
			{#each range(8) as col (col)}
				<rect
					x={14 + 17 * col}
					y={38 + 13 * row}
					width="14"
					height="10"
					rx="2.5"
					class={row * 8 + col === 14 ? 'cell on' : row * 8 + col < 14 ? 'cell fill' : 'cell'}
				/>
			{/each}
		{/each}
		<rect x="14" y="82" width="132" height="6" rx="3" class="bar" />
		<rect x="14" y="82" width="84" height="6" rx="3" class="bar on" />
	{:else if id === 'part-reinforcement-learning'}
		{#each range(3) as row (row)}
			{#each range(5) as col (col)}
				<rect
					x={14 + 26 * col}
					y={38 + 16 * row}
					width="26"
					height="16"
					class={(col === 2 && row === 2) || (col === 0 && row === 0) ? 'cell fill' : 'cell'}
				/>
			{/each}
		{/each}
		<path
			d="M{cx(0)} {cy(2)} L{cx(1)} {cy(2)} L{cx(1)} {cy(1)} L{cx(3)} {cy(1)} L{cx(3)} {cy(0)} L{cx(
				4
			)} {cy(0)}"
			class="line acc draw"
			pathLength="1"
		/>
		<circle cx={cx(0)} cy={cy(2)} r="4" class="dot on" />
		<circle cx={cx(4)} cy={cy(0)} r="5.5" class="ring" />
	{:else if id === 'part-computer-vision'}
		{#each range(4) as row (row)}
			{#each range(7) as col (col)}
				<rect
					x={18 + 16 * col}
					y={40 + 12 * row}
					width="16"
					height="12"
					class={LIT.has(row * 7 + col) ? 'cell fill' : 'cell'}
				/>
			{/each}
		{/each}
		<rect x="50" y="40" width="48" height="36" rx="3" class="window on" />
	{:else if id === 'part-agentic-systems'}
		<path d="M40 62 L62 47 M40 62 L62 79 M96 47 L116 62 M96 79 L116 62" class="line" />
		<rect x="10" y="54" width="30" height="16" rx="5" class="chip" />
		<rect x="62" y="40" width="34" height="14" rx="5" class="chip" />
		<rect x="62" y="72" width="34" height="14" rx="5" class="chip" />
		<rect x="116" y="54" width="30" height="16" rx="5" class="chip on" />
		<path d="M131 70 C131 92 25 92 25 70" class="line acc dash draw" pathLength="1" />
	{:else if id === 'part-distributed-systems'}
		<path d="M44 48 H116 M124 56 V72 M116 80 H44 M36 72 V56" class="line acc draw" pathLength="1" />
		{#each [[36, 48], [124, 48], [124, 80], [36, 80]] as [x, y], i (i)}
			<circle cx={x} cy={y} r="9" class="dot" />
			<circle cx={x} cy={y} r="3" class={i === 0 ? 'dot on' : 'dot core'} />
		{/each}
	{:else if id === 'part-production-reliability'}
		<path d="M14 58 H146" class="line faint dash" />
		<path
			d="M14 82 L36 74 L58 78 L80 60 L102 50 L124 42 L146 46"
			class="line acc draw"
			pathLength="1"
		/>
		<circle cx="146" cy="46" r="4" class="dot on" />
		<rect x="14" y="40" width="30" height="10" rx="5" class="cell on" />
	{:else}
		<rect x="14" y="42" width="90" height="6" rx="3" class="bar" />
		<rect x="14" y="56" width="124" height="6" rx="3" class="bar" />
		<rect x="14" y="70" width="64" height="6" rx="3" class="bar on" />
	{/if}
</ArtSheet>
