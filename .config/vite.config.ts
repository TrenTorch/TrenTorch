import path from 'node:path';
import { defineConfig } from 'vitest/config';
import tailwindcss from '@tailwindcss/vite';
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
	server: {
		fs: {
			// SvelteKit's dev-server allow-list is derived from `kit.files`
			// (svelte.config.js), which only remaps `routes` and `lib` off the
			// repo root -- `platform/assets` and `platform/fonts` (this repo's
			// other platform/ subdirectories, referenced via the `$assets`/
			// `$fonts` aliases) never made it onto that list, so the dev server
			// 403s every logo and self-hosted-font request. Allowing the whole
			// project root directly is the actual fix, not another one-off
			// entry: any future platform/* subdirectory needs this too.
			allow: [projectRoot]
		}
	},
	plugins: [
		tailwindcss(),
		// Called with no args so svelte.config.js (adapter, vitePlugin
		// compilerOptions, etc.) actually gets loaded -- passing any option
		// here instead makes SvelteKit skip that file entirely.
		sveltekit()
	],
	build: {
		rollupOptions: {
			output: {
				// The editor is one dynamic import (CodeEditor.svelte), but
				// CodeMirror is ~10 packages -- left alone Rollup emits a
				// dozen tiny chunks, i.e. a dozen requests, every time the IDE
				// route mounts. Fold the whole editor stack into one chunk.
				manualChunks(id) {
					if (
						/[\\/]node_modules[\\/](@?codemirror|@lezer|crelt|style-mod|w3c-keyname)[\\/]/.test(id)
					)
						return 'codemirror';
				}
			}
		}
	},
	test: {
		expect: { requireAssertions: true },
		projects: [
			{
				extends: thisConfigFile,
				test: {
					name: 'server',
					environment: 'node',
					include: [
						'platform/**/*.{test,spec}.{js,ts}',
						'processes/**/*.{test,spec}.{js,ts}',
						'data/**/*.{test,spec}.{js,ts}'
					],
					exclude: [
						'platform/**/*.svelte.{test,spec}.{js,ts}',
						'processes/**/*.svelte.{test,spec}.{js,ts}'
					]
				}
			}
		]
	}
});
