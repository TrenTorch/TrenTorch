<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import ModeToggle from './ModeToggle.svelte';
	import AccountButton from './AccountButton.svelte';
	import Button from './Button.svelte';
	import { Menu, X } from '@lucide/svelte';
	import Github from './GithubIcon.svelte';

	const GITHUB_URL = 'https://github.com/TrenTorch/TrenTorch-Web';

	const routes = [
		{ href: resolve('/'), label: 'Home' },
		{ href: resolve('/questions'), label: 'Questions' }
	];

	let isOpen = $state(false);
</script>

<header
	class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
>
	<div class="container flex h-14 items-center justify-between px-4 md:px-6">
		<a href={resolve('/')} class="group flex items-center gap-2">
			<span
				class="font-mono text-xl font-bold transition-colors group-hover:text-primary sm:inline-block"
			>
				Tren<span class="text-primary">Torch</span>
			</span>
		</a>

		<!-- Desktop nav -->
		<div class="hidden flex-1 items-center justify-end space-x-6 md:flex">
			<nav class="flex items-center space-x-6 font-mono text-xs tracking-wider uppercase">
				{#each routes as route (route.href)}
					<a
						href={route.href}
						class="transition-colors hover:text-primary {page.url.pathname === route.href
							? 'text-primary'
							: 'text-foreground/60'}"
					>
						{route.label}
					</a>
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
						class="block text-sm font-medium transition-colors hover:text-foreground/80 {page.url
							.pathname === route.href
							? 'text-foreground'
							: 'text-foreground/60'}"
					>
						{route.label}
					</a>
				{/each}
			</nav>
		</div>
	{/if}
</header>
