import { afterEach, describe, expect, it, vi } from 'vitest';
import { usableToken } from './connection';
import { decryptToken, encryptToken } from './crypto';
import type { Env, StoredConnection } from './env';

const SECRET = 'test-secret';

function makeEnv(store: Map<string, string>): Env {
	return {
		GITHUB_TOKENS: {
			get: async (k) => store.get(k) ?? null,
			put: async (k, v) => void store.set(k, v),
			delete: async (k) => void store.delete(k)
		},
		GITHUB_CLIENT_ID: 'id',
		GITHUB_CLIENT_SECRET: 'secret',
		GITHUB_APP_SLUG: 'trentorch-sync',
		TOKEN_SECRET: SECRET,
		PUBLIC_SUPABASE_URL: 'https://supabase.test',
		PUBLIC_SUPABASE_ANON_KEY: 'anon'
	};
}

async function entry(expiresAt?: number): Promise<StoredConnection> {
	return {
		tokenEnc: await encryptToken('ghu_old', SECRET),
		refreshEnc: await encryptToken('ghr_old', SECRET),
		login: 'rocky',
		repo: 'rocky/trentorch-solutions',
		expiresAt
	};
}

afterEach(() => vi.unstubAllGlobals());

describe('usableToken', () => {
	it('returns a still-valid token without calling GitHub', async () => {
		const fetchMock = vi.fn();
		vi.stubGlobal('fetch', fetchMock);
		const stored = await entry(Date.now() + 3_600_000);
		const token = await usableToken(makeEnv(new Map()), 'u1', stored);
		expect(token).toBe('ghu_old');
		expect(fetchMock).not.toHaveBeenCalled();
	});

	it('refreshes an expired token and stores the rotated pair', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(
				async () =>
					new Response(
						JSON.stringify({ access_token: 'ghu_new', refresh_token: 'ghr_new', expires_in: 28800 })
					)
			)
		);
		const store = new Map<string, string>();
		const stored = await entry(Date.now() - 1000);
		const token = await usableToken(makeEnv(store), 'u1', stored);
		expect(token).toBe('ghu_new');
		const saved = JSON.parse(store.get('gh:u1')!) as StoredConnection;
		expect(await decryptToken(saved.refreshEnc!, SECRET)).toBe('ghr_new');
	});

	it('drops the connection when the refresh is rejected', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () => new Response(JSON.stringify({ error: 'bad_refresh_token' })))
		);
		const store = new Map<string, string>([['gh:u1', 'x']]);
		const token = await usableToken(makeEnv(store), 'u1', await entry(Date.now() - 1000));
		expect(token).toBeNull();
		expect(store.has('gh:u1')).toBe(false);
	});
});
