import type { GeneratedQuestion } from './curriculum-index';
import { stripLoadSolutionBoilerplate } from './strip-load-solution-boilerplate';
import { collectCleanedDependencies } from './collect-cleaned-dependencies';
import { TEST_COLLECTOR } from './test-collector';

export function buildTestHarness(question: GeneratedQuestion): string {
	const { cleaned } = stripLoadSolutionBoilerplate(question.testsCode);

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

	return [prelude, cleaned, TEST_COLLECTOR].filter(Boolean).join('\n\n');
}
