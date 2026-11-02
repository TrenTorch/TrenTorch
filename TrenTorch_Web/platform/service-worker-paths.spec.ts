import { readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import {
	isLazyFile,
	isRuntimeFile,
	RUNTIME_SEGMENTS,
	shouldPrecache
} from './service-worker-paths';

const STATIC_DIR = join(import.meta.dirname, 'static');
const walk = (dir: string): string[] =>
	readdirSync(dir).flatMap((name) => {
		const path = join(dir, name);
		return statSync(path).isDirectory() ? walk(path) : [path];
	});
// The paths the service worker sees: static files, as URL paths from the site root.
const staticUrls = walk(STATIC_DIR).map((file) => file.slice(STATIC_DIR.length));

describe('the service worker precache', () => {
	it('leaves out every language runtime', () => {
		for (const path of [
			'/go-runtime/yaegi.wasm.gz',
			'/go-runtime/wasm_exec.js',
			'/rust-runtime/rustc.wasm.gz',
			'/java-runtime/rt.jar',
			'/cpp-runtime/clang.wasm.gz'
		])
			expect(shouldPrecache(path), path).toBe(false);
	});

	it('leaves out the lazily cached wheels and vendored scripts', () => {
		expect(shouldPrecache('/wheels/plotly-7.1.0-py3-none-any.whl')).toBe(false);
		expect(shouldPrecache('/vendor/plotly-4.1.1.min.js')).toBe(false);
		expect(isLazyFile('/wheels/x.whl')).toBe(true);
	});

	it('keeps what a first visit needs: pages, hashed app files, fonts, the logo', () => {
		for (const path of [
			'/_app/immutable/chunks/abc123.js',
			'/index.html',
			'/logo.webp',
			'/fonts/inter-latin.woff2',
			'/robots.txt'
		])
			expect(shouldPrecache(path), path).toBe(true);
	});

	it('does not mistake a file that merely has "runtime" in its name for a runtime folder', () => {
		expect(isRuntimeFile('/_app/immutable/chunks/runtime-helpers.js')).toBe(false);
		expect(isRuntimeFile('/runtime-notes.txt')).toBe(false);
	});

	// The reason this file exists: a new runtime folder that nobody added to the list would be downloaded by
	// every first-time visitor, in the background, next to the one language they picked.
	it('covers every "*-runtime" folder that exists under static/', () => {
		const folders = new Set(
			staticUrls
				.map((url) => url.split('/')[1])
				.filter((first) => first?.endsWith('-runtime'))
				.map((first) => `/${first}/`)
		);
		expect(folders.size).toBeGreaterThanOrEqual(4);
		expect([...folders].filter((folder) => !RUNTIME_SEGMENTS.includes(folder))).toEqual([]);
	});

	it('precaches none of the files under those folders', () => {
		const runtimeFiles = staticUrls.filter((url) => /^\/[a-z]+-runtime\//.test(url));
		expect(runtimeFiles.length).toBeGreaterThan(10);
		expect(runtimeFiles.filter(shouldPrecache)).toEqual([]);
	});
});
