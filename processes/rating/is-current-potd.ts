import { potdEntries } from '$data/potd';
import { localDateString } from '$processes/potd/local-date-string';

// Local time on purpose, matching getTodaysPotd: whatever entry the
// student's own homepage/POTD list calls "today's" is the one a solve here
// must also count as current, or a solve of the question they were just
// shown as today's POTD gets wrongly treated as a past one.
export function isCurrentPotd(questionId: string, now = new Date()): boolean {
	const today = localDateString(now);
	return potdEntries.some((entry) => entry.questionId === questionId && entry.date === today);
}
