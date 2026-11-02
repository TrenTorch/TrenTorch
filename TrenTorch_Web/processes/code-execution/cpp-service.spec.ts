import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';

// A Worker that records what it is sent and lets the test play the worker's side.
class FakeWorker {
	static instances: FakeWorker[] = [];
	postMessage = vi.fn();
	terminate = vi.fn();
	onmessage: ((e: { data: unknown }) => void) | null = null;
	onerror: ((e: unknown) => void) | null = null;
	constructor(
		public url: URL,
		public options?: WorkerOptions
	) {
		FakeWorker.instances.push(this);
	}
	listeners = new Set<(e: { data: unknown }) => void>();
	addEventListener(_type: string, listener: (e: { data: unknown }) => void) {
		this.listeners.add(listener);
	}
	removeEventListener(_type: string, listener: (e: { data: unknown }) => void) {
		this.listeners.delete(listener);
	}
	say(data: Record<string, unknown>) {
		this.onmessage?.({ data });
		for (const listener of [...this.listeners]) listener({ data });
	}
	sent(action: string) {
		return this.postMessage.mock.calls.map((c) => c[0]).filter((m) => m.action === action);
	}
}

type Service = typeof import('./cpp-service').cppService;
let service: Service;

beforeEach(async () => {
	vi.useFakeTimers();
	FakeWorker.instances = [];
	vi.stubGlobal('window', {});
	vi.stubGlobal('Worker', FakeWorker);
	vi.resetModules();
	service = (await import('./cpp-service')).cppService;
});
afterEach(() => {
	vi.useRealTimers();
	vi.unstubAllGlobals();
});

const worker = () => FakeWorker.instances[FakeWorker.instances.length - 1];

describe('CppService', () => {
	describe('starting', () => {
		it('starts one module worker, asks it to load the compiler, and says it is loading', () => {
			service.init();
			expect(FakeWorker.instances).toHaveLength(1);
			// A classic worker could not import the toolchain's modules.
			expect(worker().options).toEqual({ type: 'module' });
			expect(worker().sent('init')).toHaveLength(1);
			expect(get(service.runtimeState)).toBe('loading_runtime');
		});

		it('does not start a second worker when asked again', () => {
			service.init();
			service.init();
			expect(FakeWorker.instances).toHaveLength(1);
		});

		it('follows the status the worker reports', () => {
			service.init();
			worker().say({ type: 'status', status: 'loading_packages' });
			expect(get(service.runtimeState)).toBe('loading_packages');
			worker().say({ type: 'status', status: 'ready' });
			expect(get(service.runtimeState)).toBe('ready');
		});

		it('reports an error state if the worker itself fails', () => {
			vi.spyOn(console, 'error').mockImplementation(() => {});
			service.init();
			worker().onerror?.({});
			expect(get(service.runtimeState)).toBe('error');
		});
	});

	describe('running', () => {
		it('sends the code, and resolves with the output and the error together', async () => {
			const run = service.runCode('int main(){}');
			expect(worker().sent('run')[0]).toMatchObject({ code: 'int main(){}' });
			expect(get(service.isRunning)).toBe(true);
			const id = worker().sent('run')[0].id;
			worker().say({
				id,
				type: 'run_result',
				success: true,
				output: 'hello',
				error: null,
				durationMs: 5
			});
			await expect(run).resolves.toMatchObject({ success: true, output: 'hello', durationMs: 5 });
			expect(get(service.isRunning)).toBe(false);
			expect(get(service.consoleOutput)).toBe('hello');
			expect(get(service.consoleError)).toBe(false);
		});

		it('shows a compile error, and marks the run as failed', async () => {
			const run = service.runCode('x');
			const id = worker().sent('run')[0].id;
			worker().say({
				id,
				type: 'run_result',
				success: false,
				output: '',
				error: 'main.cpp:1:1: error',
				durationMs: 9
			});
			await expect(run).resolves.toMatchObject({ success: false });
			expect(get(service.consoleOutput)).toBe('main.cpp:1:1: error');
			expect(get(service.consoleError)).toBe(true);
		});

		it('rejects when the worker reports an error for the run', async () => {
			const run = service.runCode('x');
			const id = worker().sent('run')[0].id;
			worker().say({ id, type: 'error', error: 'worker blew up' });
			await expect(run).rejects.toThrow('worker blew up');
			expect(get(service.isRunning)).toBe(false);
			expect(get(service.consoleError)).toBe(true);
		});
	});

	describe('a program that never finishes', () => {
		it('is stopped 30 seconds after it starts running, by ending the worker', async () => {
			const run = service.runCode('int main(){ for(;;){} }');
			const caught = run.catch((e: Error) => e);
			worker().say({ type: 'status', status: 'running' });
			await vi.advanceTimersByTimeAsync(29_999);
			expect(worker().terminate).not.toHaveBeenCalled();
			await vi.advanceTimersByTimeAsync(2);
			expect(worker().terminate).toHaveBeenCalledTimes(1);
			const error = (await caught) as Error;
			expect(error.message).toMatch(/ran for more than 30 seconds.*infinite loop/);
			expect(get(service.consoleOutput)).toMatch(
				/^\[Timeout\]: The program ran for more than 30 seconds/
			);
			expect(get(service.isRunning)).toBe(false);
			expect(get(service.consoleError)).toBe(true);
			expect(get(service.runtimeState)).toBe('uninitialized');
		});

		it('does not count the time spent downloading the compiler against the program', async () => {
			const run = service.runCode('x');
			const caught = run.catch((e: Error) => e);
			await vi.advanceTimersByTimeAsync(120_000);
			expect(worker().terminate).not.toHaveBeenCalled();
			worker().say({ type: 'status', status: 'running' });
			await vi.advanceTimersByTimeAsync(29_000);
			expect(worker().terminate).not.toHaveBeenCalled();
			worker().say({
				id: worker().sent('run')[0].id,
				type: 'run_result',
				success: true,
				output: 'ok',
				durationMs: 1
			});
			await expect(run).resolves.toBeDefined();
			await caught;
		});

		it('gives up on a compiler that never finishes downloading, after 3 minutes, with a different message', async () => {
			const caught = service.runCode('x').catch((e: Error) => e);
			await vi.advanceTimersByTimeAsync(180_001);
			expect(worker().terminate).toHaveBeenCalledTimes(1);
			expect(((await caught) as Error).message).toMatch(/took too long to download/);
		});

		it('is not stopped late once its answer has arrived', async () => {
			const run = service.runCode('x');
			worker().say({ type: 'status', status: 'running' });
			worker().say({
				id: worker().sent('run')[0].id,
				type: 'run_result',
				success: true,
				output: 'ok',
				durationMs: 1
			});
			await run;
			await vi.advanceTimersByTimeAsync(600_000);
			expect(worker().terminate).not.toHaveBeenCalled();
		});

		it('starts a fresh worker for the next run, so one runaway program does not break the editor', async () => {
			const first = service.runCode('x').catch((e: Error) => e);
			worker().say({ type: 'status', status: 'running' });
			await vi.advanceTimersByTimeAsync(30_001);
			await first;
			expect(FakeWorker.instances).toHaveLength(1);

			const second = service.runCode('y');
			expect(FakeWorker.instances).toHaveLength(2);
			worker().say({
				id: worker().sent('run')[0].id,
				type: 'run_result',
				success: true,
				output: 'fine',
				durationMs: 1
			});
			await expect(second).resolves.toMatchObject({ output: 'fine' });
		});
	});

	describe('submitting', () => {
		const plan = {
			function: { name: 'f', params: [], returns: 'int' },
			compare: 'exact',
			calls: [
				{
					key: 'a:0',
					case: 'a',
					index: 0,
					args: [],
					limitMs: 1000,
					perf: false,
					reads: false,
					batch: false
				}
			]
		};

		async function submitting() {
			vi.resetModules();
			vi.doMock('./pyodide-service', () => ({
				pyodideService: {
					prepareExternal: async () => ({ plan, error: null }),
					judgeExternal: async (_h: string, outputs: Record<string, unknown>) => ({
						results: Object.keys(outputs).map((name) => ({ name, passed: true, error: null })),
						notes: [],
						error: null
					})
				}
			}));
			return (await import('./cpp-service')).cppService;
		}

		it('has Python prepare the tests, runs the student code in the worker, and has Python judge', async () => {
			const svc = await submitting();
			const done = svc.runTests('int main() {}', 'harness', 'q');
			await vi.advanceTimersByTimeAsync(0);
			expect(worker().sent('external')).toHaveLength(1);
			expect(worker().sent('external')[0]).toMatchObject({ code: 'int main() {}', plan });
			worker().say({ type: 'external_started' });
			worker().say({
				type: 'external_record',
				key: 'a:0',
				record: { outJson: '1', ms: 1, reads: null }
			});
			worker().say({ type: 'external_done' });
			await expect(done).resolves.toMatchObject({ totalTests: 1, allPassed: true });
			expect(get(svc.isRunning)).toBe(false);
		});

		it('shows the compiler message when the code does not build', async () => {
			const svc = await submitting();
			const done = svc.runTests('oops', 'harness', 'q');
			await vi.advanceTimersByTimeAsync(0);
			worker().say({
				type: 'external_failed',
				error: 'main.cpp:1:1: error: expected unqualified-id'
			});
			await expect(done).resolves.toMatchObject({
				totalTests: 0,
				allPassed: false,
				error: 'main.cpp:1:1: error: expected unqualified-id'
			});
			expect(get(svc.consoleError)).toBe(true);
			expect(get(svc.consoleOutput)).toContain('expected unqualified-id');
		});
	});
});
