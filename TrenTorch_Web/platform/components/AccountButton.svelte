<script lang="ts">
	import { resolve } from '$app/paths';
	import * as Avatar from '$components/ui/avatar';
	import { session } from '$processes/auth/session.svelte';

	// Falls back to "?" while the session is still loading and for signed-out
	// visitors alike -- only a confirmed signed-in user gets their initial.
	const initial = $derived(
		(session.user?.email ?? session.user?.user_metadata?.full_name)?.[0]?.toUpperCase() ?? '?'
	);
</script>

<a
	href={resolve('/account')}
	class="inline-flex size-9 items-center justify-center rounded-md transition-colors hover:bg-accent hover:text-accent-foreground"
	aria-label={session.user ? 'Your account' : 'Sign in'}
>
	<Avatar.Root class="size-7">
		{#if session.user?.user_metadata?.avatar_url}
			<Avatar.Image src={session.user.user_metadata.avatar_url} alt="" />
		{/if}
		<Avatar.Fallback class="font-mono text-xs">{initial}</Avatar.Fallback>
	</Avatar.Root>
</a>
