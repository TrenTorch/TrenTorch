import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import DiscussionTab from './DiscussionTab.svelte';

const mocks = vi.hoisted(() => ({
	session: { user: null as null | { id: string }, isLoading: false },
	openSignIn: vi.fn(),
	fetchDiscussionState: vi.fn(),
	fetchComments: vi.fn(),
	postComment: vi.fn(),
	editComment: vi.fn(),
	deleteComment: vi.fn(),
	setVote: vi.fn()
}));

vi.mock('$processes/auth/session.svelte', () => ({
	session: {
		get user() {
			return mocks.session.user;
		},
		get isLoading() {
			return mocks.session.isLoading;
		}
	}
}));

vi.mock('$processes/auth/sign-in-prompt.svelte', () => ({
	signInPrompt: { open: mocks.openSignIn }
}));

vi.mock('$processes/discussion/supabase-discussion-store', () => ({
	fetchDiscussionState: mocks.fetchDiscussionState,
	fetchComments: mocks.fetchComments,
	postComment: mocks.postComment,
	editComment: mocks.editComment,
	deleteComment: mocks.deleteComment,
	setVote: mocks.setVote
}));

const comment = {
	id: 'comment-1',
	content: 'My approach',
	upvotes: 0,
	downvotes: 0,
	created_at: '2026-09-28T00:00:00Z',
	updated_at: '2026-09-28T00:00:00Z',
	is_mine: true,
	my_vote: null,
	author_username: null,
	author_display_name: null
} as const;

describe('DiscussionTab', () => {
	afterEach(() => cleanup());

	beforeEach(() => {
		mocks.session.user = null;
		mocks.session.isLoading = false;
		vi.clearAllMocks();
		mocks.fetchDiscussionState.mockResolvedValue({
			unlocked: false,
			solved: false,
			hasCommented: false
		});
		mocks.fetchComments.mockResolvedValue([]);
	});

	it('prompts signed-out visitors without loading discussion data', async () => {
		render(DiscussionTab, { questionId: 'question-1' });
		expect(
			screen.getByText(/Only people who solved this Problem of the Day can post one comment/)
		).toBeInTheDocument();
		await fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
		expect(mocks.openSignIn).toHaveBeenCalledOnce();
		expect(mocks.fetchDiscussionState).not.toHaveBeenCalled();
		expect(screen.queryByText('My approach')).not.toBeInTheDocument();
	});

	it('explains the waiting period to signed-in non-solvers', async () => {
		mocks.session.user = { id: 'user-1' };
		render(DiscussionTab, { questionId: 'question-1' });
		expect(
			await screen.findByText("Discussion opens once today's problem has ended everywhere.")
		).toBeInTheDocument();
		expect(screen.queryByRole('textbox', { name: 'Your comment' })).not.toBeInTheDocument();
	});

	it('lets a solver compose privately before unlock without an early visibility note', async () => {
		mocks.session.user = { id: 'user-1' };
		mocks.fetchDiscussionState.mockResolvedValue({
			unlocked: false,
			solved: true,
			hasCommented: false
		});
		render(DiscussionTab, { questionId: 'question-1' });
		expect(await screen.findByRole('textbox', { name: 'Your comment' })).toBeInTheDocument();
		expect(screen.queryByText('Only you can see this until the discussion opens.')).toBeNull();
	});

	it('shows the solver own editable comment while the discussion is still private', async () => {
		mocks.session.user = { id: 'user-1' };
		mocks.fetchDiscussionState.mockResolvedValue({
			unlocked: false,
			solved: true,
			hasCommented: true
		});
		mocks.fetchComments.mockResolvedValue([comment]);
		render(DiscussionTab, { questionId: 'question-1' });
		expect(await screen.findByText('My approach')).toBeInTheDocument();
		expect(
			screen.getByText('Only you can see this until the discussion opens.')
		).toBeInTheDocument();
		expect(screen.getByRole('button', { name: 'Edit comment' })).toBeInTheDocument();
		expect(screen.queryByRole('textbox', { name: 'Your comment' })).not.toBeInTheDocument();
	});

	it('shows unlocked comments and collapses low-scoring comments', async () => {
		mocks.session.user = { id: 'user-2' };
		mocks.fetchDiscussionState.mockResolvedValue({
			unlocked: true,
			solved: false,
			hasCommented: false
		});
		mocks.fetchComments.mockResolvedValue([
			{
				...comment,
				id: 'comment-2',
				content: 'A low-scoring answer',
				is_mine: false,
				upvotes: 0,
				downvotes: 6
			}
		]);
		render(DiscussionTab, { questionId: 'question-1' });
		const expand = await screen.findByRole('button', {
			name: 'Low-scoring comment (-6) — expand'
		});
		expect(screen.queryByText('A low-scoring answer')).not.toBeInTheDocument();
		await fireEvent.click(expand);
		expect(screen.getByText('A low-scoring answer')).toBeInTheDocument();
		expect(screen.getByRole('button', { name: 'Upvote comment' })).toBeEnabled();
	});
});
