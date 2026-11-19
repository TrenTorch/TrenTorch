// What the IDE's list/drawer/prev-next needs about the CUDA course, without the sources or harnesses.
import { listCudaProblems } from './read-problems';

export interface CudaListEntry {
	id: string; // the IDE id, cuda-<slug>
	number: string; // CU-001
	title: string;
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
	stage: number;
	topics: string[];
}

export function cudaListEntries(): CudaListEntry[] {
	return listCudaProblems().map((p) => ({
		id: p.ideId,
		number: p.id,
		title: p.title,
		difficulty: p.difficulty,
		stage: p.stage,
		topics: p.topics
	}));
}

export function isCudaId(id: string): boolean {
	return id.startsWith('cuda-') && cudaListEntries().some((e) => e.id === id);
}

export function cudaNeighbours(id: string): { prevId: string | null; nextId: string | null } {
	const ids = cudaListEntries().map((e) => e.id);
	const i = ids.indexOf(id);
	if (i < 0) return { prevId: null, nextId: null };
	return { prevId: i > 0 ? ids[i - 1] : null, nextId: i < ids.length - 1 ? ids[i + 1] : null };
}
