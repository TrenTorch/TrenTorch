import { getSupabaseClient } from '$processes/auth/supabase-client';

export interface DiscussionState {
	unlocked: boolean;
	solved: boolean;
	hasCommented: boolean;
}

export interface DiscussionComment {
	id: string;
	content: string;
	upvotes: number;
	downvotes: number;
	created_at: string;
	updated_at: string;
	is_mine: boolean;
	my_vote: 1 | -1 | null;
	author_username: string | null;
	author_display_name: string | null;
}

function getUserMessage(error: { code?: string; message: string }, posting = false): string {
	if (posting && error.code === '23505') return 'You already commented — edit it instead.';
	if (posting && error.code === '42501') return 'Solve this problem to comment.';
	if (error.code === '23514' && error.message.includes('potd_comment_code_block_too_long')) {
		return 'Code blocks must have 6 non-empty lines or fewer.';
	}
	if (error.code === '23514' && error.message.includes('potd_comment_too_many_lines')) {
		return 'Comments must have 30 lines or fewer.';
	}
	return error.message;
}

function throwIfError(error: { code?: string; message: string } | null, posting = false): void {
	if (error) throw new Error(getUserMessage(error, posting));
}

export async function fetchDiscussionState(questionId: string): Promise<DiscussionState> {
	const { data, error } = await getSupabaseClient().rpc('get_potd_discussion_state', {
		p_question_id: questionId
	});
	throwIfError(error);
	const row = data?.[0];
	if (!row) throw new Error('Could not load discussion access.');
	return {
		unlocked: row.unlocked,
		solved: row.solved,
		hasCommented: row.has_commented
	};
}

export async function fetchComments(questionId: string): Promise<DiscussionComment[]> {
	const { data, error } = await getSupabaseClient()
		.rpc('get_potd_comments', { p_question_id: questionId })
		.abortSignal(AbortSignal.timeout(15_000));
	throwIfError(error);
	return (data ?? []) as DiscussionComment[];
}

export async function postComment(questionId: string, content: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('potd_discussion_comments')
		.insert({ question_id: questionId, content });
	throwIfError(error, true);
}

export async function editComment(id: string, content: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('potd_discussion_comments')
		.update({ content })
		.eq('id', id);
	throwIfError(error);
}

export async function deleteComment(id: string): Promise<void> {
	const { error } = await getSupabaseClient()
		.from('potd_discussion_comments')
		.delete()
		.eq('id', id);
	throwIfError(error);
}

export async function setVote(commentId: string, value: 1 | -1 | 0): Promise<void> {
	const supabase = getSupabaseClient();
	if (value === 0) {
		const { error } = await supabase
			.from('potd_comment_votes')
			.delete()
			.eq('comment_id', commentId);
		throwIfError(error);
		return;
	}

	const { data, error } = await supabase
		.from('potd_comment_votes')
		.update({ vote_value: value })
		.eq('comment_id', commentId)
		.select('comment_id');
	throwIfError(error);
	if (data?.length) return;

	const { error: insertError } = await supabase
		.from('potd_comment_votes')
		.insert({ comment_id: commentId, vote_value: value });
	throwIfError(insertError);
}
