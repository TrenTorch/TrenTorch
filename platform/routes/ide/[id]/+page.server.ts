import { loadIdeContent } from '$processes/ide-content/load-ide-content';
import { getAdjacentQuestionIds } from '$processes/ide-content/get-adjacent-question-ids';
import { curriculum } from '$data/questions';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { buildQuestionSeo } from '$processes/seo/build-question-seo';
import type { EntryGenerator, PageServerLoad } from './$types';

// Prerendered: every /ide/<slug> page is a static file, not a serverless
// render, so there is nothing to do per-request -- the editor, Pyodide,
// run/submit and progress are all client-side. What a user pulls is plain CDN
// egress of an immutable file.
export const prerender = true;

// Prerender a page for every question slug in the curriculum, not just the
// handful that have authored content yet -- the rest legitimately render
// the "not published yet" state and should still be static. Slugs beyond
// this list 404 at the edge (no function), which is correct.
export const entries: EntryGenerator = () => {
	const ids = new Set<string>();
	for (const part of curriculum)
		for (const track of part.tracks) for (const q of track.questions) ids.add(q.slug);
	// Every authored question too: a Problem of the Day is deliberately not
	// in the curriculum listing above, so without this its page would only
	// exist if the prerender crawler happened to find a link to it.
	for (const id of questionsById.keys()) ids.add(id);
	return [...ids].map((id) => ({ id }));
};

// A server load, not a universal one, on purpose. A universal load runs again
// in the browser, which forced the whole curriculum (about 4 MB of every
// question's text, starter code, solution and tests) into the JavaScript every
// visitor downloads. A server load runs once at build time; SvelteKit writes
// its result into this page's HTML and into a small static __data.json for
// in-app navigation, so a visitor downloads only the question they open.
export const load: PageServerLoad = async ({ params }) => {
	const content = await loadIdeContent(params.id);
	const { prevId, nextId } = getAdjacentQuestionIds(params.id);
	// Built here, once, at build time. Crawlers read the prerendered HTML, so this
	// is what they see; building it in the browser as well would put the whole
	// curriculum back into the JavaScript.
	const seo = buildQuestionSeo(params.id);
	// Not every question has a CompanyTag (see data/questions.ts's COMPANY_TAGS);
	// most legitimately have none. Looked up here, at build time, so the badge is
	// part of the prerendered HTML and the browser needs no company data.
	let companies;
	for (const part of curriculum) {
		for (const track of part.tracks) {
			const question = track.questions.find((q) => q.slug === params.id);
			if (question) {
				companies = question.companies;
				break;
			}
		}
		if (companies) break;
	}
	return { content, id: params.id, prevId, nextId, seo, companies };
};
