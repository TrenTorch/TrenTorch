import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { loadPyodide, type PyodideInterface } from 'pyodide';
import generated from '$data/curriculum/generated-curriculum.json';
import { buildTestHarness } from '$processes/ide-content/build-test-harness';
import { sanitizeStudentCode } from '$processes/code-execution/sanitize-student-code';
import { buildTestRunnerScript } from '$processes/code-execution/build-test-runner-script';
import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';

// Runs every code question's tests in real Pyodide, the way the browser does.
//
// Why: the tests are real pytest files and pass under CPython in CI, but
// students run them in Pyodide, which has different modules and no files on
// disk. A question can be fine under pytest and crash in the browser (for
// example `import pytest`, which Pyodide does not have). Nothing else in CI
// executes a question in that runtime.
//
// How: for each question the reference solution stands in for the student's
// code, passed through sanitizeStudentCode exactly as the app does, so any
// dependency code and renamed imports come from the test harness the way they
// do in the browser. The script that runs it is the one pyodide-worker.ts
// uses for the 'test' action (build-test-runner-script.ts). A question passes when every test passes.
//
// Known failures live in known-failures.json. A question that fails and is not
// listed fails this check, and so does a listed question that now passes, so the
// list can only shrink. To rewrite it after an intentional change:
//   PYODIDE_WRITE_BASELINE=1 npm run test:pyodide
//
// Limits: the stand-in is the reference solution, so a question can also fail
// here for a reason a real student would not hit. The list records reasons so
// each one can be looked at.

const projectRoot = join(import.meta.dirname, '..');
const KNOWN_PATH = join(import.meta.dirname, 'known-failures.json');
const WRITE_BASELINE = Boolean(process.env.PYODIDE_WRITE_BASELINE);
const CDN = 'https://cdn.jsdelivr.net/pyodide';

interface Outcome {
	ok: boolean;
	message: string;
}

type Question = GeneratedQuestion & { type?: string };

const questions = (
	generated.sections.flatMap((section) =>
		section.tracks.flatMap((track) => track.questions)
	) as unknown as Question[]
).filter((q) => q.type !== 'canvas');

// PYODIDE_ONLY=id1,id2 runs just those questions (for looking into one).
const only = process.env.PYODIDE_ONLY?.split(',').filter(Boolean);
const known: Record<string, string> = JSON.parse(readFileSync(KNOWN_PATH, 'utf8'));
const observed: Record<string, string> = {};

const toBase64 = (text: string) => Buffer.from(text, 'utf8').toString('base64');

async function runQuestion(py: PyodideInterface, question: Question): Promise<Outcome> {
	const raw = await py.runPythonAsync(
		buildTestRunnerScript({
			codeB64: toBase64(sanitizeStudentCode(question.oracleSolutionCode)),
			testB64: toBase64(buildTestHarness(question)),
			limitArg: ''
		})
	);
	const parsed = JSON.parse(raw as string) as {
		error: string | null;
		results: { name: string; passed: boolean; error: string | null }[];
	};
	const passed = parsed.results.filter((r) => r.passed).length;
	if (!parsed.error && parsed.results.length > 0 && passed === parsed.results.length) {
		return { ok: true, message: '' };
	}
	const failing = parsed.results.filter((r) => !r.passed);
	const reason = parsed.error
		? (parsed.error.trim().split('\n').pop() ?? parsed.error)
		: failing.length > 0
			? failing
					.slice(0, 3)
					.map((r) => `${r.name}: ${String(r.error ?? '').split('\n')[0] || '(no message)'}`)
					.join(' | ')
			: 'no tests were collected';
	return {
		ok: false,
		message: `${passed}/${parsed.results.length} tests passed. ${reason}`.slice(0, 400)
	};
}

async function loadRuntime(): Promise<PyodideInterface> {
	const core = join(projectRoot, 'node_modules', 'pyodide') + '/';
	const lock = JSON.parse(readFileSync(join(core, 'pyodide-lock.json'), 'utf8'));
	const { version } = JSON.parse(readFileSync(join(core, 'package.json'), 'utf8'));
	const py = await loadPyodide({ indexURL: core });
	// The core comes from the npm package; numpy is fetched from the same CDN the
	// app uses. Retried because a single CDN hiccup should not fail the whole check.
	const url = `${CDN}/v${version}/full/${lock.packages.numpy.file_name}`;
	let lastError: unknown;
	for (let attempt = 1; attempt <= 3; attempt++) {
		try {
			await py.loadPackage(url);
			return py;
		} catch (error) {
			lastError = error;
			await new Promise((resolve) => setTimeout(resolve, 2000 * attempt));
		}
	}
	throw new Error(`Could not load numpy from ${url}: ${String(lastError)}`);
}

describe('the browser runtime matches what the app loads', () => {
	it('uses the same Pyodide version as processes/code-execution/initialize-pyodide.ts', () => {
		const installed = JSON.parse(
			readFileSync(join(projectRoot, 'node_modules', 'pyodide', 'package.json'), 'utf8')
		).version;
		const source = readFileSync(
			join(projectRoot, 'processes', 'code-execution', 'initialize-pyodide.ts'),
			'utf8'
		);
		const inApp = [...source.matchAll(/pyodide\/v([0-9.]+)\/full/g)].map((m) => m[1]);
		expect(inApp.length).toBeGreaterThan(0);
		expect(new Set(inApp)).toEqual(new Set([installed]));
	});
});

describe('every code question runs in Pyodide', () => {
	let py: PyodideInterface;

	beforeAll(async () => {
		py = await loadRuntime();
	});

	afterAll(() => {
		if (!WRITE_BASELINE) return;
		const sorted = Object.fromEntries(
			Object.entries(observed).sort(([a], [b]) => a.localeCompare(b))
		);
		writeFileSync(KNOWN_PATH, JSON.stringify(sorted, null, '\t') + '\n');
	});

	it.each(questions.filter((q) => !only || only.includes(q.id)).map((q) => [q.id, q] as const))(
		'%s',
		async (id, question) => {
			const outcome = await runQuestion(py, question);
			if (WRITE_BASELINE) {
				if (!outcome.ok) observed[id] = outcome.message;
				return;
			}
			// Looking into specific questions: fail with the full detail instead of
			// comparing against the list.
			if (only) {
				expect(outcome.ok, `${id}: ${outcome.message}`).toBe(true);
				return;
			}
			if (id in known) {
				expect(
					outcome.ok,
					`${id} is in known-failures.json but now passes in Pyodide. Remove it from the list.`
				).toBe(false);
			} else {
				expect(outcome.ok, `${id} fails in Pyodide. ${outcome.message}`).toBe(true);
			}
		}
	);
});

describe('known-failures.json', () => {
	it('only lists questions that exist', () => {
		const ids = new Set(questions.map((q) => q.id));
		expect(Object.keys(known).filter((id) => !ids.has(id))).toEqual([]);
	});
});
