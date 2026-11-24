<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import type { Pathname } from '$app/types';
	import { ChevronDown } from '@lucide/svelte';
	import { Badge } from './ui/badge';
	import { gateBehindSignIn } from '$processes/auth/gate-behind-sign-in';

	export type NavItem = {
		label: string;
		hint: string;
		href?: Pathname; // omitted = coming soon
		gated?: boolean;
	};

	// resolve() wants one literal route, not the whole union.
	const to = (href: Pathname) => resolve(href as '/');

	let { label, items }: { label: string; items: NavItem[] } = $props();

	const active = $derived(
		items.some((item) => item.href && page.url.pathname.startsWith(to(item.href)))
	);
</script>

<!-- Opens on hover or keyboard focus, pure CSS. -->
<div class="group relative">
	<button
		type="button"
		aria-haspopup="menu"
		class="flex items-center gap-1 uppercase transition-colors group-focus-within:text-primary group-hover:text-primary {active
			? 'text-primary'
			: 'text-foreground'}"
	>
		{label}
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
			{#each items as item (item.label)}
				<li role="none">
					{#if item.href}
						<a
							role="menuitem"
							href={to(item.href)}
							onclick={(event) => item.gated && gateBehindSignIn(event)}
							class="group/item flex flex-col rounded-lg px-3 py-2.5 text-popover-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
						>
							<span class="flex items-center gap-1.5 [word-spacing:-0.3em]">{item.label}</span>
							<span
								class="mt-0.5 text-[11px] tracking-normal text-muted-foreground normal-case group-hover/item:text-accent-foreground/70"
								>{item.hint}</span
							>
						</a>
					{:else}
						<div
							class="flex cursor-not-allowed flex-col rounded-lg px-3 py-2.5 text-popover-foreground"
							title="Coming soon"
						>
							<span class="flex items-center gap-1.5 [word-spacing:-0.3em]">
								{item.label}
								<Badge
									variant="outline"
									class="h-4 rounded-full border-border px-1.5 text-[9px] text-muted-foreground normal-case"
									>soon</Badge
								>
							</span>
							<span class="mt-0.5 text-[11px] tracking-normal text-muted-foreground normal-case"
								>{item.hint}</span
							>
						</div>
					{/if}
				</li>
			{/each}
		</ul>
	</div>
</div>
