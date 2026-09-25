import type { PagesHandler } from '../_lib/env';
import {
	injectHead,
	PROFILE_PATH_PATTERN,
	profileHead,
	type PublicProfile
} from '../_lib/profile-page';

// Serves the normal app for /accounts/@name (the page draws the whole account
// itself) with link-preview tags for that profile filled in. Any failure falls
// back to the plain app shell, so a share link never breaks.
export const onRequestGet: PagesHandler = async ({ request, env, params }) => {
	const url = new URL(request.url);
	const shellRes = await env.ASSETS!.fetch(new URL('/404.html', url));
	const shell = await shellRes.text();
	const headers = {
		'content-type': 'text/html; charset=utf-8',
		'cache-control': 'public, max-age=60'
	};
	try {
		const raw = decodeURIComponent(String(params?.username ?? '')).toLowerCase();
		const match = PROFILE_PATH_PATTERN.exec(raw);
		if (!match) return new Response(shell, { status: 200, headers });
		const res = await fetch(`${env.PUBLIC_SUPABASE_URL}/rest/v1/rpc/get_public_profile`, {
			method: 'POST',
			headers: { apikey: env.PUBLIC_SUPABASE_ANON_KEY, 'content-type': 'application/json' },
			body: JSON.stringify({ p_username: match[1] }),
			signal: AbortSignal.timeout(5000)
		});
		const rows = res.ok ? ((await res.json()) as PublicProfile[]) : [];
		if (rows.length === 0) return new Response(shell, { status: 200, headers });
		return new Response(injectHead(shell, profileHead(rows[0], url.origin)), {
			status: 200,
			headers
		});
	} catch {
		return new Response(shell, { status: 200, headers });
	}
};
