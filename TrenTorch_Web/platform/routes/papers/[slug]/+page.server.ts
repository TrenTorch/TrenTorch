import { error } from '@sveltejs/kit';
import { readPapers } from '$processes/papers/read-papers';
import type { EntryGenerator, PageServerLoad } from './$types';

export const prerender = true;

// One prerendered page per paper folder; a new paper gets its page automatically.
export const entries: EntryGenerator = () => readPapers().map((paper) => ({ slug: paper.slug }));

export const load: PageServerLoad = ({ params }) => {
	const paper = readPapers().find((p) => p.slug === params.slug);
	if (!paper) error(404, 'Paper not found');
	return { paper };
};
