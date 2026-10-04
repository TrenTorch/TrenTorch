import { writable, type Writable } from 'svelte/store';
import type { ExecutionResult, RuntimeState, SubmissionResult, QuestionContent } from '$data/curriculum/types';
import { pyodideService } from './pyodide-service';
import { sqlService } from './sql-service';
import { detectLanguage, type Language } from './detect-language';

class UnifiedExecutor {
	public runtimeState: Writable<RuntimeState>;
	public consoleOutput: Writable<string>;
	public consoleError: Writable<boolean>;
	public testResults: Writable<SubmissionResult | null>;
	public isRunning: Writable<boolean>;

	private language: Language = 'python';

	constructor() {
		// Default to Python service's stores
		this.runtimeState = pyodideService.runtimeState;
		this.consoleOutput = pyodideService.consoleOutput;
		this.consoleError = pyodideService.consoleError;
		this.testResults = pyodideService.testResults;
		this.isRunning = pyodideService.isRunning;
	}

	public init(content: QuestionContent | null): void {
		if (content) {
			this.language = detectLanguage(content);
			if (this.language === 'sql') {
				sqlService.init();
				// Switch stores to SQL service
				this.runtimeState = sqlService.runtimeState;
				this.consoleOutput = sqlService.consoleOutput;
				this.consoleError = sqlService.consoleError;
				this.testResults = sqlService.testResults;
				this.isRunning = sqlService.isRunning;
			} else {
				pyodideService.init();
				// Switch stores to Python service
				this.runtimeState = pyodideService.runtimeState;
				this.consoleOutput = pyodideService.consoleOutput;
				this.consoleError = pyodideService.consoleError;
				this.testResults = pyodideService.testResults;
				this.isRunning = pyodideService.isRunning;
			}
		}
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
