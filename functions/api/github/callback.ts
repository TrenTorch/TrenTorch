import { storeTokens } from '../../_lib/connection';
import { verifyState } from '../../_lib/crypto';
import { REPO_NAME, type PagesHandler } from '../../_lib/env';
import { exchangeCode, findRepoAccess, getLogin, installUrl } from '../../_lib/github';

export const onRequestGet: PagesHandler = async (context) => {
	try {
		return await handle(context);
	} catch {
		return new Response(null, {
			status: 302,
			headers: { location: `${new URL(context.request.url).origin}/account?github=error` }
		});
	}
};

// Reached twice for a new user: once after authorizing, and again after the
// GitHub App install page (which sends `installation_id` along with a code).
const handle: PagesHandler = async ({ request, env }) => {
	const url = new URL(request.url);
	const redirect = (location: string) => new Response(null, { status: 302, headers: { location } });
	const back = (result: string) => redirect(`${url.origin}/account?github=${result}`);

	const code = url.searchParams.get('code');
	const state = url.searchParams.get('state');
	if (!code || !state) return back('error');
	const userId = await verifyState(state, env.TOKEN_SECRET);
	if (!userId) return back('error');

	const tokens = await exchangeCode(
		code,
		env.GITHUB_CLIENT_ID,
		env.GITHUB_CLIENT_SECRET,
		`${url.origin}/api/github/callback`
	);
	if (!tokens) return back('error');
	const login = await getLogin(tokens.accessToken);
	if (!login) return back('error');

	const access = await findRepoAccess(tokens.accessToken, login);
	if (access === 'no_installation') {
		// Coming back from the install page and still nothing installed: stop, do not loop.
		if (url.searchParams.has('installation_id')) return back('error');
		return redirect(installUrl(env.GITHUB_APP_SLUG, state));
	}
	if (access === 'no_repo') return back('norepo');
	if (access !== 'ok') return back('error');

	await storeTokens(env, userId, { login, repo: `${login}/${REPO_NAME}` }, tokens);
	return back('connected');
};
