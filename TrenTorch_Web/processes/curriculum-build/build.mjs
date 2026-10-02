#!/usr/bin/env node
/**
 * Compiles the authored curriculum content under data/app_data/ into the
 * single JSON bundle the SvelteKit app loads at runtime.
 *
 * Mirrors the TrenTorch CLI repo's own `tren dev export` pattern: author
 * in real, individually-editable source files (data/app_data/<root>/<section>/
 * <track>/<NN-question>/{README.md,starter.py,solution.py,tests.py}),
 * generate the final artifact as a build step. Never hand-edit the
 * output of this script -- edit the source files under data/app_data/
 * and re-run it.
 *
 * Two outputs, both generated, never hand-edited:
 *   generated-curriculum.json  the IDE bundle (every question's full content)
 *   generated-catalogue.json   the slim hierarchy the question list pages read
 *
 * Usage: node processes/curriculum-build/build.mjs
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { listContentDirs } from './list-content-dirs.mjs';
import { buildRoot } from './build-root.mjs';
import { buildCatalogue } from './build-catalogue.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', '..', 'data', 'app_data');
const OUTPUT_DIR = join(__dirname, '..', '..', 'data', 'curriculum');
const OUTPUT_PATH = join(OUTPUT_DIR, 'generated-curriculum.json');
const CATALOGUE_PATH = join(OUTPUT_DIR, 'generated-catalogue.json');

function build() {
	const roots = listContentDirs(DATA_DIR).map((name) => buildRoot(name, join(DATA_DIR, name)));

	let totalQuestions = 0;
	for (const root of roots) {
		for (const section of root.sections) {
			for (const track of section.tracks) {
				totalQuestions += track.questions.length;
			}
		}
	}

	// Validates (unique names/titles) before anything is written.
	const catalogue = buildCatalogue(roots);

	mkdirSync(OUTPUT_DIR, { recursive: true });
	// `meta` (titles, topics, companies) is for the catalogue; the IDE bundle
	// stays exactly the content it always was.
	const withoutMeta = roots.map((root) => ({
		id: root.id,
		sections: root.sections.map((section) => ({
			id: section.id,
			tracks: section.tracks.map((track) => ({ id: track.id, questions: track.questions }))
		}))
	}));
	writeFileSync(OUTPUT_PATH, JSON.stringify({ roots: withoutMeta }, null, 2) + '\n', 'utf-8');
	writeFileSync(CATALOGUE_PATH, JSON.stringify(catalogue, null, 2) + '\n', 'utf-8');

	console.log(`Built ${OUTPUT_PATH}`);
	console.log(`Built ${CATALOGUE_PATH}`);
	console.log(`${roots.length} roots, ${totalQuestions} questions total.`);
}

build();
