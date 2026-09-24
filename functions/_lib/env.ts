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
}

export const REPO_NAME = 'trentorch-solutions';
export const connectionKey = (userId: string) => `gh:${userId}`;

export function json(body: unknown, status = 200): Response {
	return new Response(JSON.stringify(body), {
		status,
		headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }
	});
}
