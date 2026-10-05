import type { QuestionContent } from '$data/curriculum/types';
import type { GeneratedQuestion } from './curriculum-index';
import { extractStarterCode } from './extract-starter-code';
import { buildTestHarness } from './build-test-harness';
import { buildSqlEditorStarter, isSqlQuestion, splitSqlStarter } from './sql-question';

function toSqlQuestionContent(question: GeneratedQuestion): QuestionContent {
	const raw = question.starterCode ?? '';
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
		starterCode: buildSqlEditorStarter(raw),
		dbSchema: splitSqlStarter(raw).schema,
		solutionCode: question.oracleSolutionCode,
		explanationMarkdown: question.oracleExplanationMarkdown,
		// SQL tests run in the SQL worker against SQLite, not through the Python
		// harness, so they are handed over exactly as authored.
		testHarnessCode: question.testsCode,
		widgetId: question.widgetId
	};
}

export function toQuestionContent(question: GeneratedQuestion): QuestionContent {
	if (isSqlQuestion(question.tags, question.id)) return toSqlQuestionContent(question);
	return {
		id: question.id,
		metadata: {
			name: question.id,
			title: question.title,
			tags: question.tags,
			difficulty: question.difficulty,
			kind: question.kind,
			caseCompany: question.caseCompany,
			relatedModule: question.relatedModule,
			hint: question.hint,
			tools: question.tools
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
		previewCode: question.previewCode,
		widgetId: question.widgetId
	};
}
