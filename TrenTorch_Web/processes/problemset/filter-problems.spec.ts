import { describe, expect, it } from 'vitest';
import { problemsetModules, problemsetProblems } from '$data/problemset';
import { curriculum } from '$data/questions';
import {
	filterProblemset,
	getProblemsetStatus,
	paginateProblemset,
	PROBLEMSET_PAGE_SIZE,
	type ProblemsetFilters
} from './filter-problems';

const noFilters: ProblemsetFilters = {
	query: '',
	moduleId: '',
	topic: '',
	company: '',
	difficulty: '',
	status: 'all',
	pastPotdOnly: false
};

describe('filterProblemset', () => {
	it('includes the 200 unique supplied problems', () => {
		expect(problemsetProblems).toHaveLength(200);
		expect(new Set(problemsetProblems.map((problem) => problem.slug)).size).toBe(200);
		expect(
			filterProblemset(problemsetProblems, noFilters, new Set(), new Set(), new Set())
		).toHaveLength(200);
	});

	it('links every study module to an existing learning module', () => {
		const learningPartIds = new Set(curriculum.map((part) => part.id));
		const curriculumSlugs = new Set(
			curriculum.flatMap((part) => part.tracks.flatMap((track) => track.questions.map((q) => q.slug)))
		);

		expect(problemsetModules.every((module) => learningPartIds.has(module.learningPartId))).toBe(
			true
		);
		expect(problemsetProblems.every((problem) => !curriculumSlugs.has(problem.slug))).toBe(true);
	});

	it('combines module, topic, company, and difficulty filters', () => {
		const results = filterProblemset(
			problemsetProblems,
			{
				...noFilters,
				moduleId: 'maths-stats-for-ml',
				topic: 'linear-algebra',
				company: 'Google',
				difficulty: 'Beginner'
			},
			new Set(),
			new Set(),
			new Set()
		);

		expect(results.length).toBeGreaterThan(0);
		expect(
			results.every(
				(problem) =>
					problem.moduleId === 'maths-stats-for-ml' &&
					problem.topic === 'linear-algebra' &&
					problem.caseCompany === 'Google' &&
					problem.difficulty === 'Beginner'
			)
		).toBe(true);
	});

	it('searches titles and company names without case sensitivity', () => {
		expect(
			filterProblemset(
				problemsetProblems,
				{ ...noFilters, query: 'GOOGLE' },
				new Set(),
				new Set(),
				new Set()
			).every((problem) => problem.caseCompany?.toLowerCase().includes('google'))
		).toBe(true);
	});

	it('treats solved as stronger than attempted and filters status accurately', () => {
		const [problem] = problemsetProblems;
		const solvedSlugs = new Set([problem.slug]);
		const attemptedSlugs = new Set([problem.slug, problemsetProblems[1].slug]);

		expect(getProblemsetStatus(problem.slug, solvedSlugs, attemptedSlugs)).toBe('solved');
		expect(
			filterProblemset(
				problemsetProblems,
				{ ...noFilters, status: 'attempted' },
				solvedSlugs,
				attemptedSlugs,
				attemptedSlugs
			).map((item) => item.slug)
		).toEqual([problemsetProblems[1].slug]);
	});

	it('combines the past Problem of the Day filter with other filters', () => {
		const pastPotdSlugs = new Set([problemsetProblems[0].slug, problemsetProblems[2].slug]);

		expect(
			filterProblemset(
				problemsetProblems,
				{ ...noFilters, company: 'Google', pastPotdOnly: true },
				new Set(),
				new Set(),
				pastPotdSlugs
			).map((problem) => problem.slug)
		).toEqual([problemsetProblems[2].slug]);
	});

	it('shows no more than 100 problems on each page', () => {
		const firstPage = paginateProblemset(problemsetProblems, 1);
		const secondPage = paginateProblemset(problemsetProblems, 2);

		expect(PROBLEMSET_PAGE_SIZE).toBe(100);
		expect(firstPage).toHaveLength(100);
		expect(secondPage).toHaveLength(100);
		expect(firstPage[0].slug).not.toBe(secondPage[0].slug);
		expect(paginateProblemset(problemsetProblems, 0)).toEqual(firstPage);
		expect(paginateProblemset(problemsetProblems, Number.NaN)).toEqual(firstPage);
		expect(paginateProblemset(problemsetProblems, 99)).toEqual(secondPage);
	});
});
