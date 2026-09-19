<script>
	// Add new testimonials here — the masonry grid below just maps over this array.
	// `img` is the full tweet/post screenshot.
	const testimonials = [
		{
			img: '/testimonial-screenshots/athrix.webp',
			url: 'https://x.com/athrix_codes/status/2099409710579642664?s=20'
		},
		{
			img: '/testimonial-screenshots/unmesh.webp',
			url: 'https://x.com/ascorbichelix/status/2099468952573460564?s=20'
		},
		{
			img: '/testimonial-screenshots/harsh.webp',
			url: 'https://x.com/harshbhatt7585/status/2099897450945446316?s=20'
		},
		{
			img: '/testimonial-screenshots/yug.webp',
			url: 'https://x.com/syuggupta/status/2099199455081926796?s=20'
		},
		{
			img: '/testimonial-screenshots/avrl.webp',
			url: 'https://x.com/avrldotdev/status/2099199587550711993?s=20'
		},
		{
			img: '/testimonial-screenshots/divyansh.webp',
			url: 'https://x.com/Divyansh91565/status/2099221515028042231?s=20'
		},
		{
			img: '/testimonial-screenshots/tannu.webp',
			url: 'https://x.com/serotoninwave/status/2099366590798262537?s=20'
		},
		{
			img: '/testimonial-screenshots/harshit.webp',
			url: 'https://x.com/Harry_The_Nerd/status/2099426912422736170?s=20'
		},
		{
			img: '/testimonial-screenshots/patnayak.webp',
			url: 'https://x.com/AdityaPat_/status/2099571984078368861?s=20'
		},
		{
			img: '/testimonial-screenshots/simran.webp',
			url: 'https://x.com/simm_designs/status/2099362178814140800?s=20'
		},
		{
			img: '/testimonial-screenshots/vaibhav.webp',
			url: 'https://x.com/Vaibhav_14ry/status/2099358103343165813?s=20'
		},
		{
			img: '/testimonial-screenshots/shreya.webp',
			url: 'https://x.com/tech_Shreya_200/status/2099201391038545981?s=20'
		},
		{ img: '/testimonial-screenshots/harsh-jain.webp', url: 'https://lnkd.in/p/dUNc5pqD' },
		{
			img: '/testimonial-screenshots/anushka.webp',
			url: 'https://x.com/AnushkaDesign/status/2100885885604831604?s=20'
		},
		{
			img: '/testimonial-screenshots/mitali.webp',
			url: 'https://x.com/kayleecodez/status/2099207156272927108?s=20'
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
				<img class="shot" src={t.img} alt="Testimonial screenshot" loading="lazy" />
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
		border-radius: 0.75rem;
		overflow: hidden;
		border: 1px solid rgba(255, 255, 255, 0.1);
		transition:
			border-color 0.2s ease,
			transform 0.2s ease;
	}

	.shot-link:hover {
		border-color: rgba(255, 255, 255, 0.25);
		transform: translateY(-2px);
	}

	.shot {
		display: block;
		width: 100%;
		height: auto;
		background: rgba(255, 255, 255, 0.05);
	}
</style>
