import { potdEntries, type PotdEntry } from '$data/potd';
import type { PotdSummary } from './potd-summary';

// The Problem of the Day scheduled for a 'YYYY-MM-DD' date, or undefined when
// nothing is scheduled (or the scheduled question is not in the summaries).
export function getPotdForDate(
	summaries: PotdSummary[],
	date: string,
	entries: PotdEntry[] = potdEntries
): PotdSummary | undefined {
	const entry = entries.find((e) => e.date === date);
	return entry ? summaries.find((s) => s.id === entry.questionId) : undefined;
}
