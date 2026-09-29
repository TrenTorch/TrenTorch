import { join } from 'node:path';
import { readIfExists } from './read-if-exists.mjs';
import { parseReadme } from './parse-readme.mjs';

export function buildQuestion(
	sectionId,
	trackId,
	sectionDirName,
	trackDirName,
	questionDirName,
	questionDirPath
) {
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
		section: sectionId,
		track: trackId,
		// The raw, numeric-prefixed on-disk directory names -- distinct from
		// `section`/`track` (the prefix-stripped semantic ids above). A
		// load_solution("01-classical-ml/03-decision-trees/03-best-split-
		// minimal-tree") call in some OTHER question's solution.py/tests.py
		// addresses a dependency by this exact three-segment raw path (see
		// data/app_data/_load.py's own docstring: paths are deliberately
		// section/track/folder-qualified so no two tracks' "01-..." folders
		// can ever collide). The browser-side dependency resolution needs
		// these same raw segments to reproduce that lookup faithfully --
		// resolving by bare folder name alone breaks the moment a
		// dependency lives in a different track than the question asking
		// for it.
		sectionFolder: sectionDirName,
		trackFolder: trackDirName,
		// The raw "NN-question-slug" folder name, distinct from `id`
		// (README.md frontmatter's `name`) -- kept so the app can resolve a
		// track-mate's tests.py calling load_solution("01-hypothesis-function")
		// back to a question id without guessing at a naming convention
		// between the two.
		folder: questionDirName,
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
