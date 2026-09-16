import { describe, it, expect, beforeEach } from 'vitest';
import { activeRoadmap } from './active-roadmap.svelte';
import { solved } from '$processes/progress-tracking/solved.svelte';
import { SKIP_ELIGIBLE_PART_ID } from '$data/roadmap-domains';

describe('activeRoadmap.build', () => {
	it('unions and dedups partIds across selected domains, first-occurrence ordered', () => {
		const state = activeRoadmap.build(['ds', 'ml'], { correct: 0, total: 0 }, [], []);
		const mathOccurrences = state.parts.filter((p) => p.partId === 'part-math');
		expect(mathOccurrences).toHaveLength(1);
		// Data Science is listed before Classical ML in domainDefs, and lists
		// part-data-foundations before part-math -- so part-math should sit
		// right after part-data-foundations, not at the position Classical ML
		// would have put it in on its own.
		expect(state.parts[0].partId).toBe('part-data-foundations');
		expect(state.parts[1].partId).toBe('part-math');
	});

	it('skips the eligible part only when the quiz score is >= 66%', () => {
		const mastered = activeRoadmap.build(['ml'], { correct: 2, total: 3 }, [], []);
		const skippedEntry = mastered.parts.find((p) => p.partId === SKIP_ELIGIBLE_PART_ID);
		expect(skippedEntry?.skipped).toBe(true);

		const notMastered = activeRoadmap.build(['ml'], { correct: 1, total: 3 }, [], []);
		const notSkippedEntry = notMastered.parts.find((p) => p.partId === SKIP_ELIGIBLE_PART_ID);
		expect(notSkippedEntry?.skipped).toBe(false);
	});

	it('never skips anything on a zero-question quiz', () => {
		const state = activeRoadmap.build(['ml'], { correct: 0, total: 0 }, [], []);
		expect(state.parts.every((p) => !p.skipped)).toBe(true);
	});
});

describe('activeRoadmap.activate / reset', () => {
	beforeEach(() => {
		activeRoadmap.reset();
	});

	it('activate sets the active roadmap, reset clears it', () => {
		expect(activeRoadmap.value).toBeNull();
		const state = activeRoadmap.build(['ml'], { correct: 0, total: 0 }, [], []);
		activeRoadmap.activate(state);
		expect(activeRoadmap.value).toEqual(state);
		activeRoadmap.reset();
		expect(activeRoadmap.value).toBeNull();
	});

	it('reset never touches question-completion state', () => {
		solved.markSolved('some-question-slug');
		activeRoadmap.activate(activeRoadmap.build(['ml'], { correct: 0, total: 0 }, [], []));
		activeRoadmap.reset();
		expect(solved.isSolved('some-question-slug')).toBe(true);
		solved.unmarkSolved('some-question-slug');
	});
});
