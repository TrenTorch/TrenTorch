import { curriculum } from '$data/questions';
import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { latestLiveDate } from './latest-live-date';

const STATIC_PATHS = ['/', '/questions', '/potd', '/faq', '/contact', '/privacy', '/terms'];

// /account is user-specific and carries noindex, so it is not listed.
// Questions come from every authored question, not from data/questions.ts:
// a Problem of the Day is deliberately absent from that listing but is a
// real page. Unauthored slugs render a "not published yet" state and are
// skipped, and a Problem of the Day is left out until its date so a
// scheduled question is not advertised early.
export function listSitemapPaths(today: string = latestLiveDate()): string[] {
	const notYetLive = new Set(
		potdEntries.filter((entry) => entry.date > today).map((entry) => entry.questionId)
	);

	const paths = [...STATIC_PATHS];
	for (const part of curriculum) paths.push(`/questions/${part.id}`);
	for (const id of questionsById.keys()) {
		if (!notYetLive.has(id)) paths.push(`/ide/${id}`);
	}
	return paths;
}
