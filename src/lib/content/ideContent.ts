// Loads IDE content by id from the compiled curriculum -- see
// src/lib/curriculum/generated-curriculum.json and data/README.md for
// where that file comes from (scripts/build-curriculum.mjs, compiled
// from real .py/.md files authored under data/). This module's job is
// just shaping that compiled data into what the IDE actually runs:
// deriving starter code from the problem statement's own signature, and
// turning each question's real pytest-style tests.py into something a
// single Pyodide exec can run standalone (no filesystem, no multi-file
// imports).
import generatedCurriculum from '$lib/curriculum/generated-curriculum.json';
import type { QuestionContent, QuestionMetadata } from '$lib/curriculum/types';

interface GeneratedQuestion {
	id: string;
	title: string;
	tags: string[];
	difficulty: QuestionMetadata['difficulty'];
	section: string;
	track: string;
	folder: string;
	order: number;
	statementMarkdown: string;
	theoryMarkdown: string;
	oracleSolutionCode: string;
	oracleExplanationMarkdown: string;
	testsCode: string;
}

interface GeneratedTrack {
	id: string;
	questions: GeneratedQuestion[];
}

interface GeneratedSection {
	id: string;
	tracks: GeneratedTrack[];
}

const curriculum = generatedCurriculum as { sections: GeneratedSection[] };

// Flat id -> question lookup, and id -> (track-mates, keyed by folder
// name) for resolving a question's cross-question test dependencies --
// see stripLoadSolutionBoilerplate below.
const questionsById = new Map<string, GeneratedQuestion>();
const trackMatesByQuestionId = new Map<string, Map<string, GeneratedQuestion>>();

for (const section of curriculum.sections) {
	for (const track of section.tracks) {
		const byFolder = new Map(track.questions.map((q) => [q.folder, q]));
		for (const question of track.questions) {
			questionsById.set(question.id, question);
			trackMatesByQuestionId.set(question.id, byFolder);
		}
	}
}

// The problem statement always includes the function signature(s) to
// implement as its own fenced code block -- authors write that once,
// here, rather than duplicating it into a separate starter file. This
// pulls that first fence out verbatim (docstring included, no body) as
// the editor's starting content.
//
// The student's code execs standalone, before the test harness (which
// is where `import numpy as np` would otherwise come from) -- and every
// signature here is typed against np.ndarray. On Pyodide's actual
// Python (3.12), a parameter annotation is evaluated the moment `def`
// executes, so without this the very first Run on unmodified starter
// code crashes with NameError before a student writes anything. (This
// only reproduces on the interpreter version Pyodide actually ships --
// Python 3.14 defers annotation evaluation by default and would hide
// the bug entirely; always verify against 3.12 specifically.)
function extractStarterCode(statementMarkdown: string): string {
	const match = statementMarkdown.match(/```python\n([\s\S]*?)```/);
	if (!match) return '';
	return `import numpy as np\n\n\n${match[1].trimEnd()}\n`;
}

// tests.py is real pytest, written to run standalone via `pytest
// tests.py` against the oracle solution.py sitting next to it -- see
// data/README.md. Two things about that don't hold once this same file
// runs inside a single Pyodide exec against a *student's* code instead:
//
// 1. `from _load import load_solution` -- there's no filesystem, so no
//    `_load` module exists to import at all.
// 2. `<name> = load_solution(...).{name}` -- re-binds a name that's
//    either the student's own submission (self-reference, via
//    `Path(__file__)...`) or a track-mate's oracle solution (a literal
//    folder-name string). Either way it needs a real value, which
//    `load_solution` can't produce here.
//
// The fix for both: strip the whole `from _load import load_solution`
// through the load_solution(...) assignments block (bounded by the
// first `def`, so it survives however many lines a given assignment
// spans), and instead make sure every name it would have bound already
// exists in the exec'd globals before the test functions that use it
// run -- self-references are already covered (the student's code execs
// first), and cross-question references are covered by prepending the
// referenced track-mate's oracle solution ahead of the cleaned test
// code (see buildTestHarness).
function stripLoadSolutionBoilerplate(testsCode: string): {
	cleaned: string;
	trackMateFolders: string[];
} {
	const lines = testsCode.split('\n');
	const startIdx = lines.findIndex((line) =>
		line.trim().startsWith('from _load import load_solution')
	);
	if (startIdx === -1) {
		return { cleaned: testsCode, trackMateFolders: [] };
	}

	let endIdx = lines.findIndex((line, i) => i > startIdx && /^def\s/.test(line));
	if (endIdx === -1) endIdx = lines.length;

	const boilerplate = lines.slice(startIdx, endIdx).join('\n');
	// Only quoted-string arguments are track-mate references --
	// `Path(__file__)...` (the self-reference form) never matches this,
	// which is exactly right: it needs no prelude, the student's own
	// code already defines that name.
	const trackMateFolders = [
		...new Set(
			[...boilerplate.matchAll(/load_solution\(\s*["']([^"']+)["']\s*\)/g)].map((m) => m[1])
		)
	];

	const cleaned = [...lines.slice(0, startIdx), ...lines.slice(endIdx)].join('\n');
	return { cleaned, trackMateFolders };
}

// Every test file gets the same generic collector appended: gather
// every module-level test_* function and run it, pytest-style, in the
// {name, passed, error} shape pyodideWorker.ts's run_tests() contract
// expects. Content authors never write this themselves -- they just
// write normal pytest, same as data/README.md documents.
const TEST_COLLECTOR = `

def run_tests():
    _test_fns = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    tests = []
    for name, fn in _test_fns:
        try:
            fn()
            tests.append({"name": name, "passed": True, "error": None})
        except Exception as e:
            tests.append({"name": name, "passed": False, "error": str(e)})
    return tests
`;

// A question's own oracle solution.py can *itself* use the same
// load_solution(...) pattern tests.py does -- e.g. 05-training-loop's
// solution builds on 01, 03 and 04's oracle solutions the same way a
// real implementation would. So a dependency pulled in for one
// question's tests can have its own further dependencies, which need
// resolving too before any of it is safe to exec. This walks that
// chain to a fixed point and returns every transitively-needed
// question, each already cleaned of its own load_solution boilerplate,
// deepest dependency first (post-order, so by the time a given
// dependency's code appears, everything *it* needs already has).
function collectCleanedDependencies(
	question: GeneratedQuestion,
	byFolder: Map<string, GeneratedQuestion> | undefined
): { cleanedCode: string; missing: string[] }[] {
	const resolved = new Map<string, { cleanedCode: string; missing: string[] }>();
	const visiting = new Set<string>();

	function visit(folders: string[]) {
		for (const folder of folders) {
			if (resolved.has(folder) || visiting.has(folder)) continue;
			const dep = byFolder?.get(folder);
			if (!dep) {
				resolved.set(folder, { cleanedCode: '', missing: [folder] });
				continue;
			}
			visiting.add(folder);
			const { cleaned, trackMateFolders } = stripLoadSolutionBoilerplate(dep.oracleSolutionCode);
			visit(trackMateFolders);
			visiting.delete(folder);
			resolved.set(folder, { cleanedCode: cleaned, missing: [] });
		}
	}

	// Seed from both what the hidden tests reference directly *and* what
	// the question's own reference solution calls -- a statement can (and
	// does, e.g. 05-training-loop) tell the student to call an earlier
	// question's function without that function ever appearing in
	// tests.py itself, so tests.py's references alone aren't the complete
	// picture of what needs to be pre-defined for the student.
	const fromTests = stripLoadSolutionBoilerplate(question.testsCode).trackMateFolders;
	const fromSolution = stripLoadSolutionBoilerplate(question.oracleSolutionCode).trackMateFolders;
	visit([...fromTests, ...fromSolution]);
	return [...resolved.values()];
}

function buildTestHarness(question: GeneratedQuestion): string {
	const { cleaned } = stripLoadSolutionBoilerplate(question.testsCode);
	const byFolder = trackMatesByQuestionId.get(question.id);

	const prelude = collectCleanedDependencies(question, byFolder)
		.map(({ cleanedCode, missing }) =>
			missing.length > 0
				? // Missing dependency is a content-authoring problem, not a
					// student-facing one -- fail loudly inside the harness (a
					// SyntaxError-free, deliberately-raising line) rather than
					// silently producing a NameError deep inside some test.
					`raise RuntimeError(${JSON.stringify(`Missing track-mate dependency '${missing[0]}' for question '${question.id}'`)})`
				: cleanedCode
		)
		.join('\n\n');

	return [prelude, cleaned, TEST_COLLECTOR].filter(Boolean).join('\n\n');
}

function toQuestionContent(question: GeneratedQuestion): QuestionContent {
	return {
		id: question.id,
		metadata: {
			name: question.id,
			title: question.title,
			tags: question.tags,
			difficulty: question.difficulty
		},
		descriptionMarkdown: question.statementMarkdown,
		theoryMarkdown: question.theoryMarkdown,
		starterCode: extractStarterCode(question.statementMarkdown),
		solutionCode: question.oracleSolutionCode,
		explanationMarkdown: question.oracleExplanationMarkdown,
		testHarnessCode: buildTestHarness(question)
	};
}

export async function loadIdeContent(id: string): Promise<QuestionContent | null> {
	const question = questionsById.get(id);
	return question ? toQuestionContent(question) : null;
}

export function listIdeContentIds(): string[] {
	return [...questionsById.keys()];
}
