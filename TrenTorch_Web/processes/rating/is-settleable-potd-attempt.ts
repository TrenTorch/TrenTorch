import { potdEntries } from '$data/potd';
import { istDateString } from '$processes/potd/ist-date-string';

export function isSettleablePotdAttempt(
	questionId: string,
	firstAttemptedAt: string,
	solved: boolean,
	now = new Date()
): boolean {
	if (solved) return false;
	const entry = potdEntries.find((potd) => potd.questionId === questionId);
	if (!entry || entry.date >= istDateString(now)) return false;
	return istDateString(new Date(firstAttemptedAt)) === entry.date;
}
