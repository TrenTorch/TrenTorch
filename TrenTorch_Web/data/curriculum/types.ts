// Generic content shape for the shared IDE. Sourced from
// data/curriculum/generated-curriculum.json, itself compiled by
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

// A canvas question is a real free-form node-and-wire graph, built on
// @xyflow/svelte: drag palette entries onto an open canvas to create
// nodes anywhere, drag nodes freely, connect them by dragging from one
// node's handle to another's. No code, no Pyodide.
export interface CanvasNodeSpec {
	id: string; // stable id -- referenced by requiredEdges below
	label: string;
	subtitle?: string;
	icon?: string; // lucide icon name, e.g. "Database" -- see CanvasNode.svelte's icon map
	position: { x: number; y: number };
}

export interface CanvasPaletteEntry {
	type: string; // referenced by requiredEdges as "type:<this>" -- see below
	label: string;
	subtitle?: string;
	icon?: string;
	groupLabel: string; // palette section header, e.g. "DATA"
}

export interface CanvasSpec {
	// Pre-placed, fixed nodes already on the canvas when the question
	// loads (can be moved and wired, but always exist -- typically the
	// start/end anchors of a pipeline).
	fixedNodes: CanvasNodeSpec[];
	// Draggable palette entries the student drops onto the canvas to
	// create new nodes.
	palette: CanvasPaletteEntry[];
	// Required edges for a correct solution. Each endpoint is either a
	// fixed node's `id` (exact node, e.g. "start") or a palette entry's
	// `type` prefixed with "type:" (matches ANY node the student created
	// from that palette entry, e.g. "type:batch_source") -- since a
	// palette entry can be dropped more than once, grading only cares
	// that *some* node of that type has the required connection.
	requiredEdges: { from: string; to: string }[];
	// Edges that must NOT exist for a correct solution (same endpoint
	// rules as requiredEdges) -- for questions where the lesson is
	// specifically about NOT over-connecting something (e.g. least-
	// privilege: a read-only role must never gain a write permission),
	// which requiredEdges alone can't express since it only ever checks
	// for presence, never absence. Optional; defaults to none.
	forbiddenEdges?: { from: string; to: string }[];
}

export interface QuestionContent {
	id: string; // == metadata.name
	metadata: QuestionMetadata;
	type: 'code' | 'canvas';
	descriptionMarkdown: string; // Description tab: what we're doing and how, not spoonfed
	theoryMarkdown: string; // Theory tab: what/why/how/when, pros/cons, scaling
	starterCode: string; // the function signature(s), extracted from the description's own code fence -- authors don't write a separate stub
	solutionCode: string; // Solution tab: revealed on demand, hidden again on tab switch
	explanationMarkdown: string; // shown alongside the solution once revealed: why it's written this specific way
	testHarnessCode: string; // hidden test suite -- never rendered in the UI
	canvasSpec?: CanvasSpec; // present iff type === 'canvas'
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

export interface ExecutionResult {
	success: boolean;
	output: string;
	error?: string;
	durationMs: number;
}
