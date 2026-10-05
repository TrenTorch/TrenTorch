/* eslint-disable @typescript-eslint/no-explicit-any */
import { SETUP_SCRIPT } from './pyodide-setup-script';

let pyodide: any = null;
let initPromise: Promise<any> | null = null;

// `packages` and `runSetup` let the SQL worker boot a lighter runtime (just the
// sqlite3 module, no NumPy, no Python test-capture setup). Each worker calls this
// with the same arguments every time, so the cached instance is always the right one.
export async function initializePyodide(
	packages: string[] = ['numpy'],
	runSetup = true
): Promise<any> {
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
		await pyodide.loadPackage(packages);

		// Setup standard capture harness in python
		if (runSetup) await pyodide.runPythonAsync(SETUP_SCRIPT);

		self.postMessage({ type: 'status', status: 'ready' });
		return pyodide;
	})();

	return initPromise;
}
