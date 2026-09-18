import { questionsById } from './curriculum-index';

export function listIdeContentIds(): string[] {
	return [...questionsById.keys()];
}
