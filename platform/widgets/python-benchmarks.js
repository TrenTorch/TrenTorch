/** @type {ReturnType<import('pyodide').loadPyodide> | undefined} */
let runtimePromise;

/** @returns {Promise<import('pyodide').PyodideInterface>} */
async function getRuntime() {
	if (!runtimePromise) {
		const { loadPyodide } = await import('pyodide');
		runtimePromise = loadPyodide({
			indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.2/full/'
		});
	}
	return runtimePromise;
}

/**
 * Executes the supplied benchmark in the browser's Pyodide runtime.
 * @param {string} source
 * @param {string[]} [packages]
 */
export async function runPythonBenchmark(source, packages = []) {
	const runtime = await getRuntime();
	if (packages.length > 0) await runtime.loadPackage(packages);
	await runtime.runPythonAsync(source);
	return {
		firstMs: Number(runtime.runPython('first_ms')),
		secondMs: Number(runtime.runPython('second_ms')),
		firstResult: Number(runtime.runPython('first_result')),
		secondResult: Number(runtime.runPython('second_result'))
	};
}
