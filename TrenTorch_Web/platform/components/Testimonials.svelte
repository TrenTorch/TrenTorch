<script>
	// Add new testimonials here — the masonry grid below just maps over this array.
	// `img` is the light-mode PNG of the post and `imgDark` the dark-mode PNG of
	// the same post (converted so the quality doesn't drop and the original shape
	// stays intact); the grid swaps between them automatically under .dark.
	/** @type {{ img: string; imgDark: string; url: string }[]} */
	const testimonials = [
		{
			img: '/testimonial-screenshots/athrix.png',
			imgDark: '/testimonial-screenshots/athrix-dark.png',
			url: 'https://x.com/athrix_codes/status/2099409710579642664?s=20'
		},
		{
			img: '/testimonial-screenshots/unmesh.png',
			imgDark: '/testimonial-screenshots/unmesh-dark.png',
			url: 'https://x.com/ascorbichelix/status/2099468952573460564?s=20'
		},
		{
			img: '/testimonial-screenshots/harsh.png',
			imgDark: '/testimonial-screenshots/harsh-dark.png',
			url: 'https://x.com/harshbhatt7585/status/2099897450945446316?s=20'
		},
		{
			img: '/testimonial-screenshots/yug.png',
			imgDark: '/testimonial-screenshots/yug-dark.png',
			url: 'https://x.com/syuggupta/status/2099199455081926796?s=20'
		},
		{
			img: '/testimonial-screenshots/avrl.png',
			imgDark: '/testimonial-screenshots/avrl-dark.png',
			url: 'https://x.com/avrldotdev/status/2099199587550711993?s=20'
		},
		{
			img: '/testimonial-screenshots/divyansh.png',
			imgDark: '/testimonial-screenshots/divyansh-dark.png',
			url: 'https://x.com/Divyansh91565/status/2099221515028042231?s=20'
		},
		{
			img: '/testimonial-screenshots/tanu.png',
			imgDark: '/testimonial-screenshots/tanu-dark.png',
			url: 'https://x.com/serotoninwave/status/2099366590798262537?s=20'
		},
		{
			img: '/testimonial-screenshots/harshit.png',
			imgDark: '/testimonial-screenshots/harshit-dark.png',
			url: 'https://x.com/Harry_The_Nerd/status/2099426912422736170?s=20'
		},
		{
			img: '/testimonial-screenshots/aditya.png',
			imgDark: '/testimonial-screenshots/aditya-dark.png',
			url: 'https://x.com/AdityaPat_/status/2099571984078368861?s=20'
		},
		{
			img: '/testimonial-screenshots/simran.png',
			imgDark: '/testimonial-screenshots/simran-dark.png',
			url: 'https://x.com/simm_designs/status/2099362178814140800?s=20'
		},
		{
			img: '/testimonial-screenshots/vaibhav.png',
			imgDark: '/testimonial-screenshots/vaibhav-dark.png',
			url: 'https://x.com/Vaibhav_14ry/status/2099358103343165813?s=20'
		},
		{
			img: '/testimonial-screenshots/shreya.png',
			imgDark: '/testimonial-screenshots/shreya-dark.png',
			url: 'https://x.com/tech_Shreya_200/status/2099201391038545981?s=20'
		},
		{
			img: '/testimonial-screenshots/anushka.png',
			imgDark: '/testimonial-screenshots/anushka-dark.png',
			url: 'https://x.com/AnushkaDesign/status/2100885885604831604?s=20'
		},
		{
			img: '/testimonial-screenshots/mitali.png',
			imgDark: '/testimonial-screenshots/mitali-dark.png',
			url: 'https://x.com/kayleecodez/status/2099207156272927108?s=20'
		},
		{
			img: '/testimonial-screenshots/harsh-jain.png',
			imgDark: '/testimonial-screenshots/harsh-jain-dark.png',
			url: 'https://lnkd.in/p/dUNc5pqD'
		}
	];
</script>

<section class="testimonials">
	<h2 class="testimonials-heading">What people are saying</h2>

	<div class="masonry">
		{#each testimonials as t, i (i)}
			<!-- External links to the original posts, not app routes, so resolve() does not apply. -->
			<!-- eslint-disable svelte/no-navigation-without-resolve -->
			<a
				class="shot-link"
				href={t.url}
				target="_blank"
				rel="noopener noreferrer"
				aria-label="View the original post"
			>
				<img
					class="shot {t.imgDark ? 'shot-light' : ''}"
					src={t.img}
					alt="Testimonial screenshot"
					loading="lazy"
				/>
				{#if t.imgDark}
					<img class="shot shot-dark" src={t.imgDark} alt="" loading="lazy" aria-hidden="true" />
				{/if}
			</a>
			<!-- eslint-enable svelte/no-navigation-without-resolve -->
		{/each}
	</div>
</section>

<style>
	.testimonials {
		padding: 3rem 1.5rem;
	}

	.testimonials-heading {
		text-align: center;
		margin-bottom: 2rem;
		font-size: 1.75rem;
		font-weight: 600;
	}

	.masonry {
		max-width: 1400px;
		margin: 0 auto;
		column-count: 4;
		column-gap: 1.25rem;
	}

	@media (max-width: 1100px) {
		.masonry {
			column-count: 3;
		}
	}

	@media (max-width: 800px) {
		.masonry {
			column-count: 2;
		}
	}

	@media (max-width: 500px) {
		.masonry {
			column-count: 1;
		}
	}

	.shot-link {
		display: block;
		break-inside: avoid;
		margin-bottom: 1.25rem;
		border-radius: 1rem;
		overflow: hidden;
		/* Same lighter greyish border the /questions track cards use. */
		border: 1px solid var(--border);
		transition:
			border-color 0.2s ease,
			transform 0.2s ease;
	}

	.shot-link:hover {
		border-color: color-mix(in oklab, var(--foreground) 30%, transparent);
		transform: translateY(-2px);
	}

	.shot {
		display: block;
		width: 100%;
		height: auto;
		background: rgba(255, 255, 255, 0.05);
	}

	/* Dark-mode variant swap: the dark PNG takes over under .dark. The base
	   rules come AFTER .shot on equal specificity so they win in light mode;
	   the .dark selectors outrank both. Without this order both images showed
	   stacked in light mode. */
	.shot-dark {
		display: none;
	}
	:global(.dark) .shot-light {
		display: none;
	}
	:global(.dark) .shot-dark {
		display: block;
	}
</style>
