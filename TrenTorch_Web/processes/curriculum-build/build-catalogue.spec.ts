import { describe, it, expect } from 'vitest';
import { buildCatalogue } from './build-catalogue.mjs';

const question = (id: string, difficulty = 'Beginner') => ({ id, title: `T ${id}`, difficulty });
const track = (title: string, meta = {}, ids = ['q']) => ({
	id: title.toLowerCase(),
	meta: { title, ...meta },
	questions: ids.map((id) => question(id))
});

describe('buildCatalogue', () => {
	it('names every level from its meta title and prefixes the part id', () => {
		const { parts } = buildCatalogue([
			{
				id: 'python',
				meta: { title: 'Python for Engineers' },
				sections: [{ id: 's', meta: { title: 'Semantics' }, tracks: [track('Basics')] }]
			}
		]);
		expect(parts[0].id).toBe('part-python');
		expect(parts[0].title).toBe('Python for Engineers');
		expect(parts[0].sections[0].name).toBe('Semantics');
		expect(parts[0].sections[0].tracks[0].name).toBe('Basics');
	});

	it('shows the four README difficulties as three, using the question title and id', () => {
		const { parts } = buildCatalogue([
			{
				id: 'r',
				meta: { title: 'R' },
				sections: [
					{
						id: 's',
						meta: { title: 'S' },
						tracks: [
							{
								id: 't',
								meta: { title: 'T' },
								questions: ['Beginner', 'Intermediate', 'Advanced', 'Mastery'].map((d) =>
									question(d.toLowerCase(), d)
								)
							}
						]
					}
				]
			}
		]);
		const questions = parts[0].sections[0].tracks[0].questions;
		expect(questions.map((q: { difficulty: string }) => q.difficulty)).toEqual([
			'Easy',
			'Medium',
			'Hard',
			'Hard'
		]);
		expect(questions[0]).toEqual({ slug: 'beginner', title: 'T beginner', difficulty: 'Easy' });
	});

	it('throws on a difficulty it does not know', () => {
		expect(() =>
			buildCatalogue([
				{
					id: 'r',
					meta: { title: 'R' },
					sections: [
						{
							id: 's',
							meta: { title: 'S' },
							tracks: [{ id: 't', meta: { title: 'T' }, questions: [question('x', 'Impossible')] }]
						}
					]
				}
			])
		).toThrow(/unknown difficulty/);
	});

	it('inherits topics and companies from the nearest folder that sets them', () => {
		const tag = { names: ['A'], roles: 'r' };
		const { parts } = buildCatalogue([
			{
				id: 'r',
				meta: { title: 'Root', topics: ['Root topic'] },
				sections: [
					{
						id: 'a',
						meta: { title: 'A', topics: ['Section topic'], companies: tag },
						tracks: [
							track('Inherits', {}, ['i']),
							track('Overrides', { topics: ['Track topic'] }, ['o'])
						]
					},
					{ id: 'b', meta: { title: 'B' }, tracks: [track('From root', {}, ['f'])] }
				]
			}
		]);
		const [a, b] = parts[0].sections;
		expect(a.tracks[0].topics).toEqual(['Section topic']);
		expect(a.tracks[0].companies).toEqual(tag);
		expect(a.tracks[1].topics).toEqual(['Track topic']);
		expect(b.tracks[0].topics).toEqual(['Root topic']);
		expect('companies' in b.tracks[0]).toBe(false);
	});

	it('falls back to the root title as the topic when none is set anywhere', () => {
		const { parts } = buildCatalogue([
			{
				id: 'r',
				meta: { title: 'Computer Vision' },
				sections: [{ id: 's', meta: { title: 'S' }, tracks: [track('T')] }]
			}
		]);
		expect(parts[0].sections[0].tracks[0].topics).toEqual(['Computer Vision']);
	});

	describe('uniqueness', () => {
		const root = (sections: unknown[]) => [{ id: 'rl', meta: { title: 'RL' }, sections }];
		const section = (title: string, ...tracks: unknown[]) => ({
			id: title.toLowerCase(),
			meta: { title },
			tracks
		});

		it('rejects a question name used twice, naming both places', () => {
			expect(() =>
				buildCatalogue(
					root([
						section('A', track('One', {}, ['same'])),
						section('B', track('Two', {}, ['same']))
					]) as never
				)
			).toThrow(/duplicate question name "same" \(rl\/a\/one and rl\/b\/two\)/);
		});

		it('rejects two sections with one title in a root', () => {
			expect(() =>
				buildCatalogue(
					root([
						section('Same', track('One', {}, ['a'])),
						section('Same', track('Two', {}, ['b']))
					]) as never
				)
			).toThrow(/two sections are titled "Same"/);
		});

		it('rejects two tracks with one title in a root', () => {
			expect(() =>
				buildCatalogue(
					root([
						section('A', track('Same', {}, ['a'])),
						section('B', track('Same', {}, ['b']))
					]) as never
				)
			).toThrow(/two tracks are titled "Same"/);
		});
	});
});
