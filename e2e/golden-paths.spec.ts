import { existsSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { describe, it, expect } from 'vitest';

// Deliberately not Playwright (or any real browser): this is a prerendered
// static site, so "does the golden-path route actually render" is a
// question the build's own HTML output can answer directly -- no browser
// binary, no server, no multi-second launch per test. Reads build/, so it
// only has something to check after `npm run build` -- runs for real in
// CI's "Golden-path smoke tests" step (after Build) and skips itself (not
// a failure) if run earlier via plain `npm run test`, since build/ won't
// exist yet at that point.
const BUILD_DIR = join(import.meta.dirname, '..', 'build');
const buildExists = existsSync(BUILD_DIR);

const GOLDEN_PATHS = [
	{ name: 'homepage', file: 'index.html' },
	{ name: 'questions listing', file: 'questions.html' },
	{ name: 'problem of the day', file: 'potd.html' },
	{ name: 'account', file: 'account.html' }
];

describe.skipIf(!buildExists).each(GOLDEN_PATHS)('golden path: $name ($file)', ({ file }) => {
	const filePath = join(BUILD_DIR, file);

	it('was actually emitted by the build', () => {
		expect(existsSync(filePath), `${file} missing from build/ output`).toBe(true);
	});

	it('is not an empty or truncated shell', () => {
		// A blank/broken prerender is a handful of bytes of boilerplate; a
		// real rendered page (this app's layout chrome alone: nav, fonts,
		// theme script) is tens of KB. 5 KB is comfortably below every real
		// page's size and comfortably above a broken one's.
		expect(statSync(filePath).size).toBeGreaterThan(5_000);
	});

	it('has a <title> (head rendering ran)', () => {
		const html = readFileSync(filePath, 'utf8');
		expect(html).toMatch(/<title>[^<]+<\/title>/);
	});

	it('has no unhandled SvelteKit error boilerplate', () => {
		const html = readFileSync(filePath, 'utf8');
		expect(html).not.toMatch(/This page was not found|Something went wrong|Internal Error/i);
	});
});
