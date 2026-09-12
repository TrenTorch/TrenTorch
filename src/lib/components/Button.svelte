<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { HTMLAttributes } from 'svelte/elements';

	type Variant = 'default' | 'outline' | 'ghost';
	type Size = 'default' | 'sm' | 'lg' | 'icon';

	let {
		variant = 'default',
		size = 'default',
		href,
		target,
		rel,
		class: className = '',
		children,
		...rest
	}: {
		variant?: Variant;
		size?: Size;
		href?: string;
		target?: string;
		rel?: string;
		class?: string;
		children: Snippet;
	} & HTMLAttributes<HTMLElement> = $props();

	const variants: Record<Variant, string> = {
		default: 'bg-primary text-primary-foreground hover:bg-primary/90',
		outline: 'border border-border bg-background hover:bg-accent hover:text-accent-foreground',
		ghost: 'hover:bg-accent hover:text-accent-foreground'
	};

	const sizes: Record<Size, string> = {
		default: 'h-9 px-4 py-2 text-sm',
		sm: 'h-8 px-3 text-sm',
		lg: 'h-10 px-6 text-sm',
		icon: 'size-9'
	};

	const base =
		'inline-flex shrink-0 items-center justify-center gap-2 rounded-md font-medium whitespace-nowrap transition-colors outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4';
</script>

{#if href}
	<!-- Generic component: callers pass either an already-resolve()'d internal
	     path or a full external URL, so this can't statically tell which. -->
	<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
	<a {href} {target} {rel} class="{base} {variants[variant]} {sizes[size]} {className}">
		{@render children()}
	</a>
{:else}
	<button type="button" class="{base} {variants[variant]} {sizes[size]} {className}" {...rest}>
		{@render children()}
	</button>
{/if}
