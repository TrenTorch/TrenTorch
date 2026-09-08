import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

const REPO_BLOB_ROOT = 'https://github.com/TrenTorch/TrenTorch-Web/blob/main/';

/** Rewrites repo-relative links (README links to files like LICENSE, or
 * other docs) into working GitHub URLs, since this page only ever renders
 * the README's body, not the actual repo tree around it. */
function fixRelativeLinks(markdown: string): string {
	return markdown.replace(/\]\((?!https?:\/\/|#)([^)]+)\)/g, (_match, target: string) => {
		return `](${REPO_BLOB_ROOT}${target})`;
	});
}

/** Strips the README's raw-HTML hero block (logo/title table + badges)
 * since the site's own page hero already covers that -- starts the body
 * at the first real heading instead. */
function stripHero(markdown: string): string {
	const firstHeading = markdown.indexOf('\n## ');
	return firstHeading === -1 ? markdown : markdown.slice(firstHeading + 1);
}

export function load() {
	const raw = fs.readFileSync(path.join(process.cwd(), 'README.md'), 'utf-8');
	const body = fixRelativeLinks(stripHero(raw));
	const html = marked.parse(body, { async: false });
	return { html };
}
