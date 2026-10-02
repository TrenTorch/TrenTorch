import { join } from 'node:path';
import { listContentDirs } from './list-content-dirs.mjs';
import { stripNumericPrefix } from './strip-numeric-prefix.mjs';
import { buildTrack } from './build-track.mjs';

export function buildSection(sectionDirName, sectionDirPath) {
	const sectionId = stripNumericPrefix(sectionDirName);
	// Track dirs are listed (and thus sorted) here, using their raw
	// numeric-prefixed names, before buildTrack strips the prefix from
	// each one's own exposed id -- sort order comes from the folder
	// name, the id itself stays clean.
	const trackDirs = listContentDirs(sectionDirPath);
	const tracks = trackDirs.map((name) =>
		buildTrack(sectionId, sectionDirName, name, join(sectionDirPath, name))
	);
	return { id: sectionId, tracks };
}
