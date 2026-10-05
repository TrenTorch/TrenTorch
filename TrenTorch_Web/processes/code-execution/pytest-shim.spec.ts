import { spawnSync } from 'node:child_process';
import { describe, it, expect } from 'vitest';
import { PYTEST_SHIM } from './pytest-shim';

// The shim is plain Python, so it runs under any CPython. Skipped (not failed)
// on a machine with no Python on the PATH.
const python = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
const hasPython = spawnSync(python, ['--version']).status === 0;

function run(body: string): { ok: boolean; out: string } {
	const program = ['import sys', PYTEST_SHIM, 'import pytest', body].join('\n');
	const result = spawnSync(python, ['-c', program], { encoding: 'utf8' });
	return { ok: result.status === 0, out: `${result.stdout}${result.stderr}` };
}

describe.skipIf(!hasPython)('in-browser pytest stand-in', () => {
	it('import pytest works and raises() accepts the expected exception', () => {
		const { ok, out } = run(
			['with pytest.raises(ValueError):', '    raise ValueError("bad shape")'].join('\n')
		);
		expect(ok, out).toBe(true);
	});

	it('raises() exposes the caught exception as .value', () => {
		const { ok, out } = run(
			[
				'with pytest.raises(ValueError) as info:',
				'    raise ValueError("bad shape")',
				'assert str(info.value) == "bad shape"',
				'assert info.type is ValueError'
			].join('\n')
		);
		expect(ok, out).toBe(true);
	});

	it('fails with DID NOT RAISE when nothing is raised', () => {
		const { ok, out } = run(['with pytest.raises(ValueError):', '    pass'].join('\n'));
		expect(ok).toBe(false);
		expect(out).toContain('DID NOT RAISE ValueError');
	});

	it('does not swallow a different exception type', () => {
		const { ok, out } = run(
			['with pytest.raises(ValueError):', '    raise KeyError("wrong kind")'].join('\n')
		);
		expect(ok).toBe(false);
		expect(out).toContain('KeyError');
	});

	it('accepts a tuple of exception types and a subclass of the expected one', () => {
		const { ok, out } = run(
			[
				'with pytest.raises((KeyError, ValueError)):',
				'    raise KeyError("one of two")',
				'class MyError(ValueError): pass',
				'with pytest.raises(ValueError):',
				'    raise MyError("subclass")'
			].join('\n')
		);
		expect(ok, out).toBe(true);
	});

	it('checks match= as a regular expression against the message', () => {
		const good = run(
			[
				'with pytest.raises(ValueError, match="shape.*3"):',
				'    raise ValueError("shape mismatch: 3")'
			].join('\n')
		);
		expect(good.ok, good.out).toBe(true);

		const bad = run(
			[
				'with pytest.raises(ValueError, match="dtype"):',
				'    raise ValueError("shape mismatch")'
			].join('\n')
		);
		expect(bad.ok).toBe(false);
		expect(bad.out).toContain('does not match');
	});

	it('names the missing feature instead of a confusing error for anything else', () => {
		const { ok, out } = run('pytest.fixture');
		expect(ok).toBe(false);
		expect(out).toContain('pytest.fixture is not available in the in-browser test runner');
	});

	describe('approx()', () => {
		const passes = (body: string) => {
			const { ok, out } = run(body);
			expect(ok, out).toBe(true);
		};
		const fails = (body: string) => {
			const { ok } = run(body);
			expect(ok).toBe(false);
		};

		it('compares numbers with the default tolerances of pytest (relative 1e-6, absolute 1e-12)', () => {
			passes('assert 0.1 + 0.2 == pytest.approx(0.3)');
			passes('assert 1_000_000.0 == pytest.approx(1_000_000.4)');
			passes('assert 1e-13 == pytest.approx(0.0)');
			fails('assert 1.0 == pytest.approx(1.001)');
			fails('assert 1e-9 == pytest.approx(0.0)');
		});

		it('abs= alone switches the relative tolerance off; rel= alone keeps the absolute floor', () => {
			passes('assert 100.0 == pytest.approx(101.0, abs=2)');
			fails('assert 1_000_000.0 == pytest.approx(1_000_000.4, abs=0.1)');
			passes('assert 10.0 == pytest.approx(10.5, rel=0.1)');
			fails('assert 10.0 == pytest.approx(12.0, rel=0.1)');
			passes('assert 3 == pytest.approx(3.4, rel=0.1, abs=0.5)');
		});

		it('compares lists and tuples element by element, and checks the length', () => {
			passes('assert [0.1 + 0.2, 1.0] == pytest.approx([0.3, 1.0])');
			passes('assert (1.0, 2.0) == pytest.approx([1.0, 2.0])');
			fails('assert [1.0, 2.0] == pytest.approx([1.0, 2.0, 3.0])');
			fails('assert [1.0, 2.5] == pytest.approx([1.0, 2.0])');
		});

		it('compares dicts by key and value', () => {
			passes('assert {"a": 0.1 + 0.2} == pytest.approx({"a": 0.3})');
			fails('assert {"a": 1.0} == pytest.approx({"b": 1.0})');
		});

		it('treats NaN as unequal unless nan_ok=True, and never matches an infinity to a finite value', () => {
			fails('assert float("nan") == pytest.approx(float("nan"))');
			passes('assert float("nan") == pytest.approx(float("nan"), nan_ok=True)');
			passes('assert float("inf") == pytest.approx(float("inf"))');
			fails('assert float("inf") == pytest.approx(1e308)');
		});

		it('works with !=, and has a readable repr', () => {
			passes('assert 1.0 != pytest.approx(2.0)');
			passes('assert repr(pytest.approx([1.0])) == "approx([1.0])"');
		});

		it('raises TypeError for nested data structures, like pytest does', () => {
			fails('pytest.approx([[1.0, 2.0], [3.0, 4.0]])');
		});

		it('compares NumPy arrays (either side) when NumPy is installed', () => {
			passes(
				[
					'try:',
					'    import numpy as np',
					'except ImportError:',
					'    raise SystemExit(0)',
					'assert np.array([0.1 + 0.2, 1.0]) == pytest.approx([0.3, 1.0])',
					'assert [0.3, 1.0] == pytest.approx(np.array([0.1 + 0.2, 1.0]))',
					'assert np.array([[1.0, 2.0], [3.0, 4.0]]) == pytest.approx(np.array([[1.0, 2.0], [3.0, 4.0]]))',
					'assert not (np.array([1.0, 2.0]) == pytest.approx(np.array([1.0, 2.1])))',
					'assert np.float64(0.1 + 0.2) == pytest.approx(np.float64(0.3))',
					'assert 0.1 + 0.2 == pytest.approx(np.float64(0.3))'
				].join('\n')
			);
		});
	});

	it('leaves a real pytest alone when one is already imported', () => {
		const program = [
			'import sys, types',
			'real = types.ModuleType("pytest")',
			'real.marker = "real"',
			'sys.modules["pytest"] = real',
			PYTEST_SHIM,
			'import pytest',
			'assert pytest.marker == "real"'
		].join('\n');
		const result = spawnSync(python, ['-c', program], { encoding: 'utf8' });
		expect(result.status, result.stderr).toBe(0);
	});
});
