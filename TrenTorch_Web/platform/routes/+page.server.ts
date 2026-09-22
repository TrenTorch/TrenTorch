import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { toPotdSummary } from '$processes/potd/potd-summary';
import type { PageServerLoad } from './$types';

// Same reasoning as platform/routes/potd/+page.server.ts: the homepage's
// "Today's Problem" banner needs only the few fields a PotdSummary carries,
// not the full curriculum, and which entry is "today" is still resolved
// client-side from the visitor's own date (see get-todays-potd.ts).
export const load: PageServerLoad = () => ({
	potdSummaries: potdEntries.flatMap((entry) => {
		const question = questionsById.get(entry.questionId);
		return question ? [toPotdSummary(question)] : [];
	})
});
