import { getSupabaseClient } from '$processes/auth/supabase-client';
import type { ProfileForm } from './validate-profile';

const COLUMNS =
	'display_name, username, organization, job_title, alt_email, bio, location, x_url, linkedin_url, scholar_url, github_url, website_url, is_public';

type Row = Record<string, string | boolean | null>;

const text = (value: string | boolean | null | undefined) =>
	typeof value === 'string' ? value : '';

const signal = () => AbortSignal.timeout(15_000);

export type SaveResult = { ok: true } | { ok: false; field?: keyof ProfileForm; message: string };

export async function loadProfile(userId: string): Promise<ProfileForm | null> {
	const { data, error } = await getSupabaseClient()
		.from('profiles')
		.select(COLUMNS)
		.eq('id', userId)
		.abortSignal(signal())
		.maybeSingle();
	if (error) {
		console.error('Failed to load profile', error);
		return null;
	}
	const row = (data ?? {}) as Row;
	return {
		displayName: text(row.display_name),
		username: text(row.username),
		organization: text(row.organization),
		jobTitle: text(row.job_title),
		altEmail: text(row.alt_email),
		bio: text(row.bio),
		location: text(row.location),
		xUrl: text(row.x_url),
		linkedinUrl: text(row.linkedin_url),
		scholarUrl: text(row.scholar_url),
		githubUrl: text(row.github_url),
		websiteUrl: text(row.website_url),
		isPublic: row.is_public === true
	};
}

// Empty strings are stored as null so the unique username index and the
// https-only link checks in the database only ever see real values.
const orNull = (value: string) => (value === '' ? null : value);

export async function saveProfile(userId: string, form: ProfileForm): Promise<SaveResult> {
	const { data, error } = await getSupabaseClient()
		.from('profiles')
		.update({
			display_name: orNull(form.displayName),
			username: orNull(form.username),
			organization: orNull(form.organization),
			job_title: orNull(form.jobTitle),
			alt_email: orNull(form.altEmail),
			bio: orNull(form.bio),
			location: orNull(form.location),
			x_url: orNull(form.xUrl),
			linkedin_url: orNull(form.linkedinUrl),
			scholar_url: orNull(form.scholarUrl),
			github_url: orNull(form.githubUrl),
			website_url: orNull(form.websiteUrl),
			is_public: form.isPublic
		})
		.eq('id', userId)
		.select('id')
		.abortSignal(signal());
	// An update that matches no row is not an error to Postgres, but nothing was saved.
	if (!error && data && data.length > 0) return { ok: true };
	if (!error) {
		return {
			ok: false,
			message: 'Your profile could not be found. Sign out, sign in and try again.'
		};
	}
	if (error.code === '23514') {
		return {
			ok: false,
			message: 'One of the fields is not in an accepted format. Check the links and lengths.'
		};
	}
	if (error.code === '23505') {
		return { ok: false, field: 'username', message: 'That username is taken. Try another.' };
	}
	console.error('Failed to save profile', error);
	return { ok: false, message: 'Could not save your profile. Please try again.' };
}
