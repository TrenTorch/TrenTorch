import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, it, expect, beforeAll } from 'vitest';
import { loadPyodide, type PyodideInterface } from 'pyodide';
import { curriculum as generated } from 'virtual:curriculum/bundle';
import { buildTestHarness } from '$processes/ide-content/build-test-harness';
import { sanitizeStudentCode } from '$processes/code-execution/sanitize-student-code';
import { buildTestRunnerScript } from '$processes/code-execution/build-test-runner-script';
import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';

// The DSA-sheet "make it fast" questions hand the student a correct but slow starter. This check
// runs that starter in real Pyodide through the real harness and requires a clean
// "Time limit exceeded" within a few seconds. Without the cut-off the browser's 20 second
// hard stop would show instead, with no per-test results.
//
// The reference solutions passing is checked by questions.spec.ts for every question.

const projectRoot = join(import.meta.dirname, '..');
const toBase64 = (text: string) => Buffer.from(text, 'utf8').toString('base64');

// Questions outside "make it fast" that also hand the student a slow starter.
const SLOW_STARTER_IDS = ['sheet-count-in-range', 'sheet-count-inversions'];

const slowStarters = (
	generated.roots.flatMap((root) =>
		root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
	) as GeneratedQuestion[]
).filter(
	(q) => q.kind === 'dsa' && (q.track === 'make-it-fast' || SLOW_STARTER_IDS.includes(q.id))
);

// Longest a slow starter may take to be stopped. The browser kills a run at 20 seconds.
const MAX_SECONDS = 15;

describe('DSA sheet starters that are too slow', () => {
	let py: PyodideInterface;
	beforeAll(async () => {
		// The harness setup imports numpy, which the app preloads. Same CDN as questions.spec.ts.
		const core = join(projectRoot, 'node_modules', 'pyodide') + '/';
		const lock = JSON.parse(readFileSync(join(core, 'pyodide-lock.json'), 'utf8'));
		const { version } = JSON.parse(readFileSync(join(core, 'package.json'), 'utf8'));
		py = await loadPyodide({ indexURL: core });
		await py.loadPackage(
			`https://cdn.jsdelivr.net/pyodide/v${version}/full/${lock.packages.numpy.file_name}`
		);
	});

	it('finds the slow starters', () => {
		expect(slowStarters.length).toBeGreaterThanOrEqual(7);
	});

	it.each(slowStarters.map((q) => [q.id, q] as const))(
		'%s fails with Time limit exceeded, quickly',
		async (_id, question) => {
			const code = sanitizeStudentCode(question.starterCode ?? '');
			const harness = buildTestHarness(question);
			const started = performance.now();
			const raw = await py.runPythonAsync(
				buildTestRunnerScript({ codeB64: toBase64(code), testB64: toBase64(harness), limitArg: '' })
			);
			const seconds = (performance.now() - started) / 1000;
			const { results } = JSON.parse(raw as string) as {
				results: { name: string; passed: boolean; error: string | null }[];
			};
			const failures = results.filter((r) => !r.passed);
			expect(
				failures.some((r) => /Time limit exceeded/.test(r.error ?? '')),
				`no Time limit exceeded; first failure: ${failures[0]?.error}`
			).toBe(true);
			// Every example and hidden small case still passes: the slow code is correct.
			expect(failures.every((r) => /^test_\d+_perf_/.test(r.name))).toBe(true);
			expect(seconds).toBeLessThan(MAX_SECONDS);
		}
	);
});
