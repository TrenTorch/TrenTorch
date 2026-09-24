import { decryptToken, encryptToken } from './crypto';
import { connectionKey, readConnection, type Env, type StoredConnection } from './env';
import { refreshTokens } from './github';

const REFRESH_MARGIN_MS = 60_000;

export async function storeTokens(
	env: Env,
	userId: string,
	base: Pick<StoredConnection, 'login' | 'repo'>,
	tokens: { accessToken: string; refreshToken: string | null; expiresAt: number | null }
): Promise<void> {
	const stored: StoredConnection = {
		...base,
		tokenEnc: await encryptToken(tokens.accessToken, env.TOKEN_SECRET),
		refreshEnc: tokens.refreshToken
			? await encryptToken(tokens.refreshToken, env.TOKEN_SECRET)
			: undefined,
		expiresAt: tokens.expiresAt ?? undefined
	};
	await env.GITHUB_TOKENS.put(connectionKey(userId), JSON.stringify(stored));
}

// Returns a token that is safe to use now, refreshing an expired one. Null
// means the connection is dead (and has been removed) so the user reconnects.
export async function usableToken(
	env: Env,
	userId: string,
	stored: StoredConnection
): Promise<string | null> {
	const fresh = !stored.expiresAt || stored.expiresAt - Date.now() > REFRESH_MARGIN_MS;
	if (fresh) return decryptToken(stored.tokenEnc, env.TOKEN_SECRET);

	const refresh = stored.refreshEnc
		? await decryptToken(stored.refreshEnc, env.TOKEN_SECRET)
		: null;
	const tokens = refresh
		? await refreshTokens(refresh, env.GITHUB_CLIENT_ID, env.GITHUB_CLIENT_SECRET)
		: null;
	if (tokens) {
		await storeTokens(env, userId, stored, tokens);
		return tokens.accessToken;
	}

	// Refresh tokens are single-use, so a parallel request may have just rotated
	// them. Use its result before deciding the connection is gone.
	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	const latest = raw ? readConnection(raw) : null;
	if (latest && latest.tokenEnc !== stored.tokenEnc && (latest.expiresAt ?? 0) > Date.now()) {
		return decryptToken(latest.tokenEnc, env.TOKEN_SECRET);
	}
	await env.GITHUB_TOKENS.delete(connectionKey(userId));
	return null;
}
