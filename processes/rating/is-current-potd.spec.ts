import { describe, expect, it } from 'vitest';
import { isCurrentPotd } from './is-current-potd';

describe('isCurrentPotd', () => {
	it("only matches the question scheduled for the caller's current local date", () => {
		const potdQuestion = 'regularized-linear-models-ridge-regression-gaussian-elimination';

		expect(isCurrentPotd(potdQuestion, new Date(2026, 8, 14, 12))).toBe(true);
		expect(isCurrentPotd(potdQuestion, new Date(2026, 8, 15, 0))).toBe(false);
		expect(isCurrentPotd('not-a-potd', new Date(2026, 8, 14, 12))).toBe(false);
	});
});
