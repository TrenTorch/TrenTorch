import { describe, it, expect } from 'vitest';
import { potdEntries } from '$data/potd';
import { getTodaysPotdPart, getPastPotdPart } from './get-potd-part';
import { getTodaysPotd } from './get-todays-potd';
import { localDateString } from './local-date-string';
import type { PotdSummary } from './potd-summary';

const summary = (id: string, title: string): PotdSummary => ({
	id,
	title,
	difficulty: 'Beginner',
	tags: ['classical-ml'],
	section: 'classical-ml',
	track: 'linear-models'
});

const summaries = [summary('q-one', 'One'), summary('q-two', 'Two'), summary('q-three', 'Three')];
const entries = [
	{ date: '2026-09-14', questionId: 'q-one' },
	{ date: '2026-09-15', questionId: 'q-two' },
	{ date: '2026-09-16', questionId: 'not-in-the-summaries' },
	{ date: '2026-09-18', questionId: 'q-three' }
];
// Local noon on 15 September 2026, the day of q-two.
const today = new Date(2026, 8, 15, 12);

describe('POTD lists, built from server-provided summaries', () => {
	it("today's part holds only the entry scheduled for today, with a plain title", () => {
		const [part] = getTodaysPotdPart(summaries, today, entries);
		expect(part.id).toBe('potd-today');
		expect(part.title).toBe("Today's Problem");
		const [question] = part.tracks[0].questions;
		expect(question.slug).toBe('q-two');
		expect(question.title).toBe('Two');
	});

	it('past problems holds only days strictly before today, never today or a future one', () => {
		const [part] = getPastPotdPart(summaries, today, entries);
		const slugs = part.tracks.flatMap((track) => track.questions.map((q) => q.slug));
		expect(slugs).toEqual(['q-one']);
	});

	it('drops an entry that has no matching summary instead of failing', () => {
		const later = new Date(2026, 8, 20, 12);
		const [part] = getPastPotdPart(summaries, later, entries);
		const slugs = part.tracks.flatMap((track) => track.questions.map((q) => q.slug));
		// Newest first. The 16th's entry has no summary, so it is skipped.
		expect(slugs).toEqual(['q-three', 'q-two', 'q-one']);
	});

	it('shows nothing on a day with no entry', () => {
		expect(getTodaysPotdPart(summaries, new Date(2026, 8, 17, 12), entries)).toEqual([]);
	});

	it("getTodaysPotd resolves the real schedule's first entry on its own date", () => {
		const first = potdEntries[0];
		const [year, month, day] = first.date.split('-').map(Number);
		const found = getTodaysPotd(
			[summary(first.questionId, 'The first problem')],
			new Date(year, month - 1, day, 12)
		);
		expect(found?.question.slug).toBe(first.questionId);
	});

	it("localDateString reads the visitor's own calendar date", () => {
		expect(localDateString(new Date(2026, 0, 5, 23, 59))).toBe('2026-01-05');
		expect(localDateString(new Date(2026, 11, 31, 0, 1))).toBe('2026-12-31');
	});
});
