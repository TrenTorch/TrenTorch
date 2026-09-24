import { getSupabaseClient } from '$processes/auth/supabase-client';

export interface RemoteDraft {
	contentId: string;
	code: string;
	updatedAt: string;
}

export const MAX_DRAFT_LENGTH = 50000;

// Like the solved store, none of these throw: a Supabase hiccup must never
// block the editor, whose localStorage copy is the one that always works.

export async function fetchDrafts(userId: string): Promise<RemoteDraft[] | null> {
	const { data, error } = await getSupabaseClient()
		.from('code_drafts')
		.select('content_id, code, updated_at')
		.eq('user_id', userId);
	if (error) {
		console.error('Failed to fetch code drafts', error);
		return null;
	}
	return (data ?? []).map((row) => ({
		contentId: row.content_id,
		code: row.code,
		updatedAt: row.updated_at
	}));
}

export async function upsertDrafts(userId: string, drafts: RemoteDraft[]): Promise<void> {
	const rows = drafts
		.filter((draft) => draft.code.length <= MAX_DRAFT_LENGTH)
		.map((draft) => ({
			user_id: userId,
			content_id: draft.contentId,
			code: draft.code,
			updated_at: draft.updatedAt
		}));
	if (rows.length === 0) return;
	const { error } = await getSupabaseClient()
		.from('code_drafts')
		.upsert(rows, { onConflict: 'user_id,content_id' });
	if (error) console.error('Failed to sync code drafts', error);
}

export async function deleteDraft(userId: string, contentId: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('code_drafts')
		.delete()
		.eq('user_id', userId)
		.eq('content_id', contentId);
	if (error) console.error('Failed to delete code draft', error);
}

export async function fetchAttempted(userId: string): Promise<string[] | null> {
	const { data, error } = await getSupabaseClient()
		.from('attempted_questions')
		.select('question_id')
		.eq('user_id', userId);
	if (error) {
		console.error('Failed to fetch attempted questions', error);
		return null;
	}
	return (data ?? []).map((row) => row.question_id);
}

export async function upsertAttempted(userId: string, slugs: string[]): Promise<void> {
	if (slugs.length === 0) return;
	const { error } = await getSupabaseClient()
		.from('attempted_questions')
		.upsert(
			slugs.map((slug) => ({ user_id: userId, question_id: slug })),
			{ onConflict: 'user_id,question_id', ignoreDuplicates: true }
		);
	if (error) console.error('Failed to sync attempted questions', error);
}

export async function deleteAttempted(userId: string, slug: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('attempted_questions')
		.delete()
		.eq('user_id', userId)
		.eq('question_id', slug);
	if (error) console.error('Failed to delete attempted question', error);
}
