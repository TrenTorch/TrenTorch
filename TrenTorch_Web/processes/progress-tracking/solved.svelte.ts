import { browser } from '$app/environment';
import { SvelteSet } from 'svelte/reactivity';
import { session } from '$processes/auth/session.svelte';
import { isPotdQuestion } from '$processes/potd/is-potd-question';
import { upsertSolvedQuestion, deleteSolvedQuestion } from './supabase-solved-store';

// Per-browser localStorage is the real, always-available copy -- every
// method below updates it synchronously and unconditionally, signed in or
// not. Supabase is the cross-device backup layered on top of that: a
// signed-in student's solve also gets pushed there (fire-and-forget, never
// blocking or throwing into the caller), and sync-solved-with-supabase.ts
// reconciles the two on sign-in.
const STORAGE_KEY = 'trentorch-solved-questions';
// Questions un-solved while nobody was signed in. Supabase still has them, so
// without this list the next sign-in's sync would pull them straight back in.
const PENDING_REMOVALS_KEY = 'trentorch-unsolved-pending';

function readStorage(key: string): SvelteSet<string> {
	if (!browser) return new SvelteSet();
	try {
		const raw = localStorage.getItem(key);
		return raw ? new SvelteSet(JSON.parse(raw)) : new SvelteSet();
	} catch {
		// localStorage unavailable (private mode, disabled storage) or the
		// stored value isn't valid JSON: start from empty rather than throw.
		return new SvelteSet();
	}
}

function writeStorage(key: string, current: SvelteSet<string>) {
	if (!browser) return;
	try {
		localStorage.setItem(key, JSON.stringify([...current]));
	} catch {
		// Same as above: solved state just won't persist across visits.
	}
}

// SvelteSet mutates and stays reactive in place (add/delete/has are all
// tracked), so toggling doesn't need the usual clone-and-reassign dance a
// plain Set would need under $state.
const slugs = readStorage(STORAGE_KEY);
const pendingRemovals = readStorage(PENDING_REMOVALS_KEY);

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
		if (pendingRemovals.delete(slug)) writeStorage(PENDING_REMOVALS_KEY, pendingRemovals);
		if (slugs.has(slug)) return;
		slugs.add(slug);
		writeStorage(STORAGE_KEY, slugs);
		if (session.user) {
			void upsertSolvedQuestion(session.user.id, slug, isPotdQuestion(slug));
		}
	},
	// Explicit removal, used by the IDE's "Re-attempt this question" action:
	// unlike `toggle`, this only ever un-solves, never flips an unsolved
	// question on.
	unmarkSolved(slug: string) {
		if (!slugs.has(slug)) return;
		slugs.delete(slug);
		writeStorage(STORAGE_KEY, slugs);
		if (session.user) {
			void deleteSolvedQuestion(session.user.id, slug);
		} else {
			pendingRemovals.add(slug);
			writeStorage(PENDING_REMOVALS_KEY, pendingRemovals);
		}
	},
	// Local-only: adds a slug without writing back to Supabase, for
	// sync-solved-with-supabase.ts pulling rows that already came FROM
	// Supabase -- writing them back would be a pointless round-trip.
	markSolvedFromRemote(slug: string) {
		if (slugs.has(slug)) return;
		slugs.add(slug);
		writeStorage(STORAGE_KEY, slugs);
	},
	// Un-solves made while signed out, waiting for the next sign-in's sync to
	// delete them from Supabase too.
	get pendingRemovals(): ReadonlySet<string> {
		return pendingRemovals;
	},
	clearPendingRemovals() {
		pendingRemovals.clear();
		writeStorage(PENDING_REMOVALS_KEY, pendingRemovals);
	},
	// Local-only wipe, for when this browser's progress belongs to a different
	// account than the one signing in (see sync-solved-with-supabase.ts).
	// Supabase is not touched: the other account's rows stay intact there.
	clearLocal() {
		slugs.clear();
		pendingRemovals.clear();
		writeStorage(STORAGE_KEY, slugs);
		writeStorage(PENDING_REMOVALS_KEY, pendingRemovals);
	}
};
