import { cudaListEntries } from '$processes/cuda/cuda-course-index';
import { listCudaChapters } from '$processes/cuda/read-course';
import type { PageServerLoad } from './$types';

export const prerender = true;

export const load: PageServerLoad = () => ({
	problems: cudaListEntries(),
	chapters: listCudaChapters().map(({ step, id, title, part, estMinutes }) => ({
		step,
		id,
		title,
		part,
		estMinutes
	}))
});
