import { describe, it, expect, beforeAll } from 'vitest';
import type { PyodideInterface } from 'pyodide';
import { curriculum as generated } from 'virtual:curriculum/bundle';
import { buildTestHarness } from '$processes/ide-content/build-test-harness';
import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';
import { isSqlQuestion } from '$processes/ide-content/sql-question';
import { internalsIn, loadRuntime, runTests } from './runtime';

// The starter a student sees first fails its tests, and a student's own code
// fails in many ways. Whatever happens, what they read must be Python's own
// account of their code and not the runner's.
//
// For every code question this runs, in real Pyodide through the worker's test
// script:
//
// 1. The starter exactly as shipped. This is the first thing every student runs,
//    so it is the most common failing run there is.
// 2. A solution that is broken at every function: each top-level def is wrapped
//    so that calling it raises. That puts a student-code frame under every test
//    that calls into the solution, which is the "error inside my function" case.
//
// Both must finish (no worker-level failure) and no text shown to the student
// may contain runner internals. questions.spec.ts is the other half: the
// reference solutions pass.

type Question = GeneratedQuestion & { type?: string };

const questions = (
	generated.roots.flatMap((root) =>
		root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
	) as unknown as Question[]
).filter((q) => q.type !== 'canvas' && !isSqlQuestion(q.tags, q.id));
// SQL questions run in the SQL worker, not the Python harness.

const only = process.env.PYODIDE_ONLY?.split(',').filter(Boolean);
const selected = questions.filter((q) => !only || only.includes(q.id));

// Wraps each top-level function so that calling it raises. Class bodies and
// nested functions are left alone: the aim is only an error raised from inside
// student code, not a faithful mutation of it.
const BREAK_FUNCTIONS = `
def __broken(function):
    def raiser(*args, **kwargs):
        raise ValueError("this function is broken on purpose")
    return raiser
`;

function breakEveryFunction(solution: string): string {
	const wrapped = solution.replace(/^def /gm, '@__broken\ndef ');
	return `${BREAK_FUNCTIONS}\n${wrapped}`;
}

function everyTextShown(outcome: Awaited<ReturnType<typeof runTests>>): string[] {
	return [
		outcome.error ?? '',
		outcome.stdout,
		outcome.stderr,
		...outcome.results.map((r) => r.error ?? '')
	];
}

describe('what a student sees when their code fails', () => {
	let py: PyodideInterface;

	beforeAll(async () => {
		py = await loadRuntime();
	}, 180_000);

	it.each(selected.map((q) => [q.id, q] as const))('%s: the starter as shipped', async (_id, q) => {
		const outcome = await runTests(py, q.starterCode ?? '', buildTestHarness(q));
		for (const text of everyTextShown(outcome)) {
			expect(internalsIn(text), `runner internals leaked into:\n${text}`).toBeNull();
		}
	});

	it.each(selected.map((q) => [q.id, q] as const))('%s: every function raises', async (_id, q) => {
		const outcome = await runTests(
			py,
			breakEveryFunction(q.oracleSolutionCode),
			buildTestHarness(q)
		);
		for (const text of everyTextShown(outcome)) {
			expect(internalsIn(text), `runner internals leaked into:\n${text}`).toBeNull();
		}
	});
});
