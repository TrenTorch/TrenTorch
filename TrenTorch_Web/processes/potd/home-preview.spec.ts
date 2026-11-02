import { describe, expect, it } from 'vitest';
import { buildHomePreviews, pickPreview, previewCode, previewFile } from './home-preview';
import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';

const question = (id: string, starterCode: string): GeneratedQuestion =>
	({
		id,
		title: id.toUpperCase(),
		difficulty: 'Intermediate',
		tags: ['caching', 'hit-rate', 'third'],
		root: 'deep-learning',
		section: 's',
		track: 'core-mechanics',
		starterCode
	}) as unknown as GeneratedQuestion;

describe('previewCode', () => {
	it('keeps a short starter whole, without trailing blank lines', () => {
		expect(previewCode('def f(x):\n    return x\n\n\n')).toBe('def f(x):\n    return x');
	});

	it('cuts a long starter at a line end and says there is more', () => {
		const long = Array.from({ length: 40 }, (_, i) => `line${i} = ${i}`).join('\n');
		const shown = previewCode(long).split('\n');
		expect(shown.length).toBeLessThanOrEqual(15);
		expect(shown.at(-1)).toBe('    # ...');
		expect(shown[0]).toBe('line0 = 0');
	});

	it('keeps something even when the first line alone is too long', () => {
		expect(previewCode('x = ' + '1'.repeat(2000)).length).toBeLessThan(700);
	});
});

describe('previewFile', () => {
	it('names the file after the first function', () => {
		expect(previewFile('import numpy as np\n\ndef softmax(x):\n    pass', 'q')).toBe('softmax.py');
	});
	it('falls back to the question id', () => {
		expect(previewFile('x = 1', 'some-question')).toBe('some-question.py');
	});
});

describe('buildHomePreviews', () => {
	const entries = [
		{ date: '2026-10-01', questionId: 'old' },
		{ date: '2026-10-02', questionId: 'gone' },
		{ date: '2026-10-03', questionId: 'blank' },
		{ date: '2026-10-04', questionId: 'new' }
	];
	const known = new Map([
		['old', question('old', 'def a():\n    pass')],
		['blank', question('blank', '')],
		['new', question('new', 'def b(x):\n    return x')]
	]);

	it('keeps days from the given one, drops missing and empty questions, and fills in the fields', () => {
		const previews = buildHomePreviews(entries, (id) => known.get(id), '2026-10-02').filter(
			(p) => p.date >= '2026-10-02'
		);
		expect(previews).toEqual([
			{
				date: '2026-10-04',
				id: 'new',
				title: 'NEW',
				difficulty: 'Medium',
				file: 'b.py',
				code: 'def b(x):\n    return x',
				where: 'Caching · Hit Rate'
			}
		]);
	});
});

describe('buildHomePreviews, when the schedule is behind it', () => {
	const entries = [
		{ date: '2026-09-14', questionId: 'a' },
		{ date: '2026-09-15', questionId: 'b' }
	];
	const known = new Map([
		['a', question('a', 'def a():\n    pass')],
		['b', question('b', 'def b():\n    pass')]
	]);

	it('still keeps the latest earlier day, so there is always something to show', () => {
		const previews = buildHomePreviews(entries, (id) => known.get(id), '2026-10-28');
		expect(previews.map((p) => p.date)).toEqual(['2026-09-15']);
	});

	it('does not keep it as well when a day from the given one on exists', () => {
		const more = [...entries, { date: '2026-10-29', questionId: 'a' }];
		expect(buildHomePreviews(more, (id) => known.get(id), '2026-10-28').map((p) => p.date)).toEqual(
			['2026-09-15', '2026-10-29']
		);
	});

	it('skips an earlier day whose starter is missing and takes the one before it', () => {
		const blank = new Map([...known, ['b', question('b', '')]]);
		expect(
			buildHomePreviews(entries, (id) => blank.get(id), '2026-10-28').map((p) => p.date)
		).toEqual(['2026-09-14']);
	});
});

describe('pickPreview', () => {
	const at = (date: string) => ({ date }) as never;
	const previews = [at('2026-10-10'), at('2026-10-11'), at('2026-10-13')];

	it("picks the day's own", () => {
		expect(pickPreview(previews, '2026-10-11')).toBe(previews[1]);
	});
	it('falls back to the last earlier day, then to the first later one', () => {
		expect(pickPreview(previews, '2026-10-12')).toBe(previews[1]);
		expect(pickPreview(previews, '2026-12-30')).toBe(previews[2]);
		expect(pickPreview(previews, '2026-09-01')).toBe(previews[0]);
	});
	it('is nothing when there are no previews', () => {
		expect(pickPreview([], '2026-10-11')).toBeUndefined();
	});
});
