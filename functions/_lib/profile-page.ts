export interface PublicProfile {
	username: string;
	display_name: string | null;
	bio: string | null;
	solved_count: number | string | null;
}

export const PROFILE_PATH_PATTERN = /^@([a-z0-9_]{3,20})$/;

export const escapeHtml = (value: string): string =>
	value.replace(/[&<>"']/g, (ch) => `&#${ch.charCodeAt(0)};`);

// Link-preview tags for a shared profile. The page itself is the normal app,
// which reads the rest of the profile from the database in the browser.
export function profileHead(profile: PublicProfile, origin: string): string {
	const name = profile.display_name?.trim() || `@${profile.username}`;
	const title = `${name} (@${profile.username}) | TrenTorch`;
	const solved = Number(profile.solved_count ?? 0);
	const description = profile.bio?.trim() || `${name} has solved ${solved} questions on TrenTorch.`;
	const url = `${origin}/accounts/@${profile.username}`;
	return [
		`<title>${escapeHtml(title)}</title>`,
		`<meta name="description" content="${escapeHtml(description)}">`,
		`<link rel="canonical" href="${escapeHtml(url)}">`,
		`<meta property="og:type" content="profile">`,
		`<meta property="og:title" content="${escapeHtml(title)}">`,
		`<meta property="og:description" content="${escapeHtml(description)}">`,
		`<meta property="og:url" content="${escapeHtml(url)}">`,
		`<meta name="twitter:card" content="summary">`,
		`<meta name="twitter:title" content="${escapeHtml(title)}">`,
		`<meta name="twitter:description" content="${escapeHtml(description)}">`
	].join('\n');
}

// Drops the shell's own title/description/canonical/og/twitter tags, then adds ours.
export function injectHead(shell: string, head: string): string {
	const stripped = shell
		.replace(/<title>[\s\S]*?<\/title>/i, '')
		.replace(
			/<(?:meta|link)\b[^>]*(?:name="(?:description|twitter:[^"]*)"|property="og:[^"]*"|rel="canonical")[^>]*>/gi,
			''
		);
	return stripped.replace(/<\/head>/i, () => `${head}\n</head>`);
}
