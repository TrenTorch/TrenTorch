import { error } from '@sveltejs/kit';
import { chapterMetaLine, listCudaChapters, renderCudaChapter } from '$processes/cuda/read-course';
import type { EntryGenerator, PageServerLoad } from './$types';

export const prerender = true;

export const entries: EntryGenerator = () =>
	listCudaChapters().map(({ step }) => ({ chapter: step }));

export const load: PageServerLoad = ({ params }) => {
	const chapters = listCudaChapters();
	const index = chapters.findIndex((c) => c.step === params.chapter);
	if (index < 0) error(404, 'Chapter not found');
	const pick = (c?: (typeof chapters)[number]) =>
		c ? { step: c.step, id: c.id, title: c.title } : null;
	return {
		theory: renderCudaChapter(chapters[index]),
		chapter: pick(chapters[index]),
		meta: chapterMetaLine(chapters[index]),
		prev: pick(chapters[index - 1]),
		next: pick(chapters[index + 1])
	};
};
