import { describe, it, expect } from 'vitest';
import { getAdjacentQuestionIds } from './get-adjacent-question-ids';

describe('getAdjacentQuestionIds', () => {
	it('moves through the DSA sheet in sheet order', () => {
		expect(getAdjacentQuestionIds('sheet-count-pairs')).toEqual({
			prevId: null,
			nextId: 'sheet-count-halving-steps'
		});
		expect(getAdjacentQuestionIds('sheet-normalize-text').nextId).toBe('sheet-transpose-matrix');
	});

	it('stops at the end of the sheet and does not run on into other courses', () => {
		expect(getAdjacentQuestionIds('sheet-transpose-matrix')).toEqual({
			prevId: 'sheet-normalize-text',
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
