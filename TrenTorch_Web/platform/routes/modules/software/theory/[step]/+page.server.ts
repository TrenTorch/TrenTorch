import { error } from '@sveltejs/kit';
import { listTheorySteps, renderTheory } from '$processes/dsa-theory/read-theory';
import type { EntryGenerator, PageServerLoad } from './$types';

export const prerender = true;

// One prerendered page per step folder that has a theory.md.
export const entries: EntryGenerator = () => listTheorySteps().map(({ step }) => ({ step }));

export const load: PageServerLoad = ({ params }) => {
	const step = listTheorySteps().find((s) => s.step === params.step);
	if (!step) error(404, 'Theory not found');
	return { theory: renderTheory(step) };
};
