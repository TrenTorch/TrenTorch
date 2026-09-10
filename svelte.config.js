import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// This file has to live at the true repo root: vite-plugin-svelte and the
// SvelteKit CLI both auto-discover it by that fixed name/location, with no
// override flag (unlike vite.config.ts, which we do point elsewhere via
// --config). Keep it minimal; everything else config-heavy lives in .config/.

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter(),
		prerender: {
			// The static pages (/, /account, /questions) link to /ide/[id],
			// which is dynamic and can't be prerendered. Don't treat the
			// crawler hitting those links as a build failure -- that route is
			// rendered on demand.
			handleHttpError: ({ path, message }) => {
				if (path.startsWith('/ide/')) return;
				throw new Error(message);
			}
		}
	},
	// Passed through to vite-plugin-svelte. Has to live here rather than as
	// an inline option to sveltekit() in vite.config.ts: passing any option
	// to sveltekit() directly makes it skip loading this file entirely,
	// including the adapter above (see @sveltejs/kit/src/exports/vite --
	// "svelte.config.js is ignored when options are passed via your Vite
	// config").
	vitePlugin: {
		compilerOptions: {
			// Force runes mode for the project, except for libraries. Can be
			// removed in Svelte 6.
			runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
		}
	}
};

export default config;
