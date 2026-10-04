import { writable, type Writable } from 'svelte/store';
import type { ExecutionResult, RuntimeState, SubmissionResult } from '$data/curriculum/types';

/* eslint-disable @typescript-eslint/no-explicit-any */

// Talks to sql-worker.ts. Same store surface as PyodideService so the IDE page
// can treat both runtimes alike (see unified-executor.ts).
class SqlService {
	private worker: Worker | null = null;
	private requestId = 0;
	private pendingRequests = new Map<
		number,
		{ resolve: (val: any) => void; reject: (err: any) => void }
	>();

	public runtimeState: Writable<RuntimeState> = writable('uninitialized');
	public consoleOutput: Writable<string> = writable('');
	public consoleError: Writable<boolean> = writable(false);
	public testResults: Writable<SubmissionResult | null> = writable(null);
	public isRunning: Writable<boolean> = writable(false);

	public init(): void {
		if (typeof window === 'undefined' || this.worker) return;

		try {
			this.runtimeState.set('loading_runtime');
			this.worker = new Worker(new URL('./sql-worker.ts', import.meta.url), {
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
					this.consoleError.set(Boolean(error));
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const formatted = [output || '', error || ''].filter(Boolean).join('\n\n');
						this.consoleOutput.set(formatted);
						req.resolve({
							success: Boolean(success),
							output: formatted,
							error,
							durationMs
						} as ExecutionResult);
					}
					return;
				}

				if (type === 'test_result') {
					this.isRunning.set(false);
					this.consoleError.set(Boolean(error));
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const result: SubmissionResult = {
							contentId: rest.contentId,
							totalTests: rest.totalTests,
							passedTests: rest.passedTests,
							failedTests: rest.failedTests,
							allPassed: rest.allPassed,
							totalDurationMs: rest.totalDurationMs,
							results: rest.results || [],
							rawOutput: rest.rawOutput || '',
							error: error || undefined,
							isSample: false
						};
						this.testResults.set(result);
						this.consoleOutput.set(
							error
								? `Run failed before the tests could execute:\n\n${error}`
								: result.rawOutput || `${result.passedTests}/${result.totalTests} checks passed.`
						);
						req.resolve(result);
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

			this.worker.postMessage({ id: ++this.requestId, action: 'init' });
		} catch (err) {
			console.error('Failed to instantiate SQL worker', err);
			this.runtimeState.set('error');
		}
	}

	private request<T>(
		message: Record<string, unknown>,
		timeoutMs: number,
		label: string
	): Promise<T> {
		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.delete(id)) {
					this.isRunning.set(false);
					this.consoleError.set(true);
					this.consoleOutput.set(`[Timeout]: ${label} exceeded ${timeoutMs / 1000} seconds.`);
					reject(new Error(`${label} timed out`));
				}
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

	public async runQuery(query: string, dbSchema?: string): Promise<ExecutionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set('Running query…\n');
		return this.request<ExecutionResult>(
			{ action: 'run', query, dbSchema: dbSchema ?? '' },
			// First use also downloads the SQLite runtime, hence the generous limit.
			60000,
			'SQL execution'
		);
	}

	public async runTests(
		query: string,
		testCode: string,
		dbSchema: string,
		contentId: string
	): Promise<SubmissionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set(`Running SQL tests for [${contentId}]…\n`);
		return this.request<SubmissionResult>(
			{ action: 'test', query, testCode, dbSchema, contentId },
			60000,
			'SQL tests'
		);
	}
}

export const sqlService = new SqlService();
