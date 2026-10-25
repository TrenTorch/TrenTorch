import { describe, it, expect } from 'vitest';
import { questionsById } from './curriculum-index';
import { getAdjacentQuestionIds } from './get-adjacent-question-ids';

// The sheet's questions in sheet order (the bundle lists them section by section).
const sheetIds = [...questionsById.values()].filter((q) => q.kind === 'dsa').map((q) => q.id);

describe('getAdjacentQuestionIds', () => {
	it('moves through the DSA sheet in sheet order', () => {
		expect(sheetIds[0]).toBe('sheet-count-pairs');
		expect(getAdjacentQuestionIds(sheetIds[0])).toEqual({ prevId: null, nextId: sheetIds[1] });
		expect(getAdjacentQuestionIds(sheetIds[1])).toEqual({
			prevId: sheetIds[0],
			nextId: sheetIds[2]
		});
	});

	it('stops at the end of the sheet and does not run on into other courses', () => {
		const last = sheetIds.length - 1;
		expect(getAdjacentQuestionIds(sheetIds[last])).toEqual({
			prevId: sheetIds[last - 1],
			nextId: null
		});
	});

	it('still walks the whole curriculum for other questions', () => {
		const { prevId, nextId } = getAdjacentQuestionIds('python-what-a-variable-is');
		expect(prevId).toBeNull();
		expect(nextId).not.toBeNull();
		expect(nextId?.startsWith('sheet-')).toBe(false);
	});

	it('returns nothing for an unknown id', () => {
		expect(getAdjacentQuestionIds('nope')).toEqual({ prevId: null, nextId: null });
	});
});
