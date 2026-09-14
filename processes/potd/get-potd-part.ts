import type { Part } from '$data/questions';
import { potdEntries, type PotdEntry } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { toDisplayQuestion } from './to-display-question';
import { localDateString } from './get-todays-potd';

const MONTH_FORMAT = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' });
const FULL_DATE_FORMAT = new Intl.DateTimeFormat('en-US', {
	month: 'long',
	day: 'numeric',
	year: 'numeric'
});

function monthLabel(dateStr: string): string {
	// 'YYYY-MM-DD' parses as UTC midnight -- fine here, this only ever
	// feeds a month/year display label, never a same-day comparison (that
	// split is done via localDateString, on purpose using local time).
	return MONTH_FORMAT.format(new Date(dateStr));
}

function resolveEntries(entries: PotdEntry[]) {
	return entries
		.map((entry) => ({ entry, generated: questionsById.get(entry.questionId) }))
		// An entry whose id no longer matches a real question (typo, or the
		// question was renamed) is dropped rather than crashing the page --
		// same "don't let one bad row break everything" posture as the rest
		// of this codebase's content pipelines.
		.filter((r): r is { entry: PotdEntry; generated: NonNullable<typeof r.generated> } =>
			Boolean(r.generated)
		)
		.sort((a, b) => b.entry.date.localeCompare(a.entry.date));
}

// A single Part holding just the entry scheduled for the caller's local
// calendar date (if any), titled with that actual date -- mirrors
// getTodaysPotd's own local-time "today", so the hero card and this list
// entry always agree on what counts as today. Callers on the prerendered
// static build must only call this client-side (guarded by `browser`),
// same reason as getTodaysPotd: there's no real visitor "now" at build
// time.
export function getTodaysPotdPart(now: Date = new Date(), entries: PotdEntry[] = potdEntries): Part[] {
	const today = localDateString(now);
	const match = resolveEntries(entries).find((r) => r.entry.date === today);
	if (!match) return [];

	return [
		{
			id: 'potd-today',
			title: `Today's Problem (${FULL_DATE_FORMAT.format(now)})`,
			tracks: [
				{
					name: monthLabel(match.entry.date),
					questions: [toDisplayQuestion(match.generated).question]
				}
			]
		}
	];
}

// One Part, titled "Past Problems", holding every entry OTHER than
// today's, sub-grouped into a Track per month (newest first) -- reuses
// ModuleSection/QuestionFilters/Pagination exactly as the Questions page
// does. Browser-guarded for the same reason as getTodaysPotdPart: getting
// "today" wrong at build time would misfile today's entry into this list
// instead of the one above.
export function getPastPotdPart(now: Date = new Date(), entries: PotdEntry[] = potdEntries): Part[] {
	const today = localDateString(now);
	const resolved = resolveEntries(entries).filter((r) => r.entry.date !== today);

	if (resolved.length === 0) return [];

	const monthOrder: string[] = [];
	const byMonth = new Map<string, typeof resolved>();
	for (const item of resolved) {
		const label = monthLabel(item.entry.date);
		if (!byMonth.has(label)) {
			byMonth.set(label, []);
			monthOrder.push(label);
		}
		byMonth.get(label)!.push(item);
	}

	return [
		{
			id: 'potd-past',
			title: 'Past Problems',
			tracks: monthOrder.map((label) => ({
				name: label,
				questions: byMonth.get(label)!.map(({ generated }) => toDisplayQuestion(generated).question)
			}))
		}
	];
}
