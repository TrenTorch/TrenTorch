import { afterEach, describe, expect, it, vi } from 'vitest';
import { copyText } from './copy-text';

afterEach(() => vi.unstubAllGlobals());

describe('copyText', () => {
	it('uses the async clipboard when available', async () => {
		const writeText = vi.fn().mockResolvedValue(undefined);
		vi.stubGlobal('navigator', { clipboard: { writeText } });
		expect(await copyText('https://example.com/accounts/@a')).toBe(true);
		expect(writeText).toHaveBeenCalledWith('https://example.com/accounts/@a');
	});

	it('reports failure when the clipboard rejects and there is no DOM fallback', async () => {
		vi.stubGlobal('navigator', {
			clipboard: { writeText: vi.fn().mockRejectedValue(new Error('denied')) }
		});
		vi.stubGlobal('document', undefined);
		expect(await copyText('x')).toBe(false);
	});

	it('does not throw when the clipboard API is missing', async () => {
		vi.stubGlobal('navigator', {});
		vi.stubGlobal('document', undefined);
		expect(await copyText('x')).toBe(false);
	});

	it('copies nothing for empty text', async () => {
		expect(await copyText('')).toBe(false);
	});
});
