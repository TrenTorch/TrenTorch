<script lang="ts">
	import { untrack } from 'svelte';
	import Button from '$components/Button.svelte';
	import { validateComment } from '$processes/discussion/validate-comment';

	let {
		initialContent = '',
		submitLabel = 'Post comment',
		onSubmit,
		onCancel
	}: {
		initialContent?: string;
		submitLabel?: string;
		onSubmit: (content: string) => Promise<void>;
		onCancel?: () => void;
	} = $props();

	let content = $state(untrack(() => initialContent));
	let isSubmitting = $state(false);
	let errorMessage = $state('');
	let validationError = $derived(validateComment(content));
	let characterCount = $derived([...content].length);
	let lineCount = $derived(content.replace(/\r/g, '').split('\n').length);

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (validationError || isSubmitting) return;
		isSubmitting = true;
		errorMessage = '';
		try {
			await onSubmit(content);
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Could not save your comment.';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<form class="space-y-2" onsubmit={handleSubmit}>
	<label class="sr-only" for="discussion-comment">Your comment</label>
	<textarea
		id="discussion-comment"
		bind:value={content}
		rows="5"
		placeholder="Share your approach or insight…"
		class="w-full resize-y rounded-md border border-border bg-background p-3 font-sans text-sm text-foreground placeholder:text-muted-foreground focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-none"
	></textarea>
	<div class="flex flex-wrap items-center justify-between gap-2 text-xs text-muted-foreground">
		<span>{characterCount}/2000 characters · {lineCount}/30 lines</span>
		<div class="flex items-center gap-2">
			{#if onCancel}
				<Button variant="ghost" size="sm" onclick={onCancel}>Cancel</Button>
			{/if}
			<Button type="submit" size="sm" disabled={Boolean(validationError) || isSubmitting}>
				{isSubmitting ? 'Saving…' : submitLabel}
			</Button>
		</div>
	</div>
	{#if validationError}
		<p class="text-xs text-destructive" role="status">{validationError}</p>
	{/if}
	{#if errorMessage}
		<p class="text-xs text-destructive" role="alert">{errorMessage}</p>
	{/if}
</form>
