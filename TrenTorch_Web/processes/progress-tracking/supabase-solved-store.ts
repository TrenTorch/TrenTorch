import { getSupabaseClient } from '$processes/auth/supabase-client';

export interface RemoteSolvedRow {
	question_id: string;
	is_potd: boolean;
}

// All three functions are fire-and-forget from the caller's side (errors
// are logged, never thrown) -- a Supabase hiccup should never block a
// student's local progress, which is the real, always-available copy.
// Supabase is the cross-device backup, not the source of truth for the
// current tab.

export async function fetchSolvedQuestions(userId: string): Promise<RemoteSolvedRow[]> {
	const supabase = getSupabaseClient();
	const { data, error } = await supabase
		.from('solved_questions')
		.select('question_id, is_potd')
		.eq('user_id', userId);
	if (error) {
		console.error('Failed to fetch solved questions from Supabase', error);
		return [];
	}
	return data ?? [];
}

export async function upsertSolvedQuestion(
	userId: string,
	slug: string,
	isPotd: boolean
): Promise<void> {
	const supabase = getSupabaseClient();
	const { error } = await supabase
		.from('solved_questions')
		.upsert(
			{ user_id: userId, question_id: slug, is_potd: isPotd },
			{ onConflict: 'user_id,question_id' }
		);
	if (error) console.error('Failed to sync solved question to Supabase', error);
}

export async function upsertSolvedQuestions(
	userId: string,
	rows: { slug: string; isPotd: boolean }[]
): Promise<void> {
	if (rows.length === 0) return;
	const supabase = getSupabaseClient();
	const { error } = await supabase.from('solved_questions').upsert(
		rows.map((row) => ({ user_id: userId, question_id: row.slug, is_potd: row.isPotd })),
		{ onConflict: 'user_id,question_id', ignoreDuplicates: true }
	);
	if (error) console.error('Failed to bulk-sync solved questions to Supabase', error);
}

export async function deleteSolvedQuestion(userId: string, slug: string): Promise<void> {
	const supabase = getSupabaseClient();
	const { error } = await supabase
		.from('solved_questions')
		.delete()
		.eq('user_id', userId)
		.eq('question_id', slug);
	if (error) console.error('Failed to delete solved question from Supabase', error);
}

// When each question was first solved, for the account page's contribution graph.
export async function fetchSolvedDates(userId: string): Promise<string[] | null> {
	const { data, error } = await getSupabaseClient()
		.from('solved_questions')
		.select('solved_at')
		.eq('user_id', userId)
		.abortSignal(AbortSignal.timeout(15_000));
	if (error) {
		console.error('Failed to fetch solve dates', error);
		return null;
	}
	return (data ?? []).flatMap((row) => (row.solved_at ? [row.solved_at as string] : []));
}
