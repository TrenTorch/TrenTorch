<script lang="ts">
	import * as Dialog from '$components/ui/dialog';
	import AuthPanel from './AuthPanel.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import { session } from '$processes/auth/session.svelte';
	import { clearAfterSignInDestination } from '$processes/auth/after-sign-in-destination';

	// Signing in (any method) fires onAuthStateChange, which updates
	// session.user -- close the prompt the moment that happens instead of
	// making the student close it themselves after it already did its job.
	$effect(() => {
		if (session.user && signInPrompt.isOpen) {
			signInPrompt.close();
		}
	});

	const copy = {
		run: {
			title: 'Sign in to run your code',
			description:
				'Running and submitting solutions needs an account, so your progress can actually be saved.'
		},
		browse: {
			title: 'Sign in to continue',
			description:
				'Questions and the Problem of the Day need a free account, so your progress can actually be saved.'
		}
	};
	const text = $derived(copy[signInPrompt.reason]);

	// Dismissed without signing in: forget where they were headed, so a
	// later, unrelated sign-in does not jump them to an old destination.
	function onOpenChange(open: boolean) {
		if (!open && !session.user) clearAfterSignInDestination();
	}
</script>

<Dialog.Root bind:open={signInPrompt.isOpen} {onOpenChange}>
	<Dialog.Content>
		<Dialog.Title>{text.title}</Dialog.Title>
		<Dialog.Description class="mb-4">{text.description}</Dialog.Description>
		<AuthPanel />
	</Dialog.Content>
</Dialog.Root>
