import type { Part } from '$data/questions';
import { potdEntries, type PotdEntry } from '$data/potd';
import { parseLocalDateString, toDisplayQuestion } from './to-display-question';
import { localDateString } from './local-date-string';
import type { PotdSummary } from './potd-summary';

const FULL_DATE_FORMAT = new Intl.DateTimeFormat('en-US', {
	month: 'long',
	day: 'numeric',
	year: 'numeric'
});

function resolveEntries(entries: PotdEntry[], summaries: PotdSummary[]) {
	const byId = new Map(summaries.map((s) => [s.id, s]));
	return (
		entries
			.map((entry) => ({ entry, generated: byId.get(entry.questionId) }))
			// An entry whose id no longer matches a real question (typo, or the
			// question was renamed) is dropped rather than crashing the page --
			// same "don't let one bad row break everything" posture as the rest
			// of this codebase's content pipelines.
			.filter((r): r is { entry: PotdEntry; generated: NonNullable<typeof r.generated> } =>
				Boolean(r.generated)
			)
			.sort((a, b) => b.entry.date.localeCompare(a.entry.date))
	);
}

// A single Part holding just the entry scheduled for the caller's local
// calendar date (if any), titled plainly -- the date already shows in the
// hero card above the list and in the row's own date pill, so repeating it
// in parentheses here was redundant. Mirrors getTodaysPotd's own
// local-time "today", so the hero card and this list entry always agree on
// what counts as today. Callers on the prerendered static build must only
// call this client-side (guarded by `browser`), same reason as
// getTodaysPotd: there's no real visitor "now" at build time.
export function getTodaysPotdPart(
	summaries: PotdSummary[],
	now: Date = new Date(),
	entries: PotdEntry[] = potdEntries
): Part[] {
	const today = localDateString(now);
	const match = resolveEntries(entries, summaries).find((r) => r.entry.date === today);
	if (!match) return [];

	return [
		{
			id: 'potd-today',
			title: "Today's Problem",
			tracks: [
				{
					name: FULL_DATE_FORMAT.format(parseLocalDateString(match.entry.date)),
					questions: [toDisplayQuestion(match.generated, match.entry.date).question]
				}
			]
		}
	];
}

// One Part, titled "Past Problems", holding every entry STRICTLY BEFORE
// today (never today, and never a future-scheduled entry -- a not-yet-
// revealed POTD must stay invisible until its own date arrives, the same
// way getTodaysPotdPart never shows one early), sub-grouped into a Track
// per exact date it ran (newest first) -- one question per day, so
// grouping by the full date (rather than by month) puts the date it was
// featured directly in each track's own centered header. The question rows
// themselves show just the plain question name (see toDisplayQuestion) --
// no parenthesized date repeat. Reuses PotdSection/QuestionFilters/
// Pagination exactly as the Questions page does. Browser-guarded for the
// same reason as getTodaysPotdPart: getting "today" wrong at build time
// would misfile today's (or a future) entry into this list instead of
// keeping it hidden.
export function getPastPotdPart(
	summaries: PotdSummary[],
	now: Date = new Date(),
	entries: PotdEntry[] = potdEntries
): Part[] {
	const today = localDateString(now);
	// Lexicographic comparison is correct here: dates are 'YYYY-MM-DD',
	// which sorts identically to chronological order.
	const resolved = resolveEntries(entries, summaries).filter((r) => r.entry.date < today);

	if (resolved.length === 0) return [];

	return [
		{
			id: 'potd-past',
			title: 'Past Problems',
			tracks: resolved.map((item) => ({
				name: FULL_DATE_FORMAT.format(parseLocalDateString(item.entry.date)),
				questions: [toDisplayQuestion(item.generated, item.entry.date).question]
			}))
		}
	];
}
