import { describe, expect, it } from 'vitest';
import { buildPotdProblems } from './problemset';
import { potdEntries } from './potd';
import type { PotdSummary } from '$processes/potd/potd-summary';

const summary = (id: string, extra: Partial<PotdSummary> = {}): PotdSummary =>
	({
		id,
		title: `Title of ${id}`,
		difficulty: 'Intermediate',
		tags: ['first-tag'],
		root: 'root',
		section: 'section',
		track: 'track',
		...extra
	}) as PotdSummary;

const first = potdEntries[0];
const second = potdEntries[1];

describe('buildPotdProblems (the Past POTD list)', () => {
	it("lists a pick with its date, no module, and the question's own details", () => {
		const [problem] = buildPotdProblems([
			summary(first.questionId, { topic: 'attention', tools: ['numpy'] })
		]);
		expect(problem).toMatchObject({
			slug: first.questionId,
			title: `Title of ${first.questionId}`,
			difficulty: 'Intermediate',
			moduleId: '',
			topic: 'attention',
			tools: ['numpy'],
			potdDate: first.date,
			caseCompany: null,
			kind: 'direct'
		});
	});

	it('marks a company scenario as a case study and keeps the company', () => {
		const [problem] = buildPotdProblems([summary(first.questionId, { caseCompany: 'Stripe' })]);
		expect(problem).toMatchObject({ kind: 'case-study', caseCompany: 'Stripe' });
	});

	it('falls back from topic to the first tag to "potd", and to no tools', () => {
		const [byTag] = buildPotdProblems([summary(first.questionId)]);
		expect(byTag.topic).toBe('first-tag');
		expect(byTag.tools).toEqual([]);
		const [byDefault] = buildPotdProblems([summary(first.questionId, { tags: [] })]);
		expect(byDefault.topic).toBe('potd');
	});

	// The public schedule has a single day, so these two need a second one to mean anything.
	it.skipIf(!second)(
		'drops a pick whose question is not in the summaries, instead of listing a dead link',
		() => {
			expect(buildPotdProblems([summary(second.questionId)]).map((p) => p.slug)).toEqual([
				second.questionId
			]);
			expect(buildPotdProblems([])).toEqual([]);
		}
	);

	it('leaves out Mastery questions, which are not part of the Problemset', () => {
		expect(buildPotdProblems([summary(first.questionId, { difficulty: 'Mastery' })])).toEqual([]);
	});

	it.skipIf(!second)(
		'keeps the order of the schedule, whatever order the summaries come in',
		() => {
			const out = buildPotdProblems([summary(second.questionId), summary(first.questionId)]);
			expect(out.map((p) => p.slug)).toEqual([first.questionId, second.questionId]);
		}
	);
});
