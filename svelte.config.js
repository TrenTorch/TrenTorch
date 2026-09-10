import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// This file has to live at the true repo root: vite-plugin-svelte and the
// SvelteKit CLI both auto-discover it by that fixed name/location, with no
// override flag (unlike vite.config.ts, which we do point elsewhere via
// --config). Keep it minimal; everything else config-heavy lives in .config/.

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		// Fully static output (every route is prerendered) -- no server, no
		// edge function, nothing to invoke. `fallback` emits a 404.html
		// carrying the client router, so an unmatched URL (e.g. a mistyped
		// /ide/<slug>) still boots the app and resolves to the right page or
		// a proper in-app 404 instead of the host's bare error page.
		adapter: adapter({ fallback: '404.html' }),
		prerender: {
			// Every route is prerendered, including all /ide/<slug> pages
			// (entries listed in ide/[id]/+page.ts). This guard is defensive:
			// if a question ever links to a slug outside the curriculum list,
			// the crawler hitting that 404 shouldn't fail the whole build.
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
