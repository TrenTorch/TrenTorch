import path from 'node:path';

// Absolute, not relative: prettier-plugin-tailwindcss resolves
// tailwindStylesheet relative to whichever file is currently being
// formatted (not consistently relative to this config file or to cwd),
// which breaks the moment prettier formats a file inside this same
// .config/ directory. An absolute path sidesteps that ambiguity
// entirely, computed from this file's own location (one level below
// the repo root).
const tailwindStylesheet = path.resolve(import.meta.dirname, '..', 'src/routes/layout.css');

/** @type {import("prettier").Config} */
const config = {
	useTabs: true,
	singleQuote: true,
	trailingComma: 'none',
	printWidth: 100,
	plugins: ['prettier-plugin-svelte', 'prettier-plugin-tailwindcss'],
	overrides: [{ files: '*.svelte', options: { parser: 'svelte' } }],
	tailwindStylesheet
};

export default config;
