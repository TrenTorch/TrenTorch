import { describe, it, expect, vi, afterEach } from 'vitest';
import { putFile } from './github';
import { readConnection } from './env';
import { commitMessage } from './solution-files';

afterEach(() => vi.unstubAllGlobals());

const b64 = (text: string) => btoa(text);

describe('putFile', () => {
	it('retries once when the file changed between read and write', async () => {
		let puts = 0;
		vi.stubGlobal(
			'fetch',
			vi.fn(async (_url: string, init?: RequestInit) => {
				if (init?.method === 'PUT') {
					puts += 1;
					return new Response('{}', { status: puts === 1 ? 409 : 200 });
				}
				return Response.json({ sha: `sha${puts}`, content: b64('old') });
			})
		);
		expect(await putFile('t', 'rocky/trentorch-solutions', 'q/solution.py', 'new', 'msg')).toBe(
			'updated'
		);
		expect(puts).toBe(2);
	});

	it('gives up after one retry', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async (_url: string, init?: RequestInit) =>
				init?.method === 'PUT'
					? new Response('{}', { status: 409 })
					: Response.json({ sha: 's', content: b64('old') })
			)
		);
		expect(await putFile('t', 'rocky/trentorch-solutions', 'q/solution.py', 'new', 'msg')).toBe(
			'error'
		);
	});

	it('skips the commit when the content is unchanged', async () => {
		const fetchMock = vi.fn(async () => Response.json({ sha: 's', content: b64('same') }));
		vi.stubGlobal('fetch', fetchMock);
		expect(await putFile('t', 'rocky/trentorch-solutions', 'q/solution.py', 'same', 'msg')).toBe(
			'unchanged'
		);
		expect(fetchMock).toHaveBeenCalledTimes(1);
	});

	it('reports a rate limit instead of a generic failure', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(
				async () => new Response('{}', { status: 403, headers: { 'x-ratelimit-remaining': '0' } })
			)
		);
		expect(await putFile('t', 'rocky/trentorch-solutions', 'q/solution.py', 'x', 'msg')).toBe(
			'rate_limited'
		);
	});

	it('refuses to overwrite a path that is a directory', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn(async () => Response.json([{ name: 'a' }]))
		);
		expect(await putFile('t', 'rocky/trentorch-solutions', 'q', 'x', 'msg')).toBe('error');
	});
});

describe('readConnection', () => {
	it('reads a valid record', () => {
		expect(
			readConnection(JSON.stringify({ tokenEnc: 'a.b', login: 'r', repo: 'r/x' }))?.login
		).toBe('r');
	});

	it('treats garbage or partial records as not connected', () => {
		expect(readConnection('not json')).toBeNull();
		expect(readConnection('{}')).toBeNull();
		expect(readConnection('null')).toBeNull();
	});
});

describe('commitMessage', () => {
	it('is one line and bounded', () => {
		expect(commitMessage('Line one\nline two')).toBe('Solve Line one line two');
		expect(commitMessage('x'.repeat(500)).length).toBe(120);
		expect(commitMessage('   ')).toBe('Solve a question');
	});
});
