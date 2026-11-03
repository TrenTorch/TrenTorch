import { describe, it, expect } from 'vitest';
import { curriculum } from '$data/questions';
import { problemsetProblems } from '$data/problemset';
import { potdEntries } from '$data/potd';
import { getTrackQuestions, getProblemsetList, getPotdList } from './get-track-questions';

describe('getTrackQuestions', () => {
	it('lists the whole track in Questions-page order, with its Part and title', () => {
		const part = curriculum[0];
		const track = part.tracks[0];
		const result = getTrackQuestions(track.questions[0].slug);

		expect(result.partId).toBe(part.id);
		expect(result.track).toBe(track.name);
		expect(result.questions.map((q) => q.id)).toEqual(track.questions.map((q) => q.slug));
		expect(result.questions.map((q) => q.title)).toEqual(track.questions.map((q) => q.title));
	});

	it('returns the same list from every question in the track', () => {
		const track = curriculum.flatMap((part) => part.tracks).find((t) => t.questions.length > 2)!;
		const lists = track.questions.map((q) => getTrackQuestions(q.slug).questions);
		for (const list of lists) expect(list).toEqual(lists[0]);
	});

	it('leaves out questions from sibling tracks, including in the same section', () => {
		const section = curriculum
			.flatMap((part) => part.sections ?? [])
			.find((s) => s.tracks.length > 1)!;
		const [a, b] = section.tracks;
		const ids = getTrackQuestions(a.questions[0].slug).questions.map((q) => q.id);

		expect(ids).toEqual(a.questions.map((q) => q.slug));
		for (const q of b.questions) expect(ids).not.toContain(q.slug);
	});

	it('returns an empty list for an unknown id', () => {
		expect(getTrackQuestions('no-such-question')).toEqual({
			partId: null,
			track: null,
			questions: []
		});
	});
});

describe('getProblemsetList', () => {
	it("lists the question's module siblings, and only those", () => {
		const problem = problemsetProblems[0];
		const list = getProblemsetList(problem.slug)!;
		const expected = problemsetProblems.filter((p) => p.moduleId === problem.moduleId);
		expect(list.questions.map((q) => q.id)).toEqual(expected.map((p) => p.slug));
		expect(list.questions.some((q) => q.id === problem.slug)).toBe(true);
	});

	it('is null for a question outside the Problemset', () => {
		expect(getProblemsetList('no-such-question')).toBeNull();
	});
});

describe('getPotdList', () => {
	it('lists every Problem of the Day, newest first, with dates', () => {
		const list = getPotdList(potdEntries[0].questionId)!;
		const dates = list.questions.map((q) => q.date!);
		expect(dates).toEqual([...dates].sort().reverse());
		expect(list.questions.some((q) => q.id === potdEntries[0].questionId)).toBe(true);
	});

	it('is null for a question that was never a Problem of the Day', () => {
		expect(getPotdList('no-such-question')).toBeNull();
	});
});
