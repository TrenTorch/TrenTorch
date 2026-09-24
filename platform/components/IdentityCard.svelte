<script lang="ts">
	import { LogOut } from '@lucide/svelte';
	import * as Avatar from '$components/ui/avatar';
	import { Badge } from '$components/ui/badge';
	import { Progress } from '$components/ui/progress';
	import { Separator } from '$components/ui/separator';
	import Button from '$components/Button.svelte';
	import RatingBadge from '$components/RatingBadge.svelte';
	import { session, signOut } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import { loadProfile } from '$processes/profile/profile-store';
	import { profileState } from '$processes/profile/profile-state.svelte';
	import { ratingStore } from '$processes/rating/rating-store.svelte';

	let { solvedCount, total }: { solvedCount: number; total: number } = $props();

	const profile = $derived(profileState.data);

	// The account page's form fills the shared profile state itself; on any
	// other page (the questions list) the card loads it once for the signed-in user.
	$effect(() => {
		const id = session.user?.id;
		if (!id || profileState.data) return;
		loadProfile(id).then((loaded) => {
			if (loaded && !profileState.data && session.user?.id === id) profileState.set(loaded);
		});
	});
	const signedIn = $derived(session.user !== null);
	const name = $derived(
		profile?.displayName || session.user?.user_metadata?.full_name || 'Student'
	);
	const avatarUrl = $derived(session.user?.user_metadata?.avatar_url as string | undefined);
	const initials = $derived(
		name
			.split(' ')
			.map((part: string) => part[0])
			.join('')
			.slice(0, 2)
			.toUpperCase()
	);
	const subtitle = $derived(
		[profile?.jobTitle, profile?.organization].filter(Boolean).join(' at ') ||
			profile?.location ||
			''
	);
	const percent = $derived(total === 0 ? 0 : Math.round((solvedCount / total) * 100));

	const links = $derived(
		profile
			? [
					{ label: 'X', href: profile.xUrl },
					{ label: 'LinkedIn', href: profile.linkedinUrl },
					{ label: 'Scholar', href: profile.scholarUrl },
					{ label: 'GitHub', href: profile.githubUrl },
					{ label: 'Website', href: profile.websiteUrl }
				].filter((link) => link.href)
			: []
	);
</script>

<div class="space-y-5 rounded-2xl border border-foreground p-6 lg:sticky lg:top-20">
	{#if signedIn}
		<div class="flex items-center gap-3">
			<Avatar.Root class="size-14 rounded-xl after:rounded-xl">
				{#if avatarUrl}
					<Avatar.Image src={avatarUrl} alt="" class="rounded-xl" />
				{/if}
				<Avatar.Fallback class="rounded-xl font-mono text-lg">{initials}</Avatar.Fallback>
			</Avatar.Root>
			<div class="min-w-0">
				<p class="truncate font-mono text-lg leading-tight font-semibold">{name}</p>
				{#if profile?.username}
					<p class="truncate font-mono text-sm text-primary">@{profile.username}</p>
				{/if}
			</div>
		</div>

		{#if subtitle}
			<p class="text-sm text-muted-foreground">{subtitle}</p>
		{/if}
		{#if profile?.bio}
			<p class="text-sm leading-relaxed">{profile.bio}</p>
		{/if}
		{#if links.length > 0}
			<div class="flex flex-wrap gap-2">
				{#each links as link (link.label)}
					<!-- eslint-disable svelte/no-navigation-without-resolve -->
					<Badge
						variant="outline"
						href={link.href}
						target="_blank"
						rel="noopener noreferrer"
						class="h-6 border-foreground px-3 font-mono"
					>
						{link.label}
					</Badge>
					<!-- eslint-enable svelte/no-navigation-without-resolve -->
				{/each}
			</div>
		{/if}
	{:else}
		<div>
			<p class="font-mono text-lg font-semibold">Your account</p>
			<p class="mt-1 text-sm text-muted-foreground">
				Sign in to save your progress, earn a POTD rating and set up your profile.
			</p>
		</div>
	{/if}

	<Separator />
	<div class="space-y-2">
		<div class="mb-2 flex items-baseline justify-between">
			<p class="text-xs text-muted-foreground">Curriculum solved</p>
			<p class="font-mono text-sm font-semibold tabular-nums">{solvedCount} of {total}</p>
		</div>
		<Progress value={percent} class="h-2" aria-label="Curriculum solved" />
		<p class="mt-2 text-xs text-muted-foreground">
			{signedIn
				? 'Progress and code sync across your devices.'
				: 'Sign in to sync progress and code across devices.'}
		</p>
	</div>

	{#if signedIn}
		{#if ratingStore.rating !== null}
			<Separator />
			<div class="space-y-2">
				<p class="text-xs font-medium text-muted-foreground">POTD rating</p>
				<RatingBadge rating={ratingStore.rating ?? 400} />
				<p class="text-xs text-muted-foreground">
					Solving or failing the Problem of the Day moves this, nothing else does.
				</p>
			</div>
		{/if}
		{#if session.user}
			<Separator />
			<div class="space-y-2">
				<p class="mb-2 truncate text-sm text-muted-foreground">
					Signed in as <span class="font-medium text-foreground">{session.user.email}</span>
				</p>
				<Button variant="outline" size="sm" class="rounded-xl!" onclick={signOut}>
					<LogOut class="size-3.5" />
					Sign out
				</Button>
			</div>
		{/if}
	{:else}
		<Button size="sm" class="w-full rounded-xl!" onclick={() => signInPrompt.open()}>
			Sign in / Sign up
		</Button>
	{/if}
</div>
