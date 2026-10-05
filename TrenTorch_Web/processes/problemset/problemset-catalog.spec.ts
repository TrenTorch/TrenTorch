import { describe, expect, it } from 'vitest';
import { problemsetModules, problemsetProblems } from '$data/problemset';

describe('the Test-Ready Problemset catalog', () => {
	it('contains the 250 source questions in pack order', () => {
		expect(problemsetProblems).toHaveLength(250);
		expect(problemsetProblems.map((problem) => problem.order)).toEqual(
			Array.from({ length: 250 }, (_, index) => index + 1)
		);
	});

	it('keeps company metadata on the final 50 case studies only', () => {
		expect(problemsetProblems.slice(0, 200).every((problem) => problem.caseCompany === null)).toBe(
			true
		);
		expect(problemsetProblems.slice(200).every((problem) => Boolean(problem.caseCompany))).toBe(
			true
		);
		expect(problemsetProblems.filter((problem) => problem.kind === 'case-study')).toHaveLength(50);
	});

	it('uses only canonical difficulty values and links every question to a study module', () => {
		const moduleIds = new Set(problemsetModules.map((module) => module.id));
		for (const problem of problemsetProblems) {
			expect(['Beginner', 'Intermediate', 'Advanced']).toContain(problem.difficulty);
			expect(moduleIds.has(problem.moduleId)).toBe(true);
		}
	});
});
