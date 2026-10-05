/* eslint-disable @typescript-eslint/no-explicit-any */
// Loads the libraries a question's code imports, on first use.
//
// The runtime itself only preloads NumPy (see initialize-pyodide.ts), so a
// question that imports pandas or matplotlib pays for them once, when the student
// first runs it, and every other question stays as light as before.
//
//  - Libraries Pyodide ships (pandas, matplotlib, scipy, scikit-learn, ...) are
//    found from the import statements by Pyodide itself.
//  - seaborn and plotly are pure Python but not in Pyodide's distribution. Their
//    wheels are served from this site (platform/static/wheels/, checksummed in
//    wheels.json) instead of PyPI, so there is no third-party lookup, the service
//    worker can cache them, and they work offline after the first visit. Pyodide
//    unpacks them into site-packages; what they import that Pyodide already ships is
//    loaded first.
//  - Matplotlib is switched to the headless Agg backend: there is no screen in a
//    worker, and tests inspect the figure's objects, not pixels.
//
// The versions match data/app_data/requirements-test.txt, so the content tests in CI
// run against the same libraries the browser installs.

export interface BundledWheels {
	/** Wheel files in platform/static/wheels/, in install order. */
	wheels: string[];
	/** Pyodide-provided packages they import, loaded before the wheels. */
	requires: string[];
}

export const BUNDLED_WHEELS: Record<string, BundledWheels> = {
	seaborn: {
		wheels: ['seaborn-0.13.2-py3-none-any.whl'],
		requires: ['numpy', 'pandas', 'matplotlib']
	},
	plotly: {
		wheels: ['narwhals-2.26.0-py3-none-any.whl', 'plotly-7.1.0-py3-none-any.whl'],
		requires: ['numpy', 'packaging']
	}
};

const IMPORT_STATEMENT = /^[ \t]*(?:import|from)[ \t]+([A-Za-z_][A-Za-z0-9_]*)/gm;

// Imported by every test file but never loaded as a package: the in-browser runner provides a
// small stand-in (pytest-shim.ts), and fetching the real pytest would pull in a dozen wheels.
const PROVIDED_BY_THE_RUNNER = new Set(['pytest']);

export function importedModules(...sources: string[]): Set<string> {
	const modules = new Set<string>();
	for (const source of sources) {
		for (const match of source.matchAll(IMPORT_STATEMENT)) {
			if (!PROVIDED_BY_THE_RUNNER.has(match[1])) modules.add(match[1]);
		}
	}
	return modules;
}

/**
 * Where the browser fetches a bundled wheel from. The site is served from the root of its
 * origin (svelte.config.js sets no paths.base), and in a production build the app's base
 * URL is relative ("./"), so the path is resolved against the origin, not against the worker.
 */
export function wheelUrl(file: string): string {
	return `${self.location.origin}/wheels/${file}`;
}

const installed = new WeakMap<object, Set<string>>();

/** Fetches a bundled wheel from this site (the service worker caches it after the first time). */
async function fetchWheel(file: string): Promise<ArrayBuffer> {
	const response = await fetch(wheelUrl(file));
	if (!response.ok) throw new Error(`Could not load ${file} (${response.status})`);
	return response.arrayBuffer();
}

/**
 * Installs the bundled wheels (seaborn, plotly) that `modules` import. They are pure
 * Python, so Pyodide unpacks them straight into site-packages with no dependency
 * resolution and no micropip. `read` returns a wheel's bytes: fetched from this site
 * in the browser, read from disk in the Node check.
 */
export async function installBundledWheels(
	py: any,
	modules: Set<string>,
	read: (file: string) => Promise<ArrayBuffer | Uint8Array> = fetchWheel
): Promise<void> {
	const done = installed.get(py) ?? new Set<string>();
	installed.set(py, done);
	const wanted = [...modules].filter((name) => name in BUNDLED_WHEELS && !done.has(name));
	if (wanted.length === 0) return;
	await py.loadPackage([...new Set(wanted.flatMap((name) => BUNDLED_WHEELS[name].requires))]);
	for (const name of wanted) {
		for (const file of BUNDLED_WHEELS[name].wheels) py.unpackArchive(await read(file), 'wheel');
		done.add(name);
	}
	py.invalidateCaches?.();
}

// Matplotlib has no screen in a worker, so switch it to the raster Agg backend.
export async function useHeadlessMatplotlib(py: any, modules: Set<string>): Promise<void> {
	if (modules.has('matplotlib') || modules.has('seaborn')) {
		await py.runPythonAsync("import matplotlib\nmatplotlib.use('Agg')");
	}
}

export async function ensurePackages(py: any, ...sources: string[]): Promise<void> {
	const modules = importedModules(...sources);
	await py.loadPackagesFromImports([...modules].map((name) => `import ${name}`).join('\n'));
	await installBundledWheels(py, modules);
	await useHeadlessMatplotlib(py, modules);
}
