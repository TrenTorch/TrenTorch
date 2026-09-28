import { describe, expect, it } from 'vitest';
import { isCurrentPotd } from './is-current-potd';

describe('isCurrentPotd', () => {
	it('only matches the question scheduled for the current UTC date', () => {
		const potdQuestion = 'regularized-linear-models-ridge-regression-gaussian-elimination';

		expect(isCurrentPotd(potdQuestion, new Date('2026-09-14T12:00:00Z'))).toBe(true);
		expect(isCurrentPotd(potdQuestion, new Date('2026-09-15T00:00:00Z'))).toBe(false);
		expect(isCurrentPotd('not-a-potd', new Date('2026-09-14T12:00:00Z'))).toBe(false);
	});
});
