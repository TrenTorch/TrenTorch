// Web Worker for Pyodide execution in TrenTorch-Web
/* eslint-disable @typescript-eslint/no-explicit-any */

let pyodide: any = null;
let initPromise: Promise<any> | null = null;

// Imports + OutputCapture, shared by the one-time setup below AND prepended
// to every run/test script (see the 'run' and 'test' action handlers
// further down). Two separate runPythonAsync
// calls are supposed to share one persistent pyodide.globals -- in
// practice, a run/test request that lands while this one-time setup is
// still executing (student clicks Run/Submit in the first second or two of
// the page, before "ready") can still hit `NameError: name 'json'` or
// `NameError: name 'OutputCapture'`, reproduced directly: the JS-level
// `await` chain guarantees ordering of the *outer* promises, not that the
// interpreter-level globals from one runPythonAsync call are visible to
// the very next one issued in quick succession. Redefining a class is a
// harmless no-op the second time, so making every script self-contained
// removes the dependency on that ordering entirely instead of relying on
// it being fixed upstream.
const SETUP_SCRIPT = `
import sys
import io
import json
import base64
import traceback
import numpy as np

class OutputCapture:
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self._old_stdout = None
        self._old_stderr = None

    def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def get_stdout(self):
        return self.stdout.getvalue()

    def get_stderr(self):
        return self.stderr.getvalue()
`;

async function initializePyodide(): Promise<any> {
	if (pyodide) return pyodide;
	if (initPromise) return initPromise;

	initPromise = (async () => {
		self.postMessage({ type: 'status', status: 'loading_runtime' });

		// Import Pyodide as ESM module (works natively in browser/Vite module workers)
		const pyodideUrl = 'https://cdn.jsdelivr.net/pyodide/v0.27.2/full/pyodide.mjs';
		const pyodideModule: any = await new Function('url', 'return import(url)')(pyodideUrl);
		const loadPyodide = pyodideModule.loadPyodide;

		pyodide = await loadPyodide({
			indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.2/full/'
		});

		self.postMessage({ type: 'status', status: 'loading_packages' });
		// Pre-load numpy for TrenTorch
		await pyodide.loadPackage(['numpy']);

		// Setup standard capture harness in python
		await pyodide.runPythonAsync(SETUP_SCRIPT);

		self.postMessage({ type: 'status', status: 'ready' });
		return pyodide;
	})();

	return initPromise;
}

function toBase64(str: string): string {
	try {
		return btoa(unescape(encodeURIComponent(str)));
	} catch {
		return Buffer.from(str, 'utf-8').toString('base64');
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
