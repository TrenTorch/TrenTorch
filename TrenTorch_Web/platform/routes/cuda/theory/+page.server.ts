import { listCudaChapters } from '$processes/cuda/read-course';
import type { PageServerLoad } from './$types';

export const prerender = true;

export const load: PageServerLoad = () => ({
	chapters: listCudaChapters().map(({ step, id, part, title, estMinutes, pmpp }) => ({
		step,
		id,
		part,
		title,
		estMinutes,
		pmpp
	}))
});
