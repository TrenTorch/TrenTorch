import { describe, expect, it } from 'vitest';
import { parseTestFailure } from './parse-test-failure';

describe('parseTestFailure', () => {
	it('splits a wrong answer into input, expected and the student output', () => {
		const failure = parseTestFailure(
			'Assertion failed: Wrong answer.\nInput: nums = [1, 2], k = 3\nExpected: 2\nGot: 1'
		);
		expect(failure.title).toBe('Wrong answer');
		expect(failure.facts).toEqual([
			{ label: 'Input', value: 'nums = [1, 2], k = 3' },
			{ label: 'Expected', value: '2' },
			{ label: 'Your output', value: '1' }
		]);
	});

	it('keeps a multi-line output together', () => {
		const failure = parseTestFailure(
			'Wrong answer.\nInput: n = 2\nExpected: [[1], [2]]\nGot: [[1],\n [3]]'
		);
		expect(failure.facts[2].value).toBe('[[1],\n [3]]');
	});

	it('says a hidden test is hidden, and names a random case', () => {
		expect(parseTestFailure('Assertion failed: Wrong answer on a hidden test case.').note).toBe(
			'The input of this test is hidden.'
		);
		expect(parseTestFailure('Wrong answer on random case 44 of 300.').note).toBe(
			'Random case 44 of 300.'
		);
	});

	it('shows both numbers of a time limit failure', () => {
		const failure = parseTestFailure(
			'Assertion failed: Time limit exceeded: took 5031 ms, the limit is 1500 ms. The answer is right but too slow: look for a faster approach.'
		);
		expect(failure.title).toBe('Time limit exceeded');
		expect(failure.facts).toEqual([
			{ label: 'Your code', value: '5031 ms' },
			{ label: 'Limit', value: '1500 ms' }
		]);
	});

	it('handles a skipped performance test and too many reads', () => {
		expect(
			parseTestFailure('Skipped: an earlier performance test was already too slow.').title
		).toBe('Skipped');
		const reads = parseTestFailure(
			'Right answer, but too many reads: your code read the list 40 times and the limit is 5. Reading every value is not allowed here.'
		);
		expect(reads.title).toBe('Too many reads');
		expect(reads.facts[0].value).toBe('40 times');
	});

	it('titles a Python exception with its last line and keeps the traceback', () => {
		const failure = parseTestFailure(
			'Traceback (most recent call last):\n  File "<exec>", line 3, in f\nTypeError: unsupported operand type(s)'
		);
		expect(failure.title).toBe('TypeError: unsupported operand type(s)');
		expect(failure.trace).toContain('Traceback');
	});

	it('falls back to the first line for anything else', () => {
		expect(parseTestFailure('Something odd happened.').title).toBe('Something odd happened.');
	});
});
