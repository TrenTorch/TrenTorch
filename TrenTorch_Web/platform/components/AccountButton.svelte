<script lang="ts">
	import { resolve } from '$app/paths';
	import * as Avatar from '$components/ui/avatar';
	import Button from './Button.svelte';
	import { session } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';

	// Only a confirmed signed-in user gets their initial -- signed-out
	// visitors get an actual "Sign in" button instead (see below), not a
	// bare "?" avatar that didn't read as a sign-in affordance at all.
	const initial = $derived(
		(session.user?.email ?? session.user?.user_metadata?.full_name)?.[0]?.toUpperCase() ?? '?'
	);
</script>

{#if session.user}
	<a
		href={resolve('/account')}
		class="inline-flex size-9 items-center justify-center rounded-md transition-colors hover:bg-accent hover:text-accent-foreground"
		aria-label="Your account"
	>
		<Avatar.Root class="size-7">
			{#if session.user.user_metadata?.avatar_url}
				<Avatar.Image src={session.user.user_metadata.avatar_url} alt="" />
			{/if}
			<Avatar.Fallback class="font-mono text-xs">{initial}</Avatar.Fallback>
		</Avatar.Root>
	</a>
{:else}
	<Button variant="outline" size="sm" onclick={() => signInPrompt.open()}>Sign in</Button>
{/if}
