#!/usr/bin/env node
/**
 * Compiles the authored curriculum content under data/app_data/ into the two
 * shapes the app reads. Nothing is written to disk: the Vite plugin in
 * vite-plugin-curriculum.mjs calls buildCurriculum() in memory and serves the
 * result as virtual modules, so editing a question shows up on the dev server
 * straight away and no generated file is ever committed.
 *
 *   bundle     the IDE bundle (every question's full content)
 *   catalogue  the slim hierarchy the question list pages read
 *
 * Authoring rules live in data/app_data/README.md.
 *
 * Usage: node processes/curriculum-build/build.mjs   (validates and prints a summary)
 */

import { resolve, join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { listContentDirs } from './list-content-dirs.mjs';
import { buildRoot } from './build-root.mjs';
import { buildCatalogue } from './build-catalogue.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
export const DATA_DIR = join(__dirname, '..', '..', 'data', 'app_data');

export function buildCurriculum() {
	const roots = listContentDirs(DATA_DIR).map((name) => buildRoot(name, join(DATA_DIR, name)));

	// Validates (unique names/titles) before anything is returned.
	const catalogue = buildCatalogue(roots);

	// `meta` (titles, topics, companies) is for the catalogue; the IDE bundle
	// stays exactly the content it always was.
	const bundle = {
		roots: roots.map((root) => ({
			id: root.id,
			sections: root.sections.map((section) => ({
				id: section.id,
				tracks: section.tracks.map((track) => ({ id: track.id, questions: track.questions }))
			}))
		}))
	};

	let questions = 0;
	for (const root of bundle.roots) {
		for (const section of root.sections) {
			for (const track of section.tracks) {
				questions += track.questions.length;
			}
		}
	}

	return { bundle, catalogue, rootCount: bundle.roots.length, questionCount: questions };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
	const { rootCount, questionCount } = buildCurriculum();
	console.log(`Curriculum OK: ${rootCount} roots, ${questionCount} questions.`);
}
