import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { toPotdSummary } from '$processes/potd/potd-summary';
import type { PageServerLoad } from './$types';

// Runs at build time (the page is prerendered) and its result is written into
// the page, so the browser gets the few fields the POTD list shows and never
// the curriculum. Which entry counts as "today" is still decided in the
// browser, from the visitor's own date; see get-potd-part.ts.
export const load: PageServerLoad = () => ({
	potdSummaries: potdEntries.flatMap((entry) => {
		const question = questionsById.get(entry.questionId);
		return question ? [toPotdSummary(question)] : [];
	})
});
