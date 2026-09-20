import { spawnSync } from 'node:child_process';
import { describe, it, expect } from 'vitest';
import { TEST_COLLECTOR } from './test-collector';

// The collector is plain Python, so it runs under any CPython. Skipped (not
// failed) on a machine with no Python on the PATH.
const python = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
const hasPython = spawnSync(python, ['--version']).status === 0;

type Result = { name: string; passed: boolean; error: string | null };

function collect(testsSource: string): Result[] {
	const program = [
		testsSource,
		TEST_COLLECTOR,
		'import json',
		'print(json.dumps(run_tests()))'
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
			{ name: 'test_b_fails', passed: false, error: 'arithmetic is broken' }
		]);
	});

	it('names the exception when a bare assert fails, instead of an empty message', () => {
		const [result] = collect(`
def test_bare_assert():
    assert False
`);
		expect(result.passed).toBe(false);
		expect(result.error).toBe('AssertionError');
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
});
