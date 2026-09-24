// Minimal shapes for the Cloudflare Pages runtime, so these files type-check
// without pulling in @cloudflare/workers-types.
export interface KVNamespaceLike {
	get(key: string): Promise<string | null>;
	put(key: string, value: string): Promise<void>;
	delete(key: string): Promise<void>;
}

export interface Env {
	GITHUB_TOKENS: KVNamespaceLike;
	GITHUB_CLIENT_ID: string;
	GITHUB_CLIENT_SECRET: string;
	// URL slug of the GitHub App (github.com/apps/<slug>), used for the install page.
	GITHUB_APP_SLUG: string;
	// Signs the OAuth state and derives the key that encrypts stored tokens.
	TOKEN_SECRET: string;
	PUBLIC_SUPABASE_URL: string;
	PUBLIC_SUPABASE_ANON_KEY: string;
}

export interface PagesContext {
	request: Request;
	env: Env;
}

export type PagesHandler = (context: PagesContext) => Promise<Response>;

export interface StoredConnection {
	tokenEnc: string;
	login: string;
	repo: string;
	// GitHub App user tokens expire (8 h) and refresh. Absent on legacy OAuth entries.
	refreshEnc?: string;
	expiresAt?: number;
}

export const REPO_NAME = 'trentorch-solutions';
export const connectionKey = (userId: string) => `gh:${userId}`;

export function json(body: unknown, status = 200): Response {
	return new Response(JSON.stringify(body), {
		status,
		headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }
	});
}

// A corrupt or hand-edited KV value must read as "not connected", not crash.
export function readConnection(raw: string): StoredConnection | null {
	try {
		const value = JSON.parse(raw) as Partial<StoredConnection>;
		return typeof value.tokenEnc === 'string' && typeof value.login === 'string'
			? {
					tokenEnc: value.tokenEnc,
					login: value.login,
					repo: value.repo ?? '',
					refreshEnc: typeof value.refreshEnc === 'string' ? value.refreshEnc : undefined,
					expiresAt: typeof value.expiresAt === 'number' ? value.expiresAt : undefined
				}
			: null;
	} catch {
		return null;
	}
}

// A timeout or network failure talking to Supabase, KV or GitHub becomes a
// clean JSON error the client already knows how to handle, not a raw 500 page.
export const guard =
	(handler: PagesHandler): PagesHandler =>
	async (context) => {
		try {
			return await handler(context);
		} catch {
			return json({ error: 'unavailable' }, 502);
		}
	};
