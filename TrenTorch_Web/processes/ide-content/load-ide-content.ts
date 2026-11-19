import type { QuestionContent } from '$data/curriculum/types';
import { questionsById } from './curriculum-index';
import { toQuestionContent } from './to-question-content';
import { findCudaProblem } from '../cuda/read-problems';
import { cudaToQuestionContent } from '../cuda/to-question-content';

export async function loadIdeContent(id: string): Promise<QuestionContent | null> {
	// The CUDA course lives outside the curriculum bundle (data/cuda/problems).
	const cuda = findCudaProblem(id);
	if (cuda) return cudaToQuestionContent(cuda);
	const question = questionsById.get(id);
	return question ? toQuestionContent(question) : null;
}
