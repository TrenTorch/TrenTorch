// Small deterministic simulations behind the scheduling figures (B2, B3, B5). They are teaching models,
// not the Gpubox engine; the figures label them as such.

export interface BlockEvent {
	block: number;
	sm: number;
	slot: number;
	start: number;
	end: number;
}
/** Blocks queue up and drop into free (SM, slot) places; `times[i]` is how long block i runs. */
export function simulateBlocks(opts: {
	sms: number;
	blocksPerSm: number;
	grid: number;
	times: number[];
}) {
	const slots = Array.from({ length: opts.sms * opts.blocksPerSm }, (_, i) => ({
		sm: Math.floor(i / opts.blocksPerSm),
		slot: i % opts.blocksPerSm,
		free: 0
	}));
	const events: BlockEvent[] = [];
	for (let b = 0; b < opts.grid; b++) {
		let best = slots[0];
		for (const s of slots) if (s.free < best.free) best = s; // earliest free place
		const start = best.free,
			end = start + opts.times[b % opts.times.length];
		events.push({ block: b, sm: best.sm, slot: best.slot, start, end });
		best.free = end;
	}
	const makespan = Math.max(...events.map((e) => e.end));
	const busy = events.reduce((a, e) => a + (e.end - e.start), 0);
	const capacity = opts.sms * opts.blocksPerSm;
	return {
		events,
		makespan,
		utilization: busy / (makespan * capacity),
		waves: Math.ceil(opts.grid / capacity),
		finishOrder: [...events].sort((a, b) => a.end - b.end || a.block - b.block).map((e) => e.block),
		idleInLastWave: makespan * capacity - busy
	};
}
/** Deterministic pseudo-random block durations in [1, 1 + spread]. */
export function blockTimes(n: number, random: boolean, seed = 3, spread = 0.8) {
	if (!random) return Array(n).fill(1);
	let s = seed >>> 0;
	return Array.from(
		{ length: n },
		() => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0), 1 + (s / 4294967296) * spread)
	);
}

export type WarpTick = 'issue' | 'wait' | 'ready';
/**
 * One scheduler, `warps` resident warps, each doing `compute` instructions then waiting `latency` ticks for a
 * load (one instruction issues per tick). `ilp` independent chains per warp let it issue that many loads before waiting.
 */
export function simulateLatencyHiding(opts: {
	warps: number;
	latency: number;
	compute: number;
	ticks: number;
	ilp?: number;
}) {
	const ilp = opts.ilp ?? 1;
	const warps = Array.from({ length: opts.warps }, () => ({
		left: opts.compute * ilp,
		waitUntil: -1,
		chunk: opts.compute * ilp
	}));
	const grid: WarpTick[][] = warps.map(() => []);
	const issued: number[] = [];
	for (let t = 0; t < opts.ticks; t++) {
		let pick = -1;
		warps.forEach((w, i) => {
			if (pick < 0 && w.waitUntil <= t) pick = i;
		});
		warps.forEach((w, i) => {
			if (i === pick) {
				grid[i].push('issue');
				w.left--;
				if (w.left === 0) {
					w.waitUntil = t + 1 + opts.latency;
					w.left = w.chunk;
				}
			} else grid[i].push(w.waitUntil > t ? 'wait' : 'ready');
		});
		issued.push(pick);
	}
	const used = issued.filter((x) => x >= 0).length;
	return { grid, issued, utilization: used / opts.ticks, idle: opts.ticks - used };
}

export interface HostEvent {
	lane: 'host' | 'device';
	label: string;
	start: number;
	end: number;
	kind: 'launch' | 'kernel' | 'wait' | 'copy' | 'print';
	stale?: boolean;
}
/** Host/device timeline (B5): kernel launches are asynchronous; the host waits only when told to. */
export function simulateHost(opts: {
	launches: number;
	kernelTime: number;
	launchCost: number;
	sync: boolean;
	blockingCopy: boolean;
	copyTime: number;
}) {
	const ev: HostEvent[] = [];
	let host = 0,
		deviceFree = 0;
	for (let i = 0; i < opts.launches; i++) {
		ev.push({
			lane: 'host',
			label: `launch ${i + 1}`,
			start: host,
			end: host + opts.launchCost,
			kind: 'launch'
		});
		host += opts.launchCost;
		const start = Math.max(host, deviceFree);
		ev.push({
			lane: 'device',
			label: `kernel ${i + 1}`,
			start,
			end: start + opts.kernelTime,
			kind: 'kernel'
		});
		deviceFree = start + opts.kernelTime;
	}
	if (opts.sync || opts.blockingCopy) {
		ev.push({
			lane: 'host',
			label: opts.sync ? 'cudaDeviceSynchronize (waiting)' : 'blocking cudaMemcpy (waiting)',
			start: host,
			end: deviceFree,
			kind: 'wait'
		});
		host = deviceFree;
	}
	if (opts.blockingCopy) {
		ev.push({
			lane: 'host',
			label: 'copy result',
			start: host,
			end: host + opts.copyTime,
			kind: 'copy'
		});
		host += opts.copyTime;
	}
	const stale = !opts.sync && !opts.blockingCopy && host < deviceFree;
	ev.push({
		lane: 'host',
		label: stale ? 'printf(result): STALE' : 'printf(result)',
		start: host,
		end: host + opts.launchCost,
		kind: 'print',
		stale
	});
	return {
		events: ev,
		total: Math.max(host + opts.launchCost, deviceFree),
		stale,
		deviceBusyUntil: deviceFree
	};
}
