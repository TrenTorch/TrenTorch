<script>
  // Add new testimonials here — the marquee below just maps over this array.
  // `img` is the full tweet/post screenshot.
  const testimonials = [
    {
      img: '/testimonial-screenshots/athrix.png', // static/testimonial-screenshots/athrix.png
      url: 'https://x.com/athrix_codes/status/2099409710579642664?s=20'
    },
    {
      img: '/testimonial-screenshots/unmesh.png',
      url: 'https://x.com/ascorbichelix/status/2099468952573460564?s=20'
    },
    {
      img: '/testimonial-screenshots/harsh.png',
      url: 'https://x.com/harshbhatt7585/status/2099897450945446316?s=20'
    },
    {
      img: '/testimonial-screenshots/yug.png',
      url: 'https://x.com/syuggupta/status/2099199455081926796?s=20'
    },
    {
      img: '/testimonial-screenshots/avrl.png',
      url: 'https://x.com/avrldotdev/status/2099199587550711993?s=20'
    },
    {
      img: '/testimonial-screenshots/divyansh.png',
      url: 'https://x.com/Divyansh91565/status/2099221515028042231?s=20'
    },
    {
      img: '/testimonial-screenshots/shreya.png',
      url: 'https://x.com/tech_Shreya_200/status/2099201391038545981?s=20'
    },
    {
      img: '/testimonial-screenshots/harsh-jain.png',
      url: 'https://lnkd.in/p/dUNc5pqD'
    }
    // Add more the same way — save the screenshot into static/testimonial-screenshots/
    // and add an entry here with its filename and the post URL.
  ];

  // Duplicate the list so the CSS marquee loops seamlessly with no visible seam.
  const looped = [...testimonials, ...testimonials];

  // Keep a constant visual speed regardless of how many testimonials there are —
  // a fixed duration would make the marquee speed up every time you add an item.
  const SECONDS_PER_ITEM = 4;
  const duration = testimonials.length * SECONDS_PER_ITEM;
</script>

<section class="testimonials">
  <h2 class="testimonials-heading">What people are saying</h2>

  <div class="marquee">
    <div class="marquee-track" style={`--marquee-duration: ${duration}s`}>
      {#each looped as t, i (i)}
        <a
          class="shot-link"
          href={t.url}
          target="_blank"
          rel="noopener noreferrer"
          aria-label="View testimonial on X"
        >
          <img class="shot" src={t.img} alt="Testimonial screenshot" />
        </a>
      {/each}
    </div>
  </div>
</section>

<style>
  .testimonials {
    padding: 3rem 0;
    overflow: hidden;
  }

  .testimonials-heading {
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1.75rem;
    font-weight: 600;
  }

  .marquee {
    width: 100%;
    overflow: hidden;
    mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
    -webkit-mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
  }

  .marquee-track {
    display: flex;
    width: max-content;
    gap: 1.25rem;
    animation: scroll var(--marquee-duration, 32s) linear infinite;
  }

  .marquee:hover .marquee-track {
    animation-play-state: paused;
  }

  @keyframes scroll {
    from {
      transform: translateX(0);
    }
    to {
      /* -50% because the list is duplicated once above */
      transform: translateX(-50%);
    }
  }

  .shot-link {
    flex: 0 0 auto;
    display: block;
    border-radius: 0.75rem;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: border-color 0.2s ease, transform 0.2s ease;
  }

  .shot-link:hover {
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
  }

  .shot {
    display: block;
    height: 90px;
    width: auto;
    max-width: 460px;
    object-fit: cover;
    background: rgba(255, 255, 255, 0.05); /* visible placeholder box while an image loads */
  }

  @media (prefers-reduced-motion: reduce) {
    .marquee-track {
      animation: none;
    }
    .marquee {
      overflow-x: auto;
    }
  }
</style>
