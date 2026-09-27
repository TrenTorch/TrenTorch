import { normalizeUsername, type ProfileForm } from './validate-profile';

type AccountInfo = {
	app_metadata?: Record<string, unknown>;
	user_metadata?: Record<string, unknown>;
};

const str = (value: unknown) => (typeof value === 'string' ? value.trim() : '');

// Suggests values for empty profile fields from what Google or GitHub shared
// at sign-in. Never overwrites a field the person already filled.
export function prefillFromAccount(
	form: ProfileForm,
	user: AccountInfo
): { form: ProfileForm; filled: boolean } {
	const meta = user.user_metadata ?? {};
	const suggestions: Partial<ProfileForm> = {
		displayName: str(meta.full_name) || str(meta.name)
	};
	if (user.app_metadata?.provider === 'github') {
		const handle = str(meta.user_name) || str(meta.preferred_username);
		if (/^[A-Za-z0-9-]{1,39}$/.test(handle)) {
			suggestions.githubUrl = `https://github.com/${handle}`;
		}
		const username = normalizeUsername(handle.replace(/-/g, '_'));
		if (/^[a-z0-9_]{3,20}$/.test(username)) suggestions.username = username;
	}
	const next = { ...form };
	let filled = false;
	for (const [key, value] of Object.entries(suggestions) as [keyof ProfileForm, string][]) {
		if (value && next[key] === '') {
			(next[key] as string) = value;
			filled = true;
		}
	}
	return { form: next, filled };
}
