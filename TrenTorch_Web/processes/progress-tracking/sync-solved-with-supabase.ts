import { solved } from './solved.svelte';
import { attempted } from './attempted.svelte';
import { isPotdQuestion } from '$processes/potd/is-potd-question';
import {
	deleteSolvedQuestions,
	fetchSolvedQuestions,
	upsertSolvedQuestions
} from './supabase-solved-store';

// The account this browser's local progress was last synced with. Local
// progress outlives sign-out, so without this a second person signing in on
// the same browser had the first person's solves uploaded into their account
// (and pulled the second person's into the first's on the way back).
const OWNER_KEY = 'trentorch-progress-owner';

function readOwner(): string | null {
	try {
		return localStorage.getItem(OWNER_KEY);
	} catch {
		return null;
	}
}

function writeOwner(userId: string) {
	try {
		localStorage.setItem(OWNER_KEY, userId);
	} catch {
		// Storage blocked: every sign-in then merges, the behaviour before this key existed.
	}
}

// Runs once per sign-in (see ProgressSync.svelte): a genuine two-way merge,
// not a one-directional overwrite in either direction --
//
// - Remote rows the local browser doesn't have yet (solved on another
//   device, or before this browser's storage was cleared) get pulled in.
// - Local slugs Supabase doesn't have yet (solved before ever signing in,
//   or while a previous sync attempt failed) get pushed up.
// - Questions re-attempted (un-solved) while signed out get deleted remotely
//   rather than pulled back in.
//
// Either side missing entirely (a brand-new account, or a browser that
// never solved anything locally) degenerates to a plain one-way copy. Local
// progress that belongs to a different account is dropped first, never merged.
export async function syncSolvedWithSupabase(userId: string): Promise<void> {
	const owner = readOwner();
	if (owner !== null && owner !== userId) {
		solved.clearLocal();
		attempted.clearLocal();
	}

	const removals = [...solved.pendingRemovals];
	if (await deleteSolvedQuestions(userId, removals)) solved.clearPendingRemovals();
	const removed = new Set(removals);

	const remoteRows = await fetchSolvedQuestions(userId);
	const remoteSlugs = new Set(remoteRows.map((row) => row.question_id));

	for (const slug of remoteSlugs) {
		if (!removed.has(slug)) solved.markSolvedFromRemote(slug);
	}

	const localOnlySlugs = [...solved.slugs].filter((slug) => !remoteSlugs.has(slug));
	await upsertSolvedQuestions(
		userId,
		localOnlySlugs.map((slug) => ({ slug, isPotd: isPotdQuestion(slug) }))
	);
	writeOwner(userId);
}
