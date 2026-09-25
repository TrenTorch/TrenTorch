import { describe, expect, it } from 'vitest';
import { PROFILE_PATH_PATTERN, renderProfile, type PublicProfile } from './profile-page';

const base: PublicProfile = {
	username: 'ada_l',
	display_name: 'Ada <b>L</b>',
	avatar_url: null,
	organization: 'Analytical Engines',
	job_title: 'Engineer',
	bio: '"><script>alert(1)</script>',
	location: null,
	x_url: 'javascript:alert(1)',
	linkedin_url: null,
	scholar_url: null,
	github_url: 'https://github.com/ada',
	website_url: null,
	user_rating: 1500,
	solved_count: '12'
};

describe('renderProfile', () => {
	const html = renderProfile(base, 'https://trentorch.com');

	it('escapes user text', () => {
		expect(html).not.toContain('<script>alert');
		expect(html).not.toContain('<b>L</b>');
	});
	it('drops non-http links and keeps https ones', () => {
		expect(html).not.toContain('javascript:');
		expect(html).toContain('https://github.com/ada');
	});
	it('sets the canonical url and stats', () => {
		expect(html).toContain('https://trentorch.com/accounts/@ada_l');
		expect(html).toContain('<b>12</b>');
	});
});

describe('PROFILE_PATH_PATTERN', () => {
	it('accepts @username only', () => {
		expect(PROFILE_PATH_PATTERN.test('@ada_l')).toBe(true);
		expect(PROFILE_PATH_PATTERN.test('ada_l')).toBe(false);
		expect(PROFILE_PATH_PATTERN.test('@a')).toBe(false);
	});
});
