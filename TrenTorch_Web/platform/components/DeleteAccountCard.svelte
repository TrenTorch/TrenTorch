<script lang="ts">
	import Button from '$components/Button.svelte';
	import { Input } from '$components/ui/input';
	import * as Dialog from '$components/ui/dialog';
	import { session } from '$processes/auth/session.svelte';
	import { deleteAccount } from '$processes/auth/delete-account';

	const CONFIRM_WORD = 'DELETE';

	let open = $state(false);
	let typed = $state('');
	let busy = $state(false);
	let error = $state<string | null>(null);

	const canDelete = $derived(typed.trim() === CONFIRM_WORD && !busy);

	function onOpenChange(next: boolean) {
		if (busy) return;
		open = next;
		if (!next) {
			typed = '';
			error = null;
		}
	}

	async function confirmDelete() {
		if (!canDelete) return;
		busy = true;
		error = null;
		const result = await deleteAccount();
		if (result.ok) {
			// Full reload so no signed-in state survives in memory.
			window.location.assign('/');
			return;
		}
		error = result.message;
		busy = false;
	}
</script>

{#if session.user}
	<div class="rounded-2xl border border-destructive p-6">
		<h2 class="mb-1 font-mono font-semibold text-destructive">Delete account</h2>
		<p class="mb-4 text-sm text-muted-foreground">
			Permanently deletes your account, profile, rating history, solved questions and synced code.
			This cannot be undone. Solutions already saved to your GitHub repo stay there.
		</p>
		<Button
			type="button"
			variant="outline"
			size="sm"
			class="rounded-xl! border-destructive text-destructive hover:bg-destructive hover:text-white"
			onclick={() => (open = true)}
		>
			Delete my account
		</Button>
	</div>

	<Dialog.Root bind:open {onOpenChange}>
		<Dialog.Content>
			<Dialog.Title class="text-destructive">Delete your account?</Dialog.Title>
			<Dialog.Description class="mb-4">
				This removes everything tied to {session.user.email ?? 'your account'} for good. Type
				<span class="font-mono font-semibold text-foreground">{CONFIRM_WORD}</span> to confirm.
			</Dialog.Description>
			<form
				class="space-y-3"
				onsubmit={(event) => {
					event.preventDefault();
					void confirmDelete();
				}}
			>
				<Input bind:value={typed} autocomplete="off" aria-label="Type DELETE to confirm" />
				{#if error}
					<p class="text-xs text-destructive">{error}</p>
				{/if}
				<div class="flex gap-2">
					<Button
						type="submit"
						size="sm"
						class="rounded-xl! bg-destructive text-white hover:bg-destructive/90"
						disabled={!canDelete}
					>
						{busy ? 'Deleting...' : 'Delete forever'}
					</Button>
					<Button
						type="button"
						variant="outline"
						size="sm"
						class="rounded-xl!"
						disabled={busy}
						onclick={() => onOpenChange(false)}
					>
						Cancel
					</Button>
				</div>
			</form>
		</Dialog.Content>
	</Dialog.Root>
{/if}
