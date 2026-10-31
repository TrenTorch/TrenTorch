import { potdEntries } from '$data/potd';
import { toDisplayQuestion, type PotdDisplayQuestion } from './to-display-question';
import { istDateString } from './ist-date-string';
import type { PotdSummary } from './potd-summary';

// IST on purpose (not the visitor's own local date): POTD is a single
// globally-shared problem, and the rating-eligibility check (isCurrentPotd)
// also anchors to IST, so this must agree with it or a solve can be served
// as "today's" here while being rejected there. Callers on the prerendered
// static build must only call this client-side (guarded by `browser`) --
// there's no real visitor "now" at build time.
export function getTodaysPotd(
	summaries: PotdSummary[],
	now: Date = new Date()
): PotdDisplayQuestion | undefined {
	const today = istDateString(now);
	const entry = potdEntries.find((e) => e.date === today);
	if (!entry) return undefined;
	const summary = summaries.find((s) => s.id === entry.questionId);
	return summary ? toDisplayQuestion(summary) : undefined;
}
