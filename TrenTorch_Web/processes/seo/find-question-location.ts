import { curriculum, type Part, type Track } from '$data/questions';

export interface QuestionLocation {
	part: Part;
	track: Track;
}

const locations = new Map<string, QuestionLocation>();
for (const part of curriculum) {
	for (const track of part.tracks) {
		for (const question of track.questions) locations.set(question.slug, { part, track });
	}
}

export function findQuestionLocation(slug: string): QuestionLocation | undefined {
	return locations.get(slug);
}
