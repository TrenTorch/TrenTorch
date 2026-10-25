import { describe, it, expect } from 'vitest';
import type { DsaSheetStep } from '$data/dsa-sheet';
import { countSolved, filterSheet, getSheetStatus, nextUnsolved } from './filter-sheet';

const q = (
	id: string,
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced',
	tags: string[] = []
) => ({
	id,
	title: `Title ${id}`,
	difficulty,
	tags
});
const steps: DsaSheetStep[] = [
	{
		id: 's1',
		title: 'Step 1',
		topics: [
			{
				id: 't1',
				title: 'Topic 1',
				questions: [q('a', 'Beginner', ['sorting']), q('b', 'Advanced')]
			},
			{ id: 't2', title: 'Topic 2', questions: [q('c', 'Intermediate', ['hashing'])] }
		]
	},
	{
		id: 's2',
		title: 'Step 2',
		topics: [{ id: 't3', title: 'Topic 3', questions: [q('d', 'Beginner')] }]
	}
];
const none = new Set<string>();
const all = { query: '', difficulty: '', status: 'all' as const };
const ids = (result: DsaSheetStep[]) =>
	result.flatMap((s) => s.topics.flatMap((t) => t.questions.map((x) => x.id)));

describe('getSheetStatus', () => {
	it('prefers solved over attempted', () => {
		expect(getSheetStatus('a', new Set(['a']), new Set(['a']))).toBe('solved');
		expect(getSheetStatus('a', none, new Set(['a']))).toBe('attempted');
		expect(getSheetStatus('a', none, none)).toBe('unsolved');
	});
});

describe('filterSheet', () => {
	it('keeps everything when no filter is set', () => {
		expect(ids(filterSheet(steps, all, none, none))).toEqual(['a', 'b', 'c', 'd']);
	});

	it('searches titles and tags, ignoring case and spaces around the query', () => {
		expect(ids(filterSheet(steps, { ...all, query: ' HASHING ' }, none, none))).toEqual(['c']);
		expect(ids(filterSheet(steps, { ...all, query: 'title b' }, none, none))).toEqual(['b']);
	});

	it('filters by difficulty and by status', () => {
		expect(ids(filterSheet(steps, { ...all, difficulty: 'Beginner' }, none, none))).toEqual([
			'a',
			'd'
		]);
		expect(ids(filterSheet(steps, { ...all, status: 'solved' }, new Set(['c']), none))).toEqual([
			'c'
		]);
		expect(ids(filterSheet(steps, { ...all, status: 'attempted' }, none, new Set(['b'])))).toEqual([
			'b'
		]);
		expect(ids(filterSheet(steps, { ...all, status: 'unsolved' }, new Set(['a']), none))).toEqual([
			'b',
			'c',
			'd'
		]);
	});

	it('drops topics and steps that end up empty', () => {
		const result = filterSheet(steps, { ...all, query: 'sorting' }, none, none);
		expect(result).toHaveLength(1);
		expect(result[0].topics.map((t) => t.id)).toEqual(['t1']);
	});

	it('does not change the input', () => {
		filterSheet(steps, { ...all, query: 'sorting' }, none, none);
		expect(steps[0].topics[0].questions).toHaveLength(2);
	});
});

describe('progress helpers', () => {
	const flat = steps.flatMap((s) => s.topics.flatMap((t) => t.questions));
	it('counts solved questions', () => {
		expect(countSolved(flat, new Set(['a', 'd', 'zzz']))).toEqual({ solved: 2, total: 4 });
	});
	it('finds the first unsolved question in sheet order', () => {
		expect(nextUnsolved(flat, new Set(['a']))?.id).toBe('b');
		expect(nextUnsolved(flat, new Set(['a', 'b', 'c', 'd']))).toBeNull();
	});
});
