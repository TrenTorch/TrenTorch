import path from 'node:path';
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';
import { curriculumPlugin } from '../processes/curriculum-build/vite-plugin-curriculum.mjs';

// Separate from vite.config.ts on purpose: the Pyodide check is slow and needs
// the network (it downloads the numpy wheel), so it must not run as part of
// `npm test`. Run it with `npm run test:pyodide`.
const projectRoot = path.resolve(import.meta.dirname, '..');

export default defineConfig({
	root: projectRoot,
	// Called with no args so svelte.config.js (the $data and $processes aliases)
	// is loaded, same as vite.config.ts.
	// curriculumPlugin() serves virtual:curriculum/bundle, which the check reads its questions from.
	plugins: [sveltekit(), curriculumPlugin()],
	test: {
		name: 'pyodide',
		environment: 'node',
		include: ['pyodide-check/**/*.spec.ts'],
		testTimeout: 60_000,
		hookTimeout: 180_000
	}
});
