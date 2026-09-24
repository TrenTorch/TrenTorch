<script lang="ts">
	import { resolve } from '$app/paths';
	import * as Avatar from '$components/ui/avatar';
	import { User } from '@lucide/svelte';
	import { session } from '$processes/auth/session.svelte';

	// Falls back to a person icon while the session is still loading and for
	// signed-out visitors alike -- only a confirmed signed-in user gets their
	// initial.
	const initial = $derived(
		(session.user?.email ?? session.user?.user_metadata?.full_name)?.[0]?.toUpperCase() ?? null
	);
</script>

<a
	href={resolve('/account')}
	class="inline-flex size-9 items-center justify-center border border-transparent transition-colors hover:border-foreground"
	aria-label={session.user ? 'Your account' : 'Sign in'}
>
	<Avatar.Root class="size-7 rounded-none after:rounded-none">
		{#if session.user?.user_metadata?.avatar_url}
			<Avatar.Image src={session.user.user_metadata.avatar_url} alt="" class="rounded-none" />
		{/if}
		<Avatar.Fallback class="rounded-none font-mono text-xs">
			{#if initial}
				{initial}
			{:else}
				<User class="size-4" />
			{/if}
		</Avatar.Fallback>
	</Avatar.Root>
</a>
