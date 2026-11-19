import type { QuestionContent } from '$data/curriculum/types';
import { performanceSection, type CudaProblem } from './read-problems';
import { problemTheoryRefs } from './theory-links';
import { listCudaChapters } from './read-course';

// A CUDA problem as the IDE's QuestionContent. testHarnessCode carries the problem's harness.js; the
// CUDA service hands it to the Gpubox worker, which builds the inputs, launches the learner's kernels and
// judges the output (see platform/static/gpubox/worker.js).
export function cudaToQuestionContent(p: CudaProblem): QuestionContent {
	// the first chapter section that practises this problem (derived from the chapters' Practice links)
	const ref = problemTheoryRefs().get(p.id)?.[0];
	const theory = ref ? { chapter: ref.chapter, anchor: ref.anchor } : undefined;
	const titles = new Map(listCudaChapters().map((c) => [c.id, c.title]));
	const theoryLinks = (problemTheoryRefs().get(p.id) ?? []).slice(0, 3).map((r) => ({
		step: r.chapter,
		anchor: r.anchor,
		label: `${r.chapterId} ${titles.get(r.chapterId) ?? ''}: ${r.heading}`
	}));
	return {
		id: p.ideId,
		metadata: {
			name: p.ideId,
			title: p.title,
			tags: ['cuda', ...p.topics],
			difficulty: p.difficulty,
			kind: 'cuda',
			...(theory
				? {
						theory: { step: theory.chapter, anchor: theory.anchor, course: 'cuda' as const },
						theoryLinks
					}
				: {})
		},
		descriptionMarkdown: `${p.statement.trimEnd()}\n\n_Part of the [CUDA course](/cuda). Key lesson: ${p.lesson}_\n`,
		theoryMarkdown: `**Key lesson:** ${p.lesson}\n\n**Topics:** ${p.topics.join(', ')}\n\nRead the chapters in the [CUDA theory](/cuda/theory).`,
		starterCode: p.starter,
		solutionCode: p.solution,
		explanationMarkdown: `${p.explanation.trimEnd()}\n\n${performanceSection(p.metrics)}`,
		testHarnessCode: p.harness
	};
}
