import { describe, expect, it } from 'vitest';
import { istDateString, nextPotdRollover } from './ist-date-string';

describe('istDateString', () => {
	it('returns the IST calendar date regardless of the host timezone', () => {
		// 2026-09-14T18:29:59.999Z is 2026-09-14T23:59:59.999+05:30 (still Sep 14 IST).
		expect(istDateString(new Date('2026-09-14T18:29:59.999Z'))).toBe('2026-09-14');
		// 2026-09-14T18:30:00.000Z is 2026-09-15T00:00:00.000+05:30 (rolled to Sep 15 IST).
		expect(istDateString(new Date('2026-09-14T18:30:00.000Z'))).toBe('2026-09-15');
	});
});

describe('nextPotdRollover', () => {
	it('returns the next IST midnight after the given time, as a UTC instant', () => {
		expect(nextPotdRollover(new Date('2026-09-14T18:30:00Z')).toISOString()).toBe(
			'2026-09-15T18:30:00.000Z'
		);
		expect(nextPotdRollover(new Date('2026-09-15T18:29:59Z')).toISOString()).toBe(
			'2026-09-15T18:30:00.000Z'
		);
	});
});
