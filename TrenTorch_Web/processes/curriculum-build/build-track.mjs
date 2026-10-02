import { join } from 'node:path';
import { listContentDirs } from './list-content-dirs.mjs';
import { stripNumericPrefix } from './strip-numeric-prefix.mjs';
import { buildQuestion } from './build-question.mjs';

// `parent` carries the already-resolved ids and raw folder names of the
// root and section this track sits under.
export function buildTrack(parent, trackDirName, trackDirPath) {
	const trackId = stripNumericPrefix(trackDirName);
	const questions = listContentDirs(trackDirPath)
		.map((name) => buildQuestion(parent, trackId, trackDirName, name, join(trackDirPath, name)))
		.sort((a, b) => a.order - b.order);

	return { id: trackId, questions };
}
