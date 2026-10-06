import { describe, it, expect, beforeAll } from 'vitest';
import type { PyodideInterface } from 'pyodide';
import { TEST_COLLECTOR } from '$processes/ide-content/test-collector';
import { STUDENT_CODE_MARKER } from '$processes/ide-content/harness-marker';
import { internalsIn, loadRuntime, runCode, runCustom, runPreview, runTests } from './runtime';

// What a student sees when their code does not simply work, in the real Pyodide
// runtime, through the same scripts the worker runs (see runtime.ts).
//
// The bar: the same text Python prints on any machine. Errors name the student's
// own lines and the exception, and nothing that belongs to the runner (`<exec>`,
// `__run_user_code`, `_pyodide/_base.py`, a worker-level `PythonError`) appears.
//
// The libraries are the ones students reach for that are not loaded at startup:
// pandas, matplotlib, seaborn, plotly. pandas and matplotlib are fetched from the
// Pyodide CDN on first import and seaborn and plotly are installed from the wheels
// in platform/static/wheels, so these tests need the network, like the rest of this folder.

let py: PyodideInterface;

beforeAll(async () => {
	py = await loadRuntime();
}, 180_000);

function expectClean(text: string | null | undefined) {
	expect(internalsIn(text), `runner internals leaked into:\n${text}`).toBeNull();
}

describe('Run: errors read like Python', () => {
	it('shows a NameError with the student line, and only that', async () => {
		const { error } = await runCode(py, 'x = 1\nprint(undefined_name)');
		expect(error).toContain('File "<student-code>", line 2, in <module>');
		expect(error).toContain('print(undefined_name)');
		expect(error).toContain("NameError: name 'undefined_name' is not defined");
		expectClean(error);
	});

	it('lists each student frame for an error raised inside a function', async () => {
		const { error } = await runCode(py, 'def f(a):\n    return 1 / a\n\nf(0)');
		expect(error).toContain('line 4, in <module>');
		expect(error).toContain('line 2, in f');
		expect(error).toContain('ZeroDivisionError: division by zero');
		expectClean(error);
	});

	it('shows a SyntaxError with the offending line', async () => {
		const { error } = await runCode(py, 'def f(:\n    pass');
		expect(error).toContain('<student-code>');
		expect(error).toContain('SyntaxError');
		expectClean(error);
	});

	it('shows an IndentationError', async () => {
		const { error } = await runCode(py, 'def f():\nreturn 1');
		expect(error).toContain('IndentationError');
		expectClean(error);
	});

	it('names a module that does not exist', async () => {
		const { error } = await runCode(py, 'import not_a_real_module');
		expect(error).toContain("ModuleNotFoundError: No module named 'not_a_real_module'");
		expectClean(error);
	});

	it('reports runaway recursion as Python does', async () => {
		const { error } = await runCode(py, 'def f():\n    return f()\nf()');
		expect(error).toContain('RecursionError');
		expectClean(error);
	});

	it('treats sys.exit() and sys.exit(0) as a normal finish, not a failure', async () => {
		const quiet = await runCode(py, 'import sys\nprint("before")\nsys.exit()');
		expect(quiet.error).toBeNull();
		expect(quiet.stdout).toBe('before\n');
		expect((await runCode(py, 'import sys\nsys.exit(0)')).error).toBeNull();
	});

	it('says plainly when sys.exit is called with a failure status', async () => {
		const { error } = await runCode(py, 'import sys\nsys.exit(2)');
		expect(error).toBe('Process exited with status 2 (sys.exit was called).');
	});

	it('shows a KeyboardInterrupt raised by the code like any other error', async () => {
		const { error } = await runCode(py, 'raise KeyboardInterrupt()');
		expect(error).toContain('KeyboardInterrupt');
		expectClean(error);
	});

	it('gives input() the EOFError Python raises when there is no terminal', async () => {
		const { error } = await runCode(py, 'name = input("name? ")\nprint(name)');
		expect(error).toContain('EOFError');
		expectClean(error);
	});

	it('keeps printed output and warnings', async () => {
		const { stdout, stderr, error } = await runCode(
			py,
			'import warnings\nwarnings.warn("careful")\nprint("done")'
		);
		expect(error).toBeNull();
		expect(stdout).toBe('done\n');
		expect(stderr).toContain('UserWarning: careful');
	});

	it('does not carry names between runs', async () => {
		await runCode(py, 'leaked = 1');
		const { error } = await runCode(py, 'print(leaked)');
		expect(error).toContain("NameError: name 'leaked' is not defined");
	});
});

describe('libraries that load on first import', () => {
	it('runs pandas', async () => {
		const { stdout, error } = await runCode(
			py,
			[
				'import pandas as pd',
				'df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})',
				'print(df.sum().to_dict())',
				'print(df.describe().loc["mean", "a"])'
			].join('\n')
		);
		expect(error).toBeNull();
		expect(stdout).toBe("{'a': 6, 'b': 15}\n2.0\n");
	}, 120_000);

	it('shows a pandas error with the student line, without pandas internals', async () => {
		const { error } = await runCode(
			py,
			'import pandas as pd\ndf = pd.DataFrame({"a": [1]})\nprint(df["missing"])'
		);
		expect(error).toContain('line 3, in <module>');
		expect(error).toContain("KeyError: 'missing'");
		expect(error).not.toContain('pandas/core');
		expectClean(error);
	}, 120_000);

	it('runs numpy and pandas together', async () => {
		const { stdout, error } = await runCode(
			py,
			'import numpy as np\nimport pandas as pd\nprint(pd.Series(np.arange(4)).mean())'
		);
		expect(error).toBeNull();
		expect(stdout).toBe('1.5\n');
	}, 120_000);

	it('runs matplotlib: pyplot imports, figures draw, plt.show() does not crash', async () => {
		const { stdout, stderr, error } = await runCode(
			py,
			[
				'import io',
				'import matplotlib',
				'import matplotlib.pyplot as plt',
				'fig, ax = plt.subplots()',
				'ax.plot([1, 2, 3], [3, 1, 2])',
				'ax.set_title("t")',
				'plt.show()',
				'buffer = io.BytesIO()',
				'fig.savefig(buffer, format="png")',
				'print(matplotlib.get_backend().lower(), buffer.getvalue()[:4])'
			].join('\n')
		);
		expect(error).toBeNull();
		expect(stdout).toBe("agg b'\\x89PNG'\n");
		// No "cannot be shown" or font cache notices: nothing the student can act on.
		expect(stderr).toBe('');
	}, 120_000);

	it('runs seaborn on top of pandas and matplotlib', async () => {
		const { stdout, error } = await runCode(
			py,
			[
				'import pandas as pd',
				'import seaborn as sns',
				'import matplotlib.pyplot as plt',
				'df = pd.DataFrame({"x": [1, 2, 3], "y": [3, 1, 2]})',
				'ax = sns.lineplot(data=df, x="x", y="y")',
				'plt.show()',
				'print(type(ax).__name__)'
			].join('\n')
		);
		expect(error).toBeNull();
		expect(stdout).toBe('Axes\n');
	}, 180_000);

	it('runs plotly, including fig.show()', async () => {
		const { stdout, error } = await runCode(
			py,
			[
				'import plotly.express as px',
				'import plotly.graph_objects as go',
				'fig = px.line(x=[1, 2, 3], y=[3, 1, 2])',
				'fig.show()',
				'bar = go.Figure(go.Bar(x=["a", "b"], y=[1, 2]))',
				'print(len(fig.data), len(bar.data), "plotly" in bar.to_html())'
			].join('\n')
		);
		expect(error).toBeNull();
		expect(stdout).toBe('1 1 True\n');
	}, 180_000);
});

const harness = (tests: string) => [STUDENT_CODE_MARKER, tests, TEST_COLLECTOR].join('\n');

describe('Submit: failing tests read like Python', () => {
	it('points at the line inside the student function that failed', async () => {
		const { results, error } = await runTests(
			py,
			'def reciprocal(a):\n    return 1 / a',
			harness('def test_zero():\n    assert reciprocal(0) == 1\n')
		);
		expect(error).toBeNull();
		expect(results[0].passed).toBe(false);
		expect(results[0].error).toContain('ZeroDivisionError: division by zero');
		expect(results[0].error).toContain('Your code, line 2 in reciprocal: return 1 / a');
		expectClean(results[0].error);
	});

	it('does not blame the student for a plain wrong answer', async () => {
		const { results } = await runTests(
			py,
			'def double(a):\n    return a + 1',
			harness('def test_double():\n    assert double(2) == 4, "double(2) should be 4"\n')
		);
		expect(results[0].error).toContain('Assertion failed: double(2) should be 4');
		expect(results[0].error).toContain('assert double(2) == 4');
		expect(results[0].error).not.toContain('Your code');
	});

	it('reports a SyntaxError before any test runs, naming the line', async () => {
		const { results, error } = await runTests(
			py,
			'def f(:\n    pass',
			harness('def test_a():\n    assert True\n')
		);
		expect(results).toEqual([]);
		expect(error).toContain('SyntaxError');
		expect(error).toContain('<student-code>');
		expectClean(error);
	});

	it('reports an error raised while the code is being defined, with its line', async () => {
		const { results, error } = await runTests(
			py,
			'LIMIT = 10\nvalue = LIMIT / 0',
			harness('def test_a():\n    assert True\n')
		);
		expect(results).toEqual([]);
		expect(error).toContain('line 2, in <module>');
		expect(error).toContain('ZeroDivisionError');
		expectClean(error);
	});

	it('survives sys.exit() inside the function under test and still runs the other tests', async () => {
		const { results, error } = await runTests(
			py,
			'import sys\ndef quit_now():\n    sys.exit(3)\ndef fine():\n    return 1',
			harness('def test_a_quits():\n    quit_now()\n\ndef test_b_fine():\n    assert fine() == 1\n')
		);
		expect(error).toBeNull();
		expect(results.map((r) => r.passed)).toEqual([false, true]);
		expect(results[0].error).toContain('SystemExit');
		expectClean(results[0].error);
	});

	it('explains module-level sys.exit() instead of reporting zero tests silently', async () => {
		const { results, error } = await runTests(
			py,
			'import sys\nsys.exit(0)',
			harness('def test_a():\n    assert True\n')
		);
		expect(results).toEqual([]);
		expect(error).toBe('Your code called sys.exit() before the tests could run.');
	});

	it('runs tests that use pandas', async () => {
		const { results, error } = await runTests(
			py,
			'import pandas as pd\ndef total(values):\n    return pd.Series(values).sum()',
			harness('def test_total():\n    assert total([1, 2, 3]) == 6\n')
		);
		expect(error).toBeNull();
		expect(results).toEqual([{ name: 'test_total', passed: true, error: null }]);
	}, 120_000);

	it('runs only the first checks for Run, the whole suite for Submit', async () => {
		const tests = harness(
			'def test_a():\n    assert True\ndef test_b():\n    assert True\ndef test_c():\n    assert True\n'
		);
		expect((await runTests(py, 'x = 1', tests, '2')).results).toHaveLength(2);
		expect((await runTests(py, 'x = 1', tests)).results).toHaveLength(3);
	});
});

describe('Custom input: errors read like Python', () => {
	const noTests = '';

	it('returns the result and checks it against the expected value', async () => {
		const code = 'def add(a, b):\n    return a + b';
		const ok = await runCustom(py, code, noTests, {
			functionName: 'add',
			argumentsJson: '[2, 3]',
			expectedJson: '5'
		});
		expect(ok.error).toBeNull();
		expect(ok.output).toContain('Returned: 5');
		const bad = await runCustom(py, code, noTests, {
			functionName: 'add',
			argumentsJson: '[2, 3]',
			expectedJson: '6'
		});
		expect(bad.success).toBe(false);
		expect(bad.error).toBe('Expected 6, got 5.');
	});

	it('shows the student frame for an error inside the function', async () => {
		const { error } = await runCustom(py, 'def f(a):\n    return 1 / a', noTests, {
			functionName: 'f',
			argumentsJson: '[0]'
		});
		expect(error).toContain('line 2, in f');
		expect(error).toContain('ZeroDivisionError');
		expectClean(error);
	});

	it('tells the student when the function name does not exist', async () => {
		const { error } = await runCustom(py, 'x = 1', noTests, { functionName: 'nope' });
		expect(error).toContain("NameError: No callable function named 'nope' was found.");
		expectClean(error);
	});

	it('tells the student when the arguments are not a JSON array', async () => {
		const { error } = await runCustom(py, 'def f(a):\n    return a', noTests, {
			functionName: 'f',
			argumentsJson: '{"a": 1}'
		});
		expect(error).toContain('ValueError: Arguments must be a JSON array');
		expectClean(error);
	});
});

describe('Preview: errors read like Python', () => {
	it('shows the student frame when the preview calls a function that fails', async () => {
		const { error, figures } = await runPreview(
			py,
			'def total(values):\n    return sum(values) / len(values)',
			'print(total([]))'
		);
		expect(figures).toEqual([]);
		expect(error).toContain('line 2, in total');
		expect(error).toContain('ZeroDivisionError');
		expectClean(error);
	});

	it('draws a matplotlib figure and keeps stderr free of runner notices', async () => {
		const { error, figures, stderr } = await runPreview(
			py,
			'import matplotlib.pyplot as plt\ndef chart(x, y):\n    fig, ax = plt.subplots()\n    ax.plot(x, y)\n    return fig, ax',
			'fig, ax = chart([1, 2, 3], [3, 1, 2])\nshow(fig)'
		);
		expect(error).toBeNull();
		expect(figures.map((f) => f.kind)).toEqual(['png']);
		expect(stderr).toBe('');
	}, 120_000);
});
