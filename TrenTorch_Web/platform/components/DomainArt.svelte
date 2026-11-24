<script lang="ts">
	import type { DomainId } from '$data/domains';

	// A domain's drawing: a sheet showing the call, cut open to what runs
	// inside it. Everything is drawn from theme tokens, so it follows light
	// and dark, and one stroke takes the brand accent. Decorative only.
	let { id, live = false }: { id: DomainId; live?: boolean } = $props();
</script>

<svg viewBox="34 20 572 314" class="art" class:live aria-hidden="true" focusable="false">
	<defs>
		<pattern
			id="hatch-{id}"
			width="5"
			height="5"
			patternUnits="userSpaceOnUse"
			patternTransform="rotate(45)"
		>
			<path d="M0 0V5" class="hatch" />
		</pattern>
	</defs>

	<!-- the sheet -->
	<rect x="44" y="30" width="556" height="300" rx="18" class="sheet-back" />
	<rect x="40" y="25" width="556" height="300" rx="18" class="sheet" />

	{#if id === 'aisys'}
		<text x="64" y="70" class="code"
			>model("The capital of Australia is"){#if live}<tspan class="caret">▍</tspan>{/if}</text
		>
		<path
			d="M41 100 L70 94 L98 102 L130 95 L162 103 L196 94 L230 102 L266 95 L300 103 L336 94 L370 102 L404 95 L440 103 L476 94 L510 102 L546 95 L595 101 V310 a14 14 0 0 1 -14 14 H55 a14 14 0 0 1 -14 -14 Z"
			class="inside"
		/>
		{#each ['The', 'capital', 'of', 'Austra', 'lia', 'is'] as token, i (i)}
			<rect x={58 + 78 * i} y="122" width="72" height="26" rx="7" class="chip" />
			<text x={94 + 78 * i} y="139.5" class="label mid">{token}</text>
		{/each}
		<path d="M484 150 C484 196 172 196 172 150" class="line accent draw pulse" />
		<path d="M484 150 C484 182 328 182 328 150" class="line thin draw" />
		<path d="M484 150 C484 208 94 208 94 150" class="line faint draw" />
		{#each [0, 1, 2] as row (row)}
			{#each [0, 1, 2, 3] as col (col)}
				<rect
					x={64 + 26 * col}
					y={226 + 26 * row}
					width="22"
					height="22"
					rx="4"
					class="cell"
					fill={(row + col) % 2 ? `url(#hatch-${id})` : 'none'}
				/>
			{/each}
		{/each}
		<text x="64" y="316" class="label">weights</text>
		<path d="M176 262 H252" class="line thin" />
		<path d="M246 256 L254 262 L246 268" class="line thin" />
		{#each [76, 36, 24, 15, 9, 5] as h, i (i)}
			<rect
				x={290 + 44 * i}
				y={300 - h}
				width="32"
				height={h}
				rx="4"
				class={i === 0 ? 'bar top' : 'bar'}
				style="--i: {i}"
			/>
		{/each}
		<text x="290" y="216" class="label strong">Canberra</text>
		<text x="290" y="316" class="label">next token</text>
	{:else if id === 'gpu'}
		<text x="64" y="70" class="code"
			>kernel&lt;&lt;&lt;grid, block&gt;&gt;&gt;(x){#if live}<tspan class="caret">▍</tspan
				>{/if}</text
		>
		<path
			d="M41 100 L70 94 L98 102 L130 95 L162 103 L196 94 L230 102 L266 95 L300 103 L336 94 L370 102 L404 95 L440 103 L476 94 L510 102 L546 95 L595 101 V310 a14 14 0 0 1 -14 14 H55 a14 14 0 0 1 -14 -14 Z"
			class="inside"
		/>
		{#each [0, 1, 2] as row (row)}
			{#each [0, 1, 2, 3] as col (col)}
				<rect
					x={62 + 52 * col}
					y={124 + 44 * row}
					width="44"
					height="36"
					rx="6"
					class={row === 0 && col === 2 ? 'cell pick' : 'cell'}
					fill={(row + col) % 2 ? `url(#hatch-${id})` : 'none'}
				/>
			{/each}
		{/each}
		<text x="62" y="278" class="label">multiprocessors</text>
		<path d="M218 124 L318 128" class="line thin dash" />
		<path d="M218 160 L318 222" class="line thin dash" />
		{#each [0, 1, 2, 3] as row (row)}
			{#each Array.from({ length: 16 }, (_, k) => k) as lane (lane)}
				<rect
					x={320 + 17 * lane}
					y={122 + 17 * row}
					width="12"
					height="12"
					rx="2.5"
					class={row === 0 ? 'lane on' : 'lane'}
					style="--i: {lane}"
				/>
			{/each}
		{/each}
		<text x="320" y="204" class="label strong">one warp</text>
		{#each [90, 170, 250] as w, i (i)}
			<rect x="320" y={222 + 24 * i} width={w} height="16" rx="5" class="mem" />
		{/each}
		<text x="326" y="234" class="label tiny">registers</text>
		<text x="326" y="258" class="label tiny">shared</text>
		<text x="326" y="282" class="label tiny">global</text>
	{:else if id === 'software'}
		<text x="64" y="70" class="code"
			>find(tree, 60){#if live}<tspan class="caret">▍</tspan>{/if}</text
		>
		<path
			d="M41 100 L70 94 L98 102 L130 95 L162 103 L196 94 L230 102 L266 95 L300 103 L336 94 L370 102 L404 95 L440 103 L476 94 L510 102 L546 95 L595 101 V310 a14 14 0 0 1 -14 14 H55 a14 14 0 0 1 -14 -14 Z"
			class="inside"
		/>
		<path
			d="M170 140 L110 190 M170 140 L230 190 M110 190 L80 240 M110 190 L140 240 M230 190 L200 240 M230 190 L260 240"
			class="line thin"
		/>
		<path d="M170 140 L230 190 L200 240" class="line accent draw pulse" />
		{#each [[170, 140, '50', 0], [110, 190, '25', 0], [230, 190, '75', 1], [80, 240, '10', 0], [140, 240, '30', 0], [200, 240, '60', 2], [260, 240, '90', 0]] as [x, y, n, step] (n)}
			<circle
				cx={x}
				cy={y}
				r="16"
				class={n === '50' || n === '75' || n === '60' ? 'node on' : 'node'}
				style="--i: {step}"
			/>
			<text {x} y={Number(y) + 4} class="label mid">{n}</text>
		{/each}
		<text x="64" y="316" class="label">binary search tree</text>
		{#each [0, 1, 2] as i (i)}
			<rect
				x="360"
				y={236 - 48 * i}
				width="210"
				height="38"
				rx="8"
				class={i === 2 ? 'frame on' : 'frame'}
			/>
		{/each}
		<text x="378" y="260" class="label">find(50)</text>
		<text x="378" y="212" class="label">find(75)</text>
		<text x="378" y="164" class="label strong">find(60) → true</text>
		<text x="360" y="316" class="label">call stack</text>
	{:else if id === 'system-design'}
		<text x="64" y="70" class="code"
			>scale(10_000_000){#if live}<tspan class="caret">▍</tspan>{/if}</text
		>
		<path
			d="M41 100 L70 94 L98 102 L130 95 L162 103 L196 94 L230 102 L266 95 L300 103 L336 94 L370 102 L404 95 L440 103 L476 94 L510 102 L546 95 L595 101 V310 a14 14 0 0 1 -14 14 H55 a14 14 0 0 1 -14 -14 Z"
			class="inside"
		/>
		<rect x="70" y="124" width="120" height="50" rx="9" class="chip" />
		<rect x="260" y="124" width="120" height="50" rx="9" class="chip" />
		<rect x="450" y="124" width="120" height="50" rx="9" class="chip" />
		<text x="130" y="154" class="label mid">clients</text>
		<text x="320" y="154" class="label mid">load balancer</text>
		<text x="510" y="154" class="label mid">services</text>
		<path d="M190 149 H260 M380 149 H450" class="line thin" />
		<rect x="200" y="236" width="120" height="50" rx="9" class="cell pick" />
		<rect x="360" y="236" width="120" height="50" rx="9" class="cell" fill="url(#hatch-{id})" />
		<text x="260" y="266" class="label mid">cache</text>
		<text x="420" y="266" class="label mid">database</text>
		<path d="M510 174 V205 H260 V236 M510 205 H420 V236" class="line accent" />
		<circle r="6" class="packet" />
	{:else}
		<text x="64" y="70" class="code"
			>arm.move_to(target){#if live}<tspan class="caret">▍</tspan>{/if}</text
		>
		<path
			d="M41 100 L70 94 L98 102 L130 95 L162 103 L196 94 L230 102 L266 95 L300 103 L336 94 L370 102 L404 95 L440 103 L476 94 L510 102 L546 95 L595 101 V310 a14 14 0 0 1 -14 14 H55 a14 14 0 0 1 -14 -14 Z"
			class="inside"
		/>
		<path d="M90 292 H250 M170 292 V262" class="line" />
		<g class="arm">
			<path d="M170 262 L260 190 L350 170" class="line thick" />
			<path d="M170 262 L260 190 L350 170" class="line inner" />
			<circle cx="170" cy="258" r="12" class="node" />
			<circle cx="260" cy="190" r="12" class="node" />
			<circle cx="350" cy="170" r="12" class="node on" />
			<path d="M362 166 L394 150 M362 176 L394 192" class="line" />
		</g>
		<circle cx="500" cy="170" r="22" class="target" />
		<circle cx="500" cy="170" r="9" class="target" />
		<path d="M394 150 C440 130 470 140 482 156" class="line thin dash" />
		<text x="64" y="316" class="label">joints and targets</text>
	{/if}
</svg>

<style>
	.art {
		--ink: var(--foreground);
		--paper: var(--popover);
		--shade: color-mix(in oklab, var(--foreground) 7%, var(--popover));
		display: block;
		width: 100%;
		height: auto;
		overflow: visible;
		font-family: var(--font-mono);
	}
	.sheet-back {
		fill: color-mix(in oklab, var(--foreground) 14%, var(--paper));
		stroke: var(--ink);
		stroke-width: 1.5;
	}
	.sheet {
		fill: var(--paper);
		stroke: var(--ink);
		stroke-width: 1.5;
	}
	.hatch {
		stroke: var(--ink);
		stroke-width: 0.9;
		stroke-opacity: 0.35;
	}
	.code {
		font-size: 22px;
		font-weight: 500;
		fill: var(--ink);
	}
	.caret {
		fill: var(--primary);
		font-weight: 400;
		animation: blink 1.1s steps(1, end) infinite;
	}
	.inside {
		fill: var(--shade);
		stroke: var(--ink);
		stroke-width: 1.5;
		stroke-linejoin: round;
	}
	.label {
		font-size: 15px;
		fill: color-mix(in oklab, var(--foreground) 68%, transparent);
	}
	.label.mid {
		font-size: 14px;
		text-anchor: middle;
		fill: var(--ink);
	}
	.label.tiny {
		font-size: 12px;
	}
	.label.strong {
		fill: var(--ink);
		font-weight: 600;
	}
	.chip,
	.cell,
	.frame,
	.mem,
	.bar,
	.lane,
	.node {
		fill: var(--paper);
		stroke: var(--ink);
		stroke-width: 1.4;
	}
	.cell.pick,
	.bar.top,
	.lane.on,
	.node.on,
	.frame.on {
		fill: var(--primary);
		stroke: var(--ink);
	}
	.cell.pick {
		fill: color-mix(in oklab, var(--primary) 55%, var(--paper));
	}
	.node.on {
		fill: color-mix(in oklab, var(--primary) 55%, var(--paper));
	}
	.frame.on {
		fill: color-mix(in oklab, var(--primary) 30%, var(--paper));
		stroke: var(--primary);
		stroke-width: 2;
	}
	.mem {
		fill: color-mix(in oklab, var(--foreground) 10%, var(--paper));
	}
	.line {
		fill: none;
		stroke: var(--ink);
		stroke-width: 1.8;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.line.thin {
		stroke-width: 1.3;
	}
	.line.thick {
		stroke-width: 11;
	}
	.line.inner {
		stroke-width: 6;
		stroke: var(--paper);
	}
	.line.faint {
		stroke-opacity: 0.4;
		stroke-width: 1.2;
	}
	.line.accent {
		stroke: var(--primary);
		stroke-width: 3;
	}
	.line.dash {
		stroke-dasharray: 4 4;
	}
	.target {
		fill: none;
		stroke: var(--primary);
		stroke-width: 2;
	}

	/* Hovering the card draws the curves in. */
	.draw {
		stroke-dasharray: 700;
		stroke-dashoffset: 0;
	}
	:global(.domain-card:hover) .draw,
	:global(.domain-card:focus-within) .draw {
		animation: draw 1.1s cubic-bezier(0.2, 0.8, 0.2, 1) both;
	}

	/* Ambient motion runs only on released domains (the .live class). */
	.live .bar {
		transform-box: fill-box;
		transform-origin: bottom;
		animation: breathe 2.8s ease-in-out infinite;
		animation-delay: calc(var(--i, 0) * -0.45s);
	}
	.live .pulse {
		animation: fade 3.2s ease-in-out infinite;
	}
	.live .lane.on {
		animation: sweep 2.4s ease-in-out infinite;
		animation-delay: calc(var(--i, 0) * 0.08s);
	}
	.live .cell.pick,
	.live .node.on,
	.live .frame.on {
		animation: fade 3s ease-in-out infinite;
		animation-delay: calc(var(--i, 0) * 0.6s);
	}
	.live .packet {
		fill: var(--primary);
		offset-path: path('M70 149 H570');
		animation: travel 3.6s linear infinite;
	}
	.live .arm {
		transform-origin: 0 0;
		animation: swing 4.2s ease-in-out infinite;
	}
	@keyframes breathe {
		50% {
			transform: scaleY(0.82);
		}
	}
	@keyframes fade {
		50% {
			opacity: 0.55;
		}
	}
	@keyframes sweep {
		50% {
			fill-opacity: 0.15;
		}
	}
	@keyframes travel {
		from {
			offset-distance: 0%;
		}
		to {
			offset-distance: 100%;
		}
	}
	@keyframes swing {
		0%,
		100% {
			transform: translate(170px, 262px) rotate(-3deg) translate(-170px, -262px);
		}
		50% {
			transform: translate(170px, 262px) rotate(4deg) translate(-170px, -262px);
		}
	}
	@keyframes draw {
		from {
			stroke-dashoffset: 700;
		}
		to {
			stroke-dashoffset: 0;
		}
	}
	@keyframes blink {
		50% {
			opacity: 0;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.caret,
		.live .bar,
		.live .pulse,
		.live .lane.on,
		.live .cell.pick,
		.live .node.on,
		.live .frame.on,
		.live .packet,
		.live .arm {
			animation: none;
		}
		:global(.domain-card:hover) .draw,
		:global(.domain-card:focus-within) .draw {
			animation: none;
		}
	}
</style>
