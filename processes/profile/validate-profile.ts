export type ProfileForm = {
	displayName: string;
	username: string;
	organization: string;
	jobTitle: string;
	altEmail: string;
	bio: string;
	location: string;
	xUrl: string;
	linkedinUrl: string;
	scholarUrl: string;
	githubUrl: string;
	websiteUrl: string;
	isPublic: boolean;
};

export type ProfileErrors = Partial<Record<keyof ProfileForm, string>>;

export const LIMITS = {
	displayName: 80,
	organization: 100,
	jobTitle: 80,
	bio: 280,
	location: 80
} as const;

const USERNAME_RE = /^[a-z0-9_]{3,20}$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type LinkKind = 'x' | 'linkedin' | 'scholar' | 'github' | 'website';

const HOSTS: Record<LinkKind, RegExp> = {
	x: /^(www\.)?(x|twitter)\.com$/,
	linkedin: /^([a-z]{2,3}\.)?linkedin\.com$/,
	scholar: /^scholar\.google\.[a-z.]+$/,
	github: /^(www\.)?github\.com$/,
	website: /.+\..+/
};

// A bare handle is only expanded for the sites where that is unambiguous.
const HANDLE_BASE: Partial<Record<LinkKind, string>> = {
	x: 'https://x.com/',
	linkedin: 'https://www.linkedin.com/in/',
	github: 'https://github.com/'
};

const SITE_NAMES: Record<LinkKind, string> = {
	x: 'X',
	linkedin: 'LinkedIn',
	scholar: 'Google Scholar',
	github: 'GitHub',
	website: 'website'
};

export function normalizeUsername(input: string): string {
	return input.trim().toLowerCase();
}

/** Returns the canonical https URL, '' for empty input, or null when invalid. */
export function normalizeLink(kind: LinkKind, input: string): string | null {
	const raw = input.trim();
	if (!raw) return '';
	const base = HANDLE_BASE[kind];
	if (base && /^@?[A-Za-z0-9_.-]+$/.test(raw)) return base + raw.replace(/^@/, '');
	let url: URL;
	try {
		url = new URL(/^https?:\/\//i.test(raw) ? raw : `https://${raw}`);
	} catch {
		return null;
	}
	if (url.protocol !== 'https:' && !(kind === 'website' && url.protocol === 'http:')) return null;
	if (!HOSTS[kind].test(url.hostname.toLowerCase())) return null;
	return url.toString().replace(/\/$/, '');
}

export function validateProfile(form: ProfileForm): {
	errors: ProfileErrors;
	clean: ProfileForm;
} {
	const errors: ProfileErrors = {};
	const clean: ProfileForm = {
		displayName: form.displayName.trim(),
		username: normalizeUsername(form.username),
		organization: form.organization.trim(),
		jobTitle: form.jobTitle.trim(),
		altEmail: form.altEmail.trim(),
		bio: form.bio.trim(),
		location: form.location.trim(),
		xUrl: '',
		linkedinUrl: '',
		scholarUrl: '',
		githubUrl: '',
		websiteUrl: '',
		isPublic: form.isPublic
	};

	for (const key of ['displayName', 'organization', 'jobTitle', 'bio', 'location'] as const) {
		if (clean[key].length > LIMITS[key]) errors[key] = `Keep this under ${LIMITS[key]} characters.`;
	}
	if (clean.username && !USERNAME_RE.test(clean.username)) {
		errors.username = 'Use 3 to 20 letters, numbers or underscores.';
	}
	if (clean.isPublic && !clean.username) {
		errors.username = 'Choose a username to make your profile public.';
	}
	if (clean.altEmail && !EMAIL_RE.test(clean.altEmail)) {
		errors.altEmail = 'Enter a valid email address.';
	}

	const links = [
		['xUrl', 'x'],
		['linkedinUrl', 'linkedin'],
		['scholarUrl', 'scholar'],
		['githubUrl', 'github'],
		['websiteUrl', 'website']
	] as const;
	for (const [field, kind] of links) {
		const value = normalizeLink(kind, form[field]);
		if (value === null) errors[field] = `Enter a valid ${SITE_NAMES[kind]} link.`;
		else clean[field] = value;
	}
	return { errors, clean };
}
