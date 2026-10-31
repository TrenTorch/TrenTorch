import { describe, expect, it } from 'vitest';
import { isCurrentPotd, isUpcomingPotd } from './is-current-potd';

describe('isCurrentPotd', () => {
	it('only matches the question scheduled for the current local date', () => {
		const potdQuestion = 'regularized-linear-models-ridge-regression-gaussian-elimination';

		expect(isCurrentPotd(potdQuestion, new Date('2026-09-14T12:00:00Z'))).toBe(true);
		expect(isCurrentPotd(potdQuestion, new Date('2026-09-15T00:00:00Z'))).toBe(false);
		expect(isCurrentPotd('not-a-potd', new Date('2026-09-14T12:00:00Z'))).toBe(false);
	});
});

describe('isUpcomingPotd', () => {
	const potdQuestion = 'regularized-linear-models-ridge-regression-gaussian-elimination';

	it('is true only while the UTC day has not reached the scheduled date', () => {
		// 2026-09-14 02:00 IST is still 2026-09-13 in UTC.
		expect(isUpcomingPotd(potdQuestion, new Date('2026-09-13T20:30:00Z'))).toBe(true);
		expect(isUpcomingPotd(potdQuestion, new Date('2026-09-14T00:00:00Z'))).toBe(false);
		expect(isUpcomingPotd(potdQuestion, new Date('2026-09-15T00:00:00Z'))).toBe(false);
		expect(isUpcomingPotd('not-a-potd', new Date('2026-09-13T20:30:00Z'))).toBe(false);
	});
});
