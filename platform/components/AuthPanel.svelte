<script lang="ts">
	import {
		session,
		signInWithGitHub,
		signInWithGoogle,
		signInWithMagicLink,
		signOut
	} from '$processes/auth/session.svelte';
	import Button from './Button.svelte';
	import Github from './GithubIcon.svelte';
	import { Mail, LogOut, CheckCircle2 } from '@lucide/svelte';

	let email = $state('');
	let magicLinkSent = $state(false);
	let error = $state<string | null>(null);
	let isSendingLink = $state(false);

	async function handleMagicLink(e: Event) {
		e.preventDefault();
		error = null;
		isSendingLink = true;
		try {
			await signInWithMagicLink(email);
			magicLinkSent = true;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Could not send the sign-in link.';
		} finally {
			isSendingLink = false;
		}
	}
</script>

{#if session.isLoading}
	<div class="text-sm text-muted-foreground">Checking sign-in status...</div>
{:else if session.user}
	<div class="flex items-center justify-between gap-4">
		<p class="text-sm text-muted-foreground">
			Signed in as <span class="font-medium text-foreground">{session.user.email}</span>
		</p>
		<Button variant="outline" size="sm" onclick={signOut}>
			<LogOut class="size-3.5" />
			Sign out
		</Button>
	</div>
{:else}
	<div class="flex flex-col gap-3">
		<div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
			<Button variant="outline" size="sm" class="w-full" onclick={signInWithGitHub}>
				<Github class="size-4" />
				Continue with GitHub
			</Button>
			<Button variant="outline" size="sm" class="w-full" onclick={signInWithGoogle}>
				<svg viewBox="0 0 24 24" class="size-4" aria-hidden="true">
					<path
						fill="currentColor"
						d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
					/>
					<path
						fill="currentColor"
						d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
					/>
					<path
						fill="currentColor"
						d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93z"
					/>
					<path
						fill="currentColor"
						d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
					/>
				</svg>
				Continue with Google
			</Button>
		</div>

		<div class="flex items-center gap-3 text-xs text-muted-foreground">
			<div class="h-px flex-1 bg-border"></div>
			<span>or</span>
			<div class="h-px flex-1 bg-border"></div>
		</div>

		{#if magicLinkSent}
			<p class="flex items-center gap-2 text-sm text-muted-foreground">
				<CheckCircle2 class="size-4 text-green-600 dark:text-green-400" />
				Check <span class="font-medium text-foreground">{email}</span> for a sign-in link.
			</p>
		{:else}
			<form class="flex flex-col gap-2 sm:flex-row" onsubmit={handleMagicLink}>
				<input
					type="email"
					required
					placeholder="you@example.com"
					bind:value={email}
					class="flex-1 rounded-md border border-input bg-background px-3 py-1.5 text-sm outline-none focus-visible:ring-1 focus-visible:ring-ring"
				/>
				<Button type="submit" variant="outline" size="sm" disabled={isSendingLink}>
					<Mail class="size-3.5" />
					{isSendingLink ? 'Sending...' : 'Email me a link'}
				</Button>
			</form>
			{#if error}
				<p class="text-sm text-destructive">{error}</p>
			{/if}
		{/if}
	</div>
{/if}
