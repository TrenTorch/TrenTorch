import { writable, type Writable } from 'svelte/store';
import type {
	ExecutionResult,
	PreviewFigure,
	RuntimeState,
	SingleTestResult,
	SubmissionResult
} from '$data/curriculum/types';

// CUDA problems run on the Gpubox simulator inside a Web Worker (platform/static/gpubox/worker.js, which
// loads the pinned engine from /gpubox/<version>/). Same shape as the other language services so the
// IDE page and UnifiedExecutor treat it like any other runtime. Nothing leaves the browser.
const WORKER_URL = '/gpubox/worker.js';
const LOAD_TIMEOUT_MS = 30_000;
// A kernel stuck in a loop cannot be interrupted from inside: the whole worker is terminated.
const RUN_TIMEOUT_MS = 30_000;

type Reply = {
	id: number;
	ok: boolean;
	error?: string;
	kernels?: string[];
	loadMs?: number;
	results?: {
		name: string;
		hidden: boolean;
		counters?: Record<string, number>;
		passed: boolean;
		error?: string;
		expected?: string;
		actual?: string;
		report?: string;
	}[];
	totalMs?: number;
};

class CudaService {
	private worker: Worker | null = null;
	private requestId = 0;
	private pending = new Map<
		number,
		{
			resolve: (r: Reply) => void;
			reject: (e: Error) => void;
			timer: ReturnType<typeof setTimeout>;
		}
	>();

	public runtimeState: Writable<RuntimeState> = writable('uninitialized');
	public consoleOutput: Writable<string> = writable('');
	public consoleError: Writable<boolean> = writable(false);
	public testResults: Writable<SubmissionResult | null> = writable(null);
	public isRunning: Writable<boolean> = writable(false);
	public consoleFigures: Writable<PreviewFigure[]> = writable([]);

	private discard(reason: string): void {
		this.worker?.terminate();
		this.worker = null;
		this.runtimeState.set('uninitialized');
		for (const [id, p] of this.pending) {
			clearTimeout(p.timer);
			p.reject(new Error(reason));
			this.pending.delete(id);
		}
	}

	public init(): void {
		if (typeof window === 'undefined' || this.worker) return;
		try {
			this.runtimeState.set('loading_runtime');
			const worker = new Worker(WORKER_URL);
			this.worker = worker;
			worker.onmessage = (e: MessageEvent<Reply>) => {
				const m = e.data;
				if (m.id === -1) {
					// the engine files could not be fetched
					this.runtimeState.set('error');
					this.consoleError.set(true);
					this.consoleOutput.set(`[Error]: ${m.error}`);
					return;
				}
				const p = this.pending.get(m.id);
				if (!p) return;
				clearTimeout(p.timer);
				this.pending.delete(m.id);
				if (m.ok) p.resolve(m);
				else p.reject(new Error(m.error ?? 'The simulator failed'));
			};
			worker.onerror = (err) => {
				console.error('CUDA worker error', err);
				this.discard('The CUDA simulator crashed');
				this.runtimeState.set('error');
			};
			// Warm-up: resolves once the engine scripts have loaded.
			void this.request({ action: 'ping' }, LOAD_TIMEOUT_MS)
				.then(() => this.runtimeState.set('ready'))
				.catch(() => undefined);
		} catch (err) {
			console.error('Failed to start the CUDA worker', err);
			this.runtimeState.set('error');
		}
	}

	private request(message: Record<string, unknown>, timeoutMs: number): Promise<Reply> {
		this.init();
		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timer = setTimeout(() => {
				this.pending.delete(id);
				this.discard('timeout');
				reject(
					new Error(
						`The kernel ran for more than ${timeoutMs / 1000} seconds and was stopped. Is there an infinite loop?`
					)
				);
			}, timeoutMs);
			this.pending.set(id, { resolve, reject, timer });
			this.worker?.postMessage({ id, ...message });
		});
	}

	/** Saves the first case's counters so the theory roofline can plot "my last run". */
	private rememberRun(
		contentId: string,
		cases: { report?: string; counters?: Record<string, number> }[]
	) {
		const c = cases.find((x) => x.counters)?.counters;
		if (!c) return;
		try {
			localStorage.setItem(
				'trentorch:cuda:lastrun',
				JSON.stringify({
					id: contentId,
					title: contentId.replace(/^cuda-/, '').replace(/-/g, ' '),
					flops: c.flopCount ?? 0,
					bytes: (c.globalLoadBytes ?? 0) + (c.globalStoreBytes ?? 0),
					gpu: 'A100'
				})
			);
		} catch {
			// storage blocked: the roofline just will not show the run
		}
	}

	/** Run: compile only, so a syntax error shows up without needing a harness. */
	public async runCode(code: string): Promise<ExecutionResult> {
		const start = performance.now();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set('Compiling for the GPU simulator…\n');
		try {
			const reply = await this.request({ action: 'check', source: code }, RUN_TIMEOUT_MS);
			const output = `Compiled. Kernels: ${(reply.kernels ?? []).join(', ') || '(none found)'}`;
			this.consoleOutput.set(output);
			return { success: true, output, durationMs: performance.now() - start };
		} catch (e) {
			const error = e instanceof Error ? e.message : String(e);
			this.consoleError.set(true);
			this.consoleOutput.set(error);
			return { success: false, output: '', error, durationMs: performance.now() - start };
		} finally {
			this.isRunning.set(false);
		}
	}

	public async runPreview(): Promise<{ output: string; error?: string; figures: PreviewFigure[] }> {
		return { output: '', figures: [] };
	}

	// Run (sampleLimit set): the first visible cases, no solved side effects. Submit: every case, hidden ones too.
	public async runTests(
		code: string,
		testHarnessCode: string,
		contentId: string,
		sampleLimit?: number
	): Promise<SubmissionResult> {
		const start = performance.now();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.runtimeState.set('testing');
		this.consoleOutput.set(
			sampleLimit ? 'Running sample cases on the simulator…\n' : 'Running all cases…\n'
		);
		try {
			const reply = await this.request(
				{ action: 'test', source: code, harness: testHarnessCode, sampleLimit },
				RUN_TIMEOUT_MS
			);
			const cases = reply.results ?? [];
			const results: SingleTestResult[] = cases.map((c) => ({
				name: c.hidden ? `${c.name} (hidden)` : c.name,
				passed: c.passed,
				durationMs: 0,
				error: c.error,
				expected: c.expected,
				actual: c.actual,
				stdout: c.report
			}));
			const passed = results.filter((r) => r.passed).length;
			const lines = cases.map(
				(c) => `${c.passed ? 'PASS' : 'FAIL'}  ${c.name}${c.error ? `\n      ${c.error}` : ''}`
			);
			const firstReport = cases.find((c) => c.report)?.report;
			const rawOutput = [
				lines.join('\n'),
				firstReport ? `\n--- Report (${cases[0]?.name}) ---\n${firstReport}` : ''
			].join('\n');
			const result: SubmissionResult = {
				contentId,
				totalTests: results.length,
				passedTests: passed,
				failedTests: results.length - passed,
				allPassed: results.length > 0 && passed === results.length,
				totalDurationMs: performance.now() - start,
				results,
				rawOutput,
				isSample: Boolean(sampleLimit)
			};
			this.consoleError.set(!result.allPassed);
			this.consoleOutput.set(rawOutput);
			this.testResults.set(result);
			this.rememberRun(contentId, cases);
			return result;
		} catch (e) {
			const error = e instanceof Error ? e.message : String(e);
			const result: SubmissionResult = {
				contentId,
				totalTests: 0,
				passedTests: 0,
				failedTests: 0,
				allPassed: false,
				totalDurationMs: performance.now() - start,
				results: [],
				rawOutput: error,
				error,
				isSample: Boolean(sampleLimit)
			};
			this.consoleError.set(true);
			this.consoleOutput.set(error);
			this.testResults.set(result);
			return result;
		} finally {
			this.isRunning.set(false);
			if (this.worker) this.runtimeState.set('ready');
		}
	}
}

export const cudaService = new CudaService();
