#!/usr/bin/env node
/**
 * Compiles the authored curriculum content under data/app_data/ into the
 * single JSON bundle the SvelteKit app loads at runtime.
 *
 * Mirrors the TrenTorch CLI repo's own `tren dev export` pattern: author
 * in real, individually-editable source files (data/app_data/<section>/
 * <track>/<NN-question>/{README.md,starter.py,solution.py,tests.py}),
 * generate the final artifact as a build step. Never hand-edit the
 * output of this script -- edit the source files under data/app_data/
 * and re-run it.
 *
 * Usage: node scripts/build-curriculum.mjs
 */

import { readFileSync, readdirSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', 'data', 'app_data');
const OUTPUT_PATH = join(__dirname, '..', 'src', 'lib', 'curriculum', 'generated-curriculum.json');

function isDir(path) {
	try {
		return statSync(path).isDirectory();
	} catch {
		return false;
	}
}

function readIfExists(path) {
	try {
		// Normalize to LF regardless of the authoring/checkout platform's line
		// endings -- a Windows checkout (CRLF) would otherwise bake literal
		// \r characters into every generated string, which is harmless for
		// Markdown but a real risk for Python source (mixed \r\n content
		// concatenated with \n content across questions, then exec'd).
		return readFileSync(path, 'utf-8').replace(/\r\n/g, '\n');
	} catch {
		return null;
	}
}

// Directory names that are content (section/track/question folders),
// not tooling that happens to live alongside them (e.g. _load.py,
// pytest.ini, README.md).
function listContentDirs(dir) {
	return readdirSync(dir)
		.filter((name) => !name.startsWith('_') && !name.startsWith('.'))
		.filter((name) => isDir(join(dir, name)))
		.sort();
}

// Section and track folders carry a numeric prefix purely to fix their
// display/build order (plain alphabetical sort put "classification"
// before "linear-regression", which is backwards pedagogically -- the
// same problem question folders already solved with their own "01-"
// prefixes). The prefix is not part of the semantic id: strip it before
// exposing `id`/`section`/`track`, so consumers keep working with
// "classical-ml"/"linear-regression", not "01-classical-ml".
function stripNumericPrefix(dirName) {
	return dirName.replace(/^\d+-/, '');
}

// README.md is one YAML-ish frontmatter block (name/title/tags/difficulty --
// deliberately not a real YAML parser, since authors only ever write plain
// scalars and one flow-sequence for tags) followed by exactly three `##`
// sections in a fixed order: Statement, Theory, Explanation. See
// data/app_data/README.md for the authoring contract this mirrors.
function parseFrontmatterValue(raw) {
	const trimmed = raw.trim();
	if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
		return trimmed
			.slice(1, -1)
			.split(',')
			.map((item) => parseFrontmatterValue(item))
			.filter((item) => item !== '');
	}
	if (
		(trimmed.startsWith('"') && trimmed.endsWith('"')) ||
		(trimmed.startsWith("'") && trimmed.endsWith("'"))
	) {
		return trimmed.slice(1, -1);
	}
	return trimmed;
}

function parseReadme(raw, questionDirPath) {
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

function buildQuestion(sectionId, trackId, questionDirName, questionDirPath) {
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
		testsCode: tests
	};
}

function buildTrack(sectionId, trackDirName, trackDirPath) {
	const trackId = stripNumericPrefix(trackDirName);
	const questionDirs = listContentDirs(trackDirPath);
	const questions = questionDirs
		.map((name) => buildQuestion(sectionId, trackId, name, join(trackDirPath, name)))
		.sort((a, b) => a.order - b.order);

	return { id: trackId, questions };
}

function buildSection(sectionDirName, sectionDirPath) {
	const sectionId = stripNumericPrefix(sectionDirName);
	// Track dirs are listed (and thus sorted) here, using their raw
	// numeric-prefixed names, before buildTrack strips the prefix from
	// each one's own exposed id -- sort order comes from the folder
	// name, the id itself stays clean.
	const trackDirs = listContentDirs(sectionDirPath);
	const tracks = trackDirs.map((name) => buildTrack(sectionId, name, join(sectionDirPath, name)));
	return { id: sectionId, tracks };
}

function build() {
	const sectionDirs = listContentDirs(DATA_DIR);
	const sections = sectionDirs.map((name) => buildSection(name, join(DATA_DIR, name)));

	let totalQuestions = 0;
	for (const section of sections) {
		for (const track of section.tracks) {
			totalQuestions += track.questions.length;
		}
	}

	mkdirSync(dirname(OUTPUT_PATH), { recursive: true });
	writeFileSync(OUTPUT_PATH, JSON.stringify({ sections }, null, 2) + '\n', 'utf-8');

	console.log(`Built ${OUTPUT_PATH}`);
	console.log(`${sections.length} sections, ${totalQuestions} questions total.`);
}

build();
