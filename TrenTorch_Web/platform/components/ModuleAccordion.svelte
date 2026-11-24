<script lang="ts" module>
	import type { LucideIcon } from '@lucide/svelte';

	export interface AccordionItem {
		id: string;
		title: string;
		icon: LucideIcon;
		/** What the row counts, e.g. 120 questions. */
		count: number;
		solved: number;
		/** Overrides the list's noun for this row, for a list that mixes kinds (chapters and problems). */
		noun?: string;
	}

	export const PAGE_SIZE = 4;

	/** The page a shared link should open on: ?page=N, else the page holding the linked module. */
	export function startPage(
		items: { id: string }[],
		linked: string | null,
		pageSize = PAGE_SIZE
	): number {
		if (typeof window === 'undefined') return 1;
		const fromUrl = Number(new URL(window.location.href).searchParams.get('page'));
		if (fromUrl > 0) return fromUrl;
		const at = items.findIndex((item) => item.id === linked);
		return at < 0 ? 1 : Math.floor(at / pageSize) + 1;
	}
</script>

<script lang="ts">
	import { onMount, type Snippet } from 'svelte';
	import { ChevronDown } from '@lucide/svelte';
	import Pagination from '$components/Pagination.svelte';
	import { Progress } from '$components/ui/progress';

	// One look and one behaviour for every domain page: each module is a row that
	// opens in place, and its contents are only mounted while it is open, so a
	// domain with a thousand questions still loads as a short list.
	let {
		items,
		noun = 'question',
		forceOpen = false,
		initialOpen = null,
		hue = '#9aa0a6',
		pageSize = PAGE_SIZE,
		page = $bindable(1),
		art,
		children
	}: {
		items: AccordionItem[];
		/** The domain's tint, used for the glyph tiles. */
		hue?: string;
		/** Modules per page: a few open at a time read cleaner than a dozen stacked. */
		pageSize?: number;
		/** Current page, 1-based; the page keeps it in the URL (?page=N). */
		page?: number;
		/** A small drawing for a module's tile; without it the module's icon is used. */
		art?: Snippet<[AccordionItem]>;
		noun?: string;
		/** Opens every row (used while filtering, so matches are visible); rows can still be closed. */
		forceOpen?: boolean;
		/** A row to open and scroll to when the page loads, e.g. from a shared link. */
		initialOpen?: string | null;
		children: Snippet<[AccordionItem]>;
	} = $props();

	// Rows opened by hand; unrelated to the filter, so closing one sticks afterwards.
	let opened = $state<string[]>(initialOpen ? [initialOpen] : []);
	// While filtering, rows start open so matches are visible, but a click still closes one.
	// Those closings are forgotten whenever the filter or the matching rows change.
	let dismissed = $state<string[]>([]);
	$effect.pre(() => {
		void forceOpen;
		void items.map((item) => item.id).join('|');
		dismissed = [];
	});
	const isOpen = (id: string) => (forceOpen ? !dismissed.includes(id) : opened.includes(id));
	const flip = (list: string[], id: string) =>
		list.includes(id) ? list.filter((other) => other !== id) : [...list, id];
	const toggle = (id: string) => {
		if (forceOpen) dismissed = flip(dismissed, id);
		else opened = flip(opened, id);
	};

	const totalPages = $derived(Math.max(1, Math.ceil(items.length / pageSize)));
	const current = $derived(Math.min(Math.max(1, page), totalPages));
	const shown = $derived(items.slice((current - 1) * pageSize, current * pageSize));

	// Plain history.replaceState: the URL only has to reflect the page for reload and
	// sharing; the route itself never changes.
	function goToPage(n: number) {
		page = Math.min(Math.max(1, n), totalPages);
		const url = new URL(window.location.href);
		url.searchParams.set('page', String(page));
		history.replaceState(history.state, '', url);
	}

	onMount(() => {
		if (initialOpen) document.getElementById(`module-${initialOpen}`)?.scrollIntoView();
	});
</script>

<div class="grid gap-3">
	{#each shown as item (item.id)}
		{@const open = isOpen(item.id)}
		{@const complete = item.count > 0 && item.solved >= item.count}
		{@const inProgress = item.solved > 0 && !complete}
		<section
			id="module-{item.id}"
			class="scroll-mt-20 overflow-hidden rounded-md border transition-colors {inProgress
				? 'border-primary/60'
				: 'border-border'}"
		>
			<h3>
				<button
					type="button"
					onclick={() => toggle(item.id)}
					aria-expanded={open}
					aria-controls="module-body-{item.id}"
					class="group flex w-full items-center gap-5 px-5 py-5 text-left transition-colors hover:bg-secondary/60"
				>
					<span
						class="relative flex shrink-0 items-center justify-center overflow-hidden rounded-2xl border border-border {art
							? 'h-[100px] w-40 p-2'
							: 'size-16'}"
						style="background-color: color-mix(in oklab, {hue} 24%, var(--background));"
					>
						<span
							class="absolute inset-0 blur-[0.6px]"
							style="background-image: radial-gradient(color-mix(in oklab, var(--foreground) 9%, transparent) 1px, transparent 1.4px); background-size: 5px 5px;"
							aria-hidden="true"
						></span>
						{#if art}
							<span class="relative block w-full">{@render art(item)}</span>
						{:else}
							<item.icon class="relative size-7 text-foreground" aria-hidden="true" />
						{/if}
					</span>
					<span class="min-w-0 flex-1">
						<span class="block text-lg font-semibold">{item.title}</span>
						<span class="block text-xs text-muted-foreground">
							{item.count}
							{item.noun ?? noun}{item.count === 1 ? '' : 's'}
							{#if item.solved > 0}
								&middot; {complete ? 'all done' : `${item.solved} done`}
							{/if}
						</span>
						{#if inProgress || complete}
							<Progress value={item.solved} max={item.count} class="mt-2 h-1 max-w-52" />
						{/if}
					</span>
					<ChevronDown
						class="size-4 shrink-0 text-muted-foreground transition-transform group-hover:text-primary {open
							? ''
							: '-rotate-90'}"
						aria-hidden="true"
					/>
				</button>
			</h3>
			{#if open}
				<div id="module-body-{item.id}" class="border-t border-border">
					{@render children(item)}
				</div>
			{/if}
		</section>
	{/each}
</div>
<Pagination currentPage={current} {totalPages} onPageChange={goToPage} />
