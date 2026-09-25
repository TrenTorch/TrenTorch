import { getSupabaseClient } from '$processes/auth/supabase-client';
import type { ProfileForm } from './validate-profile';

export type ViewedProfile = {
	id: string;
	profile: ProfileForm;
	avatarUrl: string | null;
	rating: number | null;
};

type Row = Record<string, string | number | null>;

const text = (value: string | number | null | undefined) =>
	typeof value === 'string' ? value : '';

// Only http(s) links are kept, so a stored `javascript:` value can never become an href.
const link = (value: string | number | null | undefined) => {
	const raw = text(value);
	try {
		const { protocol } = new URL(raw);
		return protocol === 'https:' || protocol === 'http:' ? raw : '';
	} catch {
		return '';
	}
};

// Looks a public profile up by username. Returns null when it does not exist or
// is private (the database function only answers for public profiles), and
// undefined when the lookup itself failed.
export async function fetchPublicProfile(
	username: string
): Promise<ViewedProfile | null | undefined> {
	const { data, error } = await getSupabaseClient()
		.rpc('get_public_profile', { p_username: username })
		.abortSignal(AbortSignal.timeout(15_000));
	if (error) {
		console.error('Failed to load public profile', error);
		return undefined;
	}
	const row = ((data as Row[] | null) ?? [])[0];
	if (!row) return null;
	return {
		id: String(row.id),
		avatarUrl: link(row.avatar_url) || null,
		rating: typeof row.user_rating === 'number' ? row.user_rating : null,
		profile: {
			displayName: text(row.display_name),
			username: text(row.username),
			organization: text(row.organization),
			jobTitle: text(row.job_title),
			altEmail: '',
			bio: text(row.bio),
			location: text(row.location),
			xUrl: link(row.x_url),
			linkedinUrl: link(row.linkedin_url),
			scholarUrl: link(row.scholar_url),
			githubUrl: link(row.github_url),
			websiteUrl: link(row.website_url),
			isPublic: true
		}
	};
}
