// Checks on the text of a problemset tests.py that CI cannot see by running it: a test can pass
// while proving nothing. Each function returns a list of problems (empty when the file is fine).

// Splits a Python test file into its top-level `def test_...` functions.
function testFunctions(source: string): { name: string; body: string }[] {
	const parts = source.split(/^(?=(?:@[^\n]*\n)*def test_)/m).filter((p) => /def test_/.test(p));
	return parts.map((body) => ({ name: /def (test_\w+)/.exec(body)?.[1] ?? '', body }));
}

const BASIC = /^test_(01|basic|example)/;

// The basic/example test must check a value. Wrapping it in pytest.raises hides a solution that
// crashes on its own example (the crash passes the test).
export function findCrashAssertingBasicTests(source: string): string[] {
	return testFunctions(source)
		.filter((t) => BASIC.test(t.name) && t.body.includes('pytest.raises'))
		.map((t) => `${t.name} is wrapped in pytest.raises`);
}

// `assert result is not None` passes for any return value.
export function findNoneOnlyAssertions(source: string): string[] {
	return testFunctions(source)
		.filter((t) => /\bassert\b[^\n]*\bis not None\b/.test(t.body))
		.map((t) => `${t.name} asserts "is not None"`);
}

// Tests are never skipped. The in-browser test runner has no `pytest.mark`, so a file with a
// @pytest.mark.skip fails to load there and every test in it is lost; a run-time pytest.skip(...)
// can hide a missing test. If a category does not apply to a problem, leave that test out.
export function findSkips(source: string): string[] {
	return [...source.matchAll(/^[ \t]*[^#\n]*\bpytest\.(mark\.skip\w*|skip)\b[^\n]*/gm)].map(
		(match) => `uses ${match[0].trim()}`
	);
}
