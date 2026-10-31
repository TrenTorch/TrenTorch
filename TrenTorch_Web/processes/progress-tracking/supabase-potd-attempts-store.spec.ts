import { beforeEach, describe, expect, it, vi } from 'vitest';

const rpc = vi.fn();
const refreshSession = vi.fn();

vi.mock('$processes/auth/supabase-client', () => ({
	getSupabaseClient: () => ({ rpc, auth: { refreshSession } })
}));

import { recordPotdAttempt } from './supabase-potd-attempts-store';

const call = () => recordPotdAttempt('q', 6, 6, true);

beforeEach(() => {
	vi.useFakeTimers();
	vi.spyOn(console, 'error').mockImplementation(() => {});
	rpc.mockReset();
	refreshSession.mockReset().mockResolvedValue({ error: null });
});

async function run() {
	const pending = call();
	await vi.runAllTimersAsync();
	return pending;
}

describe('recordPotdAttempt', () => {
	it('succeeds on the first try', async () => {
		rpc.mockResolvedValueOnce({ error: null, status: 204 });
		expect(await run()).toEqual({ ok: true });
		expect(rpc).toHaveBeenCalledTimes(1);
	});

	it('retries a network failure and then succeeds', async () => {
		rpc
			.mockResolvedValueOnce({
				error: { message: 'TypeError: Failed to fetch', code: '' },
				status: 0
			})
			.mockResolvedValueOnce({ error: null, status: 204 });
		expect(await run()).toEqual({ ok: true });
		expect(rpc).toHaveBeenCalledTimes(2);
	});

	it('retries a thrown fetch error', async () => {
		rpc
			.mockRejectedValueOnce(new Error('offline'))
			.mockResolvedValueOnce({ error: null, status: 204 });
		expect(await run()).toEqual({ ok: true });
	});

	it('refreshes the session on an expired JWT and retries', async () => {
		rpc
			.mockResolvedValueOnce({ error: { message: 'JWT expired', code: 'PGRST301' }, status: 401 })
			.mockResolvedValueOnce({ error: null, status: 204 });
		expect(await run()).toEqual({ ok: true });
		expect(refreshSession).toHaveBeenCalledTimes(1);
	});

	it('does not retry a deterministic database rejection and reports its code', async () => {
		rpc.mockResolvedValue({ error: { message: 'not a POTD', code: 'P0001' }, status: 400 });
		expect(await run()).toEqual({ ok: false, code: 'P0001' });
		expect(rpc).toHaveBeenCalledTimes(1);
	});

	it('gives up after three transient failures', async () => {
		rpc.mockResolvedValue({ error: { message: 'bad gateway', code: '' }, status: 502 });
		expect(await run()).toEqual({ ok: false, code: null });
		expect(rpc).toHaveBeenCalledTimes(3);
	});
});
