import type { QuestionContent } from '$data/curriculum/types';

export type Language = 'python' | 'sql';

export function detectLanguage(content: QuestionContent): Language {
	// SQL questions have 'db' in tags or start with 'db-sql-' in id
	if (content.metadata.tags.includes('db') || content.id.startsWith('db-sql-')) {
		return 'sql';
	}

	// Default to Python for everything else
	return 'python';
}
