// Page-side client for the Gpubox worker (platform/static/gpubox/worker.js).
// One worker is kept warm; a hard timeout terminates it and the next run starts a fresh one.
export const GPUBOX_VERSION = '1.0.0-tt2';
const WORKER_URL = '/gpubox/worker.js';
const RUN_TIMEOUT_MS = 20_000;

export type BufferSpec = { type: 'f32' | 'i32'; data: ArrayLike<number>; read?: boolean };
export type RunRequest = {
	source: string;
	kernel: string;
	grid: number | { x?: number; y?: number; z?: number };
	block: number | { x?: number; y?: number; z?: number };
	shared?: number;
	profile?: string;
	buffers: BufferSpec[];
	args: (number | { buf: number })[];
};
export type RunResult = {
	outputs: Record<number, number[]>;
	counters: Record<string, number>;
	diagnostics: unknown[];
	timings: Record<string, number>;
};

let worker: Worker | null = null;
let nextId = 1;

function discard() {
	worker?.terminate();
	worker = null;
}

export function runKernel(req: RunRequest): Promise<RunResult> {
	worker ??= new Worker(WORKER_URL);
	const w = worker;
	const id = nextId++;
	return new Promise((resolve, reject) => {
		const timer = setTimeout(() => {
			cleanup();
			discard();
			reject(new Error(`Timed out after ${RUN_TIMEOUT_MS / 1000}s (possible infinite loop)`));
		}, RUN_TIMEOUT_MS);
		const onMessage = (e: MessageEvent) => {
			const m = e.data;
			if (m.id !== id && m.id !== -1) return;
			cleanup();
			if (m.ok) resolve(m);
			else reject(new Error(m.error));
		};
		const onError = (e: ErrorEvent) => {
			cleanup();
			discard();
			reject(new Error(e.message || 'Gpubox worker crashed'));
		};
		const cleanup = () => {
			clearTimeout(timer);
			w.removeEventListener('message', onMessage);
			w.removeEventListener('error', onError);
		};
		w.addEventListener('message', onMessage);
		w.addEventListener('error', onError);
		w.postMessage({
			id,
			action: 'run',
			...req,
			buffers: req.buffers.map((b) => ({ ...b, data: Array.from(b.data) }))
		});
	});
}

export function pingWorker(): Promise<{ version: string; loadMs: number }> {
	worker ??= new Worker(WORKER_URL);
	const w = worker;
	const id = nextId++;
	return new Promise((resolve, reject) => {
		const onMessage = (e: MessageEvent) => {
			if (e.data.id !== id && e.data.id !== -1) return;
			w.removeEventListener('message', onMessage);
			if (e.data.ok) resolve(e.data);
			else reject(new Error(e.data.error));
		};
		w.addEventListener('message', onMessage);
		w.postMessage({ id, action: 'ping' });
	});
}
