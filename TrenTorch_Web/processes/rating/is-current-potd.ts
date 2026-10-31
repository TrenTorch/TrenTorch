import { potdEntries } from '$data/potd';
import { utcDateString } from '$processes/potd/utc-date-string';

export function isCurrentPotd(questionId: string, now = new Date()): boolean {
	const today = utcDateString(now);
	return potdEntries.some((entry) => entry.questionId === questionId && entry.date === today);
}

// Scheduled for a UTC day that has not started yet (e.g. the local calendar is
// already on the next date). Its rating window opens at 00:00 UTC.
export function isUpcomingPotd(questionId: string, now = new Date()): boolean {
	const today = utcDateString(now);
	return potdEntries.some((entry) => entry.questionId === questionId && entry.date > today);
}
