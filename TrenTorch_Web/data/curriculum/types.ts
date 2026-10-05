// Generic content shape for the shared IDE. Sourced from the compiled
// virtual:curriculum/bundle (see bundle-types.ts), compiled in memory by
// processes/curriculum-build/build.mjs from the real, individually-runnable
// files authored under data/app_data/<section>/<track>/<NN-question>/
// (see data/app_data/README.md). The IDE itself has no idea whether that
// content is a whole CLI module or a single granular question, it just
// runs whatever it's handed.

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
	dbSchema?: string; // SQL questions only: CREATE/INSERT statements loaded into a fresh SQLite database for every run
	solutionCode: string; // Solution tab: revealed on demand, hidden again on tab switch
	explanationMarkdown: string; // shown alongside the solution once revealed: why it's written this specific way
	testHarnessCode: string; // hidden test suite -- never rendered in the UI
	previewCode?: string; // optional Python run after the student's code on Run: calls their function on example data and show()s the result (see build-preview-script.ts)
	widgetId?: string; // optional client-side widget (platform/widgets/) mounted in the Theory tab
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
	// True when this came from the "Run" button (first couple of visible
	// checks only, no solved/attempted side effects), false/undefined for a
	// full "Submit" against the hidden suite.
	isSample?: boolean;
}

export type RuntimeState =
	| 'uninitialized'
	| 'loading_runtime'
	| 'loading_packages'
	| 'ready'
	| 'running'
	| 'testing'
	| 'error';

// A chart produced by a question's preview: a matplotlib/seaborn figure as a PNG
// (base64), or a plotly figure as JSON that the page draws interactively.
export type PreviewFigure = { kind: 'png'; data: string } | { kind: 'plotly'; json: string };

export interface ExecutionResult {
	success: boolean;
	output: string;
	error?: string;
	durationMs: number;
}
