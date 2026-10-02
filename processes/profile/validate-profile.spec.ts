import { describe, it, expect } from 'vitest';
import { normalizeLink, validateProfile, type ProfileForm } from './validate-profile';

const empty: ProfileForm = {
	displayName: '',
	username: '',
	organization: '',
	jobTitle: '',
	altEmail: '',
	bio: '',
	location: '',
	xUrl: '',
	linkedinUrl: '',
	scholarUrl: '',
	githubUrl: '',
	websiteUrl: '',
	isPublic: false
};

describe('normalizeLink', () => {
	it('expands handles for X, LinkedIn and GitHub', () => {
		expect(normalizeLink('x', '@rocky')).toBe('https://x.com/rocky');
		expect(normalizeLink('linkedin', 'rocky-t')).toBe('https://www.linkedin.com/in/rocky-t');
		expect(normalizeLink('github', 'rocky')).toBe('https://github.com/rocky');
	});

	it('accepts full urls and adds https when it is missing', () => {
		expect(normalizeLink('x', 'twitter.com/rocky')).toBe('https://twitter.com/rocky');
		expect(normalizeLink('scholar', 'https://scholar.google.com/citations?user=abc')).toBe(
			'https://scholar.google.com/citations?user=abc'
		);
	});

	it('rejects the wrong site and non-web schemes', () => {
		expect(normalizeLink('x', 'https://evil.com/rocky')).toBeNull();
		expect(normalizeLink('linkedin', 'javascript:alert(1)')).toBeNull();
		expect(normalizeLink('scholar', 'rocky')).toBeNull();
	});

	it('returns an empty string for empty input', () => {
		expect(normalizeLink('website', '   ')).toBe('');
	});
});

describe('validateProfile', () => {
	it('lowercases and accepts a good username', () => {
		const { errors, clean } = validateProfile({ ...empty, username: ' Rocky_07 ' });
		expect(errors.username).toBeUndefined();
		expect(clean.username).toBe('rocky_07');
	});

	it('rejects short, long and odd usernames', () => {
		for (const username of ['ab', 'a'.repeat(21), 'no spaces', 'dash-ed']) {
			expect(validateProfile({ ...empty, username }).errors.username).toBeDefined();
		}
	});

	it('flags a bad alternate email and an overlong bio', () => {
		const { errors } = validateProfile({ ...empty, altEmail: 'nope', bio: 'x'.repeat(281) });
		expect(errors.altEmail).toBeDefined();
		expect(errors.bio).toBeDefined();
	});

	it('passes an entirely empty form', () => {
		expect(validateProfile(empty).errors).toEqual({});
	});
});
