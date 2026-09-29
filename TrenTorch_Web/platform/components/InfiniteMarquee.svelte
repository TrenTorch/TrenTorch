<script lang="ts">
	import type { Snippet } from 'svelte';

	/**
	 * InfiniteMarquee — Svelte port of Wensity's `infinite-marquee`
	 * (https://ui.wensity.com/components/infinite-marquee), API kept 1:1 so the
	 * upstream docs still apply. The children snippet is rendered exactly twice
	 * and the track animates translate3d(0,0,0) → translate3d(-50%,0,0) through
	 * a CSS keyframe, so all the work stays on the compositor (zero JS, no
	 * stutter at the loop point). Supports text and icon/mask items alike.
	 */
	let {
		speed = 30,
		direction = 'left',
		pauseOnHover = false,
		gap = 'gap-20',
		fade = true,
		class: className = '',
		children
	}: {
		/** Cycle duration in seconds (lower = faster). */
		speed?: number;
		/** Animation direction. */
		direction?: 'left' | 'right';
		/** Pause the loop when the cursor enters. Off by default — most marketing
		 * marquees should keep moving so they never feel "stuck" mid-page. */
		pauseOnHover?: boolean;
		/** Tailwind gap class between items, e.g. "gap-10". */
		gap?: string;
		/** Apply the soft mask-image fade at both edges. */
		fade?: boolean;
		class?: string;
		children: Snippet;
	} = $props();
</script>

<div class="marquee {fade ? 'fade' : ''} {className}">
	<div
		class="track {direction === 'right' ? 'reverse' : ''} {pauseOnHover ? 'pause' : ''} {gap}"
		style="animation-duration: {speed}s"
	>
		<!-- Original strip -->
		<div class="strip {gap}">{@render children()}</div>
		<!-- Duplicate — exactly once — for the seamless wrap at -50%. -->
		<div class="strip {gap}" aria-hidden="true">{@render children()}</div>
	</div>
</div>

<style>
	.marquee {
		position: relative;
		width: 100%;
		overflow: hidden;
	}
	.marquee.fade {
		-webkit-mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
		mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
	}
	.track {
		display: flex;
		width: max-content;
		align-items: center;
		will-change: transform;
		animation-name: marquee-x;
		animation-timing-function: linear;
		animation-iteration-count: infinite;
	}
	.track.reverse {
		animation-name: marquee-x-reverse;
	}
	/* Wensity default: pauseOnHover is opt-in via this class. */
	.track.pause:hover {
		animation-play-state: paused;
	}
	.strip {
		display: flex;
		flex: none;
		align-items: center;
	}
	@keyframes marquee-x {
		from {
			transform: translate3d(0, 0, 0);
		}
		to {
			transform: translate3d(-50%, 0, 0);
		}
	}
	@keyframes marquee-x-reverse {
		from {
			transform: translate3d(-50%, 0, 0);
		}
		to {
			transform: translate3d(0, 0, 0);
		}
	}
	/* Honour the OS reduced-motion preference — freeze the loop. */
	@media (prefers-reduced-motion: reduce) {
		.track {
			animation: none;
		}
	}
</style>
