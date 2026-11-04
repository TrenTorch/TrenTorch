import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { dsaQuestions } from '$data/dsa-sheet';
import { readPaperTopics } from '$processes/papers/read-papers';
import { buildHomePreviews } from '$processes/potd/home-preview';
import { istDateString } from '$processes/potd/ist-date-string';
import type { PageServerLoad } from './$types';

const DAY_MS = 24 * 60 * 60 * 1000;

// Runs at build time (the page is prerendered) and its result is written into the page, so the browser gets
// the few fields the home page's code window shows for each day and never the curriculum. Which day counts as
// "today" is decided in the browser from the visitor's own clock; `buildDay` is what the prerendered page is
// drawn for until then. Days from two days back on are kept, so a page that is a little old still has today.
export const load: PageServerLoad = () => {
	const now = new Date();
	// For the two cards the minimised preview makes room for: no more than a count and a title each.
	const papers = readPaperTopics().flatMap((topic) => topic.papers);
	const newest = papers.reduce<(typeof papers)[number] | null>(
		(best, paper) => (!best || paper.year >= best.year ? paper : best),
		null
	);
	return {
		dsaTotal: dsaQuestions.length,
		latestPaper: newest ? { title: newest.title, year: newest.year } : null,
		buildDay: istDateString(now),
		potdPreviews: buildHomePreviews(
			potdEntries,
			(id) => questionsById.get(id),
			istDateString(new Date(now.getTime() - 2 * DAY_MS))
		)
	};
};
