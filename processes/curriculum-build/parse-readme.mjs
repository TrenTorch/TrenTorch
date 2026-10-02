import { parseFrontmatterValue } from './parse-frontmatter-value.mjs';

// README.md is one YAML-ish frontmatter block (name/title/tags/difficulty --
// deliberately not a real YAML parser, since authors only ever write plain
// scalars and one flow-sequence for tags) followed by exactly three `##`
// sections in a fixed order: Statement, Theory, Explanation. See
// data/app_data/README.md for the authoring contract this mirrors.
export function parseReadme(raw, questionDirPath) {
	const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
	if (!match) {
		throw new Error(`README.md in ${questionDirPath} is missing its --- frontmatter block`);
	}
	const [, frontmatterBlock, body] = match;

	const meta = {};
	for (const line of frontmatterBlock.split('\n')) {
		if (!line.trim()) continue;
		const colonIdx = line.indexOf(':');
		if (colonIdx === -1) continue;
		const key = line.slice(0, colonIdx).trim();
		meta[key] = parseFrontmatterValue(line.slice(colonIdx + 1));
	}
	for (const field of ['name', 'title', 'tags', 'difficulty']) {
		if (meta[field] === undefined) {
			throw new Error(`README.md in ${questionDirPath} is missing frontmatter field '${field}'`);
		}
	}

	const sectionMatch = body.match(
		/^\s*## Statement\n([\s\S]*?)\n## Theory\n([\s\S]*?)\n## Explanation\n([\s\S]*)$/
	);
	if (!sectionMatch) {
		throw new Error(
			`README.md in ${questionDirPath} must have ## Statement, ## Theory and ## Explanation sections in that order`
		);
	}
	const [, statement, theory, explanation] = sectionMatch;

	return {
		meta,
		statementMarkdown: statement.trim(),
		theoryMarkdown: theory.trim(),
		explanationMarkdown: explanation.trim()
	};
}
