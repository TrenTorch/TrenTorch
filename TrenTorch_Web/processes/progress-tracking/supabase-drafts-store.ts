import { getSupabaseClient } from '$processes/auth/supabase-client';

export interface RemoteDraft {
	contentId: string;
	code: string;
	updatedAt: string;
}

export interface RemoteDraftMeta {
	contentId: string;
	updatedAt: string;
}

export const MAX_DRAFT_LENGTH = 50000;

const REQUEST_TIMEOUT_MS = 15_000;
// Keeps one request comfortably under PostgREST's body limits when a first
// sign-in has to push many drafts at once.
const MAX_ROWS_PER_REQUEST = 10;
const MAX_CHARS_PER_REQUEST = 300_000;
const IDS_PER_FETCH = 25;

const signal = () => AbortSignal.timeout(REQUEST_TIMEOUT_MS);

// Like the solved store, none of these throw: a Supabase hiccup must never
// block the editor, whose localStorage copy is the one that always works.

// Timestamps only, no code: a sync then downloads just the drafts that are
// actually newer than the local copy instead of every draft the user owns.
export async function fetchDraftMeta(userId: string): Promise<RemoteDraftMeta[] | null> {
	const { data, error } = await getSupabaseClient()
		.from('code_drafts')
		.select('content_id, updated_at')
		.eq('user_id', userId)
		.abortSignal(signal());
	if (error) {
		console.error('Failed to fetch code draft list', error);
		return null;
	}
	return (data ?? []).map((row) => ({ contentId: row.content_id, updatedAt: row.updated_at }));
}

export async function fetchDraftCodes(
	userId: string,
	contentIds: string[]
): Promise<RemoteDraft[] | null> {
	const out: RemoteDraft[] = [];
	for (let i = 0; i < contentIds.length; i += IDS_PER_FETCH) {
		const { data, error } = await getSupabaseClient()
			.from('code_drafts')
			.select('content_id, code, updated_at')
			.eq('user_id', userId)
			.in('content_id', contentIds.slice(i, i + IDS_PER_FETCH))
			.abortSignal(signal());
		if (error) {
			console.error('Failed to fetch code drafts', error);
			return null;
		}
		for (const row of data ?? []) {
			out.push({ contentId: row.content_id, code: row.code, updatedAt: row.updated_at });
		}
	}
	return out;
}

function chunkDrafts(drafts: RemoteDraft[]): RemoteDraft[][] {
	const chunks: RemoteDraft[][] = [];
	let current: RemoteDraft[] = [];
	let chars = 0;
	for (const draft of drafts) {
		if (
			current.length > 0 &&
			(current.length >= MAX_ROWS_PER_REQUEST || chars + draft.code.length > MAX_CHARS_PER_REQUEST)
		) {
			chunks.push(current);
			current = [];
			chars = 0;
		}
		current.push(draft);
		chars += draft.code.length;
	}
	if (current.length > 0) chunks.push(current);
	return chunks;
}

export async function upsertDrafts(userId: string, drafts: RemoteDraft[]): Promise<void> {
	const eligible = drafts.filter((draft) => draft.code.length <= MAX_DRAFT_LENGTH);
	for (const chunk of chunkDrafts(eligible)) {
		const { error } = await getSupabaseClient()
			.from('code_drafts')
			.upsert(
				chunk.map((draft) => ({
					user_id: userId,
					content_id: draft.contentId,
					code: draft.code,
					updated_at: draft.updatedAt
				})),
				{ onConflict: 'user_id,content_id' }
			)
			.abortSignal(signal());
		if (error) {
			console.error('Failed to sync code drafts', error);
			return;
		}
	}
}

export async function deleteDraft(userId: string, contentId: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('code_drafts')
		.delete()
		.eq('user_id', userId)
		.eq('content_id', contentId)
		.abortSignal(signal());
	if (error) console.error('Failed to delete code draft', error);
}

export async function fetchAttempted(userId: string): Promise<string[] | null> {
	const { data, error } = await getSupabaseClient()
		.from('attempted_questions')
		.select('question_id')
		.eq('user_id', userId)
		.abortSignal(signal());
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
		)
		.abortSignal(signal());
	if (error) console.error('Failed to sync attempted questions', error);
}

export async function deleteAttempted(userId: string, slug: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('attempted_questions')
		.delete()
		.eq('user_id', userId)
		.eq('question_id', slug)
		.abortSignal(signal());
	if (error) console.error('Failed to delete attempted question', error);
}
