import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { describe, it, expect } from 'vitest';

// Same approach and same skip rule as golden-paths.spec.ts: read the real
// build/ output, no browser, and skip (not fail) when build/ does not exist
// yet. These cover what a per-route check cannot: every prerendered page, the
// size of what ships to the browser, and secrets that ended up in it.
const BUILD_DIR = join(import.meta.dirname, '..', 'build');
const buildExists = existsSync(BUILD_DIR);

// Headroom over the current total so normal growth passes, but a dependency or
// data file pulled into the client by accident does not. Raise it deliberately
// in the PR that needs more.
const JS_BUDGET_BYTES = 6_500_000;

// A server-only key or private key material must never appear in client output.
// sb_secret_ needs a long token after it because supabase-js itself contains
// the bare prefix (it checks the key type), which is not a leak.
const SECRET_PATTERNS = [
	/service_role/,
	/sb_secret_[A-Za-z0-9_-]{20,}/,
	/-----BEGIN [A-Z ]*PRIVATE KEY-----/
];

function walk(dir: string): string[] {
	return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
		const path = join(dir, entry.name);
		return entry.isDirectory() ? walk(path) : [path];
	});
}

const files = buildExists ? walk(BUILD_DIR) : [];
const name = (file: string) => relative(BUILD_DIR, file).split('\\').join('/');

describe.skipIf(!buildExists)('build output', () => {
	it('every prerendered page has a title and no error boilerplate', () => {
		const html = files.filter((f) => f.endsWith('.html') && name(f) !== '404.html');
		expect(html.length).toBeGreaterThan(4);

		const problems: string[] = [];
		for (const file of html) {
			const text = readFileSync(file, 'utf8');
			if (!/<title>[^<]+<\/title>/.test(text)) problems.push(`${name(file)}: no <title>`);
			if (/This page was not found|Something went wrong|Internal Error/i.test(text)) {
				problems.push(`${name(file)}: contains error boilerplate`);
			}
		}
		expect(problems).toEqual([]);
	});

	it('client JavaScript stays inside its size budget', () => {
		const total = files
			.filter((f) => f.endsWith('.js'))
			.reduce((sum, f) => sum + statSync(f).size, 0);
		expect(total, `client JS is ${total} bytes, budget ${JS_BUDGET_BYTES}`).toBeLessThan(
			JS_BUDGET_BYTES
		);
	});

	it('ships no secrets to the browser', () => {
		const leaks: string[] = [];
		for (const file of files.filter((f) => /\.(js|html|json|txt|xml)$/.test(f))) {
			const text = readFileSync(file, 'utf8');
			for (const pattern of SECRET_PATTERNS) {
				if (pattern.test(text)) leaks.push(`${name(file)} matches ${pattern}`);
			}
		}
		expect(leaks).toEqual([]);
	});
});
