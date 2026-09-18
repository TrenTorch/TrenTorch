import { solved } from './solved.svelte';
import { isPotdQuestion } from '$processes/potd/is-potd-question';
import { fetchSolvedQuestions, upsertSolvedQuestions } from './supabase-solved-store';

// Runs once per sign-in (see ProgressSync.svelte): a genuine two-way merge,
// not a one-directional overwrite in either direction --
//
// - Remote rows the local browser doesn't have yet (solved on another
//   device, or before this browser's storage was cleared) get pulled in.
// - Local slugs Supabase doesn't have yet (solved before ever signing in,
//   or while a previous sync attempt failed) get pushed up.
//
// Either side missing entirely (a brand-new account, or a browser that
// never solved anything locally) degenerates to a plain one-way copy.
export async function syncSolvedWithSupabase(userId: string): Promise<void> {
	const remoteRows = await fetchSolvedQuestions(userId);
	const remoteSlugs = new Set(remoteRows.map((row) => row.question_id));

	for (const slug of remoteSlugs) {
		solved.markSolvedFromRemote(slug);
	}

	const localOnlySlugs = [...solved.slugs].filter((slug) => !remoteSlugs.has(slug));
	await upsertSolvedQuestions(
		userId,
		localOnlySlugs.map((slug) => ({ slug, isPotd: isPotdQuestion(slug) }))
	);
}
