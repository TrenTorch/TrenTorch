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
					include: ['src/**/*.{test,spec}.{js,ts}'],
					exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
				}
			}
		]
	}
});
