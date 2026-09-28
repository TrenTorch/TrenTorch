<script lang="ts">
	import { untrack } from 'svelte';
	import Button from '$components/Button.svelte';
	import CommentComposer from './CommentComposer.svelte';
	import CommentItem from './CommentItem.svelte';
	import { session } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import {
		deleteComment,
		editComment,
		fetchComments,
		fetchDiscussionState,
		postComment,
		setVote,
		type DiscussionComment,
		type DiscussionState
	} from '$processes/discussion/supabase-discussion-store';

	let { questionId }: { questionId: string } = $props();
	let loadState = $state<'idle' | 'loading' | 'loaded'>('idle');
	let discussionState = $state<DiscussionState | null>(null);
	let comments = $state<DiscussionComment[]>([]);
	let errorMessage = $state('');
	let requestVersion = 0;

	async function refresh() {
		const version = ++requestVersion;
		const userId = session.user?.id;
		if (!userId) return;
		if (!untrack(() => discussionState)) loadState = 'loading';
		errorMessage = '';
		try {
			const nextState = await fetchDiscussionState(questionId);
			if (version !== requestVersion || session.user?.id !== userId) return;
			const nextComments = await fetchComments(questionId);
			if (version !== requestVersion || session.user?.id !== userId) return;
			discussionState = nextState;
			comments = nextComments;
			loadState = 'loaded';
		} catch (error) {
			if (version !== requestVersion) return;
			errorMessage = error instanceof Error ? error.message : 'Could not load discussion.';
			loadState = 'loaded';
		}
	}

	$effect(() => {
		const currentQuestionId = questionId;
		const userId = session.user?.id;
		const isSessionLoading = session.isLoading;

		if (isSessionLoading) return;
		if (!userId) {
			requestVersion += 1;
			discussionState = null;
			comments = [];
			loadState = 'idle';
			errorMessage = '';
			return;
		}

		discussionState = null;
		comments = [];
		loadState = 'loading';
		errorMessage = '';
		void currentQuestionId;
		void refresh();
		return () => {
			requestVersion += 1;
		};
	});

	let ownComment = $derived(comments.find((comment) => comment.is_mine));

	async function submitNewComment(content: string) {
		await postComment(questionId, content);
		if (discussionState) discussionState = { ...discussionState, hasCommented: true };
		await refresh();
	}

	async function saveComment(comment: DiscussionComment, content: string) {
		await editComment(comment.id, content);
		await refresh();
	}

	async function removeComment(comment: DiscussionComment) {
		try {
			await deleteComment(comment.id);
			await refresh();
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Could not delete your comment.';
		}
	}

	async function vote(comment: DiscussionComment, value: 1 | -1 | 0) {
		const previousVote = comment.my_vote;
		comments = comments.map((item) =>
			item.id === comment.id ? { ...item, my_vote: value === 0 ? null : value } : item
		);
		try {
			await setVote(comment.id, value);
			await refresh();
		} catch (error) {
			comments = comments.map((item) =>
				item.id === comment.id ? { ...item, my_vote: previousVote } : item
			);
			errorMessage = error instanceof Error ? error.message : 'Could not save your vote.';
		}
	}
</script>

<section class="space-y-4" aria-label="POTD discussion">
	<p
		class="rounded-md border border-amber-500/40 bg-amber-50 px-3 py-2.5 text-xs leading-relaxed text-amber-950 dark:bg-amber-950/30 dark:text-amber-100"
	>
		Only people who solved this Problem of the Day can post one comment. Everyone else can upvote or
		downvote once the discussion opens. Share hints and your approach, not a complete solution; code
		snippets are limited to six non-empty lines.
	</p>
	{#if session.isLoading}
		<p class="text-sm text-muted-foreground">Checking sign-in…</p>
	{:else if !session.user}
		<div class="space-y-2 py-4 text-center">
			<p class="text-sm text-muted-foreground">Sign in to join the discussion.</p>
			<Button size="sm" onclick={() => signInPrompt.open()}>Sign in</Button>
		</div>
	{:else if loadState === 'loading' || loadState === 'idle'}
		<p class="text-sm text-muted-foreground">Loading discussion…</p>
	{:else if errorMessage && !discussionState}
		<p class="text-sm text-destructive" role="alert">{errorMessage}</p>
		<Button variant="outline" size="sm" onclick={() => void refresh()}>Try again</Button>
	{:else if discussionState}
		{#if errorMessage}
			<p class="text-sm text-destructive" role="alert">{errorMessage}</p>
		{/if}
		{#if !discussionState.unlocked && !discussionState.solved}
			<p class="py-4 text-center text-sm text-muted-foreground">
				Discussion opens once today's problem has ended everywhere.
			</p>
		{:else if !discussionState.unlocked}
			{#if discussionState.hasCommented}
				<p class="text-xs text-muted-foreground">
					Only you can see this until the discussion opens.
				</p>
			{/if}
			{#if ownComment}
				<CommentItem
					comment={ownComment}
					unlocked={discussionState.unlocked}
					onVote={(value) => void vote(ownComment!, value)}
					onEdit={(content) => saveComment(ownComment!, content)}
					onDelete={() => void removeComment(ownComment!)}
				/>
			{:else if discussionState.solved && !discussionState.hasCommented}
				<CommentComposer onSubmit={submitNewComment} />
			{:else if discussionState.hasCommented}
				<p class="text-sm text-destructive" role="alert">
					Your comment could not be loaded. Try refreshing the discussion.
				</p>
			{/if}
		{:else}
			{#if discussionState.solved && !discussionState.hasCommented}
				<CommentComposer onSubmit={submitNewComment} />
			{/if}
			{#if comments.length === 0}
				{#if discussionState.hasCommented}
					<p class="text-sm text-destructive" role="alert">
						Your comment could not be loaded. Try refreshing the discussion.
					</p>
				{:else}
					<p class="py-4 text-center text-sm text-muted-foreground">
						No comments yet. Share your approach.
					</p>
				{/if}
			{:else}
				<div class="space-y-3">
					{#each comments as comment (comment.id)}
						<CommentItem
							{comment}
							unlocked={discussionState.unlocked}
							onVote={(value) => void vote(comment, value)}
							onEdit={(content) => saveComment(comment, content)}
							onDelete={() => void removeComment(comment)}
						/>
					{/each}
				</div>
			{/if}
		{/if}
	{/if}
</section>
