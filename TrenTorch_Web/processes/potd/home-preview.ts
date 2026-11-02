import type { PotdEntry } from '$data/potd';
import type { Difficulty } from '$data/questions';
import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';
import { toDisplayQuestion } from './to-display-question';
import { formatTopic } from './format-topic';
import { toPotdSummary } from './potd-summary';

// What the home page shows of a Problem of the Day in its code window: the start of the starter code, a file
// name, and a line saying where it sits. Built at build time for the days that are still to come (and the
// last couple that have passed), so the page carries a few hundred bytes per day and not the curriculum.

export interface HomePotdPreview {
	date: string;
	id: string;
	title: string;
	difficulty: Difficulty;
	file: string;
	code: string;
	/** What it is about, from its tags: "Caching · Hit Rate". */
	where: string;
}

const MAX_LINES = 14;
const MAX_CHARS = 640;

/** The first lines of a starter, cut at a line end, with a hint that there is more. */
export function previewCode(starter: string): string {
	const lines = starter.replace(/\s+$/, '').split('\n');
	let used = 0;
	const kept: string[] = [];
	for (const line of lines) {
		if (kept.length >= MAX_LINES || used + line.length > MAX_CHARS) break;
		kept.push(line);
		used += line.length + 1;
	}
	// Never end on the hint alone: a preview of nothing helps nobody.
	if (kept.length === 0) kept.push(lines[0].slice(0, MAX_CHARS));
	return kept.length < lines.length ? `${kept.join('\n')}\n    # ...` : kept.join('\n');
}

/** `def softmax(x):` is shown as softmax.py; a starter with no function falls back to the question's id. */
export function previewFile(starter: string, fallback: string): string {
	return `${starter.match(/^\s*def\s+([A-Za-z_]\w*)/m)?.[1] ?? fallback}.py`;
}

export function buildHomePreviews(
	entries: PotdEntry[],
	find: (id: string) => GeneratedQuestion | undefined,
	/** The first day to keep, "YYYY-MM-DD": earlier entries are left out, except the last of them (below). */
	from: string
): HomePotdPreview[] {
	// The latest earlier day stays as a fallback, so a page built after the schedule has run out (or with
	// nothing scheduled near today) still has a real problem to show rather than an empty window.
	const earlier = entries
		.filter((entry) => entry.date < from && find(entry.questionId)?.starterCode)
		.sort((a, b) => b.date.localeCompare(a.date))
		.slice(0, 1);
	return [...earlier, ...entries.filter((entry) => entry.date >= from)].flatMap((entry) => {
		const question = find(entry.questionId);
		if (!question?.starterCode) return [];
		const shown = toDisplayQuestion(toPotdSummary(question));
		return [
			{
				date: entry.date,
				id: question.id,
				title: question.title,
				difficulty: shown.question.difficulty,
				file: previewFile(question.starterCode, question.id),
				code: previewCode(question.starterCode),
				where: shown.question.topics.slice(0, 2).map(formatTopic).join(' · ')
			}
		];
	});
}

/**
 * The preview for a day: that day's if there is one, else the last one before it, else the first after. A day
 * with no entry (the schedule ran out, or the page is older than the schedule) still gets a real problem.
 */
export function pickPreview(previews: HomePotdPreview[], day: string): HomePotdPreview | undefined {
	return (
		previews.find((p) => p.date === day) ??
		[...previews].reverse().find((p) => p.date < day) ??
		previews.find((p) => p.date > day)
	);
}
