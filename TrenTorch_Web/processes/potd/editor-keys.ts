// Just enough editor behaviour for the landing page's plain textarea to be usable for Python: Tab indents
// (Shift+Tab dedents), and Enter keeps the line's indent, going one level deeper after a colon.

const INDENT = '    ';

/** Replace `value[from, to)` with `insert`, then select `[selStart, selEnd)` of the new text. */
export interface Edit {
	from: number;
	to: number;
	insert: string;
	selStart: number;
	selEnd: number;
}

const lineStart = (value: string, at: number) => value.lastIndexOf('\n', at - 1) + 1;

export function editForKey(
	value: string,
	start: number,
	end: number,
	key: 'Tab' | 'Enter',
	shift = false
): Edit | null {
	if (key === 'Enter') {
		if (shift) return null;
		const before = value.slice(lineStart(value, start), start);
		const indent = before.match(/^[ \t]*/)![0];
		const deeper = before.trimEnd().endsWith(':') ? INDENT : '';
		const insert = `\n${indent}${deeper}`;
		return {
			from: start,
			to: end,
			insert,
			selStart: start + insert.length,
			selEnd: start + insert.length
		};
	}

	const multiline = value.slice(start, end).includes('\n');
	if (!shift && !multiline) {
		// To the next multiple of four, as an editor does.
		const column = start - lineStart(value, start);
		const insert = INDENT.slice(column % INDENT.length);
		return {
			from: start,
			to: end,
			insert,
			selStart: start + insert.length,
			selEnd: start + insert.length
		};
	}

	// Whole lines from here on: every line the selection touches.
	const from = lineStart(value, start);
	const lastEnd = end > start && value[end - 1] === '\n' ? end - 1 : end;
	const nextBreak = value.indexOf('\n', lastEnd);
	const to = nextBreak === -1 ? value.length : nextBreak;
	const lines = value.slice(from, to).split('\n');
	const changed = lines.map((line) =>
		shift ? line.replace(/^ {1,4}|^\t/, '') : line.trim() === '' ? line : INDENT + line
	);
	const insert = changed.join('\n');
	const delta = (i: number) => changed[i].length - lines[i].length;
	const first = delta(0);
	const total = changed.reduce((sum, _, i) => sum + delta(i), 0);
	return {
		from,
		to,
		insert,
		selStart: Math.max(from, start + first),
		selEnd: Math.max(from, end + total)
	};
}

// The preview's function signature is shown as-is and cannot be edited: it is the one line the starter's
// tests and the rest of the file depend on. These work out whether an edit would touch it.

/** The `def` line, as it is shown in a preview. */
export const SIGNATURE_LINE = /^\s*(?:async\s+)?def\s/;

/** Start and end (before its newline) of the first line of `value` that is exactly `locked`. */
export function lockedRange(value: string, locked: string | null): [number, number] | null {
	if (locked === null) return null;
	let at = 0;
	for (const line of value.split('\n')) {
		if (line === locked) return [at, at + line.length];
		at += line.length + 1;
	}
	return null;
}

/** The part of `value` an input of `type` would replace: the selection, or what a delete key would remove. */
export function affectedRange(
	value: string,
	start: number,
	end: number,
	type: string
): [number, number] {
	if (start !== end || !type.startsWith('delete')) return [start, end];
	const backward = type.includes('Backward');
	const wide = !type.startsWith('deleteContent');
	const from = lineStart(value, start);
	const lineEnd = value.indexOf('\n', start) === -1 ? value.length : value.indexOf('\n', start);
	if (backward) return [wide && start > from ? from : Math.max(0, start - 1), start];
	return [start, wide && start < lineEnd ? lineEnd : Math.min(value.length, start + 1)];
}

/**
 * Whether replacing `value[from, to)` with `insert` would change the locked line, or join it to a neighbour.
 * Starting a new line just before or after it is fine: the line itself stays as it is.
 */
export function blocksEdit(
	value: string,
	locked: string | null,
	from: number,
	to: number,
	insert: string
): boolean {
	const range = lockedRange(value, locked);
	if (!range) return false;
	const [first, last] = range;
	if (to > from) {
		// Removes or replaces text: refused if it reaches the line or either line break around it.
		return from <= last && to > Math.max(first - 1, 0);
	}
	if (from === first) return insert !== '' && !insert.endsWith('\n');
	if (from === last) return insert !== '' && !insert.startsWith('\n');
	return from > first && from < last;
}

// The window is a taste of the editor, not the editor: it takes at most this many lines, and from GROW_FROM
// lines on it widens a little with every line, up to GROW_BY wider at the limit, so a long edit keeps its shape.
export const MAX_WINDOW_LINES = 35;
export const MIN_WINDOW_LINES = 15;
const GROW_FROM = 25;
const GROW_BY = 0.2;

/** Whether replacing `value[from, to)` with `insert` would leave more lines than the window takes. */
export function exceedsLines(
	value: string,
	from: number,
	to: number,
	insert: string,
	max: number = MAX_WINDOW_LINES
): boolean {
	const count = (text: string) => text.split('\n').length - 1;
	const after = count(value) - count(value.slice(from, to)) + count(insert);
	// Only edits that add a line are refused: one that leaves it as it was (or shorter) never makes it worse.
	return after + 1 > max && count(insert) > count(value.slice(from, to));
}

/** How much wider than usual the window is for `lines` lines: 1 up to 25 lines, 1.2 at 35, steady between. */
export function windowGrowth(lines: number): number {
	const t = Math.min(Math.max((lines - GROW_FROM) / (MAX_WINDOW_LINES - GROW_FROM), 0), 1);
	return 1 + GROW_BY * t;
}
