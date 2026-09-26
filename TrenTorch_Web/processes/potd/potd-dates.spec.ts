import { afterEach, describe, expect, it, vi } from 'vitest';
import type { PotdSummary } from './potd-summary';

const originalTimeZone = process.env.TZ;

afterEach(() => {
	if (originalTimeZone === undefined) delete process.env.TZ;
	else process.env.TZ = originalTimeZone;
	vi.resetModules();
});

const summary: PotdSummary = {
	id: 'q-one',
	title: 'One',
	difficulty: 'Beginner',
	tags: ['classical-ml'],
	section: 'classical-ml',
	track: 'linear-models'
};

describe('POTD date labels', () => {
	it('preserves the scheduled calendar day west of UTC', async () => {
		process.env.TZ = 'America/New_York';
		vi.resetModules();

		const [{ getPastPotdPart, getTodaysPotdPart }, display] = await Promise.all([
			import('./get-potd-part'),
			import('./to-display-question')
		]);

		const entry = { date: '2026-09-14', questionId: summary.id };
		expect(new Date(entry.date).getDate()).toBe(13);
		expect(display.parseLocalDateString(entry.date).getDate()).toBe(14);
		expect(display.toDisplayQuestion(summary, entry.date).question.title).toBe('One');

		const today = getTodaysPotdPart([summary], new Date(2026, 8, 14, 12), [entry]);
		expect(today[0].tracks[0].name).toBe('September 14, 2026');

		const past = getPastPotdPart([summary], new Date(2026, 8, 15, 12), [entry]);
		expect(past[0].tracks[0].name).toBe('September 14, 2026');
	});
});
