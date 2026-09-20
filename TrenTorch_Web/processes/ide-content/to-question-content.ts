import type { QuestionContent } from '$data/curriculum/types';
import type { GeneratedQuestion } from './curriculum-index';
import { extractStarterCode } from './extract-starter-code';
import { buildTestHarness } from './build-test-harness';
import { renderCanvasSolution } from './render-canvas-solution';

export function toQuestionContent(question: GeneratedQuestion): QuestionContent {
	const isCanvas = question.type === 'canvas';
	return {
		id: question.id,
		metadata: {
			name: question.id,
			title: question.title,
			tags: question.tags,
			difficulty: question.difficulty
		},
		type: question.type,
		descriptionMarkdown: question.statementMarkdown,
		theoryMarkdown: question.theoryMarkdown,
		// Prefer the hand-authored stub (starter.py) when the question has
		// one; otherwise derive a signature-only stub from the statement's
		// fenced code block. Meaningless for a canvas question (no editor
		// pane), left as an empty string rather than the code fallback.
		starterCode: isCanvas
			? ''
			: question.starterCode?.trim()
				? `${question.starterCode.trimEnd()}\n`
				: extractStarterCode(question.statementMarkdown),
		solutionCode: isCanvas
			? renderCanvasSolution(question.canvasSpec!)
			: question.oracleSolutionCode,
		explanationMarkdown: question.oracleExplanationMarkdown,
		testHarnessCode: isCanvas ? '' : buildTestHarness(question),
		canvasSpec: question.canvasSpec
	};
}
