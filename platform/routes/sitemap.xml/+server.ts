import { buildSitemapXml } from '$processes/seo/build-sitemap-xml';
import type { RequestHandler } from './$types';

// Prerendered to build/sitemap.xml. Dependency-free on purpose: no fs/path,
// the list comes from the same compiled curriculum the pages use.
export const prerender = true;

export const GET: RequestHandler = () =>
	new Response(buildSitemapXml(), {
		headers: { 'Content-Type': 'application/xml; charset=utf-8' }
	});
