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

	it('accepts a random batch and checks its shape', () => {
		const batchProblem = {
			...valid,
			stress: {
				runs: 5,
				inputs: { a: { type: 'int', lo: 0, hi: 9 }, b: { type: 'int', lo: 0, hi: 9 } }
			},
			cases: [
				...valid.cases,
				{ id: 'random_batch', batch: { count: 2, seed: 1 }, digests: ['aaaaaa', 'bbbbbb'] }
			]
		};
		expect(() => parse(batchProblem)).not.toThrow();
		const bad = (change: object) => ({
			...batchProblem,
			cases: [
				...valid.cases,
				{
					id: 'random_batch',
					batch: { count: 2, seed: 1 },
					digests: ['aaaaaa', 'bbbbbb'],
					...change
				}
			]
		});
		expect(() => parse(bad({ digests: ['aaaaaa'] }))).toThrow(/needs 2 hex digests/);
		expect(() => parse(bad({ digests: ['zz', 'bbbbbb'] }))).toThrow(/hex digests/);
		expect(() => parse(bad({ batch: { count: 0, seed: 1 } }))).toThrow(/batch.count/);
		expect(() => parse(bad({ input: { a: 1, b: 2 } }))).toThrow(/cannot also have/);
		expect(() => parse({ ...batchProblem, stress: undefined })).toThrow(/stress.inputs/);
		expect(() => parse({ ...batchProblem, compare: 'unordered' })).toThrow(/only supports compare/);
	});

	it('accepts maxReads on a case and rejects a bad value', () => {
		const withReads = (maxReads: unknown) =>
			withCase({ id: 'reads_1', maxReads, input: { a: 1, b: 2 }, expected: 3 });
		expect(() => parse(withReads(60))).not.toThrow();
		for (const bad of [0, -3, 1.5, '60']) {
			expect(() => parse(withReads(bad))).toThrow(/maxReads must be a whole number/);
		}
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

	it('has the 27 Step 0 questions', () => {
		const basics = (root?.sections ?? []).find((s) => s.id === 'basics');
		expect(basics?.tracks.flatMap((t) => t.questions)).toHaveLength(27);
	});

	it('marks every question kind dsa, named sheet-*, with three hints', () => {
		expect(questions.length).toBeGreaterThanOrEqual(27);
		expect(new Set(questions.map((q) => q.id)).size).toBe(questions.length);
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
		expect(dsaSheet.steps[0].topics.map((t: { title: string }) => t.title)).toEqual([
			'Counting Loop Steps (Big-O Basics)',
			'Making Slow Code Fast',
			'Python Built-ins and Standard Library Tricks'
		]);
		// every topic keeps a short description
		for (const step of dsaSheet.steps) {
			for (const topic of step.topics) expect(topic.description, topic.title).toBeTruthy();
		}
		const ids = dsaSheet.steps.flatMap((s: { topics: { questions: { id: string }[] }[] }) =>
			s.topics.flatMap((t) => t.questions.map((q) => q.id))
		);
		expect(ids).toHaveLength(all.filter((q) => q.kind === 'dsa').length);
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
