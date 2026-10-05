// Web Worker for the SQL questions. It runs the real SQLite engine that ships
// with Pyodide (the `sqlite3` module), so a student gets SQLite's own parsing,
// planner and error messages. The Python half lives in sql-runtime.py, which the
// content tests import as well; this file only moves strings in and out.
//
// Student code, the schema and the tests are handed to Python as variables
// (py.globals.set), never spliced into Python source, so no query text can break
// out of a string literal.
/* eslint-disable @typescript-eslint/no-explicit-any */
import { initializePyodide } from './initialize-pyodide';
import SQL_RUNTIME from './sql-runtime.py?raw';

let runtimeReady: Promise<any> | null = null;

function loadRuntime(): Promise<any> {
	runtimeReady ??= (async () => {
		const py = await initializePyodide(['sqlite3'], false);
		await py.runPythonAsync(SQL_RUNTIME);
		return py;
	})();
	return runtimeReady;
}

async function callPython(py: any, expression: string, values: Record<string, string>) {
	for (const [name, value] of Object.entries(values)) py.globals.set(name, value);
	try {
		return JSON.parse(await py.runPythonAsync(expression));
	} finally {
		for (const name of Object.keys(values)) py.globals.delete(name);
	}
}

self.onmessage = async (e: MessageEvent) => {
	const trustedOrigins = new Set([self.location.origin, 'null']);
	const messageOrigin = typeof e.origin === 'string' ? e.origin : '';
	if (messageOrigin && !trustedOrigins.has(messageOrigin)) {
		self.postMessage({ type: 'error', error: `Untrusted message origin: ${messageOrigin}` });
		return;
	}

	const { id, action, query, dbSchema, testCode, contentId } = e.data;

	try {
		const py = await loadRuntime();

		if (action === 'init') {
			self.postMessage({ id, type: 'init_complete', success: true });
			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}

		if (action === 'run') {
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();
			try {
				const result = await callPython(py, 'entry_run(__sql_query, __sql_schema)', {
					__sql_query: query ?? '',
					__sql_schema: dbSchema ?? ''
				});
				self.postMessage({
					id,
					type: 'run_result',
					success: !result.error,
					output: result.output,
					error: result.error || undefined,
					durationMs: Math.round(performance.now() - startTime)
				});
			} catch (err: any) {
				self.postMessage({
					id,
					type: 'run_result',
					success: false,
					output: '',
					error: err?.message || String(err),
					durationMs: Math.round(performance.now() - startTime)
				});
			}
			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}

		if (action === 'test') {
			self.postMessage({ type: 'status', status: 'testing' });
			const startTime = performance.now();
			let parsed: any;
			try {
				parsed = await callPython(py, 'entry_test(__sql_query, __sql_schema, __sql_tests)', {
					__sql_query: query ?? '',
					__sql_schema: dbSchema ?? '',
					__sql_tests: testCode ?? ''
				});
			} catch (err: any) {
				parsed = { results: [], error: err?.message || String(err) };
			}
			const results: any[] = (parsed.results ?? []).map((r: any) => ({
				name: r.name,
				passed: r.passed,
				durationMs: r.durationMs ?? 0,
				error: r.error ?? undefined,
				expected: r.expected ?? undefined,
				actual: r.actual ?? undefined
			}));
			const passed = results.filter((r) => r.passed).length;
			const failed = results.length - passed;
			self.postMessage({
				id,
				type: 'test_result',
				contentId,
				totalTests: results.length,
				passedTests: passed,
				failedTests: failed,
				allPassed: results.length > 0 && failed === 0 && !parsed.error,
				totalDurationMs: Math.round(performance.now() - startTime),
				results,
				rawOutput: results
					.map((r) => `${r.passed ? 'PASS' : 'FAIL'} ${r.name}${r.error ? `\n${r.error}` : ''}`)
					.join('\n'),
				error: parsed.error || undefined,
				isSample: false
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
