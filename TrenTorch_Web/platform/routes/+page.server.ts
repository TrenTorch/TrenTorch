import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { buildHomePreviews } from '$processes/potd/home-preview';
import { localDateString } from '$processes/potd/local-date-string';
import type { PageServerLoad } from './$types';

const DAY_MS = 24 * 60 * 60 * 1000;

// Runs at build time (the page is prerendered) and its result is written into the page, so the browser gets
// the few fields the home page's code window shows for each day and never the curriculum. Which day counts as
// "today" is decided in the browser from the visitor's own clock; `buildDay` is what the prerendered page is
// drawn for until then. Days from two days back on are kept, so a page that is a little old still has today.
export const load: PageServerLoad = () => {
	const now = new Date();
	return {
		buildDay: localDateString(now),
		potdPreviews: buildHomePreviews(
			potdEntries,
			(id) => questionsById.get(id),
			localDateString(new Date(now.getTime() - 2 * DAY_MS))
		)
	};
};
