import { potdEntries } from '$data/potd';
import { istDateString } from '$processes/potd/ist-date-string';

export function isCurrentPotd(questionId: string, now = new Date()): boolean {
	const today = istDateString(now);
	return potdEntries.some((entry) => entry.questionId === questionId && entry.date === today);
}

// Scheduled for an IST day that has not started yet. Used to keep a queued
// solve until its rating window opens (see pending-potd-solves).
export function isUpcomingPotd(questionId: string, now = new Date()): boolean {
	const today = istDateString(now);
	return potdEntries.some((entry) => entry.questionId === questionId && entry.date > today);
}
