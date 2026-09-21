import { describe, it, expect, vi, afterEach } from 'vitest';
import { signInSkipped } from './preview-mode';

afterEach(() => vi.unstubAllEnvs());

describe('signInSkipped', () => {
	it('is off unless the preview flag is set, so production never skips sign-in', () => {
		expect(signInSkipped()).toBe(false);
	});

	it('is on only for the exact value 1', () => {
		vi.stubEnv('VITE_PREVIEW_SKIP_SIGN_IN', '1');
		expect(signInSkipped()).toBe(true);
		for (const other of ['0', 'true', '', 'yes']) {
			vi.stubEnv('VITE_PREVIEW_SKIP_SIGN_IN', other);
			expect(signInSkipped()).toBe(false);
		}
	});
});
