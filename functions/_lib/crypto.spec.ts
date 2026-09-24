import { describe, it, expect } from 'vitest';
import { decryptToken, encryptToken, signState, verifyState } from './crypto';

describe('OAuth state', () => {
	it('round-trips the user id', async () => {
		const state = await signState('user-1', 'secret');
		expect(await verifyState(state, 'secret')).toBe('user-1');
	});

	it('rejects a state signed with another secret', async () => {
		const state = await signState('user-1', 'secret');
		expect(await verifyState(state, 'other')).toBeNull();
	});

	it('rejects a tampered payload', async () => {
		const state = await signState('user-1', 'secret');
		const forged = `${btoa(JSON.stringify({ u: 'user-2', e: Date.now() + 60000 }))}.${state.split('.')[1]}`;
		expect(await verifyState(forged, 'secret')).toBeNull();
	});

	it('rejects an expired state', async () => {
		const state = await signState('user-1', 'secret', 1000);
		expect(await verifyState(state, 'secret', 1000 + 11 * 60 * 1000)).toBeNull();
	});

	it('rejects garbage', async () => {
		expect(await verifyState('nope', 'secret')).toBeNull();
	});
});

describe('token encryption', () => {
	it('round-trips a token', async () => {
		const stored = await encryptToken('gho_abc123', 'secret');
		expect(stored).not.toContain('gho_abc123');
		expect(await decryptToken(stored, 'secret')).toBe('gho_abc123');
	});

	it('fails to decrypt with the wrong secret', async () => {
		const stored = await encryptToken('gho_abc123', 'secret');
		expect(await decryptToken(stored, 'other')).toBeNull();
	});
});
