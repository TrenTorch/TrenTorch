import { potdEntries } from '$data/potd';
import { toDisplayQuestion, type PotdDisplayQuestion } from './to-display-question';
import { utcDateString } from './utc-date-string';
import type { PotdSummary } from './potd-summary';

// UTC on purpose: the database decides which POTD may be rated by the UTC
// date (see supabase/migrations/*_guard_potd_rating_events.sql), so "today"
// here has to be the same day everywhere, or a student whose local date has
// already rolled over would be shown a POTD the server still treats as
// tomorrow's. The banner shows when it resets in the student's own time.
// Callers on the prerendered
// static build must only call this client-side (guarded by `browser`) --
// there's no real visitor "now" at build time.
export function getTodaysPotd(
	summaries: PotdSummary[],
	now: Date = new Date()
): PotdDisplayQuestion | undefined {
	const today = utcDateString(now);
	const entry = potdEntries.find((e) => e.date === today);
	if (!entry) return undefined;
	const summary = summaries.find((s) => s.id === entry.questionId);
	return summary ? toDisplayQuestion(summary) : undefined;
}
