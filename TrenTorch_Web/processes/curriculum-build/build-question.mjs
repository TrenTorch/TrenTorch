import { join } from 'node:path';
import { readIfExists } from './read-if-exists.mjs';
import { parseReadme } from './parse-readme.mjs';

export function buildQuestion(parent, trackId, questionDirName, questionDirPath) {
	const { rootId, sectionId } = parent;
	const readmeRaw = readIfExists(join(questionDirPath, 'README.md'));
	if (readmeRaw === null) {
		throw new Error(`Missing README.md in ${questionDirPath}`);
	}
	const { meta, statementMarkdown, theoryMarkdown, explanationMarkdown } = parseReadme(
		readmeRaw,
		questionDirPath
	);

	const solution = readIfExists(join(questionDirPath, 'solution.py'));
	const tests = readIfExists(join(questionDirPath, 'tests.py'));
	// Optional for now: not every question has a hand-authored student
	// stub yet. Tracks without it just won't have starterCode in the
	// output until one is added -- not a build failure.
	const starter = readIfExists(join(questionDirPath, 'starter.py'));

	for (const [fieldName, value] of Object.entries({ solution, tests })) {
		if (value === null) {
			throw new Error(
				`Missing ${fieldName === 'solution' ? 'solution.py' : 'tests.py'} in ${questionDirPath}`
			);
		}
	}

	return {
		id: meta.name,
		title: meta.title,
		tags: meta.tags,
		difficulty: meta.difficulty,
		root: rootId,
		section: sectionId,
		track: trackId,
		order: Number(questionDirName.split('-')[0]),
		statementMarkdown,
		theoryMarkdown,
		starterCode: starter,
		oracleSolutionCode: solution,
		oracleExplanationMarkdown: explanationMarkdown,
		testsCode: tests,
		// Optional: an id naming a client-side interactive widget (see
		// platform/widgets/) to mount inside the Theory tab, for questions
		// where a slider-driven canvas genuinely clarifies the idea. Most
		// questions have none.
		...(typeof meta.widget === 'string' ? { widgetId: meta.widget } : {})
	};
}
