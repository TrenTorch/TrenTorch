// Web Worker for Pyodide execution in TrenTorch-Web. Kept as one file
// rather than split further: a Web Worker needs exactly one entry file
// registered as the worker script (see pyodide-service.ts's `new
// Worker(new URL('./pyodide-worker.ts', ...))`), so the self.onmessage
// dispatch below can't be pulled into separate files the way
// initializePyodide and toBase64 (genuinely independent, stateless
// helpers) were.
/* eslint-disable @typescript-eslint/no-explicit-any */
import { SETUP_SCRIPT } from './pyodide-setup-script';
import { initializePyodide } from './initialize-pyodide';
import { toBase64 } from './to-base64';

self.onmessage = async (e: MessageEvent) => {
	// Origin verification — only trust messages from the same origin as this worker.
	// `'null'` covers blob: and data: URLs that some bundlers use in development.
	const trustedOrigins = new Set([self.location.origin, 'null']);
	const messageOrigin = typeof e.origin === 'string' ? e.origin : '';
	if (messageOrigin && !trustedOrigins.has(messageOrigin)) {
		self.postMessage({ type: 'error', error: `Untrusted message origin: ${messageOrigin}` });
		return;
	}

	const { id, action, code, testHarnessCode, contentId, sampleLimit } = e.data;

	try {
		const py = await initializePyodide();

		if (action === 'init') {
			self.postMessage({ id, type: 'init_complete', success: true });
			return;
		}

		if (action === 'run') {
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();
			const codeB64 = toBase64(code || '');

			// Prepare Python runner script with base64 decode and output capture.
			// Prefixed with SETUP_SCRIPT -- see its comment for why this script
			// can't just rely on that having already run once.
			const pythonScript = `${SETUP_SCRIPT}

def __run_user_code():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        try:
            raw_code = base64.b64decode("${codeB64}").decode("utf-8")
            exec(raw_code, exec_globals)
            err = None
        except Exception as e:
            err = traceback.format_exc()
        return {
            "stdout": cap.get_stdout(),
            "stderr": cap.get_stderr(),
            "error": err
        }

json.dumps(__run_user_code())
`;
			const rawResult = await py.runPythonAsync(pythonScript);
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

		if (action === 'test') {
			self.postMessage({ type: 'status', status: 'testing' });
			const startTime = performance.now();
			const codeB64 = toBase64(code || '');
			const testB64 = toBase64(testHarnessCode || '');
			// "Run" passes a small number here to execute only the first few
			// visible checks; "Submit" passes nothing and runs the whole suite.
			const isSample = typeof sampleLimit === 'number' && sampleLimit > 0;
			const limitArg = isSample ? String(sampleLimit) : '';

			const testRunnerScript = `${SETUP_SCRIPT}

def __run_module_tests():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        results = []
        raw_error = None
        try:
            # 1. Execute student code
            raw_code = base64.b64decode("${codeB64}").decode("utf-8")
            exec(raw_code, exec_globals)

            # 2. Execute test harness
            raw_test = base64.b64decode("${testB64}").decode("utf-8")
            exec(raw_test, exec_globals)

            # 3. Call run_tests()
            if "run_tests" in exec_globals and callable(exec_globals["run_tests"]):
                results = exec_globals["run_tests"](${limitArg})
            else:
                raw_error = "Test harness does not contain a run_tests() function."
        except Exception as e:
            raw_error = traceback.format_exc()

        return {
            "stdout": cap.get_stdout(),
            "stderr": cap.get_stderr(),
            "error": raw_error,
            "results": results
        }

json.dumps(__run_module_tests())
`;

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
			error: err?.message || String(err)
		});
		self.postMessage({ type: 'status', status: 'ready' });
	}
};

export {};
