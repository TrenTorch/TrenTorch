// Generic content shape for the shared IDE. Sourced from
// src/lib/curriculum/generated-curriculum.json, itself compiled by
// scripts/build-curriculum.mjs from the real, individually-runnable
// files authored under data/<section>/<track>/<NN-question>/ (see
// data/README.md). The IDE itself has no idea whether that content is a
// whole CLI module or a single granular question, it just runs whatever
// it's handed.

export interface QuestionMetadata {
	name: string; // == the compiled question's id, e.g. "linear-regression-hypothesis-function"
	title: string;
	tags: string[];
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced' | 'Mastery';
}

export interface QuestionContent {
	id: string; // == metadata.name
	metadata: QuestionMetadata;
	descriptionMarkdown: string; // Description tab: what we're doing and how, not spoonfed
	theoryMarkdown: string; // Theory tab: what/why/how/when, pros/cons, scaling
	starterCode: string; // the function signature(s), extracted from the description's own code fence -- authors don't write a separate stub
	solutionCode: string; // Solution tab: revealed on demand, hidden again on tab switch
	explanationMarkdown: string; // shown alongside the solution once revealed: why it's written this specific way
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
