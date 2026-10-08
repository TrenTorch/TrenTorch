import { describe, it, expect } from 'vitest';
import { getPotdForDate } from './get-potd-for-date';
import { formatTopic } from './format-topic';
import type { PotdSummary } from './potd-summary';

const summary = (id: string, title: string): PotdSummary => ({
	id,
	title,
	difficulty: 'Beginner',
	tags: ['linear-algebra'],
	root: 'potd',
	section: 'daily',
	track: 'potd'
});
const summaries = [summary('q-one', 'ONE'), summary('q-two', 'TWO')];
const entries = [
	{ date: '2026-10-08', questionId: 'q-one' },
	{ date: '2026-10-09', questionId: 'q-two' },
	{ date: '2026-10-10', questionId: 'missing-question' }
];

describe('getPotdForDate', () => {
	it('returns the summary scheduled for the date', () => {
		expect(getPotdForDate(summaries, '2026-10-09', entries)?.title).toBe('TWO');
	});
	it('returns undefined when nothing is scheduled for the date', () => {
		expect(getPotdForDate(summaries, '2026-10-11', entries)).toBeUndefined();
	});
	it('returns undefined when the scheduled question has no summary', () => {
		expect(getPotdForDate(summaries, '2026-10-10', entries)).toBeUndefined();
	});
});

describe('formatTopic', () => {
	it('turns a kebab-case tag into capitalised words', () => {
		expect(formatTopic('linear-algebra')).toBe('Linear Algebra');
		expect(formatTopic('optimization')).toBe('Optimization');
	});
	it('keeps acronyms upper-case', () => {
		expect(formatTopic('classical-ml')).toBe('Classical ML');
		expect(formatTopic('nlp')).toBe('NLP');
		expect(formatTopic('mlops')).toBe('MLOps');
	});
});
