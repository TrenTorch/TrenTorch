import { describe, expect, it, vi } from 'vitest';
import { trackEvent } from './google-tag';

describe('trackEvent', () => {
	it('does nothing when there is no window', () => {
		expect(() => trackEvent('submit_solution', { question_id: 'x', passed: true })).not.toThrow();
	});

	it('forwards the event to gtag when the tag is present', () => {
		const gtag = vi.fn();
		vi.stubGlobal('window', { gtag });
		trackEvent('submit_solution', { question_id: 'x', passed: true });
		expect(gtag).toHaveBeenCalledWith('event', 'submit_solution', {
			question_id: 'x',
			passed: true
		});
		vi.unstubAllGlobals();
	});
});
