import { error } from '@sveltejs/kit';
import { getPaper, papers } from '$data/papers';
import type { EntryGenerator, PageLoad } from './$types';

export const prerender = true;

export const entries: EntryGenerator = () => papers.map((paper) => ({ slug: paper.slug }));

export const load: PageLoad = ({ params }) => {
	const paper = getPaper(params.slug);
	if (!paper) error(404, 'Paper not found');
	return { paper };
};
