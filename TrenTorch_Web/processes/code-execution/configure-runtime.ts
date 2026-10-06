/* eslint-disable @typescript-eslint/no-explicit-any */

// Settings applied to a freshly loaded Pyodide, in one place so the worker and
// pyodide-check/ configure the runtime the same way.
export function configureRuntime(py: any): void {
	// The browser has no stdin to read. Left alone, input() waits on a prompt that a
	// Web Worker cannot show. Reporting end-of-input makes it raise
	// `EOFError: EOF when reading a line`, which is exactly what Python does when
	// run with no terminal attached, and the student can act on that.
	py.setStdin({ stdin: () => null });
}
