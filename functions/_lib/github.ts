import { REPO_NAME } from './env';

const API = 'https://api.github.com';

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

export function authorizeUrl(clientId: string, redirectUri: string, state: string): string {
	const params = new URLSearchParams({
		client_id: clientId,
		redirect_uri: redirectUri,
		scope: 'public_repo',
		state
	});
	return `https://github.com/login/oauth/authorize?${params}`;
}

export async function exchangeCode(
	code: string,
	clientId: string,
	clientSecret: string,
	redirectUri: string
): Promise<string | null> {
	const res = await fetch('https://github.com/login/oauth/access_token', {
		method: 'POST',
		headers: { accept: 'application/json', 'content-type': 'application/json' },
		body: JSON.stringify({
			client_id: clientId,
			client_secret: clientSecret,
			code,
			redirect_uri: redirectUri
		})
	});
	if (!res.ok) return null;
	const body = (await res.json()) as { access_token?: string };
	return body.access_token ?? null;
}

export async function getLogin(token: string): Promise<string | null> {
	const res = await fetch(`${API}/user`, { headers: headers(token) });
	if (!res.ok) return null;
	return ((await res.json()) as { login?: string }).login ?? null;
}

// Creates the solutions repo on first connect. An existing repo (422) is fine.
export async function ensureRepo(token: string, login: string): Promise<boolean> {
	const exists = await fetch(`${API}/repos/${login}/${REPO_NAME}`, { headers: headers(token) });
	if (exists.ok) return true;
	const res = await fetch(`${API}/user/repos`, {
		method: 'POST',
		headers: { ...headers(token), 'content-type': 'application/json' },
		body: JSON.stringify({
			name: REPO_NAME,
			description: 'My TrenTorch solutions, saved automatically.',
			private: false,
			auto_init: true
		})
	});
	return res.ok || res.status === 422;
}

export type PutResult = 'created' | 'updated' | 'unchanged' | 'error' | 'unauthorized';

// Creates or updates one file, skipping the commit when nothing changed so a
// re-solve with identical code does not add a redundant commit.
export async function putFile(
	token: string,
	login: string,
	path: string,
	content: string,
	message: string
): Promise<PutResult> {
	const url = `${API}/repos/${login}/${REPO_NAME}/contents/${path}`;
	const existing = await fetch(url, { headers: headers(token) });
	if (existing.status === 401) return 'unauthorized';
	let sha: string | undefined;
	if (existing.ok) {
		const file = (await existing.json()) as { sha: string; content?: string };
		if (file.content !== undefined && base64ToUtf8(file.content) === content) return 'unchanged';
		sha = file.sha;
	} else if (existing.status !== 404) {
		return 'error';
	}
	const res = await fetch(url, {
		method: 'PUT',
		headers: { ...headers(token), 'content-type': 'application/json' },
		body: JSON.stringify({ message, content: utf8ToBase64(content), sha })
	});
	if (res.status === 401) return 'unauthorized';
	if (!res.ok) return 'error';
	return sha ? 'updated' : 'created';
}

export async function revokeGrant(token: string, clientId: string, clientSecret: string) {
	await fetch(`${API}/applications/${clientId}/grant`, {
		method: 'DELETE',
		headers: {
			...headers(token),
			authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
			'content-type': 'application/json'
		},
		body: JSON.stringify({ access_token: token })
	}).catch(() => undefined);
}
