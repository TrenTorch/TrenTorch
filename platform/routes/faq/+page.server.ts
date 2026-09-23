import { questionsById } from '$processes/ide-content/curriculum-index';
import type { PageServerLoad } from './$types';

// The FAQ quotes how many questions there are. Counting them here, at build
// time, keeps the curriculum out of the browser's JavaScript.
export const load: PageServerLoad = () => ({ questionCount: questionsById.size });
