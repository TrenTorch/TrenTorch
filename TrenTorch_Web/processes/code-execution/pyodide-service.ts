import { writable, type Writable } from 'svelte/store';
import type { ExecutionResult, RuntimeState, SubmissionResult } from '$data/curriculum/types';
import { sanitizeStudentCode } from './sanitize-student-code';

/* eslint-disable @typescript-eslint/no-explicit-any */

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

	public runtimeState: Writable<RuntimeState> = writable('uninitialized');
	public consoleOutput: Writable<string> = writable('');
	public testResults: Writable<SubmissionResult | null> = writable(null);
	public isRunning: Writable<boolean> = writable(false);

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
					this.runtimeState.set(status as RuntimeState);
					return;
				}

				if (type === 'run_result') {
					this.isRunning.set(false);
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const formattedOut = (output || '') + (error ? `\n\nTraceback:\n${error}` : '');
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

				if (type === 'test_result') {
					this.isRunning.set(false);
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

	public async runCode(code: string): Promise<ExecutionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleOutput.set('Executing Python code in Web Worker...\n');

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.has(id)) {
					this.pendingRequests.delete(id);
					this.isRunning.set(false);
					this.consoleOutput.set(
						'[Timeout]: Execution exceeded 20 seconds. Terminating execution.'
					);
					reject(new Error('Execution timed out'));
				}
			}, 20000);

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

	public async runTests(
		code: string,
		testHarnessCode: string,
		contentId: string,
		sampleLimit?: number
	): Promise<SubmissionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleOutput.set(
			sampleLimit
				? `Running the first ${sampleLimit} checks for [${contentId}]...\n`
				: `Running test suite for [${contentId}]...\n`
		);

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.has(id)) {
					this.pendingRequests.delete(id);
					this.isRunning.set(false);
					this.consoleOutput.set('[Timeout]: Test suite exceeded 25 seconds.');
					reject(new Error('Test execution timed out'));
				}
			}, 25000);

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
}

export const pyodideService = new PyodideService();
