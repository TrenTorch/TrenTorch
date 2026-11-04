<script lang="ts">
	// The three dots of a window's title bar. On a window that does something they are its controls, and mean
	// what that window says they mean: each one is given a label ("clear", "minimise", ...), shown beside the
	// dots with a glyph inside the dot while the pointer is on it, held on a finger, or the dot has focus.
	// A dot with no action is grey and inert, and `decorative` dots are only an illustration: grey until the
	// pointer is over the window (give it `group/window`), then in colour, for feedback and nothing else.
	export type DotAction = {
		label: string;
		onclick?: () => void;
		/** An already-resolved path; the dot is then a link. */
		href?: string;
		disabled?: boolean;
		/** Green only: the glyph that points back in, for undoing an expand. */
		restore?: boolean;
	};

	const {
		red,
		yellow,
		green,
		decorative = false
	}: { red?: DotAction; yellow?: DotAction; green?: DotAction; decorative?: boolean } = $props();

	// The label of the dot under the pointer or focus. It is drawn `fixed` from the dot's own position rather
	// than inside the title bar, which every window clips, so it can sit above the dots wherever they are.
	// It remembers which dot, not what it said, so a label that changes on click ("fold" to "restore") changes
	// under the pointer too, and goes if the dot stops doing anything.
	let tipAt = $state<{ key: 'red' | 'yellow' | 'green'; x: number; y: number } | null>(null);
	function show(event: Event, key: 'red' | 'yellow' | 'green') {
		const box = (event.currentTarget as HTMLElement).getBoundingClientRect();
		tipAt = { key, x: box.left + box.width / 2, y: box.top };
	}
	const hide = () => (tipAt = null);

	const tipLabel = $derived.by(() => {
		const action = tipAt ? { red, yellow, green }[tipAt.key] : undefined;
		return action && !action.disabled ? action.label : null;
	});

	const DOTS = $derived([
		{
			key: 'red',
			action: red,
			colour: 'bg-red-500/70 hover:bg-red-500',
			hover: 'group-hover/window:bg-red-500/70',
			glyph: 'M3 3l6 6M9 3l-6 6'
		},
		{
			key: 'yellow',
			action: yellow,
			colour: 'bg-yellow-500/70 hover:bg-yellow-500',
			hover: 'group-hover/window:bg-yellow-500/70',
			glyph: 'M3 6h6'
		},
		{
			key: 'green',
			action: green,
			colour: 'bg-green-500/70 hover:bg-green-500',
			hover: 'group-hover/window:bg-green-500/70',
			glyph: 'M3 9V3h6M9 3L3 9',
			restoreGlyph: 'M9 3v6H3M3 9l6-6'
		}
	] as const);
</script>

{#if decorative}
	<span class="flex gap-1.5" aria-hidden="true">
		{#each DOTS as dot (dot.key)}
			<span
				class="size-2.5 rounded-full bg-muted-foreground/25 transition-colors duration-300 {dot.hover}"
			></span>
		{/each}
	</span>
{:else}
	<span class="group/dots relative flex gap-1.5" role="group" aria-label="Window controls">
		{#each DOTS as dot (dot.key)}
			{@const action = dot.action}
			{@const live = Boolean(action) && !action?.disabled}
			{@const cls = `relative grid size-3 shrink-0 place-items-center rounded-full text-black/60 transition-colors after:absolute after:-inset-1.5 after:content-[''] focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none ${live ? dot.colour + ' cursor-pointer' : 'cursor-default bg-muted-foreground/25'}`}
			{@const glyph = !live
				? ''
				: dot.key === 'green' && action?.restore
					? dot.restoreGlyph
					: dot.glyph}
			{#if live && action?.href}
				<!-- eslint-disable svelte/no-navigation-without-resolve -- callers pass an href already run through resolve() -->
				<a
					href={action.href}
					class={cls}
					aria-label={action.label}
					data-dot={dot.key}
					onpointerenter={(e) => show(e, dot.key)}
					onfocus={(e) => show(e, dot.key)}
					onpointerleave={hide}
					onblur={hide}
				>
					<svg
						viewBox="0 0 12 12"
						class="size-2 opacity-0 transition-opacity group-focus-within/dots:opacity-100 group-hover/dots:opacity-100"
						fill="none"
						stroke="currentColor"
						stroke-width="1.6"
						stroke-linecap="round"
						stroke-linejoin="round"
						aria-hidden="true"><path d={glyph} /></svg
					>
				</a>
				<!-- eslint-enable svelte/no-navigation-without-resolve -->
			{:else}
				<button
					type="button"
					class={cls}
					aria-label={action?.label ?? dot.key}
					aria-disabled={!live}
					disabled={!live}
					data-dot={dot.key}
					onclick={action?.onclick}
					onpointerenter={(e) => show(e, dot.key)}
					onfocus={(e) => show(e, dot.key)}
					onpointerleave={hide}
					onblur={hide}
				>
					<svg
						viewBox="0 0 12 12"
						class="size-2 opacity-0 transition-opacity group-focus-within/dots:opacity-100 group-hover/dots:opacity-100"
						fill="none"
						stroke="currentColor"
						stroke-width="1.6"
						stroke-linecap="round"
						stroke-linejoin="round"
						aria-hidden="true"><path d={glyph} /></svg
					>
				</button>
			{/if}
		{/each}
		{#if tipAt && tipLabel}
			<span
				class="pointer-events-none fixed z-50 -translate-x-1/2 -translate-y-full rounded bg-secondary px-1.5 py-0.5 font-mono text-[10px] whitespace-nowrap text-muted-foreground shadow-sm"
				style:left="{tipAt.x}px"
				style:top="{tipAt.y - 6}px"
				aria-hidden="true">{tipLabel}</span
			>
		{/if}
	</span>
{/if}
