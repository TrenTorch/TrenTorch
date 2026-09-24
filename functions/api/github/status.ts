import { verifiedUserId } from '../../_lib/auth';
import { connectionKey, json, type PagesHandler, type StoredConnection } from '../../_lib/env';

export const onRequestGet: PagesHandler = async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);
	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	if (!raw) return json({ connected: false });
	const { login, repo } = JSON.parse(raw) as StoredConnection;
	return json({ connected: true, login, repo });
};
