import { describe, it, expect } from 'vitest';
import { buildCasesTests, parseProblem } from './build-cases-tests.mjs';
import { buildCurriculum } from './build.mjs';

const valid = {
	schema: 1,
	function: {
		name: 'add',
		params: [
			{ name: 'a', type: 'int' },
			{ name: 'b', type: 'int' }
		],
		returns: 'int'
	},
	limits: { timeMs: 1000 },
	hints: ['one', 'two'],
	cases: [
		{ id: 'example_1', visible: true, input: { a: 1, b: 2 }, expected: 3 },
		{
			id: 'perf_1',
			perf: true,
			input: { a: 1, b: { $gen: { type: 'permutation', n: 5 } } },
			digest: 'abc'
		}
	]
};
const parse = (problem: unknown) => parseProblem(JSON.stringify(problem), 'dir');
const withCase = (extra: object) => ({ ...valid, cases: [...valid.cases, extra] });

describe('parseProblem', () => {
	it('accepts a complete problem and returns its hints', () => {
		expect(parse(valid).hints).toEqual(['one', 'two']);
	});

	it.each([
		['a wrong schema', { ...valid, schema: 2 }, /schema must be 1/],
		['a missing time limit', { ...valid, limits: {} }, /limits\.timeMs/],
		['an unknown compare mode', { ...valid, compare: 'fuzzy' }, /compare must be/],
		['more than four hints', { ...valid, hints: ['1', '2', '3', '4', '5'] }, /up to 4/],
		['no cases', { ...valid, cases: [] }, /cases is empty/],
		[
			'a bad case id',
			withCase({ id: 'Bad Id', input: { a: 1, b: 2 }, expected: 3 }),
			/needs an id/
		],
		[
			'a duplicate case id',
			withCase({ id: 'example_1', input: { a: 1, b: 2 }, expected: 3 }),
			/duplicate case id/
		],
		[
			'input keys that do not match the parameters',
			withCase({ id: 'x', input: { a: 1 }, expected: 3 }),
			/exactly the keys a, b/
		],
		[
			'a case with both expected and digest',
			withCase({ id: 'x', input: { a: 1, b: 2 }, expected: 3, digest: 'a' }),
			/exactly one of/
		],
		[
			'a case with neither expected nor digest',
			withCase({ id: 'x', input: { a: 1, b: 2 } }),
			/exactly one of/
		]
	])('rejects %s', (_name, problem, message) => {
		expect(() => parse(problem)).toThrow(message);
	});

	it('rejects text that is not JSON', () => {
		expect(() => parseProblem('{nope', 'dir')).toThrow(/not valid JSON/);
	});
});

describe('buildCasesTests', () => {
	it('defines one test per case, examples first, named like the IDE expects', () => {
		const code = buildCasesTests(JSON.stringify(valid), 'dir');
		expect(code).toContain('test_01_example_1 = _make_test(0)');
		expect(code).toContain('test_02_perf_1 = _make_test(1)');
	});

	it('embeds the problem text exactly, so integers above 2^53 reach Python unchanged', () => {
		const raw = JSON.stringify(valid).replace('"expected":3', '"expected":999999999999999999');
		const code = buildCasesTests(raw, 'dir');
		const literal = /load_problem\((".*")\)\n/.exec(code)?.[1] ?? '';
		// a JSON string literal is also a valid Python string literal
		expect(JSON.parse(literal)).toBe(raw);
	});

	it('leaves the shared runtime out, so it is not copied into every question', () => {
		expect(buildCasesTests(JSON.stringify(valid), 'dir')).not.toContain('def check_case');
	});
});

describe('the DSA sheet content', () => {
	const { bundle, catalogue } = buildCurriculum();
	const root = bundle.roots.find((r) => r.id === 'dsa-sheet');
	const questions = (root?.sections ?? []).flatMap((s) => s.tracks.flatMap((t) => t.questions));

	it('has the 27 Step 0 questions, all marked kind dsa with three hints', () => {
		expect(questions).toHaveLength(27);
		for (const question of questions) {
			expect(question.kind, question.id).toBe('dsa');
			expect(question.hints, question.id).toHaveLength(3);
			expect(question.id.startsWith('sheet-'), question.id).toBe(true);
		}
	});

	it('generates its tests from problem.json and does not hand-write them', () => {
		for (const question of questions) {
			expect(question.testsCode, question.id).toContain('check_case(');
		}
	});

	it('is in the IDE bundle but not in the learning catalogue', () => {
		const listed = JSON.stringify(catalogue);
		expect(listed).not.toContain('sheet-count-pairs');
	});
});

describe('the slim modules the browser pages import', () => {
	const { bundle, dsaSheet, problemset } = buildCurriculum();
	const all = bundle.roots.flatMap((root) =>
		root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
	);

	it('lists the DSA sheet as steps and topics with their folder titles', () => {
		expect(dsaSheet.title).toBe('DSA Sheet');
		expect(dsaSheet.steps).toHaveLength(1);
		expect(dsaSheet.steps[0].topics.map((t: { title: string }) => t.title)).toEqual([
			'Counting Steps',
			'Make It Fast',
			'Python Toolbox'
		]);
		// every step and topic explains itself on the /dsa page
		expect(dsaSheet.steps[0].description).toBeTruthy();
		for (const topic of dsaSheet.steps[0].topics)
			expect(topic.description, topic.title).toBeTruthy();
		const ids = dsaSheet.steps.flatMap((s: { topics: { questions: { id: string }[] }[] }) =>
			s.topics.flatMap((t) => t.questions.map((q) => q.id))
		);
		expect(ids).toHaveLength(27);
		expect(ids[0]).toBe('sheet-count-pairs');
	});

	it('gives the Problemset page every problemset question and no question text', () => {
		expect(problemset).toHaveLength(all.filter((q) => q.kind === 'problemset').length);
		expect(problemset.length).toBeGreaterThan(0);
		for (const source of problemset) {
			expect(Object.keys(source), source.id).not.toContain('statementMarkdown');
			expect(Object.keys(source), source.id).not.toContain('oracleSolutionCode');
		}
	});
});
