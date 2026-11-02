<script lang="ts">
	import { resolve } from '$app/paths';
	import * as Avatar from '$components/ui/avatar';
	import Button from './Button.svelte';
	import { User } from '@lucide/svelte';
	import { signInSkipped } from '$processes/auth/preview-mode';
	import { session } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';

	// A confirmed signed-out visitor gets a Sign in button; a signed-in user gets
	// their profile picture. While the session is still loading, and in preview
	// builds that skip sign-in, the picture slot shows a person icon instead so
	// the header does not flash a button that is about to disappear.
	const showSignIn = $derived(!session.isLoading && !session.user && !signInSkipped());

	const initial = $derived(
		(session.user?.email ?? session.user?.user_metadata?.full_name)?.[0]?.toUpperCase() ?? null
	);
</script>

{#if showSignIn}
	<Button variant="outline" size="sm" onclick={() => signInPrompt.open('header')}>Sign in</Button>
{:else}
	<a
		href={resolve('/account')}
		class="inline-flex size-9 items-center justify-center rounded-md border border-transparent transition-colors hover:border-foreground"
		aria-label={session.user ? 'Your account' : 'Account'}
	>
		<Avatar.Root class="size-7 rounded-md after:rounded-md">
			{#if session.user?.user_metadata?.avatar_url}
				<Avatar.Image src={session.user.user_metadata.avatar_url} alt="" class="rounded-md" />
			{/if}
			<Avatar.Fallback class="rounded-md font-mono text-xs">
				{#if initial}
					{initial}
				{:else}
					<User class="size-4" />
				{/if}
			</Avatar.Fallback>
		</Avatar.Root>
	</a>
{/if}
