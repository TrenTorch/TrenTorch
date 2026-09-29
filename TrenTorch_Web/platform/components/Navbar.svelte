<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import ModeToggle from './ModeToggle.svelte';
	import AccountButton from './AccountButton.svelte';
	import Button from './Button.svelte';
	import LogoBadge from './LogoBadge.svelte';
	import { Badge } from './ui/badge';
	import { Menu, X, Star, ChevronDown } from '@lucide/svelte';
	import Github from './GithubIcon.svelte';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch';

	// `gated` links ask a signed-out visitor to sign in when clicked; the
	// pages themselves stay public, so the hrefs are still plain links.
	const routes = [
		{ href: resolve('/questions'), label: 'Questions', gated: true },
		{
			href: resolve('/potd'),
			label: 'Problem of the day',
			gated: true
		}
		// "Roadmap" doesn't have a page yet -- listed here, unlinked, so
		// what's coming is visible without shipping a dead route.
	];

	// Entries in the desktop "Learn" dropdown (opens on hover or keyboard
	// focus, pure CSS). None have pages yet, so they're all unlinked.
	const comingSoonLearnLinks = [
		{ label: 'Research papers', hint: 'Curated reading, explained' },
		{ label: 'Blogs', hint: 'Writeups from the team' }
	];

	let isOpen = $state(false);

	// Live star count on the GitHub button -- fetched client-side (the site
	// is static-prerendered, so there's no build-time data source for this)
	// and left blank on failure/rate-limit rather than showing a stale or
	// fake number.
	let stars = $state<number | null>(null);
	$effect(() => {
		if (!browser) return;
		fetch('https://api.github.com/repos/TrenTorch/TrenTorch')
			.then((res) => (res.ok ? res.json() : null))
			.then((data) => {
				if (data && typeof data.stargazers_count === 'number') stars = data.stargazers_count;
			})
			.catch(() => {});
	});

	function formatStars(count: number): string {
		if (count < 1000) return String(count);
		return `${(count / 1000).toFixed(1).replace(/\.0$/, '')}k`;
	}
</script>

<header
	class="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
>
	<div
		class="container flex h-[4.75rem] items-center justify-between px-5 sm:px-7 lg:px-9 xl:px-10"
	>
		<div class="flex items-center gap-2.5">
			<LogoBadge class="size-9" />
			<span class="flex flex-col items-start gap-1">
				<a
					href={resolve('/')}
					class="font-mono text-xl leading-none font-bold tracking-wide text-foreground"
				>
					TrenTorch
				</a>
				<span class="flex items-baseline gap-1 text-[9px] leading-none text-muted-foreground">
					Sponsored by
					<a
						href="https://ui.wensity.com/?utm_source=trentorch&utm_medium=sponsorship&utm_campaign=trentorch_sponsor_2026"
						target="_blank"
						rel="noopener noreferrer"
						aria-label="Wensity, opens in a new tab"
						class="font-signature text-sm leading-none text-primary transition-colors hover:text-primary/80 focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
					>
						Wensity
					</a>
				</span>
			</span>
		</div>

		<!-- Desktop nav -->
		<div class="hidden flex-1 items-center justify-end space-x-5 lg:flex xl:space-x-6">
			<nav class="flex items-center space-x-6 font-mono text-xs tracking-wider uppercase">
				{#each routes as route (route.href)}
					<a
						href={route.href}
						onclick={(event) => route.gated && gateBehindSignIn(event)}
						class="flex items-center gap-1.5 transition-colors hover:text-primary {page.url
							.pathname === route.href
							? 'text-primary'
							: 'text-foreground'}"
					>
						{route.label}
					</a>
				{/each}
				<div class="group relative">
					<button
						type="button"
						aria-haspopup="menu"
						class="flex items-center gap-1 uppercase transition-colors group-focus-within:text-primary group-hover:text-primary"
					>
						Learn
						<ChevronDown
							class="size-3.5 transition-transform group-focus-within:rotate-180 group-hover:rotate-180"
						/>
					</button>
					<div
						class="invisible absolute top-full right-0 z-50 translate-y-1 pt-3 opacity-0 transition duration-200 group-focus-within:visible group-focus-within:translate-y-0 group-focus-within:opacity-100 group-hover:visible group-hover:translate-y-0 group-hover:opacity-100 motion-reduce:transition-none"
					>
						<ul
							class="w-64 rounded-xl border border-border bg-popover p-1.5 shadow-2xl shadow-black/40"
							role="menu"
						>
							<li
								role="none"
								class="flex cursor-not-allowed items-center gap-1.5 rounded-lg px-3 py-2.5 text-popover-foreground/30"
								title="Coming soon"
							>
								Roadmap
								<Badge
									variant="outline"
									class="h-4 rounded-full border-border px-1.5 text-[9px] text-popover-foreground/40 normal-case"
									>soon</Badge
								>
							</li>
							{#each comingSoonLearnLinks as link (link.label)}
								<li
									role="none"
									class="flex cursor-not-allowed flex-col rounded-lg px-3 py-2.5 text-popover-foreground/30"
									title="Coming soon"
								>
									<span class="flex items-center gap-1.5">
										{link.label}
										<Badge
											variant="outline"
											class="h-4 rounded-full border-border px-1.5 text-[9px] text-popover-foreground/40 normal-case"
											>soon</Badge
										>
									</span>
									<span class="mt-0.5 text-[11px] tracking-normal normal-case">{link.hint}</span>
								</li>
							{/each}
						</ul>
					</div>
				</div>
			</nav>
			<Button
				variant="outline"
				size="sm"
				href={GITHUB_URL}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Github class="size-4" />
				GitHub
				{#if stars !== null}
					<span class="flex items-center gap-1 border-l border-current/20 pl-2 text-current/60">
						<Star class="size-3.5 fill-[#e3b341] text-[#e3b341]" />
						{formatStars(stars)}
					</span>
				{/if}
			</Button>
			<ModeToggle />
			<AccountButton />
		</div>

		<!-- Mobile nav toggle -->
		<div class="flex items-center space-x-2 lg:hidden">
			<Button
				variant="ghost"
				size="icon"
				href={GITHUB_URL}
				target="_blank"
				rel="noopener noreferrer"
			>
				<Github class="size-5" />
				<span class="sr-only">GitHub</span>
			</Button>
			<ModeToggle />
			<AccountButton />
			<button
				type="button"
				class="inline-flex size-9 items-center justify-center rounded-md hover:bg-accent hover:text-accent-foreground lg:hidden"
				onclick={() => (isOpen = !isOpen)}
			>
				<span class="sr-only">Toggle menu</span>
				{#if isOpen}
					<X class="size-5" />
				{:else}
					<Menu class="size-5" />
				{/if}
			</button>
		</div>
	</div>

	<!-- Mobile nav menu -->
	{#if isOpen}
		<div class="border-t bg-background lg:hidden">
			<nav class="container flex flex-col space-y-4 px-5 py-5 sm:px-6">
				{#each routes as route (route.href)}
					<a
						href={route.href}
						onclick={(event) => {
							isOpen = false;
							if (route.gated) gateBehindSignIn(event);
						}}
						class="flex items-center gap-1.5 text-sm font-medium transition-colors hover:text-foreground/80 {page
							.url.pathname === route.href
							? 'text-foreground'
							: 'text-foreground'}"
					>
						{route.label}
					</a>
				{/each}
				<span class="flex cursor-not-allowed items-center gap-1.5 text-sm text-foreground/30">
					Roadmap
					<Badge variant="outline" class="h-4 px-1 text-[9px] text-foreground/40">soon</Badge>
				</span>
			</nav>
		</div>
	{/if}
</header>
