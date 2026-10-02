import { join } from 'node:path';
import { listContentDirs } from './list-content-dirs.mjs';
import { stripNumericPrefix } from './strip-numeric-prefix.mjs';
import { buildSection } from './build-section.mjs';
import { readMeta } from './read-meta.mjs';

// Root = the top-level curriculum track (Python, Mathematics, ...); it
// holds sections, which hold sub-sections ("tracks" in the output), which
// hold questions -- the same hierarchy /questions shows. A section with no
// questions yet is a placeholder (just its folder and meta.json) and is left out.
export function buildRoot(rootDirName, rootDirPath) {
	const rootId = stripNumericPrefix(rootDirName);
	const meta = readMeta(rootDirPath, 'root');
	const sections = listContentDirs(rootDirPath)
		.map((name) => buildSection(rootId, name, join(rootDirPath, name)))
		.filter((section) => section.tracks.length > 0);
	return { id: rootId, meta, sections };
}
