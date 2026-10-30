// Shape of the IDE bundle served by the virtual:curriculum/bundle module
// (compiled in memory by processes/curriculum-build/build.mjs, never written
// to disk). Consumers import the types from here; the module declaration
// lives in processes/curriculum-build/virtual-curriculum.d.ts.
import type { QuestionMetadata } from './types';

// What the Problemset list reads from a question (virtual:curriculum/problemset).
export type ProblemsetSource = Pick<
	GeneratedQuestion,
	'id' | 'title' | 'difficulty' | 'order' | 'relatedModule' | 'topic' | 'caseCompany' | 'tools'
>;

// The DSA sheet as /dsa shows it (virtual:curriculum/dsa-sheet): steps, topics and question titles only.
export interface DsaSheetQuestion {
	id: string;
	title: string;
	difficulty: QuestionMetadata['difficulty'];
	tags: string[];
}
export interface DsaSheetTopic {
	id: string;
	title: string;
	description?: string;
	questions: DsaSheetQuestion[];
}
export interface DsaSheetStep {
	id: string;
	title: string;
	// The step has a theory page (/dsa/theory/<id>).
	hasTheory: boolean;
	topics: DsaSheetTopic[];
}
export interface DsaSheet {
	title: string;
	steps: DsaSheetStep[];
}

export interface DsaSignature {
	name: string;
	params: { name: string; type: string }[];
	returns: string;
	example?: Record<string, unknown>;
}

export interface GeneratedQuestion {
	id: string;
	title: string;
	tags: string[];
	difficulty: QuestionMetadata['difficulty'];
	// Problemset fields: set only on questions authored for the Problemset page.
	kind?: QuestionMetadata['kind'];
	caseCompany?: string;
	relatedModule?: QuestionMetadata['relatedModule'];
	hint?: string;
	// DSA sheet: up to four hints, shown one at a time (from problem.json).
	hints?: string[];
	// DSA sheet: the function's signature and its first example input, from problem.json. The IDE
	// writes the starter code for every language but Python from it (build-language-starters.ts).
	signature?: DsaSignature;
	// DSA sheet: further reading, shown under the keywords (from references.json).
	references?: { title: string; url: string }[];
	// DSA sheet: the step's theory page and the heading anchor to link to.
	theory?: { step: string; anchor: string };
	tools?: string[];
	topic?: string;
	root: string;
	section: string;
	track: string;
	order: number;
	statementMarkdown: string;
	theoryMarkdown: string;
	// Hand-authored student stub (data/<...>/starter.py). Optional: older
	// questions don't have one and fall back to a signature derived from
	// the statement fence. See extractStarterCode.
	starterCode?: string;
	// Optional example run shown after Run (data/<...>/preview.py). See build-preview-script.ts.
	previewCode?: string;
	oracleSolutionCode: string;
	// DSA sheet: the solution in the languages other than Python, from solution.<ext> next to solution.py.
	languageSolutions?: Partial<Record<'javascript' | 'cpp' | 'java' | 'go' | 'rust', string>>;
	oracleExplanationMarkdown: string;
	testsCode: string;
	// Optional id of a client-side widget (platform/widgets/) to mount in
	// the Theory tab. See README.md frontmatter's `widget` field.
	widgetId?: string;
}

export interface GeneratedTrack {
	id: string;
	questions: GeneratedQuestion[];
}

export interface GeneratedSection {
	id: string;
	tracks: GeneratedTrack[];
}

export interface GeneratedRoot {
	id: string;
	sections: GeneratedSection[];
}

export interface CurriculumBundle {
	roots: GeneratedRoot[];
}
