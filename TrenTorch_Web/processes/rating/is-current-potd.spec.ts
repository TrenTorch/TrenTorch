import { describe, expect, it } from 'vitest';
import { isCurrentPotd, isUpcomingPotd } from './is-current-potd';

const potdQuestion = 'regularized-linear-models-ridge-regression-gaussian-elimination';

describe('isCurrentPotd', () => {
	it('only matches the question scheduled for the current IST calendar date', () => {
		// IST rolls from 2026-09-14 to 2026-09-15 at 2026-09-14T18:30:00Z.
		expect(isCurrentPotd(potdQuestion, new Date('2026-09-14T18:29:59Z'))).toBe(true);
		expect(isCurrentPotd(potdQuestion, new Date('2026-09-14T18:30:00Z'))).toBe(false);
		expect(isCurrentPotd('not-a-potd', new Date('2026-09-14T12:00:00Z'))).toBe(false);
	});
});

describe('isUpcomingPotd', () => {
	it('is true only before the IST day the question is scheduled for', () => {
		// 2026-09-14 in IST starts at 2026-09-13T18:30:00Z.
		expect(isUpcomingPotd(potdQuestion, new Date('2026-09-13T18:29:59Z'))).toBe(true);
		expect(isUpcomingPotd(potdQuestion, new Date('2026-09-13T18:30:00Z'))).toBe(false);
		expect(isUpcomingPotd(potdQuestion, new Date('2026-09-15T00:00:00Z'))).toBe(false);
		expect(isUpcomingPotd('not-a-potd', new Date('2026-09-01T00:00:00Z'))).toBe(false);
	});
});
