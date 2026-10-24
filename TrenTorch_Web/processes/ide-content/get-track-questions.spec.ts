import { describe, it, expect } from 'vitest';
import { questionsById } from './curriculum-index';
import { getTrackQuestions } from './get-track-questions';

describe('getTrackQuestions', () => {
	it('lists only the current question track, including itself, in curriculum order', () => {
		const first = [...questionsById.values()][0];
		const { track, questions } = getTrackQuestions(first.id);

		expect(track).toBe(first.track);
		expect(questions[0].id).toBe(first.id);
		for (const q of questions) expect(questionsById.get(q.id)!.track).toBe(first.track);
	});

	it('returns an empty list for an unknown id', () => {
		expect(getTrackQuestions('no-such-question')).toEqual({ track: null, questions: [] });
	});
});
