import { describe, it, expect } from 'vitest';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { findCrashAssertingBasicTests, findNoneOnlyAssertions, findSkips } from './test-guards';

const PROBLEMSET = join(import.meta.dirname, '..', '..', 'data', 'app_data', '12-problemset');

function testFiles(dir: string): string[] {
	return readdirSync(dir).flatMap((name) => {
		const path = join(dir, name);
		if (statSync(path).isDirectory()) return testFiles(path);
		return name === 'tests.py' ? [path] : [];
	});
}

describe('guards', () => {
	it('flags a basic test wrapped in pytest.raises', () => {
		const source = [
			'def test_01_basic_example():',
			'    with pytest.raises(NameError):',
			'        solve(1)',
			'',
			'def test_02_empty():',
			'    with pytest.raises(ValueError):',
			'        solve([])',
			''
		].join('\n');
		expect(findCrashAssertingBasicTests(source)).toEqual([
			'test_01_basic_example is wrapped in pytest.raises'
		]);
	});

	it('flags "is not None" assertions', () => {
		expect(findNoneOnlyAssertions('def test_x():\n    assert solve(1) is not None\n')).toEqual([
			'test_x asserts "is not None"'
		]);
		expect(findNoneOnlyAssertions('def test_x():\n    assert solve(1) == 2\n')).toEqual([]);
	});

	it('flags any skip, marker or run-time', () => {
		expect(findSkips('@pytest.mark.skip(reason="x")\ndef test_x():\n    pass\n')).toHaveLength(1);
		expect(findSkips('def test_x():\n    pytest.skip("no")\n')).toHaveLength(1);
		expect(findSkips('# pytest.skip is not used\ndef test_x():\n    assert 1 == 1\n')).toEqual([]);
	});
});

describe('problemset tests.py files', () => {
	const files = testFiles(PROBLEMSET);

	it('finds the 250 problems', () => {
		expect(files).toHaveLength(250);
	});

	const checks = [
		['no basic test is wrapped in pytest.raises', findCrashAssertingBasicTests],
		['no test only asserts "is not None"', findNoneOnlyAssertions],
		['no test is skipped (the in-browser runner has no pytest.mark)', findSkips]
	] as const;

	for (const [title, check] of checks) {
		it(title, () => {
			const problems = files.flatMap((file) =>
				check(readFileSync(file, 'utf8')).map((p) => `${relative(PROBLEMSET, file)}: ${p}`)
			);
			expect(problems).toEqual([]);
		});
	}
});
