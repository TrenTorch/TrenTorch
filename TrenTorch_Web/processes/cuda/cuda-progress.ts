// Client-safe helpers for the CUDA pages: filtering the problem list and reading progress. No fs imports, so
// the pages can use it in the browser (the list itself arrives as data from the server load).
import type { CudaListEntry } from './cuda-course-index';

export type CudaStatus = 'all' | 'solved' | 'attempted' | 'unsolved';

export interface CudaFilters {
	query: string;
	difficulty: string;
	topic: string;
	status: CudaStatus;
}

export const CUDA_STAGES: Record<number, string> = {
	1: 'Elementwise operations',
	2: 'Reductions',
	3: 'Row-wise normalization and losses',
	4: 'Stencils',
	5: 'Memory patterns, scan, histogram, sorting',
	6: 'Matrix multiplication ladder',
	7: 'Advanced, debugging and multi-GPU'
};

export function statusOf(
	id: string,
	solvedIds: ReadonlySet<string>,
	attemptedIds: ReadonlySet<string>
): Exclude<CudaStatus, 'all'> {
	if (solvedIds.has(id)) return 'solved';
	if (attemptedIds.has(id)) return 'attempted';
	return 'unsolved';
}

export function filterCuda(
	entries: CudaListEntry[],
	f: CudaFilters,
	solvedIds: ReadonlySet<string>,
	attemptedIds: ReadonlySet<string>
): CudaListEntry[] {
	const q = f.query.trim().toLowerCase();
	return entries.filter((e) => {
		const text = [e.title, e.number, ...e.topics].join(' ').toLowerCase();
		return (
			(!q || text.includes(q)) &&
			(!f.difficulty || e.difficulty === f.difficulty) &&
			(!f.topic || e.topics.includes(f.topic)) &&
			(f.status === 'all' || statusOf(e.id, solvedIds, attemptedIds) === f.status)
		);
	});
}

/** Topic choices for the filter popover, most common first. */
export function topicChoices(entries: CudaListEntry[]) {
	const counts = new Map<string, number>();
	for (const e of entries) for (const t of e.topics) counts.set(t, (counts.get(t) ?? 0) + 1);
	return [...counts]
		.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
		.map(([value, count]) => ({ value, label: value.replace(/-/g, ' '), count }));
}

export function countSolvedIn(entries: CudaListEntry[], solvedIds: ReadonlySet<string>) {
	const solved = entries.filter((e) => solvedIds.has(e.id)).length;
	return { solved, total: entries.length };
}

/** Where "Continue" goes: a problem started but not solved, else the first unsolved one in course order. */
export function resumeTarget(
	entries: CudaListEntry[],
	solvedIds: ReadonlySet<string>,
	attemptedIds: ReadonlySet<string>
): { entry: CudaListEntry; kind: 'continue' | 'start' | 'next' } | null {
	const started = entries.find((e) => attemptedIds.has(e.id) && !solvedIds.has(e.id));
	if (started) return { entry: started, kind: 'continue' };
	const next = entries.find((e) => !solvedIds.has(e.id));
	if (!next) return null;
	return { entry: next, kind: solvedIds.size === 0 ? 'start' : 'next' };
}
