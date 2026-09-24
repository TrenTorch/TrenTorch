import { REPO_NAME } from './env';

const API = 'https://api.github.com';
const TIMEOUT_MS = 8000;

// Every outbound call gets a deadline: a hung GitHub must not hold the function open.
const call = (url: string, init?: RequestInit) =>
	fetch(url, { ...init, signal: AbortSignal.timeout(TIMEOUT_MS) });

const headers = (token: string) => ({
	authorization: `Bearer ${token}`,
	accept: 'application/vnd.github+json',
	'user-agent': 'trentorch-solution-sync',
	'x-github-api-version': '2022-11-28'
});

const utf8ToBase64 = (text: string): string => {
	let bin = '';
	for (const b of new TextEncoder().encode(text)) bin += String.fromCharCode(b);
	return btoa(bin);
};

const base64ToUtf8 = (b64: string): string =>
	new TextDecoder().decode(Uint8Array.from(atob(b64.replace(/\s/g, '')), (c) => c.charCodeAt(0)));

// A GitHub App asks for no scopes: what it can touch is set by the app's
// permissions and by the repos the user picks when installing it.
export function authorizeUrl(clientId: string, redirectUri: string, state: string): string {
	const params = new URLSearchParams({ client_id: clientId, redirect_uri: redirectUri, state });
	return `https://github.com/login/oauth/authorize?${params}`;
}

export const installUrl = (slug: string, state: string): string =>
	`https://github.com/apps/${encodeURIComponent(slug)}/installations/new?${new URLSearchParams({ state })}`;

export interface GithubTokens {
	accessToken: string;
	refreshToken: string | null;
	expiresAt: number | null;
}

async function requestTokens(payload: Record<string, string>): Promise<GithubTokens | null> {
	const res = await call('https://github.com/login/oauth/access_token', {
		method: 'POST',
		headers: { accept: 'application/json', 'content-type': 'application/json' },
		body: JSON.stringify(payload)
	});
	if (!res.ok) return null;
	// Errors come back as 200 with an `error` field and no access_token.
	const body = (await res.json()) as {
		access_token?: string;
		refresh_token?: string;
		expires_in?: number;
	};
	if (!body.access_token) return null;
	return {
		accessToken: body.access_token,
		refreshToken: body.refresh_token ?? null,
		expiresAt: body.expires_in ? Date.now() + body.expires_in * 1000 : null
	};
}

export const exchangeCode = (
	code: string,
	clientId: string,
	clientSecret: string,
	redirectUri: string
) =>
	requestTokens({
		client_id: clientId,
		client_secret: clientSecret,
		code,
		redirect_uri: redirectUri
	});

// Refresh tokens are single-use: the response carries the next pair.
export const refreshTokens = (refreshToken: string, clientId: string, clientSecret: string) =>
	requestTokens({
		client_id: clientId,
		client_secret: clientSecret,
		grant_type: 'refresh_token',
		refresh_token: refreshToken
	});

export async function getLogin(token: string): Promise<string | null> {
	const res = await call(`${API}/user`, { headers: headers(token) });
	if (!res.ok) return null;
	return ((await res.json()) as { login?: string }).login ?? null;
}

export type RepoAccess = 'ok' | 'no_installation' | 'no_repo' | 'error';

// The app can only write where the user installed it, so ask which repos the
// installation covers instead of assuming the solutions repo exists.
export async function findRepoAccess(token: string, login: string): Promise<RepoAccess> {
	const installs = await call(`${API}/user/installations?per_page=100`, {
		headers: headers(token)
	});
	if (!installs.ok) return 'error';
	const list =
		((await installs.json()) as { installations?: { id: number }[] }).installations ?? [];
	if (list.length === 0) return 'no_installation';
	const wanted = `${login}/${REPO_NAME}`.toLowerCase();
	for (const { id } of list) {
		const repos = await call(`${API}/user/installations/${id}/repositories?per_page=100`, {
			headers: headers(token)
		});
		if (!repos.ok) return 'error';
		const names = ((await repos.json()) as { repositories?: { full_name: string }[] }).repositories;
		if (names?.some((r) => r.full_name.toLowerCase() === wanted)) return 'ok';
	}
	return 'no_repo';
}

export type PutResult =
	'created' | 'updated' | 'unchanged' | 'error' | 'unauthorized' | 'rate_limited';

const isRateLimited = (res: Response) =>
	res.headers.get('x-ratelimit-remaining') === '0' || res.headers.has('retry-after');

// Creates or updates one file, skipping the commit when nothing changed so a
// re-solve with identical code does not add a redundant commit. A stale sha
// (409/422, another save landed between our read and write) is retried once.
export async function putFile(
	token: string,
	login: string,
	path: string,
	content: string,
	message: string
): Promise<PutResult> {
	const url = `${API}/repos/${login}/${REPO_NAME}/contents/${path}`;
	for (let attempt = 0; attempt < 2; attempt++) {
		const existing = await call(url, { headers: headers(token) });
		if (existing.status === 401) return 'unauthorized';
		if (existing.status === 429 || (existing.status === 403 && isRateLimited(existing))) {
			return 'rate_limited';
		}
		let sha: string | undefined;
		if (existing.ok) {
			const file = (await existing.json()) as { sha?: string; content?: string };
			// A directory listing or a file with no sha is not ours to overwrite.
			if (!file.sha) return 'error';
			if (file.content !== undefined && base64ToUtf8(file.content) === content) return 'unchanged';
			sha = file.sha;
		} else if (existing.status !== 404) {
			return 'error';
		}
		const res = await call(url, {
			method: 'PUT',
			headers: { ...headers(token), 'content-type': 'application/json' },
			body: JSON.stringify({ message, content: utf8ToBase64(content), sha })
		});
		if (res.status === 401) return 'unauthorized';
		if (res.status === 429 || (res.status === 403 && isRateLimited(res))) return 'rate_limited';
		if ((res.status === 409 || res.status === 422) && attempt === 0) continue;
		if (!res.ok) return 'error';
		return sha ? 'updated' : 'created';
	}
	return 'error';
}

export async function revokeGrant(token: string, clientId: string, clientSecret: string) {
	await call(`${API}/applications/${clientId}/grant`, {
		method: 'DELETE',
		headers: {
			...headers(token),
			authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
			'content-type': 'application/json'
		},
		body: JSON.stringify({ access_token: token })
	}).catch(() => undefined);
}
