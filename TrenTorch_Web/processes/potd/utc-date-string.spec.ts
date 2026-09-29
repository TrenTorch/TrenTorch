import { describe, expect, it } from 'vitest';
import { utcDateString } from './utc-date-string';

describe('utcDateString', () => {
	it('returns the UTC calendar date regardless of the host timezone', () => {
		expect(utcDateString(new Date('2026-09-14T23:59:59.999Z'))).toBe('2026-09-14');
		expect(utcDateString(new Date('2026-09-15T00:00:00.000Z'))).toBe('2026-09-15');
	});
});
