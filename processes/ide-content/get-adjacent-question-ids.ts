import { questionsById } from './curriculum-index';

// Prev/next in the same curriculum order /questions lists them in --
// questionsById is populated by iterating sections then tracks then
// questions, so Map key order already matches that order for free.
export function getAdjacentQuestionIds(id: string): {
	prevId: string | null;
	nextId: string | null;
} {
	const ids = [...questionsById.keys()];
	const index = ids.indexOf(id);
	if (index === -1) return { prevId: null, nextId: null };
	return {
		prevId: index > 0 ? ids[index - 1] : null,
		nextId: index < ids.length - 1 ? ids[index + 1] : null
	};
}
