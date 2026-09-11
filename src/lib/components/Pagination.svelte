<script lang="ts">
	import { ChevronLeft, ChevronRight } from '@lucide/svelte';

	let {
		currentPage,
		totalPages,
		onPageChange
	}: {
		currentPage: number;
		totalPages: number;
		onPageChange: (page: number) => void;
	} = $props();

	const pageNumbers = $derived(Array.from({ length: totalPages }, (_, i) => i + 1));
</script>

{#if totalPages > 1}
	<nav
		class="flex items-center justify-center gap-1 font-mono text-xs"
		aria-label="Questions page navigation"
	>
		<button
			type="button"
			disabled={currentPage <= 1}
			onclick={() => onPageChange(currentPage - 1)}
			class="flex items-center rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground disabled:pointer-events-none disabled:opacity-30"
			aria-label="Previous page"
		>
			<ChevronLeft class="size-4" />
		</button>

		{#each pageNumbers as pageNum (pageNum)}
			<button
				type="button"
				onclick={() => onPageChange(pageNum)}
				aria-current={pageNum === currentPage ? 'page' : undefined}
				class="min-w-7 rounded px-2 py-1.5 tabular-nums transition-colors {pageNum === currentPage
					? 'bg-primary text-primary-foreground'
					: 'text-muted-foreground hover:bg-secondary hover:text-foreground'}"
			>
				{pageNum}
			</button>
		{/each}

		<button
			type="button"
			disabled={currentPage >= totalPages}
			onclick={() => onPageChange(currentPage + 1)}
			class="flex items-center rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground disabled:pointer-events-none disabled:opacity-30"
			aria-label="Next page"
		>
			<ChevronRight class="size-4" />
		</button>
	</nav>
{/if}
