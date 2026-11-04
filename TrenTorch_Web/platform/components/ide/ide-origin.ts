// Which list a question was opened from, which decides where the IDE's back arrow (in the header, and the red
// dot on the question pane) goes and what the questions drawer lists. ?src= says so when a list linked here; a
// Problemset question opened any other way (search, a shared link) has no module track, so it falls back to its
// Problemset module.
export type IdeOrigin = 'dsa' | 'potd' | 'problemset' | 'module';

export function ideOrigin(from: {
	isDsa: boolean;
	fromPotd: boolean;
	fromProblemset: boolean;
	hasPotdList: boolean;
	hasProblemsetList: boolean;
	hasTrack: boolean;
}): IdeOrigin {
	if (from.isDsa) return 'dsa';
	if (from.fromPotd && from.hasPotdList) return 'potd';
	if (from.fromProblemset && from.hasProblemsetList) return 'problemset';
	if (!from.hasTrack && from.hasProblemsetList) return 'problemset';
	return from.fromPotd ? 'potd' : 'module';
}
