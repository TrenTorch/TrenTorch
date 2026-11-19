import type { QuestionContent } from '$data/curriculum/types';
import { isSqlQuestion } from '../ide-content/sql-question';

export type Language = 'python' | 'sql' | 'javascript' | 'cpp' | 'java' | 'go' | 'rust' | 'cuda';

// DSA questions let the student pick their language in the IDE; every other
// question kind is auto-detected the way it always was.
export const DSA_LANGUAGES: Language[] = ['python', 'javascript', 'cpp', 'java', 'go', 'rust'];

export function detectLanguage(content: QuestionContent): Language {
	// CUDA problems are their own course: kernels run on the Gpubox simulator (cuda-service.ts).
	if (content.metadata.kind === 'cuda') return 'cuda';
	return isSqlQuestion(content.metadata.tags, content.id) ? 'sql' : 'python';
}

export function isLanguageSelectable(content: QuestionContent): boolean {
	return content.metadata.kind === 'dsa';
}
