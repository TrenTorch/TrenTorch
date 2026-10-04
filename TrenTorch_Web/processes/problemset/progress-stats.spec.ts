import { describe, expect, it } from 'vitest';
import { problemsetProblems } from '$data/problemset';
import { getProblemsetProgressStats } from './progress-stats';

describe('getProblemsetProgressStats', () => {
	it('counts only Problemset questions and breaks solves down by difficulty', () => {
		const easy = problemsetProblems.find((problem) => problem.difficulty === 'Easy');
		const hard = problemsetProblems.find((problem) => problem.difficulty === 'Hard');
		const solvedSlugs = [easy?.slug, hard?.slug, 'unrelated-curriculum-question'].filter(
			(slug): slug is string => Boolean(slug)
		);
		const stats = getProblemsetProgressStats(new Set(solvedSlugs));

		expect(stats.solved).toBe(2);
		expect(stats.total).toBe(200);
		expect(stats.byDifficulty).toEqual([
			{ difficulty: 'Easy', solved: 1, total: 68 },
			{ difficulty: 'Medium', solved: 0, total: 68 },
			{ difficulty: 'Hard', solved: 1, total: 64 }
		]);
	});
});
