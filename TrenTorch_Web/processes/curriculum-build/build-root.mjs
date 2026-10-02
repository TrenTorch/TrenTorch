import { join } from 'node:path';
import { listContentDirs } from './list-content-dirs.mjs';
import { stripNumericPrefix } from './strip-numeric-prefix.mjs';
import { buildSection } from './build-section.mjs';

// Root = the top-level curriculum track (Python, Mathematics, ...); it
// holds sections, which hold sub-sections ("tracks" in the output), which
// hold questions -- the same hierarchy /questions shows.
export function buildRoot(rootDirName, rootDirPath) {
	const rootId = stripNumericPrefix(rootDirName);
	const sections = listContentDirs(rootDirPath).map((name) =>
		buildSection(rootId, rootDirName, name, join(rootDirPath, name))
	);
	return { id: rootId, sections };
}
