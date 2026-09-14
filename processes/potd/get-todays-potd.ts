import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { toDisplayQuestion, type PotdDisplayQuestion } from './to-display-question';

export function localDateString(date: Date): string {
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0');
	const day = String(date.getDate()).padStart(2, '0');
	return `${year}-${month}-${day}`;
}

// Local time on purpose (not UTC): "today" should match the calendar date
// on the student's own clock, the same day they'd expect to see change at
// their own midnight, not somewhere else's. Callers on the prerendered
// static build must only call this client-side (guarded by `browser`) --
// there's no real visitor "now" at build time.
export function getTodaysPotd(now: Date = new Date()): PotdDisplayQuestion | undefined {
	const today = localDateString(now);
	const entry = potdEntries.find((e) => e.date === today);
	if (!entry) return undefined;
	const generated = questionsById.get(entry.questionId);
	return generated ? toDisplayQuestion(generated, entry.date) : undefined;
}
