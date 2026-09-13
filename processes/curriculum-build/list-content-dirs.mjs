import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import { isDir } from './is-dir.mjs';

// Directory names that are content (section/track/question folders),
// not tooling that happens to live alongside them (e.g. _load.py,
// pytest.ini, README.md).
export function listContentDirs(dir) {
	return readdirSync(dir)
		.filter((name) => !name.startsWith('_') && !name.startsWith('.'))
		.filter((name) => isDir(join(dir, name)))
		.sort();
}
