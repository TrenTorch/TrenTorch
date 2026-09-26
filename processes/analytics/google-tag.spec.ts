import { describe, expect, it } from 'vitest';
import { analyticsEnabled, loadGoogleTag, trackEvent, trackPageView } from './google-tag';

describe('google tag', () => {
	it('is disabled outside a production build with an ID, and every call is a no-op', () => {
		expect(analyticsEnabled()).toBe(false);
		expect(() => {
			loadGoogleTag();
			trackPageView('/questions');
			trackEvent('submit_solution', { question_id: 'x', passed: true });
		}).not.toThrow();
	});
});
