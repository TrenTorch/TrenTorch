import type { PagesHandler } from '../_lib/env';
import {
	PROFILE_PATH_PATTERN,
	renderNotFound,
	renderProfile,
	type PublicProfile
} from '../_lib/profile-page';

const html = (body: string, status: number, cache: string) =>
	new Response(body, {
		status,
		headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': cache }
	});

export const onRequestGet: PagesHandler = async ({ request, env, params }) => {
	try {
		return await render(request, env, params);
	} catch {
		return html(renderNotFound(new URL(request.url).origin), 502, 'no-store');
	}
};

const render = async (
	request: Request,
	env: Parameters<PagesHandler>[0]['env'],
	params: Parameters<PagesHandler>[0]['params']
) => {
	const origin = new URL(request.url).origin;
	const raw = decodeURIComponent(String(params?.username ?? '')).toLowerCase();
	const match = PROFILE_PATH_PATTERN.exec(raw);
	if (!match) return html(renderNotFound(origin), 404, 'public, max-age=60');

	const res = await fetch(`${env.PUBLIC_SUPABASE_URL}/rest/v1/rpc/get_public_profile`, {
		method: 'POST',
		headers: {
			apikey: env.PUBLIC_SUPABASE_ANON_KEY,
			'content-type': 'application/json'
		},
		body: JSON.stringify({ p_username: match[1] }),
		signal: AbortSignal.timeout(8000)
	});
	if (!res.ok) return html(renderNotFound(origin), 502, 'no-store');
	const rows = (await res.json()) as PublicProfile[];
	if (rows.length === 0) return html(renderNotFound(origin), 404, 'public, max-age=60');
	return html(renderProfile(rows[0], origin), 200, 'public, max-age=60');
};
