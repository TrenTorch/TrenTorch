// The landing page's code window is editable. What a visitor types there is carried to the IDE as a
// draft: the window only shows the start of the starter (see home-preview.ts), so the draft keeps how
// many starter lines were on show and the IDE puts the rest back after the edited part.

import { toRows } from './home-preview';

const KEY = 'trentorch_home_draft';
const MAX_AGE_MS = 30 * 60 * 1000;
const HINT = '    # ...';

export interface HomeDraft {
	id: string;
	/** The edited text of the window, without the "# ..." hint. */
	text: string;
	/** How many lines of the starter the window was showing. */
	shownLines: number;
	/** The IDE code the window was showing, when it was not the starter. The draft only applies to exactly that. */
	base?: string;
}

/** The edit as the user left it, minus the trailing hint line if it is still there. */
export function stripHint(text: string): string {
	const lines = text.replace(/\s+$/, '').split('\n');
	return (lines.at(-1)?.trim() === HINT.trim() ? lines.slice(0, -1) : lines).join('\n');
}

/**
 * The edited window followed by the part of the code (the starter, or `draft.base`) it never showed. A signature the preview joined onto
 * one line goes back to the starter's own wrapping unless the visitor changed it.
 */
export function mergeDraft(starter: string, draft: HomeDraft): string {
	const all = starter.replace(/\s+$/, '').split('\n');
	let lines = draft.text.split('\n');
	let covered = 0;
	for (const row of toRows(all)) {
		if (covered >= draft.shownLines) break;
		covered += row.consumed;
		const at = row.original ? lines.indexOf(row.text) : -1;
		if (row.original && at !== -1)
			lines = [...lines.slice(0, at), ...row.original, ...lines.slice(at + 1)];
	}
	const rest = all.slice(draft.shownLines);
	return `${[...lines, ...rest].join('\n')}\n`;
}

export function saveHomeDraft(draft: HomeDraft | null): void {
	try {
		if (draft) localStorage.setItem(KEY, JSON.stringify({ ...draft, at: Date.now() }));
		else localStorage.removeItem(KEY);
	} catch {
		// Storage can be blocked; the window still works, it just won't carry over.
	}
}

/** The draft for this question, if there is one. It is always cleared: a draft is used once or not at all. */
export function takeHomeDraft(id: string): HomeDraft | null {
	if (typeof localStorage === 'undefined') return null;
	try {
		const raw = localStorage.getItem(KEY);
		if (!raw) return null;
		localStorage.removeItem(KEY);
		const draft = JSON.parse(raw) as Partial<HomeDraft> & { at?: number };
		// Typed and then abandoned: not something to spring on a visit hours later.
		if (typeof draft.at !== 'number' || Date.now() - draft.at > MAX_AGE_MS) return null;
		const valid =
			draft.id === id &&
			typeof draft.text === 'string' &&
			typeof draft.shownLines === 'number' &&
			(draft.base === undefined || typeof draft.base === 'string');
		return valid ? (draft as HomeDraft) : null;
	} catch {
		return null;
	}
}
