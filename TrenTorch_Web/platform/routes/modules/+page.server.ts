import { cudaListEntries } from '$processes/cuda/cuda-course-index';
import { listCudaChapters } from '$processes/cuda/read-course';
import type { PageServerLoad } from './$types';

export const prerender = true;

// Only what the hub's GPU card needs: the problem ids (to count what is
// solved) and how many chapters there are.
export const load: PageServerLoad = () => ({
	cudaIds: cudaListEntries().map((entry) => entry.id),
	cudaChapters: listCudaChapters().length
});
