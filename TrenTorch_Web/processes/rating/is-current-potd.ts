import { potdEntries } from '$data/potd';
import { utcDateString } from '$processes/potd/utc-date-string';

export function isCurrentPotd(questionId: string, now = new Date()): boolean {
	const today = utcDateString(now);
	return potdEntries.some((entry) => entry.questionId === questionId && entry.date === today);
}
