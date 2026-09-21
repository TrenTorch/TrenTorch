import type { GeneratedQuestion } from './curriculum-index';
import { questionsByFullPath } from './curriculum-index';
import { stripLoadSolutionBoilerplate } from './strip-load-solution-boilerplate';
import { collectCleanedDependencies } from './collect-cleaned-dependencies';
import { TEST_COLLECTOR } from './test-collector';
import { buildLoadSolutionShim } from './load-solution-shim';
import { STUDENT_CODE_MARKER } from './harness-marker';

// A solution together with everything it depends on, as one block of code that
// can run in a namespace of its own (see load-solution-shim.ts).
function isolatedSolutionSource(path: string): string | null {
	const solution = questionsByFullPath.get(path);
	if (!solution) return null;
	const dependencies = collectCleanedDependencies({
		...solution,
		testsCode: solution.oracleSolutionCode
	}).map(({ cleanedCode, missing }) =>
		missing.length > 0
			? `raise RuntimeError(${JSON.stringify(`Missing dependency '${missing[0]}' for '${path}'`)})`
			: cleanedCode
	);
	return [...dependencies, stripLoadSolutionBoilerplate(solution.oracleSolutionCode).cleaned]
		.filter(Boolean)
		.join('\n\n');
}

// The harness has two sections, split by STUDENT_CODE_MARKER, that run on
// either side of the student's code:
//
// 1. Before: everything the student's code may need while it is being defined.
//    The dependency solutions (a base class to subclass, a function used as a
//    default argument or at module level), the renamed imports the starter
//    gives them, and the load_solution stand-in. Running these after the
//    student's code meant `class LazyLinear(Module)` crashed with a NameError
//    before a single test ran.
// 2. After: bindings for any module variables the tests use, the tests
//    themselves, and the collector that runs them.
export function buildTestHarness(question: GeneratedQuestion): string {
	const { cleaned, moduleVars, namespacePaths } = stripLoadSolutionBoilerplate(question.testsCode);

	const prelude = collectCleanedDependencies(question)
		.map(({ cleanedCode, missing }) =>
			missing.length > 0
				? // Missing dependency is a content-authoring problem, not a
					// student-facing one -- fail loudly inside the harness (a
					// SyntaxError-free, deliberately-raising line) rather than
					// silently producing a NameError deep inside some test.
					`raise RuntimeError(${JSON.stringify(`Missing dependency '${missing[0]}' for question '${question.id}'`)})`
				: cleanedCode
		)
		.join('\n\n');

	// The starter (and the reference solution) may import a dependency's
	// function under a new name, `softmax_axis1 = load_solution("...").softmax`.
	// Student code has that line removed before it runs (sanitize-student-code.ts),
	// which would leave the new name unbound, so bind it here. Defined before the
	// student's code, so a student who writes their own version still wins.
	const renames = [question.starterCode ?? '', question.oracleSolutionCode].flatMap(
		(code) => stripLoadSolutionBoilerplate(code).renames
	);
	const rebinds = [...new Map(renames.map((r) => [r.target, r])).values()]
		.map(({ target, attr }) => `${target} = ${attr}`)
		.join('\n');

	// Tests that still use load_solution or a module variable after the
	// boilerplate is gone (`_module.helper`, `plain_gb.train(...)`, or a
	// load_solution call inside a test) need something to call. See
	// load-solution-shim.ts.
	const usedModuleVars = moduleVars.filter(({ name }) => new RegExp(`\\b${name}\\b`).test(cleaned));
	const needsShim = usedModuleVars.length > 0 || /\bload_solution\s*\(/.test(cleaned);
	const sources: Record<string, string> = {};
	for (const path of namespacePaths) {
		const source = isolatedSolutionSource(path);
		if (source !== null) sources[path] = source;
	}
	const moduleBindings = usedModuleVars
		.map(({ name, self, path }) =>
			self
				? `${name} = _Namespace(globals())`
				: path
					? `${name} = load_solution(${JSON.stringify(path)})`
					: ''
		)
		.filter(Boolean)
		.join('\n');

	const beforeStudentCode = [prelude, rebinds, needsShim ? buildLoadSolutionShim(sources) : '']
		.filter(Boolean)
		.join('\n\n');
	const afterStudentCode = [moduleBindings, cleaned, TEST_COLLECTOR].filter(Boolean).join('\n\n');

	return [beforeStudentCode, STUDENT_CODE_MARKER, afterStudentCode].filter(Boolean).join('\n\n');
}
