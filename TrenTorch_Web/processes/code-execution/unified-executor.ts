import { writable, type Writable } from 'svelte/store';
import type {
	ExecutionResult,
	PreviewFigure,
	RuntimeState,
	SubmissionResult,
	QuestionContent
} from '$data/curriculum/types';
import { pyodideService } from './pyodide-service';
import { sqlService } from './sql-service';
import { jsService } from './js-service';
import { cppService } from './cpp-service';
import { javaService } from './java-service';
import { goService } from './go-service';
import { rustService } from './rust-service';
import { cudaService } from './cuda-service';
import { detectLanguage, type Language } from './detect-language';

type Service =
	| typeof pyodideService
	| typeof sqlService
	| typeof jsService
	| typeof cppService
	| typeof javaService
	| typeof goService
	| typeof rustService
	| typeof cudaService;

function serviceFor(language: Language): Service {
	switch (language) {
		case 'sql':
			return sqlService;
		case 'javascript':
			return jsService;
		case 'cpp':
			return cppService;
		case 'java':
			return javaService;
		case 'go':
			return goService;
		case 'rust':
			return rustService;
		case 'cuda':
			return cudaService;
		default:
			return pyodideService;
	}
}

class UnifiedExecutor {
	// Stable stores: the IDE page grabs these once, so they must not be swapped
	// out when the language changes. Whichever runtime is active forwards its
	// values into them (see bind()).
	public runtimeState: Writable<RuntimeState> = writable('uninitialized');
	public consoleOutput: Writable<string> = writable('');
	public consoleError: Writable<boolean> = writable(false);
	public testResults: Writable<SubmissionResult | null> = writable(null);
	public isRunning: Writable<boolean> = writable(false);
	public consoleFigures: Writable<PreviewFigure[]> = writable([]);

	private language: Language = 'python';
	private unbind: Array<() => void> = [];

	constructor() {
		this.bind(pyodideService);
	}

	private bind(service: Service): void {
		this.unbind.forEach((stop) => stop());
		this.unbind = [
			service.runtimeState.subscribe((v) => this.runtimeState.set(v)),
			service.consoleOutput.subscribe((v) => this.consoleOutput.set(v)),
			service.consoleError.subscribe((v) => this.consoleError.set(v)),
			service.testResults.subscribe((v) => this.testResults.set(v)),
			service.isRunning.subscribe((v) => this.isRunning.set(v)),
			service.consoleFigures.subscribe((v) => this.consoleFigures.set(v))
		];
	}

	public init(content: QuestionContent | null): void {
		if (!content) return;
		const next = detectLanguage(content);
		if (next !== this.language || next === 'sql') {
			this.language = next;
			this.bind(serviceFor(next));
		}
		// Warm the SQL runtime early (it is small); Python/JS/C++ keep loading on first Run.
		if (next === 'sql') sqlService.init();
	}

	/** Lets the IDE page override the auto-detected language for DSA questions, where the
	 *  student picks Python/JavaScript/C++ from a dropdown rather than it being content-derived. */
	public setLanguage(language: Language): void {
		if (language === this.language) return;
		this.language = language;
		const service = serviceFor(language);
		this.bind(service);
		// Start fetching the runtime and its packages now, so the first Run is not the one that waits.
		service.init();
	}

	public getLanguage(): Language {
		return this.language;
	}

	public async runCode(code: string, dbSchema?: string): Promise<ExecutionResult> {
		if (this.language === 'sql') {
			return sqlService.runQuery(code, dbSchema);
		}
		if (this.language === 'javascript') {
			return jsService.runCode(code);
		}
		if (this.language === 'cpp') {
			return cppService.runCode(code);
		}
		if (this.language === 'java') {
			return javaService.runCode(code);
		}
		if (this.language === 'go') {
			return goService.runCode(code);
		}
		if (this.language === 'rust') {
			return rustService.runCode(code);
		}
		if (this.language === 'cuda') {
			return cudaService.runCode(code);
		}
		return pyodideService.runCode(code);
	}

	/** The question's example run, shown after Run. Python only; other languages have nothing to draw. */
	public async runPreview(code: string, previewCode: string) {
		if (this.language !== 'python') return { output: '', figures: [] as PreviewFigure[] };
		return pyodideService.runPreview(code, previewCode);
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
		if (this.language === 'javascript') {
			return jsService.runTests(code, testHarnessCode, contentId, sampleLimit);
		}
		if (this.language === 'cpp') {
			return cppService.runTests(code, testHarnessCode, contentId, sampleLimit);
		}
		if (this.language === 'java') {
			return javaService.runTests(code, testHarnessCode, contentId, sampleLimit);
		}
		if (this.language === 'go') {
			return goService.runTests(code, testHarnessCode, contentId, sampleLimit);
		}
		if (this.language === 'rust') {
			return rustService.runTests(code, testHarnessCode, contentId, sampleLimit);
		}
		if (this.language === 'cuda') {
			return cudaService.runTests(code, testHarnessCode, contentId, sampleLimit);
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
		if (this.language === 'javascript') {
			return jsService.runCustomTest(
				code,
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			);
		}
		if (this.language === 'cpp') {
			return cppService.runCustomTest(
				code,
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			);
		}
		if (this.language === 'java') {
			return javaService.runCustomTest(
				code,
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			);
		}
		if (this.language === 'go') {
			return goService.runCustomTest(
				code,
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			);
		}
		if (this.language === 'rust') {
			return rustService.runCustomTest(
				code,
				testHarnessCode,
				contentId,
				functionName,
				argumentsJson,
				expectedJson
			);
		}
		if (this.language === 'cuda') {
			return {
				success: false,
				output: '',
				error: 'Custom tests are not available for CUDA problems yet',
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
