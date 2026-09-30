import { browser } from '$app/environment';
import { SvelteSet } from 'svelte/reactivity';

// Persists which curriculum folders (roots, sections and sub-sections on
// the Questions page) a student has toggled away from its default
// (localStorage, per-browser, same story as solved/attempted -- see those
// files). Stores only deviations, so a folder the student never touched
// keeps whatever default its caller gives it.
const STORAGE_KEY = 'trentorch-toggled-folders';

function readStorage(): SvelteSet<string> {
	if (!browser) return new SvelteSet();
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? new SvelteSet(JSON.parse(raw)) : new SvelteSet();
	} catch {
		// localStorage unavailable (private mode, disabled storage) or the
		// stored value isn't valid JSON: start from empty (everything closed).
		return new SvelteSet();
	}
}

function writeStorage(current: SvelteSet<string>) {
	if (!browser) return;
	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify([...current]));
	} catch {
		// Same as above: the open/closed setting just won't persist.
	}
}

const openKeys = readStorage();

export const collapsedSections = {
	isOpen(key: string, defaultOpen = false): boolean {
		return defaultOpen !== openKeys.has(key);
	},
	toggle(key: string) {
		if (openKeys.has(key)) openKeys.delete(key);
		else openKeys.add(key);
		writeStorage(openKeys);
	}
};
