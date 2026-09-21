import { afterEach, describe, expect, it, vi } from 'vitest';

const originalTimeZone = process.env.TZ;

afterEach(() => {
	if (originalTimeZone === undefined) delete process.env.TZ;
	else process.env.TZ = originalTimeZone;
	vi.resetModules();
});

describe('POTD date labels', () => {
	it('preserves the scheduled calendar day west of UTC', async () => {
		process.env.TZ = 'America/New_York';
		vi.resetModules();

		const [{ questionsById }, { getPastPotdPart, getTodaysPotdPart }, display] = await Promise.all([
			import('$processes/ide-content/curriculum-index'),
			import('./get-potd-part'),
			import('./to-display-question')
		]);
		const generated = questionsById.values().next().value;
		if (!generated) throw new Error('Expected at least one generated curriculum question');

		const entry = { date: '2026-09-14', questionId: generated.id };
		expect(new Date(entry.date).getDate()).toBe(13);
		expect(display.parseLocalDateString(entry.date).getDate()).toBe(14);
		expect(display.toDisplayQuestion(generated, entry.date).question.title).toContain(
			'(September 14, 2026)'
		);

		const today = getTodaysPotdPart(new Date(2026, 8, 14, 12), [entry]);
		expect(today[0].tracks[0].name).toBe('September 14, 2026');

		const past = getPastPotdPart(new Date(2026, 8, 15, 12), [entry]);
		expect(past[0].tracks[0].name).toBe('September 14, 2026');
	});
});
