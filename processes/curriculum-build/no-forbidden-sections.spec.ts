import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { describe, it, expect } from 'vitest';
import { isDir } from './is-dir.mjs';

// parseReadme has no notion of a "meta" or "author-only" section -- it
// captures everything from "## Explanation" to end-of-file verbatim (see
// parse-readme.spec.ts). So the only thing standing between an author-only
// aside and shipping to students is never writing it in the source
// README. This got missed twice for real (THE SURGE and THE MARGIN both
// shipped with a "Notes for the Judge / Setter" and a "This site's
// interface" section before being caught and stripped by hand) -- this is
// the automated guard against that mistake recurring.
const FORBIDDEN_HEADINGS = [
	/notes for the judge/i,
	/notes for the setter/i,
	/this site'?s interface/i
];

const APP_DATA_ROOT = join(import.meta.dirname, '..', '..', 'data', 'app_data');

function findReadmes(dir: string): string[] {
	const readmes: string[] = [];
	for (const name of readdirSync(dir)) {
		if (name.startsWith('_') || name.startsWith('.')) continue;
		const full = join(dir, name);
		if (isDir(full)) {
			readmes.push(...findReadmes(full));
		} else if (name === 'README.md' && dir !== APP_DATA_ROOT) {
			// The top-level data/app_data/README.md is the authoring guide
			// itself, not student-facing content -- it's allowed to talk
			// about what not to write.
			readmes.push(full);
		}
	}
	return readmes;
}

describe('question READMEs contain no author-only sections', () => {
	const readmes = findReadmes(APP_DATA_ROOT);

	it('found at least one question README to check', () => {
		expect(readmes.length).toBeGreaterThan(0);
	});

	it.each(readmes)('%s has no forbidden heading', (path) => {
		const content = readFileSync(path, 'utf8');
		for (const pattern of FORBIDDEN_HEADINGS) {
			expect(content, `${path} matched forbidden heading ${pattern}`).not.toMatch(pattern);
		}
	});
});
