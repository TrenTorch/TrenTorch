import type { GeneratedQuestion } from './curriculum-index';
import { stripLoadSolutionBoilerplate } from './strip-load-solution-boilerplate';

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
export function collectCleanedDependencies(
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
