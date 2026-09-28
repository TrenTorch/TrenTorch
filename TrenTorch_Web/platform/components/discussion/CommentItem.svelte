<script lang="ts">
	import Button from '$components/Button.svelte';
	import CommentComposer from './CommentComposer.svelte';
	import { LOW_SCORE_COLLAPSE_THRESHOLD } from '$processes/discussion/constants';
	import type { DiscussionComment } from '$processes/discussion/supabase-discussion-store';
	import { ChevronDown, ChevronUp, Pencil, ThumbsDown, ThumbsUp, Trash2 } from '@lucide/svelte';

	let {
		comment,
		unlocked,
		onVote,
		onEdit,
		onDelete
	}: {
		comment: DiscussionComment;
		unlocked: boolean;
		onVote: (value: 1 | -1 | 0) => void;
		onEdit: (content: string) => Promise<void>;
		onDelete: () => void;
	} = $props();

	let isEditing = $state(false);
	let isExpanded = $state(false);
	let score = $derived(comment.upvotes - comment.downvotes);
	let shouldCollapse = $derived(score <= LOW_SCORE_COLLAPSE_THRESHOLD);
	let isCollapsed = $derived(shouldCollapse && !isExpanded);
	let authorHref = $derived(
		comment.author_username ? `/accounts/${encodeURIComponent(comment.author_username)}` : undefined
	);

	function deleteComment() {
		if (confirm('Delete your comment?')) onDelete();
	}
</script>

<article class="rounded-md border border-border bg-background p-3">
	<div class="mb-2 flex flex-wrap items-center justify-between gap-2 text-xs">
		<div class="flex items-center gap-2 text-muted-foreground">
			{#if authorHref}
				<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
				<a href={authorHref} class="font-medium text-foreground hover:underline">
					@{comment.author_username}
				</a>
			{:else}
				<span class="font-medium text-foreground">Anonymous solver</span>
			{/if}
			<time datetime={comment.created_at}>{new Date(comment.created_at).toLocaleDateString()}</time>
		</div>
		{#if comment.is_mine}
			<div class="flex items-center gap-1">
				<Button
					variant="ghost"
					size="icon"
					class="size-7"
					aria-label="Edit comment"
					onclick={() => (isEditing = !isEditing)}
				>
					<Pencil class="size-3.5" />
				</Button>
				<Button
					variant="ghost"
					size="icon"
					class="size-7"
					aria-label="Delete comment"
					onclick={deleteComment}
				>
					<Trash2 class="size-3.5" />
				</Button>
			</div>
		{/if}
	</div>

	{#if isEditing && comment.is_mine}
		<CommentComposer
			initialContent={comment.content}
			submitLabel="Save edit"
			onSubmit={async (content) => {
				await onEdit(content);
				isEditing = false;
			}}
			onCancel={() => (isEditing = false)}
		/>
	{:else if isCollapsed}
		<button
			type="button"
			class="flex w-full items-center justify-center gap-1 rounded bg-secondary px-3 py-2 text-xs text-muted-foreground hover:text-foreground"
			onclick={() => (isExpanded = true)}
		>
			<ChevronDown class="size-3.5" />
			Low-scoring comment ({score}) — expand
		</button>
	{:else}
		<p class="font-sans text-sm break-words whitespace-pre-wrap text-foreground">
			{comment.content}
		</p>
		{#if shouldCollapse}
			<button
				type="button"
				class="mt-2 flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground"
				onclick={() => (isExpanded = false)}
			>
				<ChevronUp class="size-3.5" />
				Collapse
			</button>
		{/if}
	{/if}

	{#if !isEditing}
		<div class="mt-2 flex items-center gap-1 border-t border-border pt-2">
			<Button
				variant="ghost"
				size="sm"
				disabled={comment.is_mine || !unlocked}
				aria-label="Upvote comment"
				aria-pressed={comment.my_vote === 1}
				class="h-7 px-2 {comment.my_vote === 1 ? 'text-primary' : ''}"
				onclick={() => onVote(comment.my_vote === 1 ? 0 : 1)}
			>
				<ThumbsUp class="size-3.5" />
				<span>{comment.upvotes}</span>
			</Button>
			<Button
				variant="ghost"
				size="sm"
				disabled={comment.is_mine || !unlocked}
				aria-label="Downvote comment"
				aria-pressed={comment.my_vote === -1}
				class="h-7 px-2 {comment.my_vote === -1 ? 'text-primary' : ''}"
				onclick={() => onVote(comment.my_vote === -1 ? 0 : -1)}
			>
				<ThumbsDown class="size-3.5" />
				<span>{comment.downvotes}</span>
			</Button>
		</div>
	{/if}
</article>
