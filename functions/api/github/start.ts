import { verifiedUserId } from '../../_lib/auth';
import { signState } from '../../_lib/crypto';
import { guard, json, type PagesHandler } from '../../_lib/env';
import { authorizeUrl } from '../../_lib/github';

// The browser asks for the GitHub authorize URL (rather than linking to it
// directly) so the signed state can be tied to the verified signed-in user.
export const onRequestPost: PagesHandler = guard(async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);
	const redirectUri = `${new URL(request.url).origin}/api/github/callback`;
	const state = await signState(userId, env.TOKEN_SECRET);
	return json({ url: authorizeUrl(env.GITHUB_CLIENT_ID, redirectUri, state) });
});
