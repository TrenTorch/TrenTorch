<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { browser } from '$app/environment';
	import ModeToggle from './ModeToggle.svelte';
	import AccountButton from './AccountButton.svelte';
	import Button from './Button.svelte';
	import LogoBadge from './LogoBadge.svelte';
	import { Badge } from './ui/badge';
	import { Menu, X, Star } from '@lucide/svelte';
	import Github from './GithubIcon.svelte';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch-Web';

	const routes = [
		{ href: resolve('/'), label: 'Home' },
		{ href: resolve('/questions'), label: 'Questions' },
		{ href: resolve('/potd'), label: 'Problem of the day', pill: 'new' as const }
		// "Problem set" (a curated multi-question challenge set, distinct from
		// the single daily POTD) doesn't have a page yet -- listed here,
		// unlinked, so the roadmap is visible without shipping a dead route.
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
	class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
>
	<div class="container flex h-14 items-center justify-between px-4 md:px-6">
		<a href={resolve('/')} class="group flex items-center gap-2">
			<LogoBadge class="size-7" />
			<span class="font-mono text-base font-bold tracking-wide text-foreground sm:inline-block">
				TrenTorch
			</span>
		</a>

		<!-- Desktop nav -->
		<div class="hidden flex-1 items-center justify-end space-x-6 md:flex">
			<nav class="flex items-center space-x-6 font-mono text-xs tracking-wider uppercase">
				{#each routes as route (route.href)}
					<a
						href={route.href}
						class="flex items-center gap-1.5 transition-colors hover:text-primary {page.url
							.pathname === route.href
							? 'text-primary'
							: 'text-foreground/60'}"
					>
						{route.label}
						{#if route.pill === 'new'}
							<Badge variant="destructive" class="h-4 px-1 text-[9px] normal-case">new</Badge>
						{/if}
					</a>
				{/each}
				<span
					class="flex cursor-not-allowed items-center gap-1.5 text-foreground/30"
					title="Coming soon"
				>
					Problem set
					<Badge variant="outline" class="h-4 px-1 text-[9px] text-foreground/40 normal-case"
						>soon</Badge
					>
				</span>
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
					<span class="flex items-center gap-1 border-l border-current/20 pl-2 text-foreground/60">
						<Star class="size-3.5 fill-current" />
						{formatStars(stars)}
					</span>
				{/if}
			</Button>
			<ModeToggle />
			<AccountButton />
		</div>

		<!-- Mobile nav toggle -->
		<div class="flex items-center space-x-2 md:hidden">
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
				class="inline-flex size-9 items-center justify-center rounded-md hover:bg-accent hover:text-accent-foreground md:hidden"
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
		<div class="border-t bg-background md:hidden">
			<nav class="container flex flex-col space-y-4 px-4 py-4">
				{#each routes as route (route.href)}
					<a
						href={route.href}
						onclick={() => (isOpen = false)}
						class="flex items-center gap-1.5 text-sm font-medium transition-colors hover:text-foreground/80 {page
							.url.pathname === route.href
							? 'text-foreground'
							: 'text-foreground/60'}"
					>
						{route.label}
						{#if route.pill === 'new'}
							<Badge variant="destructive" class="h-4 px-1 text-[9px]">new</Badge>
						{/if}
					</a>
				{/each}
				<span class="flex cursor-not-allowed items-center gap-1.5 text-sm text-foreground/30">
					Problem set
					<Badge variant="outline" class="h-4 px-1 text-[9px] text-foreground/40">soon</Badge>
				</span>
			</nav>
		</div>
	{/if}
</header>
