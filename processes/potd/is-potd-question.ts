import { potdEntries } from '$data/potd';

// Whether a question id was ever featured as a Problem of the Day, on any
// date -- not just today's. A student who solves an older POTD later still
// gets it counted, rather than only the exact calendar day it ran.
export function isPotdQuestion(questionId: string): boolean {
	return potdEntries.some((entry) => entry.questionId === questionId);
}
