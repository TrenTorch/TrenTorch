import { describe, it, expect } from 'vitest';
import { filterCuda, resumeTarget, topicChoices, topicLabel, countSolvedIn } from './cuda-progress';
import type { CudaListEntry } from './cuda-course-index';

const e = (
	id: string,
	difficulty: CudaListEntry['difficulty'],
	topics: string[],
	stage = 1
): CudaListEntry => ({
	id,
	number: id.toUpperCase(),
	title: `Problem ${id}`,
	difficulty,
	stage,
	topics
});
const list = [
	e('a', 'Beginner', ['map']),
	e('b', 'Intermediate', ['reduction', 'map']),
	e('c', 'Advanced', ['nccl'], 7)
];

describe('CUDA progress helpers', () => {
	it('filters by text, difficulty, topic and status', () => {
		const none = new Set<string>();
		const base = { query: '', difficulty: '', topic: '', status: 'all' as const };
		expect(filterCuda(list, base, none, none)).toHaveLength(3);
		expect(filterCuda(list, { ...base, topic: 'map' }, none, none).map((x) => x.id)).toEqual([
			'a',
			'b'
		]);
		expect(
			filterCuda(list, { ...base, difficulty: 'Advanced' }, none, none).map((x) => x.id)
		).toEqual(['c']);
		expect(filterCuda(list, { ...base, query: 'reduction' }, none, none).map((x) => x.id)).toEqual([
			'b'
		]);
		expect(
			filterCuda(list, { ...base, status: 'solved' }, new Set(['a']), none).map((x) => x.id)
		).toEqual(['a']);
		expect(
			filterCuda(list, { ...base, status: 'attempted' }, new Set(['a']), new Set(['b'])).map(
				(x) => x.id
			)
		).toEqual(['b']);
		expect(
			filterCuda(list, { ...base, status: 'unsolved' }, new Set(['a']), new Set(['b'])).map(
				(x) => x.id
			)
		).toEqual(['c']);
	});

	it('counts topics, most common first', () => {
		expect(topicChoices(list)[0]).toEqual({ value: 'map', label: 'Map', count: 2 });
	});

	it('capitalises topic labels and keeps acronyms upper-case', () => {
		expect(topicLabel('shared-memory')).toBe('Shared Memory');
		expect(topicLabel('multi-gpu')).toBe('Multi GPU');
		expect(topicLabel('nccl')).toBe('NCCL');
		expect(topicLabel('2d-indexing')).toBe('2d Indexing');
	});

	it('counts solved problems', () => {
		expect(countSolvedIn(list, new Set(['a', 'c']))).toEqual({ solved: 2, total: 3 });
	});

	it('resumes the started problem, else the next unsolved one', () => {
		expect(resumeTarget(list, new Set(), new Set())).toMatchObject({
			kind: 'start',
			entry: { id: 'a' }
		});
		expect(resumeTarget(list, new Set(['a']), new Set(['c']))).toMatchObject({
			kind: 'continue',
			entry: { id: 'c' }
		});
		expect(resumeTarget(list, new Set(['a']), new Set())).toMatchObject({
			kind: 'next',
			entry: { id: 'b' }
		});
		expect(resumeTarget(list, new Set(['a', 'b', 'c']), new Set())).toBeNull();
	});
});
