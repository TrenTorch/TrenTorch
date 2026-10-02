import type { QuestionContent } from '$data/curriculum/types';
import { questionsById } from './curriculum-index';
import { toQuestionContent } from './to-question-content';

export async function loadIdeContent(id: string): Promise<QuestionContent | null> {
	const question = questionsById.get(id);
	return question ? toQuestionContent(question) : null;
}
