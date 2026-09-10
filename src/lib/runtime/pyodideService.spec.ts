import { describe, it, expect } from 'vitest';
import { sanitizeStudentCode } from './pyodideService';

describe('sanitizeStudentCode', () => {
	it('leaves ordinary student code untouched', () => {
		const code = 'import numpy as np\n\n\ndef linear_forward(X, w, b):\n    return X @ w + b\n';
		expect(sanitizeStudentCode(code)).toBe(code);
	});

	it('strips the dev-only _load header a pasted solution.py carries', () => {
		const pasted = [
			'import sys',
			'from pathlib import Path',
			'',
			'import numpy as np',
			'',
			'sys.path.insert(0, str(Path(__file__).resolve().parents[3]))',
			'from _load import load_solution  # noqa: E402',
			'',
			'linear_forward = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear_forward',
			'mse_grad = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_grad',
			'',
			'def train_linear_regression(X, y, lr, epochs):',
			'    return linear_forward(X, np.zeros(X.shape[1]), 0.0)'
		].join('\n');

		const cleaned = sanitizeStudentCode(pasted);

		expect(cleaned).not.toContain('sys.path.insert');
		expect(cleaned).not.toContain('from _load import');
		expect(cleaned).not.toContain('= load_solution(');
		// the actual implementation and its real imports survive
		expect(cleaned).toContain('import numpy as np');
		expect(cleaned).toContain('def train_linear_regression(X, y, lr, epochs):');
		expect(cleaned).toContain('return linear_forward(X, np.zeros(X.shape[1]), 0.0)');
	});

	it('does not touch a legitimate call to load_solution mid-expression', () => {
		// Only `name = load_solution(...)` bindings are boilerplate; a bare
		// call (hypothetical) is left alone.
		const code = 'result = compute(load_solution)\n';
		expect(sanitizeStudentCode(code)).toBe(code);
	});
});
