import { browser } from '$app/environment';
import { SvelteSet } from 'svelte/reactivity';

// No backend/progress tracking exists yet -- this is a real, working
// per-browser solved-state store (localStorage), not a placeholder, so the
// solved/unsolved filter on the Questions page actually does something.
// Swap this for a real API-backed store once auth/progress persistence
// exists; nothing importing `solved` needs to change, only this file.
const STORAGE_KEY = 'trentorch-solved-questions';

function readStorage(): SvelteSet<string> {
	if (!browser) return new SvelteSet();
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? new SvelteSet(JSON.parse(raw)) : new SvelteSet();
	} catch {
		// localStorage unavailable (private mode, disabled storage) or the
		// stored value isn't valid JSON: start from empty rather than throw.
		return new SvelteSet();
	}
}

function writeStorage(current: SvelteSet<string>) {
	if (!browser) return;
	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify([...current]));
	} catch {
		// Same as above: solved state just won't persist across visits.
	}
}

// SvelteSet mutates and stays reactive in place (add/delete/has are all
// tracked), so toggling doesn't need the usual clone-and-reassign dance a
// plain Set would need under $state.
const slugs = readStorage();

export const solved = {
	get slugs(): ReadonlySet<string> {
		return slugs;
	},
	isSolved(slug: string): boolean {
		return slugs.has(slug);
	},
	// No toggle() here on purpose: solved state is earned, not set directly.
	// It used to be toggleable from the Questions list (a checkbox calling
	// this), which let anyone mark a question solved with a single click --
	// markSolved/unmarkSolved below are the only ways in, and both are only
	// ever called from real IDE submission outcomes.
	//
	// Idempotent, additive-only: the IDE calls this when every hidden test
	// passes on Submit, so a question earned solved by actually passing
	// never gets silently un-solved by this call (only the manual checkbox
	// toggle above can remove it).
	markSolved(slug: string) {
		if (slugs.has(slug)) return;
		slugs.add(slug);
		writeStorage(slugs);
	},
	// Explicit removal, used by the IDE's "Re-attempt this question" action:
	// unlike `toggle`, this only ever un-solves, never flips an unsolved
	// question on.
	unmarkSolved(slug: string) {
		if (!slugs.has(slug)) return;
		slugs.delete(slug);
		writeStorage(slugs);
	}
};
