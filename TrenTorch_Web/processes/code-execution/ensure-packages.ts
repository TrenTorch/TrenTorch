/* eslint-disable @typescript-eslint/no-explicit-any */
// Loads the libraries a question's code imports, on first use.
//
// The runtime itself only preloads NumPy (see initialize-pyodide.ts), so a
// question that imports pandas or matplotlib pays for them once, when the student
// first runs it, and every other question stays as light as before.
//
//  - Libraries Pyodide ships (pandas, matplotlib, scipy, scikit-learn, ...) are
//    found from the import statements by Pyodide itself.
//  - Libraries that are pure Python but not in Pyodide's distribution (seaborn,
//    plotly) are installed with micropip, pinned so a release cannot change what a
//    question does. Pyodide supplies their dependencies (pandas, matplotlib,
//    numpy) from its own build.
//  - Matplotlib is switched to the headless Agg backend: there is no screen in a
//    worker, and tests inspect the figure's objects, not pixels.
//
// The pins match data/app_data/requirements-test.txt, so the content tests in CI
// run against the same versions the browser installs.

export const MICROPIP_PACKAGES: Record<string, string> = {
	seaborn: 'seaborn==0.13.2',
	plotly: 'plotly==7.1.0'
};

const IMPORT_STATEMENT = /^[ \t]*(?:import|from)[ \t]+([A-Za-z_][A-Za-z0-9_]*)/gm;

export function importedModules(...sources: string[]): Set<string> {
	const modules = new Set<string>();
	for (const source of sources) {
		for (const match of source.matchAll(IMPORT_STATEMENT)) modules.add(match[1]);
	}
	return modules;
}

const installed = new WeakMap<object, Set<string>>();

// Installs the pinned pure-Python packages (seaborn, plotly) that `modules` import.
export async function installFromPyPI(py: any, modules: Set<string>): Promise<void> {
	const done = installed.get(py) ?? new Set<string>();
	installed.set(py, done);
	const missing = [...modules].filter((name) => name in MICROPIP_PACKAGES && !done.has(name));
	if (missing.length === 0) return;
	await py.loadPackage('micropip');
	const micropip = py.pyimport('micropip');
	await micropip.install(missing.map((name) => MICROPIP_PACKAGES[name]));
	missing.forEach((name) => done.add(name));
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
	await installFromPyPI(py, modules);
	await useHeadlessMatplotlib(py, modules);
}
