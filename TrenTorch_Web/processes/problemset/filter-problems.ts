import type { ProblemsetProblem } from '$data/problemset';

export type ProblemsetStatus = 'all' | 'solved' | 'attempted' | 'unsolved';
export const PROBLEMSET_PAGE_SIZE = 100;

export interface ProblemsetFilters {
	query: string;
	moduleId: string;
	topic: string;
	company: string;
	difficulty: string;
	status: ProblemsetStatus;
	pastPotdOnly: boolean;
}

export function getProblemsetStatus(
	slug: string,
	solvedSlugs: ReadonlySet<string>,
	attemptedSlugs: ReadonlySet<string>
): Exclude<ProblemsetStatus, 'all'> {
	if (solvedSlugs.has(slug)) return 'solved';
	if (attemptedSlugs.has(slug)) return 'attempted';
	return 'unsolved';
}

export function filterProblemset(
	problems: ProblemsetProblem[],
	filters: ProblemsetFilters,
	solvedSlugs: ReadonlySet<string>,
	attemptedSlugs: ReadonlySet<string>,
	pastPotdSlugs: ReadonlySet<string>
): ProblemsetProblem[] {
	const query = filters.query.trim().toLowerCase();

	return problems.filter((problem) => {
		const status = getProblemsetStatus(problem.slug, solvedSlugs, attemptedSlugs);
		const searchableText = [
			problem.title,
			problem.caseCompany ?? '',
			problem.moduleId,
			problem.topic
		]
			.join(' ')
			.toLowerCase();

		return (
			(!query || searchableText.includes(query)) &&
			(!filters.moduleId || problem.moduleId === filters.moduleId) &&
			(!filters.topic || problem.topic === filters.topic) &&
			(!filters.company || problem.caseCompany === filters.company) &&
			(!filters.difficulty || problem.difficulty === filters.difficulty) &&
			(!filters.pastPotdOnly || pastPotdSlugs.has(problem.slug)) &&
			(filters.status === 'all' || status === filters.status)
		);
	});
}

export function paginateProblemset<T>(
	items: T[],
	page: number,
	pageSize = PROBLEMSET_PAGE_SIZE
): T[] {
	const safePage = Number.isFinite(page) ? Math.max(1, Math.trunc(page)) : 1;
	const safePageSize = Number.isFinite(pageSize) ? Math.max(1, Math.trunc(pageSize)) : 1;
	const lastPage = Math.max(1, Math.ceil(items.length / safePageSize));
	const currentPage = Math.min(safePage, lastPage);
	const start = (currentPage - 1) * safePageSize;
	return items.slice(start, start + safePageSize);
}
