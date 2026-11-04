// Where the DSA sheet should send a student next, in the order they would want it:
//  - continue: the question they last opened and left unsolved;
//  - start: nothing solved and nothing opened yet, so the sheet's first question;
//  - next: otherwise (back after a while, nothing half-done), the first question still unsolved.
// The cards on the home page and the green dot on /dsa share this.
export interface DsaResumeQuestion {
	id: string;
	title: string;
}

/** What the green dot calls each case. */
export const RESUME_LABEL = {
	continue: 'continue',
	start: 'start',
	next: 'next question'
} as const;

export type DsaResume = { kind: 'continue' | 'start' | 'next'; question: DsaResumeQuestion } | null;

export function dsaResume(
	questions: readonly DsaResumeQuestion[],
	solved: ReadonlySet<string>,
	lastOpened: string | undefined
): DsaResume {
	const last = lastOpened ? questions.find((q) => q.id === lastOpened) : undefined;
	if (last && !solved.has(last.id)) return { kind: 'continue', question: last };
	const first = questions[0];
	if (!first) return null;
	if (!questions.some((q) => solved.has(q.id))) return { kind: 'start', question: first };
	const next = questions.find((q) => !solved.has(q.id));
	return next ? { kind: 'next', question: next } : null;
}
