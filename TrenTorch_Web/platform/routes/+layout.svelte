<script lang="ts">
	import './layout.css';
	import 'katex/dist/katex.min.css';
	import { page } from '$app/state';
	import { onNavigate } from '$app/navigation';
	import { tick } from 'svelte';
	import { clearMorph, pendingMorph } from '$processes/navigation/morph';
	import favicon from '$assets/trentorch-logo.webp';
	import Navbar from '$components/Navbar.svelte';
	import Footer from '$components/Footer.svelte';
	import SignInDialog from '$components/SignInDialog.svelte';
	import ProgressSync from '$components/ProgressSync.svelte';
	import RatingSettle from '$components/RatingSettle.svelte';
	import AfterSignInRedirect from '$components/AfterSignInRedirect.svelte';

	let { children } = $props();

	// A page that was minimised (see morph.ts) has its header (the `data-minimise` element, from the window dots
	// down to just above the list) scaled onto its place: the old page's snapshot is clipped to that box, then
	// shrunk quickly onto the target and faded only at the very end, with the home page already underneath.
	const MORPH_MS = 420;
	onNavigate((navigation) => {
		const morph = pendingMorph();
		const source = document.querySelector('[data-minimise]')?.getBoundingClientRect();
		if (
			!morph ||
			!source ||
			!document.startViewTransition ||
			matchMedia('(prefers-reduced-motion: reduce)').matches
		) {
			return;
		}
		return new Promise((done) => {
			let target: DOMRect | undefined;
			const transition = document.startViewTransition(async () => {
				done();
				await navigation.complete;
				await tick();
				target = [...document.querySelectorAll(`[data-morph="${morph.target}"]`)]
					.map((el) => el.getBoundingClientRect())
					.find((box) => box.width > 0 && box.height > 0);
			});
			void transition.ready.then(() => {
				const { clientWidth: w, clientHeight: h } = document.documentElement;
				// The header is fitted to the target's own box, so it lands in a window, card or capsule as that
				// shape; onto a navbar tab it keeps its proportions instead. A target that is not on screen (the
				// tabs on a phone) is the middle of the screen.
				const to = target ?? new DOMRect(w * 0.4, h * 0.4, w * 0.2, h * 0.2);
				const tab = !target || morph.target.startsWith('tab:');
				const sx = tab
					? Math.min(to.width / source.width, to.height / source.height)
					: to.width / source.width;
				const sy = tab ? sx : to.height / source.height;
				const x = to.left + to.width / 2 - (source.left + source.width / 2) * sx;
				const y = to.top + to.height / 2 - (source.top + source.height / 2) * sy;
				const clip = `inset(${source.top}px ${w - source.right}px ${h - source.bottom}px ${source.left}px round 16px)`;
				document.documentElement.animate(
					[
						{ transform: 'translate(0, 0) scale(1, 1)', clipPath: clip, opacity: 1, offset: 0 },
						{ clipPath: clip, opacity: 1, offset: 0.72 },
						{
							transform: `translate(${x}px, ${y}px) scale(${sx}, ${sy})`,
							clipPath: clip,
							opacity: 0,
							offset: 1
						}
					],
					{
						duration: MORPH_MS,
						easing: 'cubic-bezier(0.5, 0, 0.2, 1)',
						fill: 'forwards',
						pseudoElement: '::view-transition-old(root)'
					}
				);
			});
			void transition.finished.finally(clearMorph);
		});
	});

	// Footer only appears on the homepage. It was previously shown on every
	// route except /ide, but a long, scrollable list page (Questions,
	// Account) doesn't want a footer competing with pagination for "the
	// bottom of the content" -- the homepage is the one place it's meant to
	// be a page-ending element.
	let showFooter = $derived(page.url.pathname === '/');

	// The IDE has its own single top bar (logo, back, Run, Submit, account), so the
	// site navbar steps aside there and the workspace gets its height back. The long theory
	// pages hide it too, so the side menu and the text get the full height.
	let showNavbar = $derived(
		!page.url.pathname.startsWith('/ide') && !page.url.pathname.startsWith('/dsa/theory')
	);
</script>

<svelte:head>
	<link rel="icon" type="image/webp" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&display=swap"
	/>
</svelte:head>

<!-- No max-width here: the navbar and footer bars go full-bleed edge to
     edge on any screen size, and each page's own sections cap their
     content at a readable width via the shared .container class instead. -->
<div class="relative flex min-h-screen flex-col">
	{#if showNavbar}
		<Navbar />
	{/if}
	<div class="w-full flex-1">
		{@render children()}
	</div>
	{#if showFooter}
		<Footer />
	{/if}
</div>
<SignInDialog />
<ProgressSync />
<RatingSettle />
<AfterSignInRedirect />
