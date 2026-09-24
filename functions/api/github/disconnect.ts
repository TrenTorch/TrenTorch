import { verifiedUserId } from '../../_lib/auth';
import { decryptToken } from '../../_lib/crypto';
import { connectionKey, json, type PagesHandler, type StoredConnection } from '../../_lib/env';
import { revokeGrant } from '../../_lib/github';

export const onRequestPost: PagesHandler = async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);
	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	if (raw) {
		const token = await decryptToken(
			(JSON.parse(raw) as StoredConnection).tokenEnc,
			env.TOKEN_SECRET
		);
		if (token) await revokeGrant(token, env.GITHUB_CLIENT_ID, env.GITHUB_CLIENT_SECRET);
		await env.GITHUB_TOKENS.delete(connectionKey(userId));
	}
	return json({ connected: false });
};
