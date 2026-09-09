// Generic content shape for the shared IDE. One folder under
// src/lib/data/ide-content/<name>/ describes one question -- metadata.json
// (name/title/tags/difficulty) plus separate description.md, theory.md,
// starter.py, solution.py and tests.py files, authored as real Markdown
// and Python rather than JSON-escaped strings. The IDE itself has no idea
// whether that content is a whole CLI module or a single granular
// question, it just runs whatever it's handed.

export interface QuestionMetadata {
	name: string; // matches the folder name, e.g. "tensor-foundation"
	title: string;
	tags: string[];
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced' | 'Mastery';
}

export interface QuestionContent {
	id: string; // == metadata.name
	metadata: QuestionMetadata;
	descriptionMarkdown: string; // Description tab: what we're doing and how, not spoonfed
	theoryMarkdown: string; // Theory tab: what/why/how/when, pros/cons, scaling
	starterCode: string;
	solutionCode: string; // Solution tab: revealed on demand, hidden again on tab switch
	testHarnessCode: string; // hidden test suite -- never rendered in the UI
}

export interface SingleTestResult {
	name: string;
	passed: boolean;
	durationMs: number;
	error?: string;
	expected?: string;
	actual?: string;
	stdout?: string;
}

export interface SubmissionResult {
	contentId: string;
	totalTests: number;
	passedTests: number;
	failedTests: number;
	allPassed: boolean;
	totalDurationMs: number;
	results: SingleTestResult[];
	rawOutput: string;
	error?: string;
}

export type RuntimeState =
	| 'uninitialized'
	| 'loading_runtime'
	| 'loading_packages'
	| 'ready'
	| 'running'
	| 'testing'
	| 'error';

export interface ExecutionResult {
	success: boolean;
	output: string;
	error?: string;
	durationMs: number;
}
