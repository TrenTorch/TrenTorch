import { potdEntries } from '$data/potd';
import { utcDateString } from '$processes/potd/utc-date-string';

export function isSettleablePotdAttempt(
	questionId: string,
	firstAttemptedAt: string,
	solved: boolean,
	now = new Date()
): boolean {
	if (solved) return false;
	const entry = potdEntries.find((potd) => potd.questionId === questionId);
	if (!entry || entry.date >= utcDateString(now)) return false;
	return utcDateString(new Date(firstAttemptedAt)) === entry.date;
}
