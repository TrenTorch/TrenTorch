import { describe, it, expect } from 'vitest';
import { describePackageFailure, describeWorkerFailure } from './describe-failures';

describe('describePackageFailure', () => {
	it('names what the code imports, leaving out numpy, and says what to do', () => {
		const text = describePackageFailure(
			['import numpy as np\nimport seaborn as sns\nfrom pandas import DataFrame'],
			new Error('Failed to fetch')
		);
		expect(text).toBe(
			'Could not download the Python packages that your code imports (seaborn, pandas). ' +
				'Check your internet connection and run it again.\n(Failed to fetch)'
		);
	});

	it('still reads sensibly when nothing but numpy is imported', () => {
		const text = describePackageFailure(['import numpy as np'], 'offline');
		expect(text).toContain('Could not download the Python packages that your code imports.');
		expect(text).toContain('(offline)');
	});

	it('looks at the question tests too, not only the student code', () => {
		expect(
			describePackageFailure(['x = 1', 'import plotly.express as px'], new Error('x'))
		).toContain('(plotly)');
	});
});

describe('describeWorkerFailure', () => {
	it('keeps only the last line of a Pyodide traceback', () => {
		const text = describeWorkerFailure(
			new Error(
				'PythonError: Traceback (most recent call last):\n  File "/lib/python312.zip/_pyodide/_base.py", line 597, in eval_code_async\nMemoryError'
			)
		);
		expect(text).toBe(
			'The Python runtime hit an unexpected problem and could not finish: MemoryError\n' +
				'Try running again. If it keeps happening, reload the page.'
		);
		expect(text).not.toContain('_pyodide');
	});

	it('copes with a non-Error value', () => {
		expect(describeWorkerFailure('boom')).toContain('could not finish: boom');
	});
});
