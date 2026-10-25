// Serves the curriculum as four virtual modules, built in memory from
// data/app_data/ (see build.mjs). Nothing generated is written to disk.
//
//   import { curriculum } from 'virtual:curriculum/bundle';
//   import { catalogue } from 'virtual:curriculum/catalogue';
//   import { problemsetSources } from 'virtual:curriculum/problemset';
//   import { dsaSheet } from 'virtual:curriculum/dsa-sheet';
//
// On the dev server, the plugin watches data/app_data and reloads the page
// whenever a file there changes. The next import rebuilds from source, so
// there is no separate build step to run after an edit.

import { sep } from 'node:path';
import { buildCurriculum, DATA_DIR } from './build.mjs';

const BUNDLE_ID = 'virtual:curriculum/bundle';
const CATALOGUE_ID = 'virtual:curriculum/catalogue';
const PROBLEMSET_ID = 'virtual:curriculum/problemset';
const DSA_SHEET_ID = 'virtual:curriculum/dsa-sheet';
const RESOLVED = new Map([
	[BUNDLE_ID, '\0' + BUNDLE_ID],
	[CATALOGUE_ID, '\0' + CATALOGUE_ID],
	[PROBLEMSET_ID, '\0' + PROBLEMSET_ID],
	[DSA_SHEET_ID, '\0' + DSA_SHEET_ID]
]);

export function curriculumPlugin() {
	// Built lazily on first import and dropped whenever a source file changes.
	let built = null;
	const current = () => (built ??= buildCurriculum());

	return {
		name: 'trentorch-curriculum',

		resolveId(id) {
			return RESOLVED.get(id);
		},

		load(id) {
			if (id === RESOLVED.get(BUNDLE_ID)) {
				return `export const curriculum = ${JSON.stringify(current().bundle)};`;
			}
			if (id === RESOLVED.get(CATALOGUE_ID)) {
				return `export const catalogue = ${JSON.stringify(current().catalogue)};`;
			}
			if (id === RESOLVED.get(PROBLEMSET_ID)) {
				return `export const problemsetSources = ${JSON.stringify(current().problemset)};`;
			}
			if (id === RESOLVED.get(DSA_SHEET_ID)) {
				return `export const dsaSheet = ${JSON.stringify(current().dsaSheet)};`;
			}
		},

		configureServer(server) {
			server.watcher.add(DATA_DIR);
			server.watcher.on('all', (_event, file) => {
				if (!file.startsWith(DATA_DIR + sep)) return;
				built = null;
				for (const resolved of RESOLVED.values()) {
					const mod = server.moduleGraph.getModuleById(resolved);
					if (mod) server.moduleGraph.invalidateModule(mod);
				}
				server.ws.send({ type: 'full-reload' });
			});
		}
	};
}
