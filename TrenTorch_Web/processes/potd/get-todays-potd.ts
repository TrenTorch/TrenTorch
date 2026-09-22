import { potdEntries } from '$data/potd';
import { toDisplayQuestion, type PotdDisplayQuestion } from './to-display-question';
import { localDateString } from './local-date-string';
import type { PotdSummary } from './potd-summary';

// Local time on purpose (not UTC): "today" should match the calendar date
// on the student's own clock, the same day they'd expect to see change at
// their own midnight, not somewhere else's. Callers on the prerendered
// static build must only call this client-side (guarded by `browser`) --
// there's no real visitor "now" at build time.
export function getTodaysPotd(
	summaries: PotdSummary[],
	now: Date = new Date()
): PotdDisplayQuestion | undefined {
	const today = localDateString(now);
	const entry = potdEntries.find((e) => e.date === today);
	if (!entry) return undefined;
	const summary = summaries.find((s) => s.id === entry.questionId);
	return summary ? toDisplayQuestion(summary, entry.date) : undefined;
}
