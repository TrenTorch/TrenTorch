import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { loadPyodide, type PyodideInterface } from 'pyodide';
import { configureRuntime } from '$processes/code-execution/configure-runtime';
import {
	importedModules,
	installBundledWheels,
	useHeadlessMatplotlib
} from '$processes/code-execution/ensure-packages';
import { buildPreviewScript } from '$processes/code-execution/build-preview-script';
import { buildRunScript } from '$processes/code-execution/build-run-script';
import { buildCustomRunScript } from '$processes/code-execution/build-custom-run-script';
import { buildTestRunnerScript } from '$processes/code-execution/build-test-runner-script';
import { sanitizeStudentCode } from '$processes/code-execution/sanitize-student-code';

// Shared by the specs in this folder: a Pyodide set up the way the worker sets it
// up, and the three ways the worker runs code, driven through the same script
// builders and package loader the app uses.

const projectRoot = join(import.meta.dirname, '..');
const CDN = 'https://cdn.jsdelivr.net/pyodide';

export async function loadRuntime(): Promise<PyodideInterface> {
	const core = join(projectRoot, 'node_modules', 'pyodide') + '/';
	const { version } = JSON.parse(readFileSync(join(core, 'package.json'), 'utf8'));
	// The npm package has the runtime but not the wheels; they come from the same
	// CDN the app uses. Retried because one CDN hiccup should not fail the run.
	let lastError: unknown;
	for (let attempt = 1; attempt <= 3; attempt++) {
		try {
			const py = await loadPyodide({ indexURL: core, packageBaseUrl: `${CDN}/v${version}/full/` });
			configureRuntime(py);
			await py.loadPackage('numpy');
			return py;
		} catch (error) {
			lastError = error;
			await new Promise((resolve) => setTimeout(resolve, 2000 * attempt));
		}
	}
	throw new Error(`Could not load Pyodide: ${String(lastError)}`);
}

// What the worker's ensurePackages (ensure-packages.ts) does, except that the bundled
// wheels are read from platform/static/wheels instead of fetched from the site.
export async function ensureLibraries(py: PyodideInterface, sources: string[]): Promise<void> {
	const modules = importedModules(...sources);
	await py.loadPackagesFromImports([...modules].map((name) => `import ${name}`).join('\n'));
	await installBundledWheels(
		py,
		modules,
		async (file) =>
			new Uint8Array(readFileSync(join(projectRoot, 'platform', 'static', 'wheels', file)))
	);
	await useHeadlessMatplotlib(py, modules);
}

const toBase64 = (text: string) => Buffer.from(text, 'utf8').toString('base64');

export interface RunOutcome {
	stdout: string;
	stderr: string;
	error: string | null;
}

// The worker's 'run' action: load what the code imports, then run it.
export async function runCode(py: PyodideInterface, code: string): Promise<RunOutcome> {
	const source = sanitizeStudentCode(code);
	await ensureLibraries(py, [source]);
	return JSON.parse(
		(await py.runPythonAsync(buildRunScript({ codeB64: toBase64(source) }))) as string
	);
}

export interface TestOutcome {
	stdout: string;
	stderr: string;
	error: string | null;
	results: { name: string; passed: boolean; error: string | null }[];
}

// The worker's 'test' action.
export async function runTests(
	py: PyodideInterface,
	code: string,
	harness: string,
	limit = ''
): Promise<TestOutcome> {
	const source = sanitizeStudentCode(code);
	await ensureLibraries(py, [source, harness]);
	return JSON.parse(
		(await py.runPythonAsync(
			buildTestRunnerScript({
				codeB64: toBase64(source),
				testB64: toBase64(harness),
				limitArg: limit
			})
		)) as string
	);
}

export interface PreviewOutcome {
	stdout: string;
	stderr: string;
	error: string | null;
	figures: { kind: string }[];
}

// The worker's 'preview' action: the student's code, then the question's preview.py.
export async function runPreview(
	py: PyodideInterface,
	code: string,
	previewCode: string
): Promise<PreviewOutcome> {
	const source = sanitizeStudentCode(code);
	await ensureLibraries(py, [source, previewCode]);
	return JSON.parse(
		(await py.runPythonAsync(
			buildPreviewScript({ codeB64: toBase64(source), previewB64: toBase64(previewCode) })
		)) as string
	);
}

export interface CustomOutcome {
	output: string;
	error: string | null;
	success: boolean;
}

// The worker's 'custom' action: call one function with JSON arguments.
export async function runCustom(
	py: PyodideInterface,
	code: string,
	harness: string,
	call: { functionName: string; argumentsJson?: string; expectedJson?: string }
): Promise<CustomOutcome> {
	const source = sanitizeStudentCode(code);
	await ensureLibraries(py, [source, harness]);
	return JSON.parse(
		(await py.runPythonAsync(
			buildCustomRunScript({
				codeB64: toBase64(source),
				testB64: toBase64(harness),
				functionB64: toBase64(call.functionName),
				argumentsB64: toBase64(call.argumentsJson ?? '[]'),
				expectedB64: toBase64(call.expectedJson ?? '')
			})
		)) as string
	);
}

// Things that only exist in the runner. If any of these shows up in text a
// student is shown, the runner is leaking its own internals.
const INTERNALS =
	/<exec>|__run_user_code|__run_module_tests|__run_custom_case|_pyodide|\/lib\/python3|webloop|exec_globals|user_error_text|compile_user_code|_call_test|PythonError|pyodide\.asm|<string>/;

export function internalsIn(text: string | null | undefined): string | null {
	const match = text ? INTERNALS.exec(text) : null;
	return match ? match[0] : null;
}
