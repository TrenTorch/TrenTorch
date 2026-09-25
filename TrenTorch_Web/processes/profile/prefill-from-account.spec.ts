import { describe, it, expect } from 'vitest';
import { prefillFromAccount } from './prefill-from-account';
import type { ProfileForm } from './validate-profile';

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

describe('prefillFromAccount', () => {
	it('fills name from Google', () => {
		const r = prefillFromAccount(empty, {
			app_metadata: { provider: 'google' },
			user_metadata: { full_name: 'Ada Lovelace' }
		});
		expect(r.form.displayName).toBe('Ada Lovelace');
		expect(r.form.githubUrl).toBe('');
		expect(r.filled).toBe(true);
	});

	it('fills name, username and GitHub link from GitHub', () => {
		const r = prefillFromAccount(empty, {
			app_metadata: { provider: 'github' },
			user_metadata: { name: 'Rocky', user_name: 'Rocky-07' }
		});
		expect(r.form.username).toBe('rocky_07');
		expect(r.form.githubUrl).toBe('https://github.com/Rocky-07');
	});

	it('never overwrites filled fields', () => {
		const r = prefillFromAccount(
			{ ...empty, displayName: 'Mine' },
			{ app_metadata: { provider: 'google' }, user_metadata: { full_name: 'Other' } }
		);
		expect(r.form.displayName).toBe('Mine');
		expect(r.filled).toBe(false);
	});
});
