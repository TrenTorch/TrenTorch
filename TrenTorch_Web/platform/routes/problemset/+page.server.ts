import { loadPotdSummaries } from '$processes/potd/load-potd-summaries';
import type { PageServerLoad } from './$types';

// Feeds the Problem of the Day banner. Which entry is "today" is decided in the
// browser, from the visitor's own date.
export const load: PageServerLoad = () => ({ potdSummaries: loadPotdSummaries() });
