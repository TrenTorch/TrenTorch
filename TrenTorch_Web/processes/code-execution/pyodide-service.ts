import { writable, type Writable } from 'svelte/store';
import type {
	ExecutionResult,
	PreviewFigure,
	RuntimeState,
	SubmissionResult
} from '$data/curriculum/types';
import { sanitizeStudentCode } from './sanitize-student-code';
import type { ExternalJudgement, ExternalOutputs, ExternalPlan } from './external-protocol';

/* eslint-disable @typescript-eslint/no-explicit-any */

// Single cohesive class, kept as one file rather than split further: its
// methods share private state (worker, pendingRequests, requestId) via
// `this`, so pulling them into separate files would either break that
// encapsulation or require passing the whole instance around anyway.
const LOAD_TIMEOUT_MS = 120_000;

class PyodideService {
	private worker: Worker | null = null;
	private requestId = 0;
	private pendingRequests = new Map<
		number,
		{ resolve: (val: any) => void; reject: (err: any) => void }
	>();

	// Settles once the worker has loaded Pyodide and NumPy; a request's own timeout only starts
	// after this, so a slow download is never mistaken for a hung program.
	private ready: Promise<void> | null = null;
	private settleReady: { resolve: () => void; reject: (err: Error) => void } | null = null;
	private initId = 0;
	private loadTimer: ReturnType<typeof setTimeout> | undefined;

	public runtimeState: Writable<RuntimeState> = writable('uninitialized');
	public consoleOutput: Writable<string> = writable('');
	public consoleError: Writable<boolean> = writable(false);
	public testResults: Writable<SubmissionResult | null> = writable(null);
	public isRunning: Writable<boolean> = writable(false);
	// Charts drawn by the question's preview (see build-preview-script.ts).
	public consoleFigures: Writable<PreviewFigure[]> = writable([]);

	public init(): void {
		if (typeof window === 'undefined' || this.worker) return;

		try {
			this.runtimeState.set('loading_runtime');
			this.worker = new Worker(new URL('./pyodide-worker.ts', import.meta.url), {
				type: 'module'
			});

			this.worker.onmessage = (e: MessageEvent) => {
				const { id, type, status, output, error, success, durationMs, ...rest } = e.data;

				if (type === 'status') {
					// A stray status from a worker we already replaced must not touch the UI.
					if (e.target === this.worker) this.runtimeState.set(status as RuntimeState);
					return;
				}

				if (id === this.initId && (type === 'init_complete' || type === 'error')) {
					if (type === 'error') {
						this.failInit(`The Python runtime could not be loaded: ${error}`);
					} else {
						clearTimeout(this.loadTimer);
						this.settleReady?.resolve();
						this.settleReady = null;
					}
					return;
				}

				if (type === 'run_result') {
					this.isRunning.set(false);
					this.consoleError.set(Boolean(error));
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const formattedOut = [output || '', error || ''].filter(Boolean).join('\n\n');
						this.consoleOutput.set(formattedOut);
						req.resolve({
							success: Boolean(success),
							output: formattedOut,
							error,
							durationMs
						} as ExecutionResult);
					}
					return;
				}

				if (type === 'preview_result') {
					this.isRunning.set(false);
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const figures = (rest.figures || []) as PreviewFigure[];
						this.consoleFigures.set(figures);
						req.resolve({ output: output || '', error, figures });
					}
					return;
				}

				if (type === 'test_result') {
					this.isRunning.set(false);
					this.consoleError.set(Boolean(error));
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const subResult: SubmissionResult = {
							contentId: rest.contentId,
							totalTests: rest.totalTests,
							passedTests: rest.passedTests,
							failedTests: rest.failedTests,
							allPassed: rest.allPassed,
							totalDurationMs: rest.totalDurationMs,
							results: rest.results || [],
							rawOutput: rest.rawOutput || '',
							// `error` is destructured out of e.data above, so it is
							// NOT in `rest` -- reading rest.error here silently
							// dropped every harness/exec traceback, leaving the UI
							// stuck on "Running test suite..." with a bare "0/0" and
							// nothing below it.
							error: error || undefined,
							isSample: Boolean(rest.isSample)
						};
						this.testResults.set(subResult);
						// Make the console reflect the outcome instead of freezing
						// on the "Running..." line: the traceback when the run blew
						// up before any test could execute, otherwise the run's own
						// stdout (or a short summary if it printed nothing).
						if (error) {
							this.consoleOutput.set(`Run failed before the tests could execute:\n\n${error}`);
						} else if (subResult.rawOutput.trim()) {
							this.consoleOutput.set(subResult.rawOutput);
						} else {
							this.consoleOutput.set(
								`${subResult.passedTests}/${subResult.totalTests} checks passed.`
							);
						}
						// Marking a question solved (and reflecting that back on the
						// Questions list) is the caller's job -- see +page.svelte's
						// handleRunTests, which owns the `solved` store this service
						// doesn't know about.
						req.resolve(subResult);
					}
					return;
				}

				if (type === 'external_prepared' || type === 'external_judged') {
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						req.resolve({ error, ...rest });
					}
					return;
				}

				if (type === 'error') {
					this.isRunning.set(false);
					this.consoleError.set(true);
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						req.reject(new Error(error));
					}
					this.consoleOutput.update((prev) => prev + `\n[Error]: ${error}`);
				}
			};

			this.worker.onerror = (err) => {
				console.error('Worker error', err);
				this.failInit('The Python runtime crashed. Reload the page and try again.');
			};

			this.ready = new Promise<void>((resolve, reject) => {
				this.settleReady = { resolve, reject };
			});
			// Whoever awaits `ready` sees the failure; this keeps it from also being reported as unhandled.
			this.ready.catch(() => {});
			this.loadTimer = setTimeout(
				() =>
					this.failInit(
						'The Python runtime took more than 2 minutes to load. Check your connection (cdn.jsdelivr.net must be reachable) and try again.'
					),
				LOAD_TIMEOUT_MS
			);

			// Send init message
			this.initId = ++this.requestId;
			this.worker.postMessage({ id: this.initId, action: 'init' });
		} catch (err) {
			console.error('Failed to instantiate Pyodide worker', err);
			this.runtimeState.set('error');
		}
	}

	// Throws the worker away -- the only way to stop Python code that never returns -- and lets
	// the next request start a fresh one. Every request still waiting is rejected with `reason`.
	private resetWorker(reason: string): void {
		clearTimeout(this.loadTimer);
		this.worker?.terminate();
		this.worker = null;
		this.ready = null;
		this.settleReady = null;
		this.isRunning.set(false);
		const pending = [...this.pendingRequests.values()];
		this.pendingRequests.clear();
		for (const req of pending) req.reject(new Error(reason));
	}

	private failInit(message: string): void {
		const settle = this.settleReady;
		this.runtimeState.set('error');
		this.resetWorker(message);
		settle?.reject(new Error(message));
	}

	// Called when a request outlives its time limit: report it, then restart the runtime so a
	// runaway loop cannot leave every later Run and Submit stuck behind it.
	private expire(id: number, message: string): void {
		const req = this.pendingRequests.get(id);
		if (!req) return;
		this.pendingRequests.delete(id);
		this.consoleError.set(true);
		this.consoleOutput.set(message);
		this.resetWorker('The runtime was restarted after a timeout.');
		this.runtimeState.set('uninitialized');
		req.reject(new Error(message));
	}

	// Starts the runtime if needed and waits until it can take requests. On failure the console
	// says why and the next click starts over, instead of the button spinning forever.
	private async awaitReady(): Promise<void> {
		this.init();
		try {
			await this.ready;
		} catch (err) {
			this.isRunning.set(false);
			this.consoleError.set(true);
			this.consoleOutput.set(`[Error]: ${err instanceof Error ? err.message : String(err)}`);
			throw err;
		}
	}

	public async runCode(code: string): Promise<ExecutionResult> {
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set('Executing Python code in Web Worker...\n');
		await this.awaitReady();

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(
				() =>
					this.expire(
						id,
						'[Timeout]: Execution exceeded 20 seconds. The runtime was restarted; check for an infinite loop.'
					),
				20000
			);

			this.pendingRequests.set(id, {
				resolve: (res) => {
					clearTimeout(timeout);
					resolve(res);
				},
				reject: (err) => {
					clearTimeout(timeout);
					reject(err);
				}
			});

			this.worker?.postMessage({
				id,
				action: 'run',
				code: sanitizeStudentCode(code)
			});
		});
	}

	public async runCustomTest(
		code: string,
		testHarnessCode: string,
		contentId: string,
		functionName: string,
		argumentsJson: string,
		expectedJson: string
	): Promise<ExecutionResult> {
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set(`Running custom input for [${contentId}]...\n`);
		await this.awaitReady();

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(
				() =>
					this.expire(
						id,
						'[Timeout]: Custom run exceeded 20 seconds. The runtime was restarted; check for an infinite loop.'
					),
				20000
			);

			this.pendingRequests.set(id, {
				resolve: (result) => {
					clearTimeout(timeout);
					resolve(result);
				},
				reject: (error) => {
					clearTimeout(timeout);
					reject(error);
				}
			});

			this.worker?.postMessage({
				id,
				action: 'custom',
				code: sanitizeStudentCode(code),
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			});
		});
	}

	/**
	 * Runs the question's preview after the student's code and returns what it printed and
	 * the charts it drew. Unlike runTests this does not touch the console text: the caller
	 * decides where the output goes. A preview that fails reports `error` instead of throwing.
	 */
	public async runPreview(
		code: string,
		previewCode: string
	): Promise<{ output: string; error?: string; figures: PreviewFigure[] }> {
		this.isRunning.set(true);
		this.consoleFigures.set([]);
		try {
			await this.awaitReady();
		} catch (err) {
			return { output: '', error: String((err as Error)?.message ?? err), figures: [] };
		}

		return new Promise((resolve) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				const req = this.pendingRequests.get(id);
				if (!req) return;
				this.pendingRequests.delete(id);
				this.resetWorker('The runtime was restarted after a timeout.');
				this.runtimeState.set('uninitialized');
				resolve({ output: '', error: 'The preview took longer than 30 seconds.', figures: [] });
			}, 30000);

			this.pendingRequests.set(id, {
				resolve: (res) => {
					clearTimeout(timeout);
					resolve(res);
				},
				reject: (err) => {
					clearTimeout(timeout);
					resolve({ output: '', error: String(err?.message ?? err), figures: [] });
				}
			});

			this.worker?.postMessage({ id, action: 'preview', code, previewCode });
		});
	}

	public async runTests(
		code: string,
		testHarnessCode: string,
		contentId: string,
		sampleLimit?: number
	): Promise<SubmissionResult> {
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set(
			sampleLimit
				? `Running the first ${sampleLimit} checks for [${contentId}]...\n`
				: `Running test suite for [${contentId}]...\n`
		);
		await this.awaitReady();

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(
				() =>
					this.expire(
						id,
						'[Timeout]: Test suite exceeded 25 seconds. The runtime was restarted; check for an infinite loop or a very slow solution.'
					),
				25000
			);

			this.pendingRequests.set(id, {
				resolve: (res) => {
					clearTimeout(timeout);
					resolve(res);
				},
				reject: (err) => {
					clearTimeout(timeout);
					reject(err);
				}
			});

			this.worker?.postMessage({
				id,
				action: 'test',
				code: sanitizeStudentCode(code),
				testHarnessCode,
				contentId,
				sampleLimit
			});
		});
	}

	// Python's two parts of judging a submission in another language (see external-protocol.ts). The
	// caller owns the console and the running flag, because the language runs in between.
	private async askExternal<T>(message: Record<string, unknown>, timeoutMs = 60000): Promise<T> {
		await this.awaitReady();
		return new Promise<T>((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				const req = this.pendingRequests.get(id);
				if (!req) return;
				this.pendingRequests.delete(id);
				this.resetWorker('The runtime was restarted after a timeout.');
				this.runtimeState.set('uninitialized');
				req.reject(new Error('Judging timed out'));
			}, timeoutMs);
			this.pendingRequests.set(id, {
				resolve: (res) => {
					clearTimeout(timeout);
					resolve(res);
				},
				reject: (err) => {
					clearTimeout(timeout);
					reject(err);
				}
			});
			this.worker?.postMessage({ id, ...message });
		});
	}

	public prepareExternal(
		testHarnessCode: string,
		maxInt: string,
		sampleLimit?: number
	): Promise<{ plan: ExternalPlan | null; error: string | null }> {
		return this.askExternal({ action: 'external_prepare', testHarnessCode, maxInt, sampleLimit });
	}

	public judgeExternal(
		testHarnessCode: string,
		outputs: ExternalOutputs,
		sampleLimit?: number
	): Promise<ExternalJudgement> {
		return this.askExternal({
			action: 'external_judge',
			testHarnessCode,
			outputsJson: JSON.stringify(outputs),
			sampleLimit
		});
	}
}

export const pyodideService = new PyodideService();
