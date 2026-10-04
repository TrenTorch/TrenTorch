import { describe, expect, it } from 'vitest';
import { problemsetProblems } from '$data/problemset';
import { getProblemsetProgressStats } from './progress-stats';

describe('getProblemsetProgressStats', () => {
	it('counts only Problemset questions and breaks solves down by difficulty', () => {
		const beginner = problemsetProblems.find((problem) => problem.difficulty === 'Beginner');
		const advanced = problemsetProblems.find((problem) => problem.difficulty === 'Advanced');
		const solvedSlugs = [beginner?.slug, advanced?.slug, 'unrelated-curriculum-question'].filter(
			(slug): slug is string => Boolean(slug)
		);
		const stats = getProblemsetProgressStats(new Set(solvedSlugs));

		expect(stats.solved).toBe(2);
		expect(stats.total).toBe(250);
		expect(stats.byDifficulty.map((item) => item.difficulty)).toEqual([
			'Beginner',
			'Intermediate',
			'Advanced'
		]);
		expect(stats.byDifficulty.reduce((total, item) => total + item.total, 0)).toBe(250);
		expect(stats.byDifficulty.reduce((total, item) => total + item.solved, 0)).toBe(2);
		expect(stats.byDifficulty.every((item) => item.solved <= item.total)).toBe(true);
	});
});
