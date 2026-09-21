import path from 'node:path';
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

// Separate from vite.config.ts on purpose: the Pyodide check is slow and needs
// the network (it downloads the numpy wheel), so it must not run as part of
// `npm test`. Run it with `npm run test:pyodide`.
const projectRoot = path.resolve(import.meta.dirname, '..');

export default defineConfig({
	root: projectRoot,
	// Called with no args so svelte.config.js (the $data and $processes aliases)
	// is loaded, same as vite.config.ts.
	plugins: [sveltekit()],
	test: {
		name: 'pyodide',
		environment: 'node',
		include: ['pyodide-check/**/*.spec.ts'],
		testTimeout: 60_000,
		hookTimeout: 180_000
	}
});
