// The CUDA course's theory chapters. Each folder under data/cuda/theory holds a meta.json and a theory.md and
// becomes /cuda/theory/<slug>. Rendering is shared with the DSA sheet theory pages
// (processes/dsa-theory/read-theory.ts): same Markdown conventions, same heading anchors.
import { join } from 'node:path';
import { listTheoryStepsIn, renderTheory, type TheoryStep } from '../dsa-theory/read-theory';
import { listCudaProblems } from './read-problems';

export const CUDA_THEORY_DIR = join('data', 'cuda', 'theory');

export interface CudaChapter extends TheoryStep {
	/** A1, B4, G1 ... */
	id: string;
	part: string;
	pmpp: string[];
	estMinutes: number;
	prereqs: string[];
	/** real problems this chapter practises (CU-xxx) */
	problems: string[];
	/** announced but not built yet */
	proposedProblems: string[];
	prereqNote: string;
	problemsNote: string;
}

export function listCudaChapters(): CudaChapter[] {
	return listTheoryStepsIn(CUDA_THEORY_DIR).map((step) => {
		const m = step.meta as Partial<CudaChapter> & { title: string };
		return {
			...step,
			id: m.id ?? step.step,
			part: m.part ?? '',
			pmpp: m.pmpp ?? [],
			estMinutes: m.estMinutes ?? 0,
			prereqs: m.prereqs ?? [],
			problems: m.problems ?? [],
			proposedProblems: m.proposedProblems ?? [],
			prereqNote: m.prereqNote ?? '',
			problemsNote: m.problemsNote ?? ''
		};
	});
}

/** CU-001 -> /ide/cuda-vector-addition, for every problem that exists. */
export function problemHrefs(): Map<string, string> {
	return new Map(listCudaProblems().map((p) => [p.id, `/ide/${p.ideId}`]));
}

/**
 * Renders a chapter. `[text](problem:CU-xxx)` becomes a link to the problem when it exists; a link to a
 * problem that does not exist yet becomes plain text marked "(coming soon)" (those are rendered as cards).
 */
export function renderCudaChapter(step: TheoryStep) {
	const hrefs = problemHrefs();
	return renderTheory(step, {
		transform: (md) =>
			md.replace(/\[([^\]]+)\]\(problem:(CU-\d+)\)/g, (_all, text: string, id: string) => {
				const href = hrefs.get(id);
				return href ? `[${text}](${href})` : `${text} _(coming soon)_`;
			})
	});
}

/** One line for the chapter header. */
export function chapterMetaLine(c: CudaChapter): string {
	const parts = [`${c.estMinutes} min`];
	if (c.prereqs.length) parts.push(`after ${c.prereqs.join(', ')}`);
	if (c.pmpp.length) parts.push(`PMPP 4th ed. ${c.pmpp.join(', ')}`);
	return parts.join(' · ');
}
