import { describe, expect, it } from 'vitest';
import { injectHead, PROFILE_PATH_PATTERN, profileHead } from './profile-page';

const profile = {
	username: 'ada_l',
	display_name: 'Ada <b>L</b>',
	bio: '"><script>alert(1)</script>',
	solved_count: '12'
};

describe('profileHead', () => {
	const head = profileHead(profile, 'https://trentorch.com');

	it('escapes user text', () => {
		expect(head).not.toContain('<script>');
		expect(head).not.toContain('<b>L</b>');
	});
	it('sets the canonical url', () => {
		expect(head).toContain('href="https://trentorch.com/accounts/@ada_l"');
	});
	it('falls back to a solved count description', () => {
		expect(profileHead({ ...profile, bio: null }, 'https://x.y')).toContain('solved 12 questions');
	});
});

describe('injectHead', () => {
	it('replaces the shell title and og tags', () => {
		const shell =
			'<head><title>Old</title><meta property="og:title" content="Old"><link rel="canonical" href="/"></head>';
		const out = injectHead(shell, '<title>New</title>');
		expect(out).not.toContain('Old');
		expect(out).toContain('<title>New</title>');
	});
});

describe('PROFILE_PATH_PATTERN', () => {
	it('accepts @username only', () => {
		expect(PROFILE_PATH_PATTERN.test('@ada_l')).toBe(true);
		expect(PROFILE_PATH_PATTERN.test('ada_l')).toBe(false);
		expect(PROFILE_PATH_PATTERN.test('@a')).toBe(false);
	});
});
