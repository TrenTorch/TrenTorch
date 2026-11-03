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
	/** How many lines of the starter `code` covers; see previewParts. */
	lines: number;
	/** How many lines the whole starter has: a student's saved code of another length has been changed. */
	total: number;
	/** What it is about, from its tags: "Caching · Hit Rate". */
	where: string;
}

const MAX_LINES = 14;
const MAX_CHARS = 640;

// A signature a formatter wrapped over several lines ("def f(", the parameters, ") -> float:") reads as one
// line in a preview; spending three of its few lines on it would crowd out the body.
const WRAPPED_DEF = /^(\s*(?:async\s+)?def\s+\w+\()$/;

export interface Row {
	text: string;
	/** The starter's own lines, when this row joined several. */
	original?: string[];
	/** How many lines of the starter this row stands for. */
	consumed: number;
}

export function toRows(lines: string[]): Row[] {
	const rows: Row[] = [];
	for (let i = 0; i < lines.length; i++) {
		const open = WRAPPED_DEF.exec(lines[i]);
		const close = open ? lines.findIndex((l, j) => j > i && /^\s*\)/.test(l)) : -1;
		if (!open || close === -1) {
			rows.push({ text: lines[i], consumed: 1 });
			continue;
		}
		const params = lines
			.slice(i + 1, close)
			.map((l) => l.trim())
			.join(' ')
			.replace(/,$/, '');
		rows.push({
			text: `${open[1]}${params}${lines[close].trim()}`,
			consumed: close - i + 1,
			original: lines.slice(i, close + 1)
		});
		i = close;
	}
	return rows;
}

/**
 * The first lines of a starter, cut at a line end, with a hint that there is more -- and how many of the
 * starter's own lines that covers (a joined signature covers several), so an edit can be put back in place.
 * `room` lets code a student has already written run a few lines longer, so an edit near the end still shows.
 */
export function previewParts(starter: string, room = 0): { code: string; lines: number } {
	const all = starter.replace(/\s+$/, '').split('\n');
	const rows = toRows(all);
	let used = 0;
	const kept: Row[] = [];
	for (const row of rows) {
		if (kept.length >= MAX_LINES + room || used + row.text.length > MAX_CHARS + room * 45) break;
		kept.push(row);
		used += row.text.length + 1;
	}
	// Never end on the hint alone: a preview of nothing helps nobody.
	if (kept.length === 0) kept.push({ text: all[0].slice(0, MAX_CHARS), consumed: 1 });
	const lines = kept.reduce((sum, row) => sum + row.consumed, 0);
	const text = kept.map((row) => row.text).join('\n');
	return { code: lines < all.length ? `${text}\n    # ...` : text, lines };
}

export function previewCode(starter: string): string {
	return previewParts(starter).code;
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
		const { code, lines } = previewParts(question.starterCode);
		return [
			{
				date: entry.date,
				id: question.id,
				title: question.title,
				difficulty: shown.question.difficulty,
				file: previewFile(question.starterCode, question.id),
				code,
				lines,
				total: question.starterCode.replace(/\s+$/, '').split('\n').length,
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
