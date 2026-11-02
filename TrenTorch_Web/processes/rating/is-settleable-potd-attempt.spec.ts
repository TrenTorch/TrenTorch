import { describe, expect, it } from 'vitest';
import { isSettleablePotdAttempt } from './is-settleable-potd-attempt';

describe('isSettleablePotdAttempt', () => {
	const questionId = 'regularized-linear-models-ridge-regression-gaussian-elimination';
	const now = new Date('2026-09-15T12:00:00Z');

	it('settles only an unsolved attempt made on its scheduled POTD date', () => {
		expect(isSettleablePotdAttempt(questionId, '2026-09-14T13:00:00Z', false, now)).toBe(true);
		expect(isSettleablePotdAttempt(questionId, '2026-09-14T13:00:00Z', true, now)).toBe(false);
		expect(isSettleablePotdAttempt(questionId, '2026-09-15T13:00:00Z', false, now)).toBe(false);
	});

	it('does not settle attempts for the current POTD or a non-POTD question', () => {
		// 2026-09-14T18:00:00Z is still 2026-09-14 in IST (23:30 IST), the
		// entry's own day, so the question is still "today's" and unsettled.
		expect(
			isSettleablePotdAttempt(
				questionId,
				'2026-09-14T13:00:00Z',
				false,
				new Date('2026-09-14T18:00:00Z')
			)
		).toBe(false);
		expect(isSettleablePotdAttempt('not-a-potd', '2026-09-14T13:00:00Z', false, now)).toBe(false);
	});
});
