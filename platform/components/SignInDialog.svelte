<script lang="ts">
	import * as Dialog from '$components/ui/dialog';
	import AuthPanel from './AuthPanel.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import { session } from '$processes/auth/session.svelte';

	// Signing in (any method) fires onAuthStateChange, which updates
	// session.user -- close the prompt the moment that happens instead of
	// making the student close it themselves after it already did its job.
	$effect(() => {
		if (session.user && signInPrompt.isOpen) {
			signInPrompt.close();
		}
	});
</script>

<Dialog.Root bind:open={signInPrompt.isOpen}>
	<Dialog.Content>
		<Dialog.Title>Sign in to run your code</Dialog.Title>
		<Dialog.Description class="mb-4">
			Running and submitting solutions needs an account, so your progress can actually be saved.
		</Dialog.Description>
		<AuthPanel />
	</Dialog.Content>
</Dialog.Root>
