<script lang="ts">
	import './diagram.css';
</script>

<figure class="dg">
	<svg
		viewBox="0 0 720 300"
		role="img"
		aria-label="A CPU with host RAM on the left, a GPU with device memory on the right, joined by a PCIe link"
	>
		<defs>
			<marker
				id="ah"
				viewBox="0 0 10 10"
				refX="9"
				refY="5"
				markerWidth="7"
				markerHeight="7"
				orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ar" /></marker
			>
		</defs>
		<text class="t h" x="20" y="24">Host</text>
		<rect class="box" x="20" y="34" width="260" height="240" rx="14" />
		<rect class="a" x="40" y="54" width="220" height="80" rx="10" />
		<text class="t h" x="150" y="86" text-anchor="middle">CPU</text>
		<text class="t s" x="150" y="108" text-anchor="middle">few strong cores, big caches</text>
		<rect class="b" x="40" y="168" width="220" height="82" rx="10" />
		<text class="t h" x="150" y="202" text-anchor="middle">Host RAM</text>
		<text class="t s" x="150" y="224" text-anchor="middle">tens of GB/s</text>
		<path class="ln" d="M150 134V168" marker-end="url(#ah)" marker-start="url(#ah)" />

		<text class="t h" x="440" y="24">Device</text>
		<rect class="box" x="440" y="34" width="260" height="240" rx="14" />
		<rect class="a" x="460" y="54" width="220" height="80" rx="10" />
		<text class="t h" x="570" y="86" text-anchor="middle">GPU</text>
		<text class="t s" x="570" y="108" text-anchor="middle">thousands of simple lanes</text>
		<rect class="c" x="460" y="168" width="220" height="82" rx="10" />
		<text class="t h" x="570" y="202" text-anchor="middle">Device memory</text>
		<text class="t s" x="570" y="224" text-anchor="middle">hundreds of GB/s to TB/s</text>
		<path class="ln" d="M570 134V168" marker-end="url(#ah)" marker-start="url(#ah)" />

		<path class="ln" d="M280 150H440" marker-end="url(#ah)" marker-start="url(#ah)" />
		<text class="t" x="360" y="138" text-anchor="middle">PCIe</text>
		<text class="t s" x="360" y="172" text-anchor="middle">~12 to 25 GB/s</text>
		<text class="t s" x="360" y="190" text-anchor="middle">the slowest road</text>
	</svg>
	<figcaption>
		Two separate worlds. Data crosses the PCIe link in cudaMemcpy, and it is the narrowest part of
		the system.
	</figcaption>
</figure>
