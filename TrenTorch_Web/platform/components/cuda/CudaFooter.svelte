<!-- The banner is drawn for a dark page with no background of its own, so it sits directly on the page. In the
     light theme its greys are inverted (hue kept) so the figure and captions stay readable on the light page. -->
<footer class="mx-auto mt-14 w-full max-w-3xl px-4 pb-10 sm:px-5 md:px-6">
	<img
		src="/cuda/climb.svg"
		alt="A stick figure made of stars climbs a constellation mountain toward a glowing red star while small figures say you can't. Neural networks were out of fashion for decades; Geoffrey Hinton kept training them anyway. Believe in your intuition."
		class="climb w-full opacity-60"
		loading="lazy"
		width="960"
		height="440"
	/>
</footer>

<style>
	:global(html:not(.dark)) .climb {
		filter: invert(1) hue-rotate(180deg);
	}
</style>
