import type { Part } from '$data/questions';
import { potdEntries, type PotdEntry } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { toDisplayQuestion } from './to-display-question';

const MONTH_FORMAT = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' });

function monthLabel(dateStr: string): string {
	// 'YYYY-MM-DD' parses as UTC midnight -- fine here, this only ever
	// feeds a month/year display label, never a same-day comparison
	// (that's getTodaysPotd's job, and it uses local time on purpose).
	return MONTH_FORMAT.format(new Date(dateStr));
}

// One Part, titled "Problems of the Day", sub-grouped into a Track per
// month (newest first) -- reuses ModuleSection/QuestionFilters/Pagination
// exactly as the Questions page does, rather than a bespoke layout, so the
// two pages genuinely share styling and behavior instead of just looking
// similar.
export function getPotdPart(entries: PotdEntry[] = potdEntries): Part[] {
	const resolved = entries
		.map((entry) => ({ entry, generated: questionsById.get(entry.questionId) }))
		// An entry whose id no longer matches a real question (typo, or the
		// question was renamed) is dropped rather than crashing the page --
		// same "don't let one bad row break everything" posture as the rest
		// of this codebase's content pipelines.
		.filter((r): r is { entry: PotdEntry; generated: NonNullable<typeof r.generated> } =>
			Boolean(r.generated)
		)
		.sort((a, b) => b.entry.date.localeCompare(a.entry.date));

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
			id: 'potd',
			title: 'Problems of the Day',
			tracks: monthOrder.map((label) => ({
				name: label,
				questions: byMonth.get(label)!.map(({ generated }) => toDisplayQuestion(generated).question)
			}))
		}
	];
}
