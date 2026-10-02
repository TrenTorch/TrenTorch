import { browser } from '$app/environment';
import { SvelteSet } from 'svelte/reactivity';

// Persists which curriculum Parts a student has collapsed on the
// Questions page (localStorage, per-browser, same story as solved/
// attempted -- see those files). Stores only what deviates from the
// default (every Part starts open, so this set holds *closed* ids, not
// open ones): a newly-added Part a student has never seen is open by
// default, not silently collapsed just because it wasn't in the set yet.
const STORAGE_KEY = 'trentorch-collapsed-parts';

function readStorage(): SvelteSet<string> {
	if (!browser) return new SvelteSet();
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? new SvelteSet(JSON.parse(raw)) : new SvelteSet();
	} catch {
		// localStorage unavailable (private mode, disabled storage) or the
		// stored value isn't valid JSON: start from empty (everything open)
		// rather than throw.
		return new SvelteSet();
	}
}

function writeStorage(current: SvelteSet<string>) {
	if (!browser) return;
	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify([...current]));
	} catch {
		// Same as above: the collapsed/open setting just won't persist.
	}
}

const closedPartIds = readStorage();

export const collapsedSections = {
	isOpen(partId: string): boolean {
		return !closedPartIds.has(partId);
	},
	toggle(partId: string) {
		if (closedPartIds.has(partId)) closedPartIds.delete(partId);
		else closedPartIds.add(partId);
		writeStorage(closedPartIds);
	}
};
