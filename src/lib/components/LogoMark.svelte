<script lang="ts">
	// The same pulsing-bolt mark used in the TrenTorch repo README
	// (.github/assets/trentorch-bolt.svg), simplified for a small navbar icon.
	let { class: className = '' }: { class?: string } = $props();
</script>

<svg viewBox="0 0 200 200" class={className} aria-hidden="true">
	<defs>
		<linearGradient id="boltFill" x1="0%" y1="0%" x2="100%" y2="100%">
			<stop offset="0%" stop-color="#ffcf70" />
			<stop offset="55%" stop-color="#ff9d2e" />
			<stop offset="100%" stop-color="#d4740c" />
		</linearGradient>
	</defs>
	<g transform="translate(100 100)">
		<polygon
			points="14,-70 -46,10 -6,10 -14,70 46,-10 6,-10"
			fill="url(#boltFill)"
			stroke="currentColor"
			stroke-opacity="0.35"
			stroke-width="2.5"
			stroke-linejoin="round"
		/>
	</g>
</svg>
