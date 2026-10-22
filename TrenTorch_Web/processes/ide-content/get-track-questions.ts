import { questionsById } from './curriculum-index';
import type { QuestionMetadata } from '$data/curriculum/types';

export interface TrackQuestion {
	id: string;
	title: string;
	difficulty: QuestionMetadata['difficulty'];
}

// Every question in the same track as `id`, in curriculum order -- the
// IDE header's quick-nav drawer lists these. Scoped to one track rather
// than the whole curriculum so each prerendered page only carries a
// handful of titles, not hundreds.
export function getTrackQuestions(id: string): {
	track: string | null;
	questions: TrackQuestion[];
} {
	const current = questionsById.get(id);
	if (!current) return { track: null, questions: [] };
	const questions = [...questionsById.values()]
		.filter(
			(q) => q.root === current.root && q.section === current.section && q.track === current.track
		)
		.map(({ id, title, difficulty }) => ({ id, title, difficulty }));
	return { track: current.track, questions };
}
