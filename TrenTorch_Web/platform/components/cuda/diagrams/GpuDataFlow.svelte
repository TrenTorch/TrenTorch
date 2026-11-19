<script lang="ts">
	import './diagram.css';
	import Stepper from '../viz/_shared/Stepper.svelte';
	import { GPU_NAMES, getProfile, type GpuName } from '$processes/cuda/model';

	// Follow one launch down the hierarchy: host -> device memory -> GigaThread -> GPC -> SM -> warp -> thread.
	// Numbers (SM and GPC counts, residency limits) come from the GPU profile, the same source as every other figure.
	let gpu = $state<GpuName>('A100');
	let blocks = $state(24);
	let threads = $state(128);
	let step = $state(0);
	let sel = $state(0);
	let warpSel = $state(0);

	const p = $derived(getProfile(gpu));
	const perGpc = $derived(Math.ceil(p.sms / p.gpcs));
	const cap = $derived(
		Math.max(1, Math.min(p.maxBlocksPerSm, Math.floor(p.maxThreadsPerSm / threads)))
	);
	const warps = $derived(Math.ceil(threads / 32));
	// block b goes to GPC b % gpcs, then to the least-loaded SM of that GPC (what the GigaThread Engine does in spirit)
	const place = $derived.by(() => {
		const load: number[] = Array(p.sms).fill(0);
		const out: { gpc: number; sm: number; wave: number }[] = [];
		for (let b = 0; b < blocks; b++) {
			const g = b % p.gpcs;
			const lo = g * perGpc;
			const hi = Math.min(p.sms, lo + perGpc);
			let best = lo;
			for (let s = lo; s < hi; s++) if (load[s] < load[best]) best = s;
			out.push({ gpc: g, sm: best, wave: Math.floor(load[best] / cap) });
			load[best]++;
		}
		return { out, load };
	});
	const sb = $derived(Math.min(sel, blocks - 1));
	const sw = $derived(Math.min(warpSel, warps - 1));
	const sp = $derived(place.out[sb]);
	const tone = (b: number) => ['a', 'b', 'c'][b % 3];
	const firstWave = $derived(place.out.filter((x) => x.wave === 0).length);

	const STEPS = ['Host', 'Launch', 'Grid to GPCs', 'GPC to SM', 'SM to warps', 'Warp to threads'];
	const caption = $derived(
		[
			`The host copies the input over PCIe (about ${p.pcieGBs} GB/s on the ${gpu}) into device memory. Nothing runs yet.`,
			`The launch <<<${blocks}, ${threads}>>> creates a grid of ${blocks} blocks of ${threads} threads each, ${(blocks * threads).toLocaleString('en-US')} threads in all. The GigaThread Engine receives the grid.`,
			`The GigaThread Engine deals the ${blocks} blocks out across the ${p.gpcs} GPCs of the ${gpu}. Colours match block numbers.`,
			`Inside a GPC each block is placed on an SM with room: up to ${cap} blocks fit on one SM at a time. ${firstWave} of ${blocks} blocks start in the first wave${firstWave < blocks ? '; the rest wait for a slot' : ''}.`,
			`Block ${sb} sits on SM ${sp.sm} of GPC ${sp.gpc}. The SM cuts its ${threads} threads into ${warps} warp${warps === 1 ? '' : 's'} of 32 and hands them to its 4 warp schedulers.`,
			`Warp ${sw} of block ${sb}: 32 lanes run one instruction together. Lane ${0} gets global index ${sb * threads + sw * 32}, and the last lane ${sb * threads + sw * 32 + 31}.`
		][step]
	);
</script>

<figure class="dg flow">
	<div class="ctl">
		<label
			>GPU
			<select bind:value={gpu}
				>{#each GPU_NAMES as g (g)}<option value={g}>{g}</option>{/each}</select
			>
		</label>
		<label
			>Blocks {blocks}
			<input type="range" min="1" max="96" bind:value={blocks} />
		</label>
		<label
			>Threads / block {threads}
			<input type="range" min="32" max="1024" step="32" bind:value={threads} />
		</label>
		<Stepper bind:index={step} count={STEPS.length} />
	</div>
	<div class="tabs" role="tablist" aria-label="Stage">
		{#each STEPS as s, i (s)}
			<button type="button" role="tab" aria-selected={step === i} onclick={() => (step = i)}
				>{i + 1}. {s}</button
			>
		{/each}
	</div>
	<svg
		viewBox="0 0 720 440"
		role="img"
		aria-label="Data moving from host memory through GPCs and SMs down to warps and threads"
	>
		<defs>
			<marker
				id="gah"
				viewBox="0 0 10 10"
				refX="9"
				refY="5"
				markerWidth="7"
				markerHeight="7"
				orient="auto"><path d="M0 0L10 5L0 10z" class="ar" /></marker
			>
		</defs>
		<rect class="box" class:hi={step === 0} x="10" y="8" width="120" height="40" rx="8" />
		<text class="t" x="70" y="33" text-anchor="middle">Host RAM</text>
		<path class="ln" class:live={step === 0} d="M130 28H590" marker-end="url(#gah)" />
		<text class="t s" x="360" y="22" text-anchor="middle">PCIe {p.pcieGBs} GB/s</text>
		<rect class={step === 0 ? 'c' : 'box'} x="590" y="8" width="120" height="40" rx="8" />
		<text class="t" x="650" y="33" text-anchor="middle">Device memory</text>

		<rect
			class="box"
			class:hi={step === 1 || step === 2}
			x="10"
			y="62"
			width="700"
			height="30"
			rx="8"
		/>
		<text class="t" x="360" y="82" text-anchor="middle"
			>GigaThread Engine{step >= 1 ? `: ${blocks} blocks waiting` : ''}</text
		>
		{#if step >= 1}
			{#each Array.from({ length: Math.min(blocks, 48) }, (_, i) => i) as b (b)}
				<rect
					class={step >= 2 ? tone(b) : 'a'}
					x={16 + b * 14.4}
					y="96"
					width="11"
					height="9"
					rx="2"
				/>
			{/each}
		{/if}

		{#each Array.from({ length: p.gpcs }, (_, i) => i) as g (g)}
			{@const col = g % 4}
			{@const row = Math.floor(g / 4)}
			{@const gx = 10 + col * 177}
			{@const gy = 116 + row * 100}
			<rect
				class="box"
				class:hi={step >= 3 && sp.gpc === g && step >= 4}
				x={gx}
				y={gy}
				width="169"
				height="92"
				rx="9"
			/>
			<text class="t s" x={gx + 8} y={gy + 14}>GPC {g}</text>
			{#if step >= 2}
				<text class="t s" x={gx + 161} y={gy + 14} text-anchor="end"
					>{place.out.filter((x) => x.gpc === g).length} blocks</text
				>
			{/if}
			{#each Array.from({ length: Math.min(perGpc, p.sms - g * perGpc) }, (_, i) => g * perGpc + i) as s (s)}
				{@const k = s - g * perGpc}
				{@const n = place.load[s]}
				<rect
					class={step >= 3 && n > 0 ? (step >= 4 && s === sp.sm ? 'a' : 'c') : 'box'}
					x={gx + 8 + (k % 8) * 19}
					y={gy + 24 + Math.floor(k / 8) * 22}
					width="15"
					height="17"
					rx="3"
				/>
				{#if step >= 3 && n > 0}
					<text
						class="t s"
						x={gx + 15.5 + (k % 8) * 19}
						y={gy + 36.5 + Math.floor(k / 8) * 22}
						text-anchor="middle"
						font-size="9">{n}</text
					>
				{/if}
			{/each}
			{#if step >= 3}<text class="t s" x={gx + 8} y={gy + 86}
					>number = blocks queued on that SM</text
				>{/if}
		{/each}

		<rect class="box" x="10" y="326" width="700" height="106" rx="10" />
		{#if step < 4}
			<text class="t s" x="360" y="384" text-anchor="middle"
				>Go to step 5 to see inside one SM.</text
			>
		{:else if step === 4}
			<text class="t h" x="20" y="348">SM {sp.sm}: block {sb} is cut into {warps} warps</text>
			{#each Array.from({ length: Math.min(warps, 32) }, (_, i) => i) as w (w)}
				<rect
					class={tone(w)}
					x={20 + (w % 16) * 43}
					y={360 + Math.floor(w / 16) * 30}
					width="38"
					height="24"
					rx="4"
				/>
				<text
					class="t s"
					x={39 + (w % 16) * 43}
					y={376 + Math.floor(w / 16) * 30}
					text-anchor="middle">W{w}</text
				>
			{/each}
		{:else}
			<text class="t h" x="20" y="348">Warp {sw}: lanes 0 to 31</text>
			{#each Array.from({ length: 32 }, (_, i) => i) as l (l)}
				<rect class="a" x={20 + l * 21.5} y="358" width="18" height="30" rx="3" />
				<text class="t s" x={29 + l * 21.5} y="378" text-anchor="middle" font-size="9">{l}</text>
			{/each}
			<text class="t s" x="20" y="408"
				>threadIdx.x = {sw * 32}..{sw * 32 + 31} global index = blockIdx.x * blockDim.x + threadIdx.x
				= {sb * threads + sw * 32}..{sb * threads + sw * 32 + 31}</text
			>
		{/if}
	</svg>
	{#if step >= 4}
		<div class="ctl pick">
			<label
				>Block {sb}
				<input type="range" min="0" max={blocks - 1} bind:value={sel} />
			</label>
			{#if step === 5}
				<label
					>Warp {sw}
					<input type="range" min="0" max={warps - 1} bind:value={warpSel} />
				</label>
			{/if}
		</div>
	{/if}
	<figcaption role="status" aria-live="polite">{caption}</figcaption>
</figure>

<style>
	.ctl {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem 1.25rem;
		align-items: center;
		margin-bottom: 0.6rem;
		font-size: 0.8rem;
	}
	.ctl label {
		display: flex;
		align-items: center;
		gap: 0.4rem;
	}
	.ctl select {
		background: var(--card);
		color: var(--foreground);
		border: 1px solid var(--border);
		border-radius: 6px;
		padding: 2px 6px;
	}
	.tabs {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		margin-bottom: 0.6rem;
	}
	.tabs button {
		padding: 4px 10px;
		border: 1px solid var(--border);
		border-radius: 999px;
		background: transparent;
		color: var(--muted-foreground);
		font-size: 0.78rem;
		cursor: pointer;
	}
	.tabs button[aria-selected='true'] {
		background: var(--primary);
		color: var(--primary-foreground);
		border-color: var(--primary);
	}
	.ln.live {
		stroke: var(--primary);
		stroke-dasharray: 6 5;
		animation: dash 1s linear infinite;
	}
	@keyframes dash {
		to {
			stroke-dashoffset: -22;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.ln.live {
			animation: none;
		}
	}
	.pick {
		margin: 0.5rem 0 0;
	}
</style>
