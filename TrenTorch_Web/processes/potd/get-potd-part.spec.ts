import { describe, it, expect } from 'vitest';
import { potdEntries } from '$data/potd';
import { getTodaysPotdPart, getPastPotdPart } from './get-potd-part';
import { getTodaysPotd } from './get-todays-potd';
import { istDateString } from './ist-date-string';
import type { PotdSummary } from './potd-summary';

const summary = (id: string, title: string): PotdSummary => ({
	id,
	title,
	difficulty: 'Beginner',
	tags: ['classical-ml'],
	root: 'classical-ml',
	section: 'supervised-models',
	track: 'linear-models'
});

const summaries = [summary('q-one', 'One'), summary('q-two', 'Two'), summary('q-three', 'Three')];
const entries = [
	{ date: '2026-09-14', questionId: 'q-one' },
	{ date: '2026-09-15', questionId: 'q-two' },
	{ date: '2026-09-16', questionId: 'not-in-the-summaries' },
	{ date: '2026-09-18', questionId: 'q-three' }
];
// IST noon on 15 September 2026 (06:30 UTC), the day of q-two.
const today = new Date('2026-09-15T06:30:00Z');

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
		const later = new Date('2026-09-20T06:30:00Z');
		const [part] = getPastPotdPart(summaries, later, entries);
		const slugs = part.tracks.flatMap((track) => track.questions.map((q) => q.slug));
		// Newest first. The 16th's entry has no summary, so it is skipped.
		expect(slugs).toEqual(['q-three', 'q-two', 'q-one']);
	});

	it('shows nothing on a day with no entry', () => {
		expect(getTodaysPotdPart(summaries, new Date('2026-09-17T06:30:00Z'), entries)).toEqual([]);
	});

	it("getTodaysPotd resolves the real schedule's first entry on its own IST date", () => {
		const first = potdEntries[0];
		const found = getTodaysPotd(
			[summary(first.questionId, 'The first problem')],
			new Date(`${first.date}T06:30:00Z`)
		);
		expect(found?.question.slug).toBe(first.questionId);
	});

	it('istDateString reads the IST calendar date regardless of the host timezone', () => {
		expect(istDateString(new Date('2026-01-05T18:29:00Z'))).toBe('2026-01-05');
		expect(istDateString(new Date('2026-01-05T18:30:00Z'))).toBe('2026-01-06');
	});
});
