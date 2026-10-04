import { writable, type Writable } from 'svelte/store';
import type { ExecutionResult, RuntimeState, SubmissionResult } from '$data/curriculum/types';

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

			const id = ++this.requestId;
			this.worker.postMessage({ id, action: 'init' });
		} catch (err) {
			console.error('Failed to instantiate SQL worker', err);
			this.runtimeState.set('error');
		}
	}

	public async runQuery(query: string, dbSchema?: string): Promise<ExecutionResult> {
		this.init();
		this.isRunning.set(true);
		this.consoleError.set(false);
		this.consoleOutput.set('Executing SQL query in Web Worker...\n');

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.has(id)) {
					this.pendingRequests.delete(id);
					this.isRunning.set(false);
					this.consoleOutput.set('[Timeout]: SQL execution exceeded 20 seconds.');
					reject(new Error('SQL execution timed out'));
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
				query,
				dbSchema
			});
		});
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
		this.consoleOutput.set(`Running SQL tests for [${contentId}]...\n`);

		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.has(id)) {
					this.pendingRequests.delete(id);
					this.isRunning.set(false);
					this.consoleOutput.set('[Timeout]: SQL tests exceeded 25 seconds.');
					reject(new Error('SQL test execution timed out'));
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
				query,
				testCode,
				dbSchema,
				contentId
			});
		});
	}
}

export const sqlService = new SqlService();
