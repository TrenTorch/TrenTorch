import { cudaListEntries } from '$processes/cuda/cuda-course-index';
import type { PageServerLoad } from './$types';

export const prerender = true;

export const load: PageServerLoad = () => ({ problems: cudaListEntries() });
