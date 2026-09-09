import { loadIdeContent } from '$lib/content/ideContent';
import type { PageLoad } from './$types';

// Most question ids don't have IDE content yet (Maanas authors it question
// by question as the curriculum lands), so a miss here is an expected,
// common state -- not an error page. The route renders it inline instead.
export const load: PageLoad = async ({ params }) => {
	const content = await loadIdeContent(params.id);
	return { content, id: params.id };
};
