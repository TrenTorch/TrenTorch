import { browser } from '$app/environment';
import { SvelteSet } from 'svelte/reactivity';

// Parallel to solved.svelte.ts, one state weaker: a question is "attempted"
// the moment Submit actually runs its hidden tests, whether or not they all
// pass. Lets the Questions page show "you've had a go at this one" distinctly
// from "you've cleared it". Same per-browser localStorage story -- swap for an
// API-backed store once auth/progress persistence exists; importers only touch
// this file.
const STORAGE_KEY = 'trentorch-attempted-questions';

function readStorage(): SvelteSet<string> {
	if (!browser) return new SvelteSet();
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? new SvelteSet(JSON.parse(raw)) : new SvelteSet();
	} catch {
		return new SvelteSet();
	}
}

function writeStorage(current: SvelteSet<string>) {
	if (!browser) return;
	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify([...current]));
	} catch {
		// Attempted state just won't persist across visits.
	}
}

const slugs = readStorage();

export const attempted = {
	get slugs(): ReadonlySet<string> {
		return slugs;
	},
	isAttempted(slug: string): boolean {
		return slugs.has(slug);
	},
	// Idempotent, additive-only: called on every Submit that reached the
	// test runner. Nothing removes a slug from this set -- once tried, tried.
	markAttempted(slug: string) {
		if (slugs.has(slug)) return;
		slugs.add(slug);
		writeStorage(slugs);
	},
	// Used by the IDE's "Re-attempt this question" action to return a
	// question to its untouched state.
	unmarkAttempted(slug: string) {
		if (!slugs.has(slug)) return;
		slugs.delete(slug);
		writeStorage(slugs);
	}
};
