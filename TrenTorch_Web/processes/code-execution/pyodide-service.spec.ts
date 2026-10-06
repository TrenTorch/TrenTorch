import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';

// The service's time limit and what it does when Python never comes back. The
// worker is replaced by a stand-in that the test drives by hand, so no Pyodide is
// involved; pyodide-check/ covers what Python itself reports.

class FakeWorker {
	static instances: FakeWorker[] = [];
	onmessage: ((e: { data: Record<string, unknown> }) => void) | null = null;
	onerror: (() => void) | null = null;
	posted: Record<string, unknown>[] = [];
	terminated = false;

	constructor() {
		FakeWorker.instances.push(this);
	}
	postMessage(message: Record<string, unknown>) {
		this.posted.push(message);
	}
	terminate() {
		this.terminated = true;
	}
	emit(data: Record<string, unknown>) {
		this.onmessage?.({ data });
	}
	lastRequestId() {
		return this.posted[this.posted.length - 1].id as number;
	}
}

async function freshService() {
	vi.resetModules();
	return (await import('./pyodide-service')).pyodideService;
}

beforeEach(() => {
	FakeWorker.instances = [];
	vi.stubGlobal('window', {});
	vi.stubGlobal('Worker', FakeWorker);
	vi.useFakeTimers();
});

afterEach(() => {
	vi.useRealTimers();
	vi.unstubAllGlobals();
});

describe('the time limit on running code', () => {
	it('stops code that never finishes and starts a fresh worker for the next run', async () => {
		const service = await freshService();
		service.init();
		const first = FakeWorker.instances[0];

		const run = service.runCode('while True:\n    pass');
		const outcome = run.then(
			() => 'resolved',
			(error: Error) => error.message
		);
		first.emit({ type: 'status', status: 'running' });
		await vi.advanceTimersByTimeAsync(20_000);

		expect(await outcome).toMatch(/^\[Timeout\]: Your code ran for more than 20 seconds/);
		// The stuck worker is gone: leaving it would block every later run.
		expect(first.terminated).toBe(true);
		expect(FakeWorker.instances).toHaveLength(2);
		expect(get(service.isRunning)).toBe(false);
		expect(get(service.consoleError)).toBe(true);
		expect(get(service.consoleOutput)).toContain('Check for a loop that never ends.');

		// The replacement worker serves the next request.
		const next = service.runCode('print(1)');
		const replacement = FakeWorker.instances[1];
		replacement.emit({
			id: replacement.lastRequestId(),
			type: 'run_result',
			success: true,
			output: '1\n',
			durationMs: 1
		});
		await expect(next).resolves.toMatchObject({ success: true, output: '1\n' });
	});

	it('does not count the time spent downloading packages', async () => {
		const service = await freshService();
		service.init();
		const worker = FakeWorker.instances[0];

		const run = service.runCode('import seaborn');
		const id = worker.lastRequestId();
		let settled = false;
		void run.then(
			() => (settled = true),
			() => (settled = true)
		);

		worker.emit({ type: 'status', status: 'loading_packages' });
		await vi.advanceTimersByTimeAsync(120_000);
		expect(settled).toBe(false);
		expect(worker.terminated).toBe(false);

		// The clock starts once Python is actually running the code.
		worker.emit({ type: 'status', status: 'running' });
		await vi.advanceTimersByTimeAsync(19_000);
		expect(settled).toBe(false);
		worker.emit({ id, type: 'run_result', success: true, output: 'ok\n', durationMs: 5 });
		await expect(run).resolves.toMatchObject({ success: true });
		expect(worker.terminated).toBe(false);
	});

	it('gives the test suite a little longer than a plain run', async () => {
		const service = await freshService();
		service.init();
		const worker = FakeWorker.instances[0];

		const run = service.runTests('x = 1', 'harness', 'q1');
		const outcome = run.then(
			() => 'resolved',
			(error: Error) => error.message
		);
		worker.emit({ type: 'status', status: 'testing' });
		await vi.advanceTimersByTimeAsync(24_000);
		expect(worker.terminated).toBe(false);
		await vi.advanceTimersByTimeAsync(1_000);
		expect(await outcome).toMatch(/^\[Timeout\]: The tests ran for more than 25 seconds/);
		expect(worker.terminated).toBe(true);
	});

	it('leaves the worker alone when the code finishes in time', async () => {
		const service = await freshService();
		service.init();
		const worker = FakeWorker.instances[0];

		const run = service.runCode('print(1)');
		worker.emit({ type: 'status', status: 'running' });
		worker.emit({
			id: worker.lastRequestId(),
			type: 'run_result',
			success: true,
			output: '1\n',
			durationMs: 1
		});
		await run;
		await vi.advanceTimersByTimeAsync(60_000);

		expect(worker.terminated).toBe(false);
		expect(FakeWorker.instances).toHaveLength(1);
	});
});
