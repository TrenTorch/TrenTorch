<script lang="ts">
	import './diagram.css';
</script>

<figure class="dg">
	<svg
		viewBox="0 0 720 420"
		role="img"
		aria-label="Nested view of a GPU: GPCs contain SMs, each SM has four sub-partitions with a warp scheduler, register file and cores, plus shared memory; the L2 cache and memory controllers sit outside the GPCs"
	>
		<rect class="box" x="10" y="10" width="700" height="400" rx="16" />
		<text class="t h" x="26" y="34">GPU</text>
		<rect class="box hi" x="26" y="46" width="668" height="30" rx="8" />
		<text class="t" x="360" y="66" text-anchor="middle"
			>GigaThread Engine: global scheduler that hands thread blocks to SMs</text
		>
		<rect class="a" x="26" y="90" width="430" height="256" rx="12" />
		<text class="t h" x="40" y="112">GPC (graphics processing cluster)</text>
		<rect class="box" x="40" y="124" width="402" height="210" rx="10" />
		<text class="t h" x="52" y="146">SM (streaming multiprocessor): where your code runs</text>
		{#each [0, 1, 2, 3] as p (p)}
			<rect class="b" x={52 + p * 98} y="158" width="90" height="118" rx="8" />
			<text class="t s" x={97 + p * 98} y="176" text-anchor="middle">sub-partition {p}</text>
			<text class="t s" x={97 + p * 98} y="196" text-anchor="middle">warp scheduler</text>
			<text class="t s" x={97 + p * 98} y="214" text-anchor="middle">register file</text>
			<text class="t s" x={97 + p * 98} y="232" text-anchor="middle">FP32 cores</text>
			<text class="t s" x={97 + p * 98} y="250" text-anchor="middle">tensor cores</text>
			<text class="t s" x={97 + p * 98} y="268" text-anchor="middle">load/store, SFU</text>
		{/each}
		<rect class="c" x="52" y="288" width="378" height="36" rx="8" />
		<text class="t" x="241" y="311" text-anchor="middle">shared memory / L1 cache (one per SM)</text
		>
		<text class="t s" x="40" y="338" opacity="0">.</text>
		<text class="t s" x="40" y="362"
			>A GPC holds several SMs (two SMs per TPC in recent chips).</text
		>
		<text class="t s" x="40" y="380">A full chip has many GPCs side by side.</text>
		<rect class="box" x="476" y="90" width="218" height="124" rx="12" />
		<text class="t h" x="490" y="114">L2 cache</text>
		<text class="t s" x="490" y="134">shared by every SM</text>
		<text class="t s" x="490" y="152">tens of MB on recent chips</text>
		<rect class="box" x="476" y="226" width="218" height="120" rx="12" />
		<text class="t h" x="490" y="250">Memory controllers</text>
		<text class="t s" x="490" y="270">HBM or GDDR channels</text>
		<text class="t s" x="490" y="288">device memory, off-chip</text>
		<rect class="box" x="476" y="358" width="218" height="38" rx="10" />
		<text class="t" x="585" y="382" text-anchor="middle">PCIe interface</text>
	</svg>
	<figcaption>
		The same pattern repeats at every level: a scheduler hands work to units that each have their
		own registers and fast memory.
	</figcaption>
</figure>
