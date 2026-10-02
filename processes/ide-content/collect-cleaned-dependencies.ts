import type { GeneratedQuestion } from './curriculum-index';
import { questionsByFullPath } from './curriculum-index';
import { stripLoadSolutionBoilerplate } from './strip-load-solution-boilerplate';

// A question's own oracle solution.py can *itself* use the same
// load_solution(...) pattern tests.py does -- e.g. 05-training-loop's
// solution builds on 01, 03 and 04's oracle solutions the same way a
// real implementation would, and that dependency is routinely in a
// DIFFERENT track (see curriculum-index.ts's comment on
// questionsByFullPath for why the lookup has to be global, not scoped
// to the current question's own track). So a dependency pulled in for
// one question's tests can have its own further dependencies, which
// need resolving too before any of it is safe to exec. This walks that
// chain to a fixed point and returns every transitively-needed
// question, each already cleaned of its own load_solution boilerplate,
// deepest dependency first (post-order, so by the time a given
// dependency's code appears, everything *it* needs already has).
export function collectCleanedDependencies(
	question: GeneratedQuestion
): { cleanedCode: string; missing: string[] }[] {
	const resolved = new Map<string, { cleanedCode: string; missing: string[] }>();
	const visiting = new Set<string>();

	function visit(paths: string[]) {
		for (const depPath of paths) {
			if (resolved.has(depPath) || visiting.has(depPath)) continue;
			const dep = questionsByFullPath.get(depPath);
			if (!dep) {
				resolved.set(depPath, { cleanedCode: '', missing: [depPath] });
				continue;
			}
			visiting.add(depPath);
			const { cleaned, dependencyPaths } = stripLoadSolutionBoilerplate(dep.oracleSolutionCode);
			visit(dependencyPaths);
			visiting.delete(depPath);
			resolved.set(depPath, { cleanedCode: cleaned, missing: [] });
		}
	}

	// Seed from both what the hidden tests reference directly *and* what
	// the question's own reference solution calls -- a statement can (and
	// does, e.g. 05-training-loop) tell the student to call an earlier
	// question's function without that function ever appearing in
	// tests.py itself, so tests.py's references alone aren't the complete
	// picture of what needs to be pre-defined for the student.
	const fromTests = stripLoadSolutionBoilerplate(question.testsCode).dependencyPaths;
	const fromSolution = stripLoadSolutionBoilerplate(question.oracleSolutionCode).dependencyPaths;
	visit([...fromTests, ...fromSolution]);
	return [...resolved.values()];
}
