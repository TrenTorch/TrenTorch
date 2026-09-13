import { join } from 'node:path';
import { listContentDirs } from './list-content-dirs.mjs';
import { stripNumericPrefix } from './strip-numeric-prefix.mjs';
import { buildQuestion } from './build-question.mjs';

export function buildTrack(sectionId, sectionDirName, trackDirName, trackDirPath) {
	const trackId = stripNumericPrefix(trackDirName);
	const questionDirs = listContentDirs(trackDirPath);
	const questions = questionDirs
		.map((name) =>
			buildQuestion(
				sectionId,
				trackId,
				sectionDirName,
				trackDirName,
				name,
				join(trackDirPath, name)
			)
		)
		.sort((a, b) => a.order - b.order);

	return { id: trackId, questions };
}
