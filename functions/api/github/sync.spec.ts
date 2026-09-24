import { describe, it, expect, vi, afterEach } from 'vitest';
import { encryptToken } from '../../_lib/crypto';
import type { Env } from '../../_lib/env';
import { onRequestPost } from './sync';

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
		TOKEN_SECRET: SECRET,
		PUBLIC_SUPABASE_URL: 'https://supabase.test',
		PUBLIC_SUPABASE_ANON_KEY: 'anon'
	};
}

const body = {
	questionId: 'gelu',
	title: 'GELU',
	difficulty: 'Beginner',
	tags: [],
	description: 'Implement GELU.',
	code: 'def gelu(x): return x'
};

const request = (payload: unknown = body) =>
	new Request('https://trentorch.com/api/github/sync', {
		method: 'POST',
		headers: { authorization: 'Bearer jwt' },
		body: JSON.stringify(payload)
	});

async function connected(): Promise<Map<string, string>> {
	const store = new Map<string, string>();
	store.set(
		'gh:user-1',
		JSON.stringify({
			tokenEnc: await encryptToken('gho_token', SECRET),
			login: 'rocky',
			repo: 'rocky/trentorch-solutions'
		})
	);
	return store;
}

afterEach(() => vi.unstubAllGlobals());

describe('sync endpoint', () => {
	it('rejects an unverified caller', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () => new Response('{}', { status: 401 }))
		);
		const res = await onRequestPost({ request: request(), env: makeEnv(await connected()) });
		expect(res.status).toBe(401);
	});

	it('returns 409 when no repo is connected', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () => Response.json({ id: 'user-1' }))
		);
		const res = await onRequestPost({ request: request(), env: makeEnv(new Map()) });
		expect(res.status).toBe(409);
	});

	it('writes the solution and README into the users repo', async () => {
		const puts: { url: string; message: string }[] = [];
		vi.stubGlobal(
			'fetch',
			vi.fn(async (url: string, init?: RequestInit) => {
				if (url.includes('supabase')) return Response.json({ id: 'user-1' });
				if (init?.method === 'PUT') {
					puts.push({ url, message: JSON.parse(init.body as string).message });
					return Response.json({}, { status: 201 });
				}
				return new Response('{}', { status: 404 });
			})
		);
		const res = await onRequestPost({ request: request(), env: makeEnv(await connected()) });
		expect(res.status).toBe(200);
		expect(puts.map((p) => p.url)).toEqual([
			'https://api.github.com/repos/rocky/trentorch-solutions/contents/gelu/solution.py',
			'https://api.github.com/repos/rocky/trentorch-solutions/contents/gelu/README.md'
		]);
		expect(puts[0].message).toBe('Solve GELU');
	});

	it('drops the stored token when GitHub says it was revoked', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async (url: string) =>
				url.includes('supabase')
					? Response.json({ id: 'user-1' })
					: new Response('{}', { status: 401 })
			)
		);
		const store = await connected();
		const res = await onRequestPost({ request: request(), env: makeEnv(store) });
		expect(res.status).toBe(409);
		expect(store.size).toBe(0);
	});

	it('rejects an unsafe question id', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () => Response.json({ id: 'user-1' }))
		);
		const res = await onRequestPost({
			request: request({ ...body, questionId: '../evil' }),
			env: makeEnv(await connected())
		});
		expect(res.status).toBe(400);
	});
});
