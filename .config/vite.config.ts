import path from 'node:path';
import { defineConfig } from 'vitest/config';
import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-auto';
import { sveltekit } from '@sveltejs/kit/vite';

// Config now lives one level below the repo root. Vite defaults `root`
// to the directory containing this file, which would otherwise make it
// look for src/, static/, etc. inside .config/ itself -- point it back
// at the real project root explicitly.
const projectRoot = path.resolve(import.meta.dirname, '..');

// vitest's projects[].extends resolves relative to `root` (set above to
// the real project root), not relative to this config file's own
// directory -- a bare './vite.config.ts' self-reference would resolve to
// a file at the repo root that no longer exists. Absolute path
// sidesteps that, same fix as prettier.config.js's tailwindStylesheet.
const thisConfigFile = path.resolve(import.meta.dirname, 'vite.config.ts');

export default defineConfig({
	root: projectRoot,
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},

			// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
			// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
			// See https://svelte.dev/docs/kit/adapters for more information about adapters.
			adapter: adapter()
		})
	],
	test: {
		expect: { requireAssertions: true },
		projects: [
			{
				extends: thisConfigFile,
				test: {
					name: 'server',
					environment: 'node',
					include: ['src/**/*.{test,spec}.{js,ts}'],
					exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
				}
			}
		]
	}
});
