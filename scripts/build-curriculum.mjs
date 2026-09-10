#!/usr/bin/env node
/**
 * Compiles the authored curriculum content under data/ into the single
 * JSON bundle the SvelteKit app loads at runtime.
 *
 * Mirrors the TrenTorch CLI repo's own `tren dev export` pattern: author
 * in real, individually-editable source files (data/<section>/<track>/
 * <NN-question>/{meta.json,statement.md,theory.md,solution.py,
 * explanation.md,tests.py}), generate the final artifact as a build
 * step. Never hand-edit the output of this script -- edit the source
 * files under data/ and re-run it.
 *
 * Usage: node scripts/build-curriculum.mjs
 */

import { readFileSync, readdirSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', 'data');
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
		return readFileSync(path, 'utf-8');
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

function buildQuestion(sectionId, trackId, questionDirName, questionDirPath) {
	const metaRaw = readIfExists(join(questionDirPath, 'meta.json'));
	if (metaRaw === null) {
		throw new Error(`Missing meta.json in ${questionDirPath}`);
	}
	const meta = JSON.parse(metaRaw);

	const statement = readIfExists(join(questionDirPath, 'statement.md'));
	const theory = readIfExists(join(questionDirPath, 'theory.md'));
	const solution = readIfExists(join(questionDirPath, 'solution.py'));
	const explanation = readIfExists(join(questionDirPath, 'explanation.md'));
	const tests = readIfExists(join(questionDirPath, 'tests.py'));
	// Optional for now: not every question has a hand-authored student
	// stub yet. Tracks without it just won't have starterCode in the
	// output until one is added -- not a build failure.
	const starter = readIfExists(join(questionDirPath, 'starter.py'));

	for (const [fieldName, value] of Object.entries({
		statement,
		theory,
		solution,
		explanation,
		tests
	})) {
		if (value === null) {
			throw new Error(`Missing ${fieldName} in ${questionDirPath}`);
		}
	}

	return {
		id: meta.name,
		title: meta.title,
		tags: meta.tags,
		difficulty: meta.difficulty,
		section: sectionId,
		track: trackId,
		order: Number(questionDirName.split('-')[0]),
		statementMarkdown: statement.trim(),
		theoryMarkdown: theory.trim(),
		starterCode: starter,
		oracleSolutionCode: solution,
		oracleExplanationMarkdown: explanation.trim(),
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
	const tracks = trackDirs.map((name) =>
		buildTrack(sectionId, name, join(sectionDirPath, name))
	);
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
