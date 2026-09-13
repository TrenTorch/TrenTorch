import { loadIdeContent } from '$lib/content/ideContent';
import { curriculum } from '$lib/data/questions';
import type { EntryGenerator, PageLoad } from './$types';

// Prerendered: every /ide/<slug> page is a static file, not a serverless
// render. `content` comes straight from the compiled curriculum JSON (no
// request, no cookies), so there is nothing to do per-request -- the
// editor, Pyodide, run/submit and progress are all client-side. This
// removes function invocations (compute + their bandwidth tier) entirely;
// what a user pulls is plain CDN egress of an immutable file.
export const prerender = true;

// Prerender a page for every question slug in the curriculum, not just the
// handful that have authored content yet -- the rest legitimately render
// the "not published yet" state and should still be static. Slugs beyond
// this list 404 at the edge (no function), which is correct.
export const entries: EntryGenerator = () => {
	const ids = new Set<string>();
	for (const part of curriculum)
		for (const track of part.tracks) for (const q of track.questions) ids.add(q.slug);
	return [...ids].map((id) => ({ id }));
};

export const load: PageLoad = async ({ params }) => {
	const content = await loadIdeContent(params.id);
	return { content, id: params.id };
};
