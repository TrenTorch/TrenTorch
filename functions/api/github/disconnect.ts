import { verifiedUserId } from '../../_lib/auth';
import { decryptToken } from '../../_lib/crypto';
import { connectionKey, guard, json, readConnection, type PagesHandler } from '../../_lib/env';
import { revokeGrant } from '../../_lib/github';

export const onRequestPost: PagesHandler = guard(async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);
	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	if (raw) {
		const stored = readConnection(raw);
		const token = stored ? await decryptToken(stored.tokenEnc, env.TOKEN_SECRET) : null;
		if (token) await revokeGrant(token, env.GITHUB_CLIENT_ID, env.GITHUB_CLIENT_SECRET);
		await env.GITHUB_TOKENS.delete(connectionKey(userId));
	}
	return json({ connected: false });
});
