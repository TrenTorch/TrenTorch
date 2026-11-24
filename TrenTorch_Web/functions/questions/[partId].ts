import type { PagesHandler } from '../_lib/env';

// /questions/<partId> moved to /modules/aisys?part=<partId>. A static rule in
// _redirects cannot do this: when the destination has its own query, Cloudflare
// drops the request's one, which loses the ?topic= of Problemset links. So the
// redirect is built here, keeping every query parameter.
export const onRequestGet: PagesHandler = async ({ request, params }) => {
	const url = new URL(request.url);
	const partId = String(params?.partId ?? '');
	const target = new URL(partId === 'part-research-papers' ? '/papers' : '/modules/aisys', url);
	if (partId !== 'part-research-papers') target.searchParams.set('part', partId);
	for (const [key, value] of url.searchParams) {
		if (key !== 'part') target.searchParams.append(key, value);
	}
	return Response.redirect(target.toString(), 301);
};
