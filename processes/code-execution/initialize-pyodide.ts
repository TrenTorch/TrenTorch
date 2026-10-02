/* eslint-disable @typescript-eslint/no-explicit-any */
import { SETUP_SCRIPT } from './pyodide-setup-script';

let pyodide: any = null;
let initPromise: Promise<any> | null = null;

export async function initializePyodide(): Promise<any> {
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
