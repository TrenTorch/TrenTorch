/* eslint-disable @typescript-eslint/no-explicit-any */
import { importedModules } from './ensure-packages';

// What the student reads when the problem is not in their code. Their own errors
// come back as results (see python-error-format.ts); these two are for the runtime
// failing, which still has to say something they can act on. Separate from the
// worker so they can be tested without a worker.

// A download failed. The packages named are the non-numpy modules the code imports,
// which are the ones fetched on demand.
export function describePackageFailure(sources: string[], cause: any): string {
	const names = [...importedModules(...sources)].filter((name) => name !== 'numpy');
	const detail = String(cause?.message ?? cause)
		.trim()
		.split('\n')
		.pop();
	return (
		'Could not download the Python packages that your code imports' +
		(names.length > 0 ? ` (${names.join(', ')})` : '') +
		'. Check your internet connection and run it again.' +
		(detail ? `\n(${detail})` : '')
	);
}

// Anything that reaches the worker's catch-all is the runtime itself failing. Pyodide's
// own message for that is a Python traceback through its internals; its last line is the
// part that says what went wrong.
export function describeWorkerFailure(err: any): string {
	const message = String(err?.message || err || '').trim();
	const lastLine = message.split('\n').pop()?.trim() || message;
	return `The Python runtime hit an unexpected problem and could not finish: ${lastLine}\nTry running again. If it keeps happening, reload the page.`;
}
