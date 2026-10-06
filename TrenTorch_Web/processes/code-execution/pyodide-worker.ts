// Web Worker for Pyodide execution in TrenTorch-Web. Kept as one file
// rather than split further: a Web Worker needs exactly one entry file
// registered as the worker script (see pyodide-service.ts's `new
// Worker(new URL('./pyodide-worker.ts', ...))`), so the self.onmessage
// dispatch below can't be pulled into separate files the way
// initializePyodide and toBase64 (genuinely independent, stateless
// helpers) were.
/* eslint-disable @typescript-eslint/no-explicit-any */
import { initializePyodide } from './initialize-pyodide';
import { buildTestRunnerScript } from './build-test-runner-script';
import { buildCustomRunScript } from './build-custom-run-script';
import { buildRunScript } from './build-run-script';
import { sanitizeStudentCode } from './sanitize-student-code';
import { toBase64 } from './to-base64';
import { ensurePackages } from './ensure-packages';
import { describePackageFailure, describeWorkerFailure } from './describe-failures';
import { buildPreviewScript } from './build-preview-script';

// Fetches whatever the code (and the question's tests) import before anything
// runs. A failed download is a problem the student can act on, so it is returned
// as the result of the run, in the shape a Python error would have, rather than
// thrown as a worker failure. Returns false once it has reported one.
async function loadPackagesOrReport(
	py: any,
	id: number,
	action: 'run' | 'custom' | 'test' | 'preview',
	sources: string[],
	testFields: Record<string, unknown> = {}
): Promise<boolean> {
	self.postMessage({ type: 'status', status: 'loading_packages' });
	try {
		await ensurePackages(py, ...sources);
		return true;
	} catch (cause: any) {
		const error = describePackageFailure(sources, cause);
		if (action === 'test') {
			self.postMessage({
				id,
				type: 'test_result',
				...testFields,
				allPassed: false,
				totalTests: 0,
				passedTests: 0,
				failedTests: 0,
				totalDurationMs: 0,
				results: [],
				rawOutput: '',
				error
			});
		} else if (action === 'preview') {
			self.postMessage({
				id,
				type: 'preview_result',
				output: '',
				error,
				figures: [],
				durationMs: 0
			});
		} else {
			self.postMessage({
				id,
				type: 'run_result',
				success: false,
				output: '',
				error,
				durationMs: 0
			});
		}
		self.postMessage({ type: 'status', status: 'ready' });
		return false;
	}
}

self.onmessage = async (e: MessageEvent) => {
	// Origin verification — only trust messages from the same origin as this worker.
	// `'null'` covers blob: and data: URLs that some bundlers use in development.
	const trustedOrigins = new Set([self.location.origin, 'null']);
	const messageOrigin = typeof e.origin === 'string' ? e.origin : '';
	if (messageOrigin && !trustedOrigins.has(messageOrigin)) {
		self.postMessage({ type: 'error', error: `Untrusted message origin: ${messageOrigin}` });
		return;
	}

	const {
		id,
		action,
		code,
		testHarnessCode,
		contentId,
		sampleLimit,
		functionName,
		argumentsJson,
		expectedJson,
		previewCode
	} = e.data;

	try {
		const py = await initializePyodide();

		if (action === 'init') {
			self.postMessage({ id, type: 'init_complete', success: true });
			return;
		}

		if (action === 'run') {
			if (!(await loadPackagesOrReport(py, id, action, [code || '']))) return;
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();
			const rawResult = await py.runPythonAsync(buildRunScript({ codeB64: toBase64(code || '') }));
			const parsed = JSON.parse(rawResult);
			const durationMs = Math.round(performance.now() - startTime);

			self.postMessage({
				id,
				type: 'run_result',
				success: !parsed.error,
				output: parsed.stdout + (parsed.stderr ? '\n[STDERR]\n' + parsed.stderr : ''),
				error: parsed.error,
				durationMs
			});
			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}

		if (action === 'preview') {
			if (!(await loadPackagesOrReport(py, id, action, [code || '', previewCode || '']))) return;
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();
			const rawResult = await py.runPythonAsync(
				buildPreviewScript({
					codeB64: toBase64(sanitizeStudentCode(code || '')),
					previewB64: toBase64(previewCode || '')
				})
			);
			const parsed = JSON.parse(rawResult);
			self.postMessage({
				id,
				type: 'preview_result',
				output: parsed.stdout + (parsed.stderr ? '\n[STDERR]\n' + parsed.stderr : ''),
				error: parsed.error || undefined,
				figures: parsed.figures || [],
				durationMs: Math.round(performance.now() - startTime)
			});
			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}

		if (action === 'custom') {
			if (!(await loadPackagesOrReport(py, id, action, [code || '', testHarnessCode || ''])))
				return;
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();
			const script = buildCustomRunScript({
				codeB64: toBase64(sanitizeStudentCode(code || '')),
				testB64: toBase64(testHarnessCode || ''),
				functionB64: toBase64(functionName || ''),
				argumentsB64: toBase64(argumentsJson || '[]'),
				expectedB64: toBase64(expectedJson || '')
			});
			const rawResult = await py.runPythonAsync(script);
			const parsed = JSON.parse(rawResult);

			self.postMessage({
				id,
				type: 'run_result',
				success: Boolean(parsed.success),
				output: parsed.output || '',
				error: parsed.error || undefined,
				durationMs: Math.round(performance.now() - startTime)
			});
			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}

		if (action === 'test') {
			// "Run" passes a small number here to execute only the first few
			// visible checks; "Submit" passes nothing and runs the whole suite.
			const isSample = typeof sampleLimit === 'number' && sampleLimit > 0;
			if (
				!(await loadPackagesOrReport(py, id, action, [code || '', testHarnessCode || ''], {
					contentId,
					isSample
				}))
			)
				return;
			self.postMessage({ type: 'status', status: 'testing' });
			const startTime = performance.now();
			const codeB64 = toBase64(code || '');
			const testB64 = toBase64(testHarnessCode || '');
			const limitArg = isSample ? String(sampleLimit) : '';

			const testRunnerScript = buildTestRunnerScript({ codeB64, testB64, limitArg });

			const rawResult = await py.runPythonAsync(testRunnerScript);
			const parsed = JSON.parse(rawResult);
			const durationMs = Math.round(performance.now() - startTime);

			const testResults = (parsed.results || []).map((t: any) => ({
				name: t.name,
				passed: Boolean(t.passed),
				durationMs: t.durationMs || 1,
				error: t.error || undefined
			}));

			const passedCount = testResults.filter((t: any) => t.passed).length;
			const totalCount = testResults.length;
			const allPassed = !parsed.error && totalCount > 0 && passedCount === totalCount;

			self.postMessage({
				id,
				type: 'test_result',
				contentId,
				isSample,
				allPassed,
				totalTests: totalCount,
				passedTests: passedCount,
				failedTests: totalCount - passedCount,
				totalDurationMs: durationMs,
				results: testResults,
				rawOutput: parsed.stdout + (parsed.stderr ? '\n' + parsed.stderr : ''),
				error: parsed.error
			});
			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}
	} catch (err: any) {
		self.postMessage({
			id,
			type: 'error',
			error: describeWorkerFailure(err)
		});
		self.postMessage({ type: 'status', status: 'ready' });
	}
};

export {};
