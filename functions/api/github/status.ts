import { verifiedUserId } from '../../_lib/auth';
import { connectionKey, guard, json, readConnection, type PagesHandler } from '../../_lib/env';

export const onRequestGet: PagesHandler = guard(async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);
	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	if (!raw) return json({ connected: false });
	const stored = readConnection(raw);
	if (!stored) return json({ connected: false });
	return json({ connected: true, login: stored.login, repo: stored.repo });
});
