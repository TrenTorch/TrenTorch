import { describe, it, expect } from 'vitest';
import { potdEntries } from './potd';
import { questionsById } from '$processes/ide-content/curriculum-index';

describe('potd schedule', () => {
	it('every entry points at a real question (a wrong id is silently dropped at runtime)', () => {
		const missing = potdEntries.filter((e) => !questionsById.has(e.questionId));
		expect(missing).toEqual([]);
	});

	it('every date is a real YYYY-MM-DD calendar date', () => {
		for (const { date } of potdEntries) {
			expect(date).toMatch(/^\d{4}-\d{2}-\d{2}$/);
			const parsed = new Date(`${date}T00:00:00Z`);
			expect(parsed.toISOString().slice(0, 10)).toBe(date);
		}
	});

	it('has one entry per date', () => {
		const dates = potdEntries.map((e) => e.date);
		expect(new Set(dates).size).toBe(dates.length);
	});

	it('never schedules the same question twice', () => {
		const ids = potdEntries.map((e) => e.questionId);
		expect(new Set(ids).size).toBe(ids.length);
	});

	it('is in ascending date order, so the newest entry is always last', () => {
		const dates = potdEntries.map((e) => e.date);
		expect(dates).toEqual([...dates].sort());
	});
});
