<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import ModeToggle from './ModeToggle.svelte';
	import AccountButton from './AccountButton.svelte';
	import Button from './Button.svelte';
	import LogoBadge from './LogoBadge.svelte';
	import { Badge } from './ui/badge';
	import NavDropdown, { type NavItem } from './NavDropdown.svelte';
	import { Menu, X, Star } from '@lucide/svelte';
	import Github from './GithubIcon.svelte';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch';

	// `gated` links ask a signed-out visitor to sign in when clicked; the
	// pages themselves stay public, so the hrefs are still plain links.
	const routes = [
		{ href: resolve('/modules'), label: 'Module', gated: false }
	];

	// Desktop dropdowns open on hover or keyboard focus; the mobile menu lists
	// the same entries. Items without an href are shown as "soon".
	const menus: { label: string; items: NavItem[] }[] = [
		{
			label: 'Practice',
			items: [
				{
					label: 'Problem of the day',
					hint: 'A new question, featured every day',
					href: '/potd',
					gated: true
				},
				{
					label: 'Problemset',
					hint: 'Every practice problem, filterable',
					href: '/problemset'
				}
			]
		},
		{
			label: 'Learn',
			items: [
				{ label: 'Roadmap', hint: 'Where to start and what comes next' },
				{ label: 'Papers', hint: 'Research papers, explained', href: '/papers' },
				{ label: 'Blogs', hint: 'Writeups from the team' }
			]
		}
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
	<div class="container flex h-14 items-center justify-between px-5 sm:px-7 lg:px-9 xl:px-10">
		<div class="flex items-center gap-2.5">
			<LogoBadge class="size-8" />
			<span class="flex flex-col items-start gap-0.5">
				<a
					href={resolve('/')}
					class="font-mono text-lg leading-none font-bold tracking-wide text-foreground"
				>
					TrenTorch
				</a>
			</span>
		</div>

		<!-- Desktop nav -->
		<div class="hidden flex-1 items-center justify-end space-x-5 lg:flex xl:space-x-6">
			<nav class="flex items-center space-x-6 font-mono text-xs tracking-wider uppercase">
				{#each routes as route (route.href)}
					<a
						href={route.href}
						onclick={(event) => route.gated && gateBehindSignIn(event)}
						class="flex items-center gap-1.5 transition-colors [word-spacing:-0.3em] hover:text-primary {page
							.url.pathname === route.href
							? 'text-primary'
							: 'text-foreground'}"
					>
						{route.label}
					</a>
				{/each}
				{#each menus as menu (menu.label)}
					<NavDropdown label={menu.label} items={menu.items} />
				{/each}
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
				{#each menus as menu (menu.label)}
					<span class="pt-2 font-mono text-[11px] tracking-wider text-muted-foreground uppercase"
						>{menu.label}</span
					>
					{#each menu.items as item (item.label)}
						{#if item.href}
							<a
								href={item.href}
								onclick={(event) => {
									isOpen = false;
									if (item.gated) gateBehindSignIn(event);
								}}
								class="flex items-center gap-1.5 text-sm font-medium text-foreground transition-colors hover:text-foreground/80"
							>
								{item.label}
							</a>
						{:else}
							<span class="flex cursor-not-allowed items-center gap-1.5 text-sm text-foreground/30">
								{item.label}
								<Badge variant="outline" class="h-4 px-1 text-[9px] text-foreground/40">soon</Badge>
							</span>
						{/if}
					{/each}
				{/each}
			</nav>
		</div>
	{/if}
</header>
