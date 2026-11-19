<script lang="ts">
	import './viz.css';
	import { GPU_NAMES, getProfile } from '$processes/cuda/model/profiles';
	import {
		LAST_RUN_KEY,
		initialState,
		type LastRun,
		type Control,
		type Frame,
		type Panel,
		type State,
		type VizConfig,
		type VizOutput,
		type Tone
	} from '$processes/cuda/viz/types';
	import LaneStrip from './LaneStrip.svelte';
	import MemoryGrid from './MemoryGrid.svelte';
	import ReadoutBar from './ReadoutBar.svelte';
	import Stepper from './Stepper.svelte';
	import CellBox from './CellBox.svelte';

	let {
		config,
		mode = '',
		title = ''
	}: { config: VizConfig; mode?: string; title?: string } = $props();

	let state = $state<State>(initialState(config, mode || undefined));
	let lastRun = $state<LastRun | null>(null);
	$effect(() => {
		try {
			const raw = localStorage.getItem(LAST_RUN_KEY);
			lastRun = raw ? (JSON.parse(raw) as LastRun) : null;
		} catch {
			lastRun = null;
		}
	});
	let step = $state(0);

	const hidden = $derived(new Set(config.modes?.[mode]?.hide ?? []));
	const controls = $derived(config.controls.filter((c) => !hidden.has(c.id)));
	const result = $derived.by((): VizOutput => {
		try {
			return config.compute(state, { mode: mode || undefined, lastRun });
		} catch (e) {
			return {
				panels: [],
				readouts: [],
				live: `This figure could not be drawn: ${e instanceof Error ? e.message : e}`
			};
		}
	});
	const framePanels = $derived(
		result.panels.filter((p): p is Extract<Panel, { kind: 'frames' }> => p.kind === 'frames')
	);
	const frameCount = $derived(Math.max(1, ...framePanels.map((p) => p.frames.length)));
	const toneVar: Record<Tone, string> = {
		memory: 'var(--viz-stall)',
		compute: 'var(--viz-active)',
		launch: 'var(--viz-masked)',
		good: 'var(--viz-good)',
		bad: 'var(--viz-error)',
		neutral: 'var(--muted-foreground)',
		tint0: 'var(--viz-t0)',
		tint1: 'var(--viz-t1)',
		tint2: 'var(--viz-t2)',
		tint3: 'var(--viz-t3)',
		tint4: 'var(--viz-t4)'
	};

	// ---- controls ----
	const logValue = (c: Extract<Control, { type: 'range' }>, t: number) => {
		const v = c.min * (c.max / c.min) ** t;
		return c.step >= 1 ? Math.max(c.min, Math.round(v / c.step) * c.step) : v;
	};
	const logPos = (c: Extract<Control, { type: 'range' }>, v: number) =>
		Math.log(Number(v) / c.min) / Math.log(c.max / c.min);
	const show = (c: Extract<Control, { type: 'range' }>, v: number) =>
		c.format ? c.format(v) : String(Number(v.toPrecision(4)));

	// ---- charts ----
	const W = 460,
		H = 220,
		PAD = { l: 52, r: 12, t: 12, b: 36 };
	function scale(lo: number, hi: number, log: boolean, a: number, b: number) {
		const f = log ? (x: number) => Math.log(Math.max(x, 1e-12)) : (x: number) => x;
		const l = f(lo),
			h = f(hi);
		return (x: number) => a + ((f(x) - l) / (h - l || 1)) * (b - a);
	}
	function line(p: Extract<Panel, { kind: 'line' }>) {
		const pts = p.series.flatMap((s) => s.points);
		const xs = pts.map((q) => q[0]),
			ys = pts.map((q) => q[1]);
		const xlo = Math.min(...xs),
			xhi = Math.max(...xs),
			ylo = p.yLog ? Math.min(...ys.filter((y) => y > 0)) : 0,
			yhi = p.yMax ?? Math.max(...ys);
		const sx = scale(xlo, xhi, !!p.xLog, PAD.l, W - PAD.r),
			sy = scale(ylo, yhi, !!p.yLog, H - PAD.b, PAD.t);
		const ticks = (lo: number, hi: number, log: boolean) =>
			log
				? Array.from(
						{ length: Math.max(2, Math.floor(Math.log10(hi / lo)) + 1) },
						(_, i) => lo * 10 ** i
					).filter((v) => v <= hi * 1.01)
				: Array.from({ length: 5 }, (_, i) => lo + ((hi - lo) * i) / 4);
		return {
			sx,
			sy,
			xt: ticks(xlo, xhi, !!p.xLog),
			yt: ticks(ylo, yhi, !!p.yLog),
			path: (s: { points: [number, number][] }) =>
				s.points
					.map((q, i) => `${i ? 'L' : 'M'}${sx(q[0]).toFixed(1)},${sy(q[1]).toFixed(1)}`)
					.join(' ')
		};
	}
	const tickText = (v: number) =>
		Math.abs(v) >= 1000 || (Math.abs(v) < 0.01 && v !== 0)
			? v.toExponential(0)
			: String(Number(v.toPrecision(3)));
	const barMax = (p: Extract<Panel, { kind: 'bars' }>) =>
		p.max ?? Math.max(1e-12, ...p.bars.map((b) => b.segments.reduce((a, s) => a + s.value, 0)));
</script>

<figure class="cuda-figure">
	<figcaption>
		<strong>{title || config.title}</strong>
		{#if config.illustrative}<span class="badge" title="Teaching numbers, not measurements"
				>illustrative numbers</span
			>{/if}
		{#if mode}<span class="badge">{config.modes?.[mode]?.title ?? mode}</span>{/if}
	</figcaption>

	{#if controls.length}
		<div class="controls">
			{#each controls as c (c.id)}
				<label class="ctl" title={c.hint}>
					<span class="lbl">{c.label}</span>
					{#if c.type === 'range'}
						<input
							type="range"
							min={c.log ? 0 : c.min}
							max={c.log ? 1 : c.max}
							step={c.log ? 0.001 : c.step}
							value={c.log ? logPos(c, Number(state[c.id])) : state[c.id]}
							oninput={(e) => {
								const raw = Number(e.currentTarget.value);
								state[c.id] = c.log ? logValue(c, raw) : raw;
							}}
							aria-valuetext={show(c, Number(state[c.id]))}
						/>
						<output>{show(c, Number(state[c.id]))}</output>
					{:else if c.type === 'select'}
						<select bind:value={state[c.id]}
							>{#each c.options as o (o.value)}<option value={o.value}>{o.label}</option
								>{/each}</select
						>
					{:else if c.type === 'gpu'}
						<select bind:value={state[c.id]}
							>{#each GPU_NAMES as g (g)}<option value={g}>{g} ({getProfile(g).sms} SMs)</option
								>{/each}</select
						>
					{:else}
						<input
							type="checkbox"
							checked={Boolean(state[c.id])}
							onchange={(e) => (state[c.id] = e.currentTarget.checked)}
						/>
					{/if}
				</label>
			{/each}
		</div>
	{/if}

	{#if framePanels.length && frameCount > 1}<Stepper bind:index={step} count={frameCount} />{/if}

	{#each result.panels as p, pi (pi)}
		<section class="panel">
			{#if 'title' in p && p.title}<h4>{p.title}</h4>{/if}
			{#if p.kind === 'frames'}
				{@const fr = p.frames[Math.min(step, p.frames.length - 1)] as Frame}
				{#each fr.rows as r (r.label)}
					<div class="row">
						<span class="rl">{r.label}</span>
						{#if r.lanes}<LaneStrip lanes={r.cells} />{:else}<MemoryGrid
								cells={r.cells}
								columns={Math.min(r.cells.length, 32)}
							/>{/if}
						{#if r.note}<span class="rn">{r.note}</span>{/if}
					</div>
				{/each}
				<p class="caption">{fr.caption}</p>
			{:else if p.kind === 'bars'}
				{@const mx = barMax(p)}
				<div class="bars">
					{#each p.bars as b (b.label)}
						<div class="brow">
							<span class="bl">{b.label}</span>
							<span
								class="track"
								role="img"
								aria-label="{b.label}: {b.segments
									.map((s) => `${s.label ?? ''} ${Number(s.value.toPrecision(3))}`)
									.join(', ')}"
							>
								{#each b.segments as s, si (si)}
									<span
										class="seg"
										style="width:{Math.min(100, (s.value / mx) * 100)}%; background:{toneVar[
											s.tone
										]}"
										title={s.label}
									></span>
								{/each}
							</span>
							<span class="bv"
								>{b.note ??
									b.segments.map((s) => Number(s.value.toPrecision(3))).join(' + ')}{p.unit
									? ` ${p.unit}`
									: ''}</span
							>
						</div>
					{/each}
				</div>
			{:else if p.kind === 'line'}
				{@const L = line(p)}
				<svg
					viewBox="0 0 {W} {H}"
					class="chart"
					role="img"
					aria-label="{p.title ?? 'chart'}: {p.yLabel} against {p.xLabel}"
				>
					{#each L.yt as t (t)}<line
							x1={PAD.l}
							x2={W - PAD.r}
							y1={L.sy(t)}
							y2={L.sy(t)}
							class="grid"
						/><text x={PAD.l - 4} y={L.sy(t) + 3} text-anchor="end">{tickText(t)}</text>{/each}
					{#each L.xt as t (t)}<line
							y1={PAD.t}
							y2={H - PAD.b}
							x1={L.sx(t)}
							x2={L.sx(t)}
							class="grid"
						/><text x={L.sx(t)} y={H - PAD.b + 13} text-anchor="middle">{tickText(t)}</text>{/each}
					{#each p.series.filter((q) => q.points.length === 1) as s (s.name)}<circle
							cx={L.sx(s.points[0][0])}
							cy={L.sy(s.points[0][1])}
							r="3.5"
							fill={toneVar[s.tone]}><title>{s.name}</title></circle
						>{/each}
					{#each p.series.filter((q) => q.points.length > 1) as s (s.name)}<path
							d={L.path(s)}
							fill="none"
							stroke={toneVar[s.tone]}
							stroke-width="2"
							stroke-dasharray={s.dashed ? '5 4' : undefined}><title>{s.name}</title></path
						>{/each}
					{#each p.markers ?? [] as m (m.label)}<line
							x1={L.sx(m.x)}
							x2={L.sx(m.x)}
							y1={PAD.t}
							y2={H - PAD.b}
							class="marker"
						/><text x={L.sx(m.x) + 3} y={PAD.t + 9} class="mt">{m.label}</text>{/each}
					{#if p.point}<circle
							cx={L.sx(p.point.x)}
							cy={L.sy(p.point.y)}
							r="5"
							fill="var(--viz-active)"
							stroke="var(--foreground)"><title>{p.point.label}</title></circle
						>{/if}
					<text x={W / 2} y={H - 2} text-anchor="middle" class="ax">{p.xLabel}</text>
					<text x="10" y={H / 2} transform="rotate(-90 10 {H / 2})" text-anchor="middle" class="ax"
						>{p.yLabel}</text
					>
				</svg>
				<ul class="legend">
					{#each p.series as s (s.name)}<li>
							<span class="sw" style="background:{toneVar[s.tone]}"></span>{s.name}
						</li>{/each}
				</ul>
			{:else if p.kind === 'table'}
				<div class="tbl">
					<table>
						<thead
							><tr
								>{#each p.header as h (h)}<th>{h}</th>{/each}</tr
							></thead
						>
						<tbody
							>{#each p.rows as row, ri (ri)}<tr class:hl={p.highlight === ri}
									>{#each row as c, ci (ci)}<td>{c}</td>{/each}</tr
								>{/each}</tbody
						>
					</table>
				</div>
			{:else}
				<p class="text">{p.text}</p>
			{/if}
		</section>
	{/each}

	{#if result.readouts.length}<ReadoutBar readouts={result.readouts} />{/if}
	<p class="live" aria-live="polite" role="status">{result.live}</p>
	{#if result.footnote}<p class="foot">{result.footnote}</p>{/if}
	<span class="vh"><CellBox cell={{ state: 'idle' }} size={1} /></span>
</figure>

<style>
	figure {
		margin: 0;
		padding: 0.9rem 1rem 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
		font-family: var(--ide-sans, inherit);
	}
	figcaption {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		flex-wrap: wrap;
	}
	.badge {
		font-size: 0.68rem;
		padding: 0.05rem 0.45rem;
		border: 1px solid var(--border);
		border-radius: 999px;
		color: var(--muted-foreground);
	}
	.controls {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr));
		gap: 0.5rem 1rem;
	}
	.ctl {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.8rem;
		min-width: 0;
	}
	.lbl {
		min-width: 7rem;
		color: var(--muted-foreground);
	}
	.ctl input[type='range'] {
		flex: 1;
		min-width: 5rem;
	}
	output {
		font: 600 0.78rem var(--font-mono, monospace);
		min-width: 3.5rem;
		text-align: right;
	}
	select {
		flex: 1;
		padding: 0.2rem 0.4rem;
		border: 1px solid var(--border);
		border-radius: 0.35rem;
		background: var(--card);
		color: var(--foreground);
	}
	.panel h4 {
		margin: 0 0 0.4rem;
		font-size: 0.85rem;
	}
	.row {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		margin: 0.3rem 0;
		flex-wrap: wrap;
	}
	.rl {
		width: 8rem;
		font-size: 0.75rem;
		color: var(--muted-foreground);
	}
	.rn,
	.caption,
	.live,
	.foot,
	.text {
		font-size: 0.8rem;
		color: var(--muted-foreground);
		margin: 0.2rem 0;
	}
	.live {
		color: var(--foreground);
	}
	.bars {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}
	.brow {
		display: grid;
		grid-template-columns: 9rem 1fr auto;
		gap: 0.5rem;
		align-items: center;
		font-size: 0.78rem;
	}
	.track {
		display: flex;
		height: 0.9rem;
		background: var(--secondary);
		border-radius: 4px;
		overflow: hidden;
	}
	.seg {
		display: block;
		height: 100%;
	}
	.bv {
		font: 600 0.75rem var(--font-mono, monospace);
		color: var(--muted-foreground);
	}
	.chart {
		width: 100%;
		max-width: 34rem;
		overflow: visible;
	}
	.chart text {
		font-size: 9px;
		fill: var(--muted-foreground);
	}
	.chart .ax {
		font-size: 10px;
	}
	.chart .grid {
		stroke: var(--border);
		stroke-width: 0.5;
	}
	.chart .marker {
		stroke: var(--viz-error);
		stroke-dasharray: 3 3;
	}
	.chart .mt {
		fill: var(--viz-error);
	}
	.legend {
		display: flex;
		flex-wrap: wrap;
		gap: 0.8rem;
		margin: 0;
		padding: 0;
		list-style: none;
		font-size: 0.75rem;
	}
	.sw {
		display: inline-block;
		width: 0.7rem;
		height: 0.7rem;
		margin-right: 0.3rem;
		border-radius: 2px;
	}
	.tbl {
		overflow-x: auto;
	}
	table {
		border-collapse: collapse;
		font-size: 0.78rem;
		width: 100%;
	}
	th,
	td {
		border: 1px solid var(--border);
		padding: 0.25rem 0.5rem;
		text-align: left;
	}
	tr.hl td {
		background: color-mix(in oklab, var(--viz-active) 18%, transparent);
	}
	.vh {
		display: none;
	}
</style>
