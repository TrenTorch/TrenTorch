// LocalStorage persistence for student code, keyed generically by whatever
// content id the current /ide/[id] route is showing -- the IDE doesn't know
// or care if that's a question or a module. Solved status itself lives in
// $lib/stores/solved.svelte.ts, the same store the Questions page reads,
// so passing an IDE's hidden tests and manually checking a question off
// on /questions both land in one place.

const CODE_KEY_PREFIX = 'trentorch_code_';

export function saveUserCode(contentId: string, code: string): void {
	if (typeof window === 'undefined') return;
	try {
		localStorage.setItem(`${CODE_KEY_PREFIX}${contentId}`, code);
	} catch (e) {
		console.error('Failed to save code to localStorage', e);
	}
}

export function loadUserCode(contentId: string, defaultCode: string): string {
	if (typeof window === 'undefined') return defaultCode;
	try {
		const saved = localStorage.getItem(`${CODE_KEY_PREFIX}${contentId}`);
		return saved !== null ? saved : defaultCode;
	} catch (e) {
		console.error('Failed to load code from localStorage', e);
		return defaultCode;
	}
}

export function resetUserCode(contentId: string): void {
	if (typeof window === 'undefined') return;
	try {
		localStorage.removeItem(`${CODE_KEY_PREFIX}${contentId}`);
	} catch (e) {
		console.error('Failed to reset code in localStorage', e);
	}
}

// Pane sizes for the resizable IDE layout (left guide/code split, code/
// console split). Shared across every question -- a student who drags the
// panes to a comfortable size shouldn't have to redo it each time.
const LAYOUT_KEY = 'trentorch_ide_layout';

export interface IdeLayout {
	leftPanePercent: number;
	bottomPanePercent: number;
}

export function loadIdeLayout(defaults: IdeLayout): IdeLayout {
	if (typeof window === 'undefined') return defaults;
	try {
		const raw = localStorage.getItem(LAYOUT_KEY);
		if (!raw) return defaults;
		const parsed = JSON.parse(raw);
		return {
			leftPanePercent:
				typeof parsed.leftPanePercent === 'number'
					? parsed.leftPanePercent
					: defaults.leftPanePercent,
			bottomPanePercent:
				typeof parsed.bottomPanePercent === 'number'
					? parsed.bottomPanePercent
					: defaults.bottomPanePercent
		};
	} catch (e) {
		console.error('Failed to load IDE layout', e);
		return defaults;
	}
}

export function saveIdeLayout(layout: IdeLayout): void {
	if (typeof window === 'undefined') return;
	try {
		localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout));
	} catch (e) {
		console.error('Failed to save IDE layout', e);
	}
}
