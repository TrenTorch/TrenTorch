import { encryptToken, verifyState } from '../../_lib/crypto';
import { REPO_NAME, connectionKey, type PagesHandler, type StoredConnection } from '../../_lib/env';
import { ensureRepo, exchangeCode, getLogin } from '../../_lib/github';

export const onRequestGet: PagesHandler = async ({ request, env }) => {
	const url = new URL(request.url);
	const back = (result: string) =>
		new Response(null, {
			status: 302,
			headers: { location: `${url.origin}/account?github=${result}` }
		});

	const code = url.searchParams.get('code');
	const state = url.searchParams.get('state');
	if (!code || !state) return back('error');
	const userId = await verifyState(state, env.TOKEN_SECRET);
	if (!userId) return back('error');

	const token = await exchangeCode(
		code,
		env.GITHUB_CLIENT_ID,
		env.GITHUB_CLIENT_SECRET,
		`${url.origin}/api/github/callback`
	);
	if (!token) return back('error');
	const login = await getLogin(token);
	if (!login || !(await ensureRepo(token, login))) return back('error');

	const stored: StoredConnection = {
		tokenEnc: await encryptToken(token, env.TOKEN_SECRET),
		login,
		repo: `${login}/${REPO_NAME}`
	};
	await env.GITHUB_TOKENS.put(connectionKey(userId), JSON.stringify(stored));
	return back('connected');
};
