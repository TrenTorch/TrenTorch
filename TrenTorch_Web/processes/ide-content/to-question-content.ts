import type { QuestionContent } from '$data/curriculum/types';
import type { GeneratedQuestion } from './curriculum-index';
import { extractStarterCode } from './extract-starter-code';
import { buildTestHarness } from './build-test-harness';

export function toQuestionContent(question: GeneratedQuestion): QuestionContent {
	return {
		id: question.id,
		metadata: {
			name: question.id,
			title: question.title,
			tags: question.tags,
			difficulty: question.difficulty
		},
		descriptionMarkdown: question.statementMarkdown,
		theoryMarkdown: question.theoryMarkdown,
		// Prefer the hand-authored stub (starter.py) when the question has
		// one; otherwise derive a signature-only stub from the statement's
		// fenced code block.
		starterCode: question.starterCode?.trim()
			? `${question.starterCode.trimEnd()}\n`
			: extractStarterCode(question.statementMarkdown),
		solutionCode: question.oracleSolutionCode,
		explanationMarkdown: question.oracleExplanationMarkdown,
		testHarnessCode: buildTestHarness(question),
		widgetId: question.widgetId
	};
}
