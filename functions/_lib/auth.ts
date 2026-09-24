import type { Env } from './env';

// Asks Supabase who the bearer token belongs to instead of verifying the JWT
// here: no signing keys to copy into Cloudflare, and revoked sessions fail too.
export async function verifiedUserId(request: Request, env: Env): Promise<string | null> {
	const header = request.headers.get('authorization');
	if (!header?.startsWith('Bearer ')) return null;
	const res = await fetch(`${env.SUPABASE_URL}/auth/v1/user`, {
		headers: { authorization: header, apikey: env.SUPABASE_ANON_KEY }
	});
	if (!res.ok) return null;
	const user = (await res.json()) as { id?: string };
	return user.id ?? null;
}
