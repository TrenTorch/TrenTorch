import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { toPotdSummary, type PotdSummary } from './potd-summary';

// Runs at build time (server load of a prerendered page), so the browser gets
// only the few fields a Problem of the Day card shows and never the curriculum.
// Entries whose question is not in the curriculum are dropped.
export function loadPotdSummaries(): PotdSummary[] {
	return potdEntries.flatMap((entry) => {
		const question = questionsById.get(entry.questionId);
		return question ? [toPotdSummary(question)] : [];
	});
}
