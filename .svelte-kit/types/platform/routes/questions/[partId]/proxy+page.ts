// @ts-nocheck
import { error } from '@sveltejs/kit';
import { curriculum } from '$data/questions';
import type { EntryGenerator, PageLoad } from './$types';

// Prerendered: the curriculum's Part list is fixed at build time (same
// compiled data +page.svelte's siblings already use), so there is nothing
// to fetch per-request -- a real 404 for anything outside it, computed at
// build time rather than left as a client-side "not found" state.
export const prerender = true;

export const entries: EntryGenerator = () => curriculum.map((part) => ({ partId: part.id }));

export const load = ({ params }: Parameters<PageLoad>[0]) => {
	const part = curriculum.find((p) => p.id === params.partId);
	if (!part) error(404, 'Track not found');
	return { part };
};
