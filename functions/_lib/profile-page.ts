export interface PublicProfile {
	username: string;
	display_name: string | null;
	avatar_url: string | null;
	organization: string | null;
	job_title: string | null;
	bio: string | null;
	location: string | null;
	x_url: string | null;
	linkedin_url: string | null;
	scholar_url: string | null;
	github_url: string | null;
	website_url: string | null;
	user_rating: number | null;
	solved_count: number | string | null;
}

export const PROFILE_PATH_PATTERN = /^@([a-z0-9_]{3,20})$/;

export const escapeHtml = (value: string): string =>
	value.replace(/[&<>"']/g, (ch) => `&#${ch.charCodeAt(0)};`);

// Only http(s) URLs become links, so a stored `javascript:` value can never render.
const safeUrl = (value: string | null): string | null => {
	if (!value) return null;
	try {
		const url = new URL(value);
		return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : null;
	} catch {
		return null;
	}
};

const LINKS: [keyof PublicProfile, string][] = [
	['website_url', 'Website'],
	['github_url', 'GitHub'],
	['x_url', 'X'],
	['linkedin_url', 'LinkedIn'],
	['scholar_url', 'Scholar']
];

const STYLE = `
:root{color-scheme:light dark;--bg:#fafaf9;--fg:#111;--muted:#666;--line:#111}
@media(prefers-color-scheme:dark){:root{--bg:#0b0b0b;--fg:#f2f2f2;--muted:#9a9a9a;--line:#f2f2f2}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 ui-sans-serif,system-ui,sans-serif}
main{max-width:34rem;margin:0 auto;padding:4rem 1rem}
.card{border:1px solid var(--line);border-radius:1rem;padding:1.5rem}
.top{display:flex;gap:1rem;align-items:center}
.avatar{width:4.5rem;height:4.5rem;border-radius:50%;object-fit:cover;border:1px solid var(--line);
display:flex;align-items:center;justify-content:center;font:600 1.5rem ui-monospace,monospace}
h1{margin:0;font:600 1.4rem ui-monospace,monospace;overflow-wrap:anywhere}
.muted{color:var(--muted);margin:0;font-size:.9rem}
.bio{margin:1.25rem 0 0;overflow-wrap:anywhere}
.stats{display:flex;gap:2rem;margin:1.25rem 0 0;font-family:ui-monospace,monospace}
.stats b{display:block;font-size:1.4rem}
.links{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.25rem 0 0;padding:0;list-style:none}
.links a{color:var(--fg);border:1px solid var(--line);border-radius:.75rem;padding:.25rem .75rem;font-size:.85rem;text-decoration:none}
.links a:hover{text-decoration:underline}
footer{margin-top:1.5rem;text-align:center;font-size:.85rem}
footer a{color:var(--muted)}
`;

const shell = (
	title: string,
	description: string,
	canonical: string,
	body: string,
	noindex = false
) =>
	`<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(title)}</title>
<meta name="description" content="${escapeHtml(description)}">
<link rel="canonical" href="${escapeHtml(canonical)}">
${noindex ? '<meta name="robots" content="noindex">' : ''}
<meta property="og:site_name" content="TrenTorch">
<meta property="og:type" content="profile">
<meta property="og:title" content="${escapeHtml(title)}">
<meta property="og:description" content="${escapeHtml(description)}">
<meta property="og:url" content="${escapeHtml(canonical)}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="${escapeHtml(title)}">
<meta name="twitter:description" content="${escapeHtml(description)}">
<style>${STYLE}</style></head><body><main>${body}
<footer><a href="/">Build PyTorch by hand on TrenTorch</a></footer></main></body></html>`;

export function renderProfile(profile: PublicProfile, origin: string): string {
	const name = profile.display_name?.trim() || `@${profile.username}`;
	const role = [profile.job_title, profile.organization].filter(Boolean).join(' at ');
	const sub = [role, profile.location].filter(Boolean).join(' · ');
	const solved = Number(profile.solved_count ?? 0);
	const avatar = safeUrl(profile.avatar_url);
	const links = LINKS.flatMap(([key, label]) => {
		const href = safeUrl(profile[key] as string | null);
		return href
			? [
					`<li><a href="${escapeHtml(href)}" rel="noopener nofollow ugc" target="_blank">${label}</a></li>`
				]
			: [];
	});
	const description = profile.bio?.trim() || `${name} has solved ${solved} questions on TrenTorch.`;
	const body = `<div class="card"><div class="top">
${
	avatar
		? `<img class="avatar" src="${escapeHtml(avatar)}" alt="" referrerpolicy="no-referrer">`
		: `<div class="avatar" aria-hidden="true">${escapeHtml(name.replace(/^@/, '').charAt(0).toUpperCase())}</div>`
}
<div><h1>${escapeHtml(name)}</h1><p class="muted">@${escapeHtml(profile.username)}</p>${
		sub ? `<p class="muted">${escapeHtml(sub)}</p>` : ''
	}</div></div>
${profile.bio?.trim() ? `<p class="bio">${escapeHtml(profile.bio.trim())}</p>` : ''}
<div class="stats"><div><b>${solved}</b><span class="muted">solved</span></div>${
		profile.user_rating == null
			? ''
			: `<div><b>${escapeHtml(String(profile.user_rating))}</b><span class="muted">rating</span></div>`
	}</div>
${links.length ? `<ul class="links">${links.join('')}</ul>` : ''}</div>`;
	return shell(
		`${name} (@${profile.username}) | TrenTorch`,
		description,
		`${origin}/accounts/@${profile.username}`,
		body
	);
}

export const renderNotFound = (origin: string): string =>
	shell(
		'Profile not found | TrenTorch',
		'This profile does not exist or is private.',
		`${origin}/`,
		'<div class="card"><h1>Profile not found</h1><p class="muted">This profile does not exist or is private.</p></div>',
		true
	);
