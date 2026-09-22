import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';

// The few fields the POTD page shows for a question. The page used to look
// questions up in the full curriculum index, which put every question's
// statement, theory, starter, solution and tests into the browser's JavaScript
// (about 4 MB). It needs only this, and the server provides it (see
// platform/routes/potd/+page.server.ts).
export type PotdSummary = Pick<
	GeneratedQuestion,
	'id' | 'title' | 'difficulty' | 'tags' | 'section' | 'track'
>;

export function toPotdSummary(question: GeneratedQuestion): PotdSummary {
	const { id, title, difficulty, tags, section, track } = question;
	return { id, title, difficulty, tags, section, track };
}
