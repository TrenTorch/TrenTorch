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
			['with pytest.raises(ValueError, match="shape.*3"):', '    raise ValueError("shape mismatch: 3")'].join(
				'\n'
			)
		);
		expect(good.ok, good.out).toBe(true);

		const bad = run(
			['with pytest.raises(ValueError, match="dtype"):', '    raise ValueError("shape mismatch")'].join('\n')
		);
		expect(bad.ok).toBe(false);
		expect(bad.out).toContain('does not match');
	});

	it('names the missing feature instead of a confusing error for anything else', () => {
		const { ok, out } = run('pytest.approx(1.0)');
		expect(ok).toBe(false);
		expect(out).toContain('pytest.approx is not available in the in-browser test runner');
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
