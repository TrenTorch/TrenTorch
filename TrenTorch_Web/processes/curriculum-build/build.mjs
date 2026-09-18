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
 * Usage: node processes/curriculum-build/build.mjs
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { listContentDirs } from './list-content-dirs.mjs';
import { buildSection } from './build-section.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', '..', 'data', 'app_data');
const OUTPUT_PATH = join(__dirname, '..', '..', 'data', 'curriculum', 'generated-curriculum.json');

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
