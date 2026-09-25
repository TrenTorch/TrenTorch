import { SITE_URL } from './site';

// Canonical form: no trailing slash on any path except the homepage, matching
// SvelteKit's default trailingSlash: 'never' and how the static host serves
// /questions.html at /questions.
export function absoluteUrl(path: string): string {
	if (path === '/' || path === '') return `${SITE_URL}/`;
	const normalized = path.startsWith('/') ? path : `/${path}`;
	return `${SITE_URL}${normalized.replace(/\/+$/, '')}`;
}
