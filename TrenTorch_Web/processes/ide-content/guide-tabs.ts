export type GuideTab = 'description' | 'theory' | 'solution' | 'discussion';

type PotdEntry = { questionId: string; date: string };

// Which tabs the IDE guide pane offers for a question.
//
// DSA sheet questions always get Description, Solution and Discussion: the Solution tab is there
// from the start (it still sits behind its own Reveal button), and there is no Theory tab because
// the Description links to the step's theory page.
//
// Problem of the Day questions get a reduced guide: today's, and any scheduled for a future date,
// show only Description and Discussion; Theory comes back once the entry's own date is strictly in
// the past; Solution stays off for every POTD question. Other questions get the full set.
//
// `today` is the IST date string, or null when there is no real "now" (prerender), in which case
// a POTD question gets the full set until hydration can compute it.
export function guideTabsFor(
	question: { id: string; kind?: string } | undefined,
	potdEntries: readonly PotdEntry[],
	today: string | null
): GuideTab[] {
	if (!question) return ['description', 'theory', 'solution'];
	if (question.kind === 'dsa') return ['description', 'solution', 'discussion'];
	const entry = potdEntries.find((e) => e.questionId === question.id);
	if (!entry || today === null) return ['description', 'theory', 'solution'];
	return entry.date < today ? ['description', 'theory', 'discussion'] : ['description', 'discussion'];
}
