import type { QuestionContent } from '$data/curriculum/types';
import { isSqlQuestion } from '../ide-content/sql-question';

export type Language = 'python' | 'sql';

export function detectLanguage(content: QuestionContent): Language {
	return isSqlQuestion(content.metadata.tags, content.id) ? 'sql' : 'python';
}
