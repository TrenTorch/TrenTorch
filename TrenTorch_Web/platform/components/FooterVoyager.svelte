<!-- A constellation, not an illustration: the astronaut and the small graph
     she reaches for are both drawn the same way, as points and the lines
     between them. That's the whole idea in one image: training a network is
     mapping the dark one connection at a time, the same motion as tracing a
     figure out of scattered stars. Hand-authored, native SVG only, no raster
     assets, per the artifact-diagramming mechanics. -->
<figure class="m-0">
	<svg
		viewBox="0 0 1200 260"
		class="h-auto w-full text-foreground"
		role="img"
		aria-label="A line drawing of an astronaut, rendered as a constellation, reaching toward a small network of connected stars"
	>
		<defs>
			<radialGradient id="voyager-glow" cx="50%" cy="50%" r="50%">
				<stop offset="0%" stop-color="var(--primary)" stop-opacity="0.9" />
				<stop offset="100%" stop-color="var(--primary)" stop-opacity="0" />
			</radialGradient>
		</defs>

		<!-- Faint orbit, cropped by the frame: depth, not a literal planet. -->
		<ellipse
			cx="1120"
			cy="18"
			rx="230"
			ry="95"
			transform="rotate(-8 1120 18)"
			fill="none"
			stroke="currentColor"
			stroke-width="1"
			opacity="0.12"
		/>

		<!-- Starfield -->
		<g fill="currentColor">
			<circle cx="42" cy="34" r="1.4" opacity="0.55" />
			<circle cx="96" cy="78" r="1" opacity="0.35" />
			<circle cx="150" cy="30" r="1.6" opacity="0.6" />
			<circle cx="70" cy="140" r="1.2" opacity="0.4" />
			<circle cx="190" cy="100" r="1" opacity="0.3" />
			<circle cx="24" cy="200" r="1.4" opacity="0.5" />
			<circle cx="130" cy="210" r="1" opacity="0.35" />
			<circle cx="210" cy="55" r="1.2" opacity="0.4" />
			<circle cx="290" cy="40" r="1.6" opacity="0.6" />
			<circle cx="420" cy="28" r="1" opacity="0.35" />
			<circle cx="460" cy="90" r="1.4" opacity="0.5" />
			<circle cx="380" cy="130" r="1" opacity="0.3" />
			<circle cx="500" cy="200" r="1.2" opacity="0.4" />
			<circle cx="560" cy="60" r="1.6" opacity="0.55" />
			<circle cx="610" cy="20" r="1" opacity="0.3" />
			<circle cx="650" cy="110" r="1.2" opacity="0.4" />
			<circle cx="600" cy="180" r="1" opacity="0.35" />
			<circle cx="700" cy="150" r="1.4" opacity="0.5" />
			<circle cx="740" cy="24" r="1" opacity="0.3" />
			<circle cx="770" cy="210" r="1.2" opacity="0.4" />
			<circle cx="840" cy="230" r="1" opacity="0.35" />
			<circle cx="960" cy="40" r="1.6" opacity="0.6" />
			<circle cx="1000" cy="110" r="1" opacity="0.3" />
			<circle cx="1040" cy="190" r="1.4" opacity="0.5" />
			<circle cx="1080" cy="70" r="1.2" opacity="0.4" />
			<circle cx="1120" cy="150" r="1" opacity="0.35" />
			<circle cx="1160" cy="220" r="1.4" opacity="0.5" />
			<circle cx="1170" cy="100" r="1" opacity="0.3" />
			<circle cx="920" cy="190" r="1.2" opacity="0.4" />
			<circle cx="880" cy="140" r="1" opacity="0.3" />
			<circle cx="520" cy="35" r="1" opacity="0.3" />
			<circle cx="340" cy="90" r="1" opacity="0.3" />
			<circle cx="250" cy="150" r="1" opacity="0.3" />
			<circle cx="110" cy="230" r="1" opacity="0.3" />
		</g>

		<!-- The small graph she's reaching toward: a handful of nodes and
		     edges, same visual grammar as the astronaut, so the two read as
		     one continuous idea rather than two separate drawings. -->
		<g stroke="currentColor" stroke-width="1" opacity="0.5" fill="none">
			<line x1="330" y1="205" x2="280" y2="175" />
			<line x1="330" y1="205" x2="265" y2="225" />
			<line x1="330" y1="205" x2="355" y2="165" />
			<line x1="330" y1="205" x2="380" y2="215" />
			<line x1="280" y1="175" x2="235" y2="195" />
			<line x1="265" y1="225" x2="310" y2="240" />
			<line x1="355" y1="165" x2="380" y2="215" />
		</g>
		<g fill="currentColor">
			<circle cx="280" cy="175" r="2.4" />
			<circle cx="265" cy="225" r="2.4" />
			<circle cx="355" cy="165" r="2.4" />
			<circle cx="380" cy="215" r="2.4" />
			<circle cx="235" cy="195" r="2" />
			<circle cx="310" cy="240" r="2" />
		</g>
		<circle cx="330" cy="205" r="3.4" fill="var(--primary)" />

		<!-- The tether: the one line connecting the figure to the graph. -->
		<path
			d="M818,152 Q560,258 330,205"
			fill="none"
			stroke="var(--primary)"
			stroke-width="1.25"
			stroke-dasharray="1 7"
			stroke-linecap="round"
			opacity="0.7"
		/>

		<!-- The figure, drawn the same way as everything around her: points
		     joined by lines. One arm reaches past the frame of her own body
		     toward the graph, the only gesture the drawing needs. -->
		<g stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.85">
			<path d="M820,38 L798,55 L820,74 L842,55 Z" />
			<path d="M820,74 L793,96 M820,74 L847,96" />
			<path d="M793,96 L820,118 L847,96" />
			<path d="M820,118 L818,152" />
			<path d="M847,96 L882,78 L918,44" />
			<path d="M793,96 L778,128 L748,156" />
			<path d="M818,152 L842,196 L858,236" />
			<path d="M818,152 L796,198 L778,238" />
		</g>
		<g fill="currentColor">
			<circle cx="820" cy="38" r="2.6" />
			<circle cx="798" cy="55" r="2.6" />
			<circle cx="842" cy="55" r="2.6" />
			<circle cx="820" cy="74" r="2.6" />
			<circle cx="793" cy="96" r="2.6" />
			<circle cx="847" cy="96" r="2.6" />
			<circle cx="820" cy="118" r="2.6" />
			<circle cx="818" cy="152" r="2.8" />
			<circle cx="882" cy="78" r="2.2" />
			<circle cx="778" cy="128" r="2.2" />
			<circle cx="748" cy="156" r="2.2" />
			<circle cx="842" cy="196" r="2.2" />
			<circle cx="796" cy="198" r="2.2" />
			<circle cx="858" cy="236" r="2" />
			<circle cx="778" cy="238" r="2" />
		</g>

		<!-- The star she's reaching for: the one warm point in the drawing. -->
		<circle cx="918" cy="44" r="14" fill="url(#voyager-glow)" opacity="0.5" />
		<circle cx="918" cy="44" r="3.2" fill="var(--primary)" />
	</svg>
	<figcaption
		class="font-signature mt-2 text-center text-xl text-muted-foreground italic md:text-2xl"
	>
		Every gradient is a step into the dark, mapped one connection at a time.
	</figcaption>
</figure>
