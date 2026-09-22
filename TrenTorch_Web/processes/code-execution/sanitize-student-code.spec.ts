import { describe, it, expect } from 'vitest';
import { sanitizeStudentCode } from './sanitize-student-code';

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

	it('strips a load_solution(...) assignment wrapped across multiple lines', () => {
		// A long folder path routinely pushes this past a formatter's line
		// length, e.g. adaboost's solution.py -- a per-line filter only drops
		// the opening line, leaving the argument and closing `).attr` lines
		// behind as orphaned syntax (IndentationError the moment Pyodide
		// execs it).
		const pasted = [
			'import sys',
			'from pathlib import Path',
			'',
			'import numpy as np',
			'',
			'sys.path.insert(0, str(Path(__file__).resolve().parents[3]))',
			'from _load import load_solution  # noqa: E402',
			'',
			'build_tree = load_solution("01-classical-ml/03-decision-trees/03-best-split-minimal-tree").build_tree',
			'predict_tree = load_solution(',
			'    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"',
			').predict_tree',
			'',
			'',
			'def adaboost_train(input, labels):',
			'    return build_tree(input, labels)'
		].join('\n');

		const cleaned = sanitizeStudentCode(pasted);

		expect(cleaned).not.toContain('load_solution');
		expect(cleaned).not.toContain('03-best-split-minimal-tree');
		expect(cleaned).not.toContain('.predict_tree\n');
		// The whole statement's three lines are gone, not just the first --
		// no dangling `).predict_tree` or bare string-literal line remains.
		expect(cleaned).not.toMatch(/^\s*\)/m);
		expect(cleaned).not.toMatch(/^\s*"[^"]*"\s*$/m);
		expect(cleaned).toContain('def adaboost_train(input, labels):');
		expect(cleaned).toContain('return build_tree(input, labels)');
	});

	it('strips a multi-line sys.path.insert(...) call the same way', () => {
		const pasted = [
			'import sys',
			'from pathlib import Path',
			'',
			'sys.path.insert(',
			'    0, str(Path(__file__).resolve().parents[3])',
			')',
			'from _load import load_solution  # noqa: E402',
			'',
			'linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear',
			'',
			'',
			'def use_it(x):',
			'    return linear(x)'
		].join('\n');

		const cleaned = sanitizeStudentCode(pasted);

		expect(cleaned).not.toContain('sys.path.insert');
		expect(cleaned).not.toMatch(/^\s*\)\s*$/m);
		expect(cleaned).toContain('def use_it(x):');
	});
});

describe('sanitizeStudentCode: module handles and their aliases', () => {
	it('drops aliases off a removed module handle, so an untouched starter runs (regression: NameError _cond_prob)', () => {
		// The starters carry the same header as the solutions. Removing only the
		// load_solution line left `marginal_x = _cond_prob.marginal_x` behind,
		// which crashed before any test ran.
		const starter = `import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_cond_prob = load_solution("00-math-and-statistics/03-probability/04-conditional-probability")
marginal_x = _cond_prob.marginal_x
marginal_y = _cond_prob.marginal_y


def mutual_information(joint):
    return 0.0
`;
		const result = sanitizeStudentCode(starter);

		expect(result).not.toContain('_cond_prob');
		expect(result).not.toContain('load_solution');
		expect(result).not.toContain('marginal_x');
		expect(result).toContain('import numpy as np');
		expect(result).toContain('def mutual_information(joint):');
	});

	it('drops a parenthesised tuple of aliases spread over several lines', () => {
		const code = `_mod = load_solution("a/b")
(
    first,
    second,
) = (
    _mod.first,
    _mod.second,
)

def solve():
    return first
`;
		const result = sanitizeStudentCode(code);

		expect(result).not.toContain('_mod');
		expect(result).toContain('def solve():');
		expect(result).toContain('return first');
	});

	it('keeps a similar-looking line that is not an alias of a removed handle', () => {
		const code = `_mod = load_solution("a/b")
alias = _mod.thing
config = settings.value
total = other.count

def solve():
    return config
`;
		const result = sanitizeStudentCode(code);

		expect(result).not.toContain('alias = _mod.thing');
		expect(result).toContain('config = settings.value');
		expect(result).toContain('total = other.count');
	});

	it('does not remove aliases when no module handle was removed', () => {
		const code = `import numpy as np
value = np.pi
name = module.attribute
`;
		expect(sanitizeStudentCode(code)).toBe(code);
	});
});
