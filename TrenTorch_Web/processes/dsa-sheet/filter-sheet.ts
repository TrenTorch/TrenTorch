import type { DsaSheetQuestion, DsaSheetStep } from '$data/dsa-sheet';

export type SheetStatus = 'all' | 'solved' | 'attempted' | 'unsolved';

export interface SheetFilters {
	query: string;
	difficulty: string;
	status: SheetStatus;
}

export function getSheetStatus(
	id: string,
	solvedIds: ReadonlySet<string>,
	attemptedIds: ReadonlySet<string>
): Exclude<SheetStatus, 'all'> {
	if (solvedIds.has(id)) return 'solved';
	if (attemptedIds.has(id)) return 'attempted';
	return 'unsolved';
}

function matches(
	question: DsaSheetQuestion,
	filters: SheetFilters,
	solvedIds: ReadonlySet<string>,
	attemptedIds: ReadonlySet<string>
): boolean {
	const query = filters.query.trim().toLowerCase();
	const text = [question.title, ...question.tags].join(' ').toLowerCase();
	return (
		(!query || text.includes(query)) &&
		(!filters.difficulty || question.difficulty === filters.difficulty) &&
		(filters.status === 'all' ||
			getSheetStatus(question.id, solvedIds, attemptedIds) === filters.status)
	);
}

// The steps with only the questions that match. A topic or step with none left is dropped, so the
// page never shows an empty heading.
export function filterSheet(
	steps: DsaSheetStep[],
	filters: SheetFilters,
	solvedIds: ReadonlySet<string>,
	attemptedIds: ReadonlySet<string>
): DsaSheetStep[] {
	return steps
		.map((step) => ({
			...step,
			topics: step.topics
				.map((topic) => ({
					...topic,
					questions: topic.questions.filter((q) => matches(q, filters, solvedIds, attemptedIds))
				}))
				.filter((topic) => topic.questions.length > 0)
		}))
		.filter((step) => step.topics.length > 0);
}

export function countSolved(
	questions: DsaSheetQuestion[],
	solvedIds: ReadonlySet<string>
): { solved: number; total: number } {
	return { solved: questions.filter((q) => solvedIds.has(q.id)).length, total: questions.length };
}

// Where "Continue" should go: the first question, in sheet order, that is not solved yet.
export function nextUnsolved(
	questions: DsaSheetQuestion[],
	solvedIds: ReadonlySet<string>
): DsaSheetQuestion | null {
	return questions.find((q) => !solvedIds.has(q.id)) ?? null;
}
