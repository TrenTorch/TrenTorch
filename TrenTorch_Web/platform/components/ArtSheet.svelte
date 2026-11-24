<script lang="ts">
	import type { Snippet } from 'svelte';

	// The frame every module drawing shares: a sheet with a code line on top,
	// cut open along a wavy edge, with the module's picture underneath.
	// Drawn from theme tokens, so it follows light and dark. Decorative only.
	let { code, children }: { code: string; children: Snippet } = $props();

	const WAVE =
		'M5 31 L20 28 L36 32 L52 28 L68 32 L84 28 L100 32 L116 28 L132 32 L151 29 V87 a9 9 0 0 1 -9 9 H13 a9 9 0 0 1 -9 -9 Z';
</script>

<svg viewBox="0 0 160 104" class="art" aria-hidden="true" focusable="false">
	<rect x="6" y="8" width="148" height="90" rx="9" class="sheet-back" />
	<rect x="4" y="6" width="148" height="90" rx="9" class="sheet" />
	<text x="13" y="21" class="code">{code}</text>
	<path d={WAVE} class="inside" />
	{@render children()}
</svg>

<style>
	.art {
		--ink: var(--foreground);
		--paper: var(--popover);
		--shade: color-mix(in oklab, var(--foreground) 7%, var(--popover));
		display: block;
		width: 100%;
		height: auto;
		font-family: var(--font-mono);
	}
	.sheet-back {
		fill: color-mix(in oklab, var(--foreground) 14%, var(--paper));
		stroke: var(--ink);
		stroke-width: 1;
	}
	.sheet {
		fill: var(--paper);
		stroke: var(--ink);
		stroke-width: 1;
	}
	.code {
		font-size: 9px;
		font-weight: 500;
		fill: var(--ink);
	}
	.inside {
		fill: var(--shade);
		stroke: var(--ink);
		stroke-width: 1;
		stroke-linejoin: round;
	}
	.art :global(.chip),
	.art :global(.cell),
	.art :global(.bar),
	.art :global(.dot) {
		fill: var(--paper);
		stroke: var(--ink);
		stroke-width: 1;
	}
	.art :global(.cell.head) {
		fill: color-mix(in oklab, var(--foreground) 16%, var(--paper));
	}
	.art :global(.cell.fill) {
		fill: color-mix(in oklab, var(--foreground) 14%, var(--paper));
	}
	.art :global(.dot.core) {
		fill: var(--ink);
	}
	.art :global(.on) {
		fill: color-mix(in oklab, var(--primary) 55%, var(--paper));
	}
	.art :global(.window) {
		fill: none;
		stroke: var(--primary);
		stroke-width: 2;
	}
	.art :global(.ring) {
		fill: none;
		stroke: var(--primary);
		stroke-width: 1.6;
	}
	.art :global(.line) {
		fill: none;
		stroke: var(--ink);
		stroke-width: 1.1;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.art :global(.line.faint) {
		stroke-opacity: 0.3;
		stroke-width: 0.8;
	}
	.art :global(.line.acc) {
		stroke: var(--primary);
		stroke-width: 2;
	}
	.art :global(.line.dash) {
		stroke-dasharray: 3 3;
	}

	/* Hovering the row draws the accent line in and wakes the highlighted bits. */
	:global(.group:hover) .art :global(.draw) {
		stroke-dasharray: 1;
		animation: draw 0.9s cubic-bezier(0.2, 0.8, 0.2, 1) both;
	}
	:global(.group:hover) .art :global(.on) {
		animation: glow 1.8s ease-in-out infinite;
	}
	@keyframes draw {
		from {
			stroke-dasharray: 1;
			stroke-dashoffset: 1;
		}
		to {
			stroke-dasharray: 1;
			stroke-dashoffset: 0;
		}
	}
	@keyframes glow {
		50% {
			opacity: 0.55;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		:global(.group:hover) .art :global(.draw),
		:global(.group:hover) .art :global(.on) {
			animation: none;
		}
	}
</style>
