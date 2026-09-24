import { describe, it, expect } from 'vitest';
import { isSafeQuestionId, parseSolutionInput, solutionFiles } from './solution-files';

const valid = {
	questionId: 'gelu',
	title: 'GELU',
	difficulty: 'Beginner',
	tags: ['activation'],
	description: 'Implement GELU.',
	code: 'def gelu(x):\n    return x'
};

describe('isSafeQuestionId', () => {
	it('accepts plain slugs', () => {
		expect(isSafeQuestionId('gelu')).toBe(true);
		expect(isSafeQuestionId('part-1_softmax.v2')).toBe(true);
	});

	it('rejects path tricks', () => {
		for (const id of ['../x', 'a/b', 'a..b', '', '.hidden', 42, null]) {
			expect(isSafeQuestionId(id)).toBe(false);
		}
	});
});

describe('parseSolutionInput', () => {
	it('parses a valid body', () => {
		expect(parseSolutionInput(valid)?.questionId).toBe('gelu');
	});

	it('rejects empty or oversized code', () => {
		expect(parseSolutionInput({ ...valid, code: '' })).toBeNull();
		expect(parseSolutionInput({ ...valid, code: 'x'.repeat(50001) })).toBeNull();
	});

	it('rejects non-objects', () => {
		expect(parseSolutionInput(null)).toBeNull();
		expect(parseSolutionInput('x')).toBeNull();
	});
});

describe('solutionFiles', () => {
	it('lays out one folder per question with the solution and a README', () => {
		const files = solutionFiles(parseSolutionInput(valid)!);
		expect(files.map((f) => f.path)).toEqual(['gelu/solution.py', 'gelu/README.md']);
		expect(files[0].content).toBe('def gelu(x):\n    return x\n');
		expect(files[1].content).toContain('# GELU');
		expect(files[1].content).toContain('Beginner | activation');
		expect(files[1].content).toContain('Implement GELU.');
	});
});
