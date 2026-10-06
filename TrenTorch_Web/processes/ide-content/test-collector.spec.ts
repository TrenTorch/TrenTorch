import { spawnSync } from 'node:child_process';
import { describe, it, expect } from 'vitest';
import { TEST_COLLECTOR } from './test-collector';
import { PYTEST_SHIM } from '../code-execution/pytest-shim';
import { STUDENT_FILENAME } from '../code-execution/python-error-format';

// The collector is plain Python, so it runs under any CPython. Skipped (not
// failed) on a machine with no Python on the PATH.
const python = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
const hasPython = spawnSync(python, ['--version']).status === 0;

type Result = { name: string; passed: boolean; error: string | null };

function collect(testsSource: string, options: { shim?: boolean; limit?: number } = {}): Result[] {
	const program = [
		...(options.shim ? ['import sys', PYTEST_SHIM, 'import pytest'] : []),
		testsSource,
		TEST_COLLECTOR,
		'import json',
		`print(json.dumps(run_tests(${options.limit ?? ''})))`
	].join('\n');
	const result = spawnSync(python, ['-c', program], { encoding: 'utf8' });
	expect(result.status, result.stderr).toBe(0);
	return JSON.parse(result.stdout.trim().split('\n').pop() ?? '[]');
}

describe.skipIf(!hasPython)('the test collector', () => {
	it('runs plain test_ functions and reports passes and failures', () => {
		const results = collect(`
def test_a_passes():
    assert 1 + 1 == 2

def test_b_fails():
    assert 1 + 1 == 3, "arithmetic is broken"
`);
		expect(results).toEqual([
			{ name: 'test_a_passes', passed: true, error: null },
			{ name: 'test_b_fails', passed: false, error: 'Assertion failed: arithmetic is broken' }
		]);
	});

	it('explains a bare assertion failure instead of returning an empty message', () => {
		const [result] = collect(`
def test_bare_assert():
    assert False
`);
		expect(result.passed).toBe(false);
		expect(result.error).toBe('Assertion failed; the expected condition was false.');
	});

	it('gives a test that asks for tmp_path a real, writable temporary directory', () => {
		const [result] = collect(`
def test_round_trip(tmp_path):
    target = tmp_path / "state.txt"
    target.write_text("saved")
    assert target.read_text() == "saved"
    assert tmp_path.is_dir()
`);
		expect(result).toEqual({ name: 'test_round_trip', passed: true, error: null });
	});

	it('gives each test its own tmp_path and removes it afterwards', () => {
		const results = collect(`
seen = []

def test_a_one(tmp_path):
    (tmp_path / "file.txt").write_text("one")
    seen.append(tmp_path)

def test_b_two(tmp_path):
    assert list(tmp_path.iterdir()) == []
    seen.append(tmp_path)

def test_c_three():
    assert len(seen) == 2
    assert seen[0] != seen[1]
    assert not seen[0].exists() and not seen[1].exists()
`);
		expect(results.map((r) => r.passed)).toEqual([true, true, true]);
	});

	it('names a fixture it cannot provide instead of failing obscurely', () => {
		const [result] = collect(`
def test_needs_monkeypatch(monkeypatch):
    pass
`);
		expect(result.passed).toBe(false);
		expect(result.error).toContain("pytest fixture 'monkeypatch' is not available");
	});

	it('survives a function that calls sys.exit(), failing only that test', () => {
		const results = collect(`
import sys

def test_a_quits():
    sys.exit(3)

def test_b_still_runs():
    assert True
`);
		expect(results.map((r) => r.passed)).toEqual([false, true]);
		expect(results[0].error).toContain('SystemExit: your code called sys.exit(3)');
	});

	it("says where inside the student's code an error was raised", () => {
		// The collector is told which file is the student's by name, as in the browser.
		const [result] = collect(`
exec(compile("def reciprocal(a):\\n    return 1 / a\\n", ${JSON.stringify(STUDENT_FILENAME)}, "exec"), globals())

def test_zero():
    reciprocal(0)
`);
		expect(result.passed).toBe(false);
		expect(result.error).toContain('ZeroDivisionError: division by zero');
		expect(result.error).toContain('Your code, line 2 in reciprocal');
	});

	it('does not point at student code for a plain failed assertion', () => {
		const [result] = collect(`
def test_wrong():
    assert 1 == 2, "nope"
`);
		expect(result.error).not.toContain('Your code');
	});

	describe('pytest marks, as the in-browser stand-in provides them', () => {
		it('runs a parametrized test once per case, named by the ids', () => {
			const results = collect(
				`
CASES = [("two-and-three", 2, 3, 5), ("zero", 0, 0, 0), ("wrong", 1, 1, 3)]

@pytest.mark.parametrize("label,a,b,expected", CASES, ids=[c[0] for c in CASES])
def test_add(label, a, b, expected):
    assert a + b == expected, "bad sum for " + label
`.replace('"label,a,b,expected", CASES', '"label,a,b,expected", [c for c in CASES]'),
				{ shim: true }
			);
			expect(results.map((r) => [r.name, r.passed])).toEqual([
				['test_add[two-and-three]', true],
				['test_add[zero]', true],
				['test_add[wrong]', false]
			]);
			expect(results[2].error).toContain('Assertion failed: bad sum for wrong');
		});

		it('names cases after their values when no ids are given', () => {
			const results = collect(
				`
@pytest.mark.parametrize("n,squared", [(2, 4), (3, 9)])
def test_square(n, squared):
    assert n * n == squared
`,
				{ shim: true }
			);
			expect(results.map((r) => r.name)).toEqual(['test_square[2-4]', 'test_square[3-9]']);
		});

		it('takes a single argument name and plain values', () => {
			const results = collect(
				`
@pytest.mark.parametrize("n", [1, 2, 3])
def test_positive(n):
    assert n > 0
`,
				{ shim: true }
			);
			expect(results.map((r) => r.name)).toEqual([
				'test_positive[1]',
				'test_positive[2]',
				'test_positive[3]'
			]);
		});

		it('leaves skipped tests out of the results rather than counting them as passes', () => {
			const results = collect(
				`
import sys

@pytest.mark.skip(reason="no input available")
def test_a_skipped():
    raise AssertionError("must not run")

@pytest.mark.skipif(True, reason="always")
def test_b_skipped_if():
    raise AssertionError("must not run")

@pytest.mark.skipif(False, reason="never")
def test_c_runs():
    assert True

def test_d_skips_itself():
    try:
        pytest.skip("needs a GPU")
    except Exception:
        raise AssertionError("pytest.skip must not be catchable as an Exception")
`,
				{ shim: true }
			);
			expect(results).toEqual([{ name: 'test_c_runs', passed: true, error: null }]);
		});

		it('reports no tests at all when every test is skipped', () => {
			const results = collect(
				`
@pytest.mark.skip(reason="No safe generated input for this problem")
def test_01_unavailable():
    pass

@pytest.mark.skip(reason="No safe generated input for this problem")
def test_02_unavailable():
    pass
`,
				{ shim: true }
			);
			expect(results).toEqual([]);
		});

		it('accepts marks it does not act on', () => {
			const results = collect(
				`
@pytest.mark.slow
@pytest.mark.timeout(5)
def test_marked():
    assert True
`,
				{ shim: true }
			);
			expect(results).toEqual([{ name: 'test_marked', passed: true, error: null }]);
		});

		it('counts the sample limit in cases, after skipped tests are removed', () => {
			const tests = `
@pytest.mark.skip(reason="x")
def test_a_skipped():
    pass

@pytest.mark.parametrize("n", [1, 2, 3])
def test_b_many(n):
    assert n
`;
			expect(collect(tests, { shim: true, limit: 2 }).map((r) => r.name)).toEqual([
				'test_b_many[1]',
				'test_b_many[2]'
			]);
		});

		it('still supports tmp_path together with parametrize', () => {
			const results = collect(
				`
@pytest.mark.parametrize("text", ["a", "b"])
def test_round_trip(tmp_path, text):
    target = tmp_path / "f.txt"
    target.write_text(text)
    assert target.read_text() == text
`,
				{ shim: true }
			);
			expect(results.map((r) => r.passed)).toEqual([true, true]);
		});
	});
});
