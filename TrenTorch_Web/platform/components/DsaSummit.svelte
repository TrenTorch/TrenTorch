<!-- The closing image of the DSA sheet: a stick figure leaping up a staircase toward a flag
     marked GM, drawn like the constellation in the footer (points and the lines between
     them) so the two read as one family. Native SVG, no raster assets; every colour is
     currentColor so it follows the light and dark themes. -->
<figure class="summit m-0">
	<svg
		viewBox="0 0 1400 432"
		class="h-auto w-full text-foreground"
		role="img"
		aria-label="A stick figure leaping up a staircase toward a flag marked GM"
	>
		<!-- A few stars -->
		<g fill="currentColor">
			<circle cx="180" cy="67" r="1.6" opacity="0.5" />
			<circle cx="388" cy="35" r="1.3" opacity="0.4" />
			<circle cx="581" cy="19" r="1.5" opacity="0.5" />
			<circle cx="501" cy="132" r="1.2" opacity="0.35" />
			<circle cx="885" cy="27" r="1.3" opacity="0.4" />
			<circle cx="982" cy="83" r="1.2" opacity="0.4" />
			<circle cx="276" cy="212" r="1.2" opacity="0.35" />
			<circle cx="1079" cy="3" r="1.3" opacity="0.4" />
			<circle cx="34" cy="164" r="1.2" opacity="0.35" />
			<circle cx="1384" cy="373" r="1.3" opacity="0.4" />
		</g>

		<!-- The staircase, one tread and one riser at a time -->
		<polyline
			points="82,405 82,360 259,360 259,315 436,315 436,270 613,270 613,225 790,225 790,180 967,180 967,135 1143,135 1143,90 1272,90"
			fill="none"
			stroke="currentColor"
			stroke-width="1.6"
			stroke-linejoin="round"
			opacity="0.7"
		/>
		<g fill="currentColor" opacity="0.8">
			<circle cx="82" cy="405" r="4" />
			<circle cx="82" cy="360" r="4" />
			<circle cx="259" cy="360" r="4" />
			<circle cx="259" cy="315" r="4" />
			<circle cx="436" cy="315" r="4" />
			<circle cx="436" cy="270" r="4" />
			<circle cx="613" cy="270" r="4" />
			<circle cx="613" cy="225" r="4" />
			<circle cx="790" cy="225" r="4" />
			<circle cx="790" cy="180" r="4" />
			<circle cx="967" cy="180" r="4" />
			<circle cx="967" cy="135" r="4" />
			<circle cx="1143" cy="135" r="4" />
			<circle cx="1143" cy="90" r="4" />
			<circle cx="1272" cy="90" r="4" />
		</g>
		<line x1="1272" y1="90" x2="1320" y2="90" stroke="currentColor" stroke-width="1.6" opacity="0.55" />
		<circle cx="1320" cy="90" r="4" fill="currentColor" opacity="0.8" />

		<!-- The figure, mid-leap: head, then arms, spine and legs as joints joined by lines -->
		<g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
			<circle cx="714" cy="80" r="15" />
			<polyline points="711,115 751,99 790,67" />
			<polyline points="711,115 684,131 664,151" />
			<polyline points="711,115 703,173" />
			<polyline points="703,173 745,163 790,180" />
			<polyline points="703,173 684,199 661,225" />
		</g>
		<g fill="currentColor">
			<circle cx="714" cy="80" r="3" />
			<circle cx="711" cy="115" r="3.2" />
			<circle cx="751" cy="99" r="3.2" />
			<circle cx="790" cy="67" r="3.6" />
			<circle cx="684" cy="131" r="3.2" />
			<circle cx="664" cy="151" r="3.6" />
			<circle cx="703" cy="173" r="3.4" />
			<circle cx="745" cy="163" r="3.2" />
			<circle cx="790" cy="180" r="3.6" />
			<circle cx="684" cy="199" r="3.2" />
			<circle cx="661" cy="225" r="3.6" />
		</g>

		<!-- The reach: a dotted arc from the hand to the flag -->
		<path
			d="M 796 66 C 930 24, 1120 22, 1252 41"
			fill="none"
			stroke="#d64545"
			stroke-width="2"
			stroke-dasharray="4 5"
			stroke-linecap="round"
		/>

		<!-- The flag -->
		<line x1="1272" y1="16" x2="1272" y2="90" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
		<polygon points="1272,16 1312,36 1272,56" fill="currentColor" />
		<circle cx="1272" cy="16" r="3.6" fill="currentColor" />
		<text
			x="1330"
			y="47"
			fill="currentColor"
			font-size="26"
			font-weight="700"
			letter-spacing="1"
			font-family="var(--font-sans)">GM</text
		>
	</svg>
	<blockquote class="summit-quote">
		Grandmasters aren’t made by courses, they’re made by consistency. Every hard problem, every
		contest, every wrong answer is a step toward the summit.
	</blockquote>
</figure>

<style>
	.summit-quote {
		margin: 1.25rem auto 0;
		max-width: 44rem;
		padding: 0 1rem;
		text-align: center;
		font-family: 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif;
		font-style: italic;
		font-size: clamp(1.05rem, 2.2vw, 1.35rem);
		line-height: 1.6;
		color: var(--muted-foreground);
		text-wrap: balance;
	}
</style>
