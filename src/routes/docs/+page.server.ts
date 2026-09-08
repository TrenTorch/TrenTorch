import { marked } from 'marked';
// A `?raw` import inlines the file's contents into the built bundle at
// build time. Reading it from disk via `fs` at request time instead (the
// first version of this file did) works locally but breaks in Vercel's
// serverless runtime: README.md never ships alongside the function code
// there, only files Vite actually bundles do.
import readme from '../../../README.md?raw';

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
	const body = fixRelativeLinks(stripHero(readme));
	const html = marked.parse(body, { async: false });
	return { html };
}
