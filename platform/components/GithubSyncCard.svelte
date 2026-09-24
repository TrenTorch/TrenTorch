<script lang="ts">
	import { page } from '$app/state';
	import Button from '$components/Button.svelte';
	import { Badge } from '$components/ui/badge';
	import { session } from '$processes/auth/session.svelte';
	import {
		githubSync,
		loadGithubStatus,
		confirmFreshConnection,
		connectGithub,
		disconnectGithub,
		resetGithubSync
	} from '$processes/github-sync/github-sync.svelte';

	// Only load once per signed-in user; the IDE page reads the same state.
	$effect(() => {
		if (session.user && githubSync.status === 'unknown') void loadGithubStatus();
		else if (!session.user && !session.isLoading) resetGithubSync();
	});

	// Coming back from GitHub: the new connection can lag behind the redirect.
	$effect(() => {
		if (session.user && page.url.searchParams.get('github') === 'connected') {
			void confirmFreshConnection();
		}
	});

	const justConnected = $derived(page.url.searchParams.get('github') === 'connected');
	const failed = $derived(page.url.searchParams.get('github') === 'error');
	const needsRepo = $derived(page.url.searchParams.get('github') === 'norepo');
	const repoUrl = $derived(githubSync.repo ? `https://github.com/${githubSync.repo}` : null);
</script>

{#if session.user && githubSync.status !== 'unavailable'}
	<div class="space-y-3 rounded-2xl border border-foreground p-6">
		<div class="flex items-center justify-between gap-2">
			<p class="text-sm font-semibold">Save solutions to GitHub</p>
			{#if githubSync.status === 'connected'}
				<Badge variant="outline" class="border-foreground font-mono">Connected</Badge>
			{/if}
		</div>

		{#if githubSync.status === 'connected'}
			<p class="text-xs text-muted-foreground">
				Each time you pass a question, your latest solution and the question description are
				committed to
				<!-- eslint-disable svelte/no-navigation-without-resolve -->
				<a
					href={repoUrl}
					target="_blank"
					rel="noopener noreferrer"
					class="font-mono text-foreground underline">{githubSync.repo}</a
				>.
				<!-- eslint-enable svelte/no-navigation-without-resolve -->
			</p>
			{#if githubSync.lastSyncedAt}
				<p class="text-xs text-muted-foreground">
					Last saved {new Date(githubSync.lastSyncedAt).toLocaleTimeString()}.
				</p>
			{/if}
			<Button
				variant="outline"
				size="sm"
				class="rounded-xl!"
				disabled={githubSync.busy}
				onclick={disconnectGithub}
			>
				Disconnect
			</Button>
		{:else}
			<p class="text-xs text-muted-foreground">
				Create an empty public <span class="font-mono">trentorch-solutions</span> repo, then connect and
				select only that repo when GitHub asks. TrenTorch can then write to that one repo and nothing
				else.
			</p>
			<Button
				size="sm"
				class="rounded-xl!"
				disabled={githubSync.busy || githubSync.status === 'unknown'}
				onclick={connectGithub}
			>
				Connect GitHub
			</Button>
		{/if}

		{#if needsRepo}
			<p class="text-xs text-destructive">
				TrenTorch cannot see a <span class="font-mono">trentorch-solutions</span> repo.
				<!-- eslint-disable svelte/no-navigation-without-resolve -->
				<a
					href="https://github.com/new?name=trentorch-solutions&visibility=public"
					target="_blank"
					rel="noopener noreferrer"
					class="underline">Create it</a
				>, or
				<a
					href="https://github.com/settings/installations"
					target="_blank"
					rel="noopener noreferrer"
					class="underline">add it to the TrenTorch app</a
				>, then connect again.
				<!-- eslint-enable svelte/no-navigation-without-resolve -->
			</p>
		{:else if failed}
			<p class="text-xs text-destructive">GitHub did not connect. Try again.</p>
		{:else if justConnected && githubSync.status === 'connected'}
			<p class="text-xs text-muted-foreground">Connected. Your repo is ready.</p>
		{/if}
		{#if githubSync.lastError}
			<p class="text-xs text-destructive">{githubSync.lastError}</p>
		{/if}
	</div>
{/if}
