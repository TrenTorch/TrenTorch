// Loads IDE content by id from src/lib/data/ide-content/<name>/ folders.
// Adding a question to the IDE is dropping a new folder there with a
// metadata.json plus description.md, theory.md, starter.py, solution.py
// and tests.py -- real Markdown and Python, no JSON-escaped strings, and
// no code changes here needed.
import type { QuestionContent, QuestionMetadata } from '$lib/curriculum/types';

const ROOT = '/src/lib/data/ide-content';

const metadataFiles = import.meta.glob<{ default: QuestionMetadata }>(
	'/src/lib/data/ide-content/*/metadata.json'
);
const descriptionFiles = import.meta.glob<string>('/src/lib/data/ide-content/*/description.md', {
	query: '?raw',
	import: 'default'
});
const theoryFiles = import.meta.glob<string>('/src/lib/data/ide-content/*/theory.md', {
	query: '?raw',
	import: 'default'
});
const starterFiles = import.meta.glob<string>('/src/lib/data/ide-content/*/starter.py', {
	query: '?raw',
	import: 'default'
});
const solutionFiles = import.meta.glob<string>('/src/lib/data/ide-content/*/solution.py', {
	query: '?raw',
	import: 'default'
});
const testFiles = import.meta.glob<string>('/src/lib/data/ide-content/*/tests.py', {
	query: '?raw',
	import: 'default'
});

async function readRaw(
	files: Record<string, () => Promise<string>>,
	path: string
): Promise<string> {
	const importer = files[path];
	return importer ? importer() : '';
}

export async function loadIdeContent(id: string): Promise<QuestionContent | null> {
	const dir = `${ROOT}/${id}`;
	const metaImporter = metadataFiles[`${dir}/metadata.json`];
	// A question with no metadata.json isn't published yet -- everything
	// else (description, theory, code) is optional per-file so a question
	// can be authored incrementally without ever rendering half-broken.
	if (!metaImporter) return null;

	const [
		metadata,
		descriptionMarkdown,
		theoryMarkdown,
		starterCode,
		solutionCode,
		testHarnessCode
	] = await Promise.all([
		metaImporter().then((mod) => mod.default),
		readRaw(descriptionFiles, `${dir}/description.md`),
		readRaw(theoryFiles, `${dir}/theory.md`),
		readRaw(starterFiles, `${dir}/starter.py`),
		readRaw(solutionFiles, `${dir}/solution.py`),
		readRaw(testFiles, `${dir}/tests.py`)
	]);

	return {
		id,
		metadata,
		descriptionMarkdown,
		theoryMarkdown,
		starterCode,
		solutionCode,
		testHarnessCode
	};
}

export function listIdeContentIds(): string[] {
	return Object.keys(metadataFiles).map((path) =>
		path.replace(`${ROOT}/`, '').replace('/metadata.json', '')
	);
}
