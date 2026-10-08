import { readPaperTopics } from '$processes/papers/read-papers';
import type { PageServerLoad } from './$types';

// Runs at build time (the page is prerendered). The papers are read from the folders under
// data/app_data/12-research-papers, so adding one needs no code change.
export const load: PageServerLoad = () => ({ topics: readPaperTopics() });
