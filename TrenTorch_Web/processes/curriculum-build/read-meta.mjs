import { join } from 'node:path';
import { readIfExists } from './read-if-exists.mjs';

// Every root, section and track folder carries a `meta.json` next to its
// children. `title` is what the app shows; `topics` and `companies` are
// optional and are inherited by everything below the folder that sets them
// (see build-catalogue.mjs), so a value shared by a whole section is written once.
export function readMeta(dirPath, kind) {
	const raw = readIfExists(join(dirPath, 'meta.json'));
	if (raw === null) throw new Error(`Missing meta.json in ${kind} folder ${dirPath}`);
	const meta = JSON.parse(raw);
	if (typeof meta.title !== 'string' || meta.title.trim() === '') {
		throw new Error(`meta.json in ${dirPath} needs a non-empty "title"`);
	}
	return meta;
}
