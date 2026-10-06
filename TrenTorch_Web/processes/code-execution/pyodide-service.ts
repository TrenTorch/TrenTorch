import { writable, type Writable } from 'svelte/store';
import type {
	ExecutionResult,
	PreviewFigure,
	RuntimeState,
	SubmissionResult
} from '$data/curriculum/types';
import { sanitizeStudentCode } from './sanitize-student-code';

/* eslint-disable @typescript-eslint/no-explicit-any */

const RUN_LIMIT_MS = 20_000;
const TEST_LIMIT_MS = 25_000;
const PREVIEW_LIMIT_MS = 30_000;
const STARTUP_ALLOWANCE_MS = 180_000;

// Single cohesive class, kept as one file rather than split further: its
// methods share private state (worker, pendingRequests, requestId) via
// `this`, so pulling them into separate files would either break that
// encapsulation or require passing the whole instance around anyway.
class PyodideService {
	private worker: Worker | null = null;
	private requestId = 0;
	private pendingRequests = new Map<
		number,
		{ resolve: (val: any) => void; reject: (err: any) => void }
	>();

	// The request being timed, if any. See dispatch().
	private watchdog: {
		id: number;
		limitMs: number;
		onTimeout: () => void;
		timer: ReturnType<typeof setTimeout>;
	} | null = null;

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
					this.updateWatchdog(status);
					this.runtimeState.set(status as RuntimeState);
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
				this.runtimeState.set('error');
				this.isRunning.set(false);
			};

			// Send init message
			const id = ++this.requestId;
			this.worker.postMessage({ id, action: 'init' });
		} catch (err) {
			console.error('Failed to instantiate Pyodide worker', err);
			this.runtimeState.set('error');
		}
	}

	// Sends one request to the worker and settles when it answers.
	//
	// The time limit only counts while Python is actually executing: the worker
	// reports 'loading_packages' while it downloads what the code imports (the
	// clock stops) and 'running' or 'testing' once execution starts (it starts).
	// Until the first of those arrives a long startup allowance applies, which
	// covers loading the runtime on a slow connection.
	//
	// Hitting the limit means Python is stuck (typically `while True:`), and a
	// worker stuck in Python cannot be interrupted, so it is thrown away and a
	// fresh one started. Merely abandoning the request would leave every later
	// Run waiting behind the loop forever.
	private dispatch<T>(
		message: Record<string, unknown>,
		limitMs: number,
		onTimeout: () => string
	): Promise<T> {
		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const clear = () => {
				if (this.watchdog?.id === id) {
					clearTimeout(this.watchdog.timer);
					this.watchdog = null;
				}
			};
			const timedOut = () => {
				const text = onTimeout();
				this.restartWorker(text);
				reject(new Error(text));
			};
			this.pendingRequests.set(id, {
				resolve: (value) => {
					clear();
					resolve(value);
				},
				reject: (error) => {
					clear();
					reject(error);
				}
			});
			this.watchdog = {
				id,
				limitMs,
				onTimeout: timedOut,
				timer: setTimeout(timedOut, STARTUP_ALLOWANCE_MS)
			};
			this.worker?.postMessage({ id, ...message });
		});
	}

	// Called on the worker's progress messages. See dispatch().
	private updateWatchdog(status: string) {
		const watchdog = this.watchdog;
		if (!watchdog) return;
		if (status === 'loading_packages') {
			clearTimeout(watchdog.timer);
		} else if (status === 'running' || status === 'testing') {
			clearTimeout(watchdog.timer);
			watchdog.timer = setTimeout(watchdog.onTimeout, watchdog.limitMs);
		}
	}

	private restartWorker(reason: string) {
		if (this.watchdog) {
			clearTimeout(this.watchdog.timer);
			this.watchdog = null;
		}
		this.worker?.terminate();
		this.worker = null;
		for (const request of this.pendingRequests.values()) request.reject(new Error(reason));
		this.pendingRequests.clear();
		this.isRunning.set(false);
		this.consoleError.set(true);
		this.consoleOutput.set(reason);
		this.init();
	}

	public async runCode(code: string): Promise<ExecutionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set('Executing Python code in Web Worker...\n');
		return this.dispatch<ExecutionResult>(
			{ action: 'run', code: sanitizeStudentCode(code) },
			RUN_LIMIT_MS,
			() =>
				`[Timeout]: Your code ran for more than ${RUN_LIMIT_MS / 1000} seconds and was stopped. ` +
				'Check for a loop that never ends.'
		);
	}

	public async runCustomTest(
		code: string,
		testHarnessCode: string,
		contentId: string,
		functionName: string,
		argumentsJson: string,
		expectedJson: string
	): Promise<ExecutionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set(`Running custom input for [${contentId}]...\n`);
		return this.dispatch<ExecutionResult>(
			{
				action: 'custom',
				code: sanitizeStudentCode(code),
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			},
			RUN_LIMIT_MS,
			() =>
				`[Timeout]: Your function ran for more than ${RUN_LIMIT_MS / 1000} seconds and was stopped. ` +
				'Check for a loop that never ends.'
		);
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
		this.init();
		this.isRunning.set(true);
		this.consoleFigures.set([]);
		try {
			return await this.dispatch<{ output: string; error?: string; figures: PreviewFigure[] }>(
				{ action: 'preview', code, previewCode },
				PREVIEW_LIMIT_MS,
				() => `The preview ran for more than ${PREVIEW_LIMIT_MS / 1000} seconds and was stopped.`
			);
		} catch (err: any) {
			return { output: '', error: String(err?.message ?? err), figures: [] };
		}
	}

	public async runTests(
		code: string,
		testHarnessCode: string,
		contentId: string,
		sampleLimit?: number
	): Promise<SubmissionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set(
			sampleLimit
				? `Running the first ${sampleLimit} checks for [${contentId}]...\n`
				: `Running test suite for [${contentId}]...\n`
		);
		return this.dispatch<SubmissionResult>(
			{
				action: 'test',
				code: sanitizeStudentCode(code),
				testHarnessCode,
				contentId,
				sampleLimit
			},
			TEST_LIMIT_MS,
			() =>
				`[Timeout]: The tests ran for more than ${TEST_LIMIT_MS / 1000} seconds and were stopped. ` +
				'Check for a loop that never ends.'
		);
	}
}

export const pyodideService = new PyodideService();
