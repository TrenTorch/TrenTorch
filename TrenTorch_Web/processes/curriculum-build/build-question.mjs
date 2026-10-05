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

	let relatedModule;
	if (meta.kind === 'problemset') {
		if (typeof meta.relatedModule !== 'string') {
			throw new Error(
				`Problemset question in ${questionDirPath} is missing relatedModule metadata`
			);
		}
		const moduleParts = meta.relatedModule.split('|');
		if (moduleParts.length !== 2 || moduleParts.some((part) => !part.trim())) {
			throw new Error(
				`Problemset question in ${questionDirPath} must use relatedModule: partId|topicTag`
			);
		}
		relatedModule = { partId: moduleParts[0].trim(), topicTag: moduleParts[1].trim() };
		if (typeof meta.caseCompany === 'string' && !meta.caseCompany.trim()) {
			throw new Error(`Problemset question in ${questionDirPath} has an empty caseCompany`);
		}
	}

	const solution = readIfExists(join(questionDirPath, 'solution.py'));
	const tests = readIfExists(join(questionDirPath, 'tests.py'));
	// Optional for now: not every question has a hand-authored student
	// stub yet. Tracks without it just won't have starterCode in the
	// output until one is added -- not a build failure.
	const starter = readIfExists(join(questionDirPath, 'starter.py'));
	// Optional: Python that runs after the student's code on Run, to draw an example.
	const preview = readIfExists(join(questionDirPath, 'preview.py'));

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
		...(meta.kind === 'problemset' ? { kind: 'problemset' } : {}),
		...(typeof meta.caseCompany === 'string' ? { caseCompany: meta.caseCompany } : {}),
		...(relatedModule ? { relatedModule } : {}),
		...(typeof meta.hint === 'string' ? { hint: meta.hint } : {}),
		...(Array.isArray(meta.tools) ? { tools: meta.tools } : {}),
		...(typeof meta.topic === 'string' ? { topic: meta.topic } : {}),
		section: sectionId,
		track: trackId,
		order: Number(questionDirName.split('-')[0]),
		statementMarkdown,
		theoryMarkdown,
		starterCode: starter,
		...(preview !== null ? { previewCode: preview } : {}),
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
