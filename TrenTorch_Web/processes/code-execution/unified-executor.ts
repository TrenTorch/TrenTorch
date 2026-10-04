import { writable, type Writable } from 'svelte/store';
import type {
	ExecutionResult,
	RuntimeState,
	SubmissionResult,
	QuestionContent
} from '$data/curriculum/types';
import { pyodideService } from './pyodide-service';
import { sqlService } from './sql-service';
import { detectLanguage, type Language } from './detect-language';

class UnifiedExecutor {
	// Stable stores: the IDE page grabs these once, so they must not be swapped
	// out when the language changes. Whichever runtime is active forwards its
	// values into them (see bind()).
	public runtimeState: Writable<RuntimeState> = writable('uninitialized');
	public consoleOutput: Writable<string> = writable('');
	public consoleError: Writable<boolean> = writable(false);
	public testResults: Writable<SubmissionResult | null> = writable(null);
	public isRunning: Writable<boolean> = writable(false);

	private language: Language = 'python';
	private unbind: Array<() => void> = [];

	constructor() {
		this.bind(pyodideService);
	}

	private bind(service: typeof pyodideService | typeof sqlService): void {
		this.unbind.forEach((stop) => stop());
		this.unbind = [
			service.runtimeState.subscribe((v) => this.runtimeState.set(v)),
			service.consoleOutput.subscribe((v) => this.consoleOutput.set(v)),
			service.consoleError.subscribe((v) => this.consoleError.set(v)),
			service.testResults.subscribe((v) => this.testResults.set(v)),
			service.isRunning.subscribe((v) => this.isRunning.set(v))
		];
	}

	public init(content: QuestionContent | null): void {
		if (!content) return;
		const next = detectLanguage(content);
		if (next !== this.language || next === 'sql') {
			this.language = next;
			this.bind(next === 'sql' ? sqlService : pyodideService);
		}
		// Warm the SQL runtime early (it is small); Python keeps loading on first Run.
		if (next === 'sql') sqlService.init();
	}

	public async runCode(code: string, dbSchema?: string): Promise<ExecutionResult> {
		if (this.language === 'sql') {
			return sqlService.runQuery(code, dbSchema);
		}
		return pyodideService.runCode(code);
	}

	public async runTests(
		code: string,
		testHarnessCode: string,
		contentId: string,
		sampleLimit?: number,
		dbSchema?: string
	): Promise<SubmissionResult> {
		if (this.language === 'sql') {
			return sqlService.runTests(code, testHarnessCode, dbSchema || '', contentId);
		}
		return pyodideService.runTests(code, testHarnessCode, contentId, sampleLimit);
	}

	public async runCustomTest(
		code: string,
		testHarnessCode: string,
		contentId: string,
		functionName: string,
		argumentsJson: string,
		expectedJson: string
	): Promise<ExecutionResult> {
		if (this.language === 'sql') {
			// SQL doesn't have custom test mode yet
			return {
				success: false,
				output: '',
				error: 'Custom tests not supported for SQL',
				durationMs: 0
			};
		}
		return pyodideService.runCustomTest(
			code,
			testHarnessCode,
			contentId,
			functionName,
			argumentsJson,
			expectedJson
		);
	}
}

export const unifiedExecutor = new UnifiedExecutor();
