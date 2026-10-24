const COMPARE_MODES = ['exact', 'unordered', 'float'];
const SLUG = /^[a-z0-9_]+$/;

/**
 * @param {string} dir
 * @param {string} message
 * @returns {never}
 */
function fail(dir, message) {
	throw new Error(`problem.json in ${dir}: ${message}`);
}

// Checks the shape of a DSA question's problem.json (see data/app_data/13-dsa-sheet/README.md).
// `raw` is the file text. It is embedded as-is, never re-serialized, because JSON.parse would
// round integers above 2^53 that Python reads exactly.
/**
 * @param {string} raw
 * @param {string} dir
 */
export function parseProblem(raw, dir) {
	/** @type {any} */
	let problem;
	try {
		problem = JSON.parse(raw);
	} catch (error) {
		fail(dir, `is not valid JSON (${/** @type {Error} */ (error).message})`);
	}
	if (problem.schema !== 1) fail(dir, 'schema must be 1');
	const fn = problem.function;
	if (!fn || !/^[a-z_][a-z0-9_]*$/.test(fn.name ?? ''))
		fail(dir, 'function.name must be snake_case');
	if (!Array.isArray(fn.params) || fn.params.some((/** @type {any} */ p) => !p.name || !p.type)) {
		fail(dir, 'function.params must be a list of {name, type}');
	}
	if (!fn.returns) fail(dir, 'function.returns is required');
	if (problem.compare !== undefined && !COMPARE_MODES.includes(problem.compare)) {
		fail(dir, `compare must be one of ${COMPARE_MODES.join(', ')}`);
	}
	if (!Number.isFinite(problem.limits?.timeMs)) fail(dir, 'limits.timeMs is required');
	const hints = problem.hints ?? [];
	if (!Array.isArray(hints) || hints.length > 4 || hints.some((h) => typeof h !== 'string' || !h)) {
		fail(dir, 'hints must be up to 4 non-empty strings');
	}
	if (!Array.isArray(problem.cases) || problem.cases.length === 0) fail(dir, 'cases is empty');
	const names = fn.params.map((/** @type {any} */ p) => p.name).sort();
	const seen = new Set();
	for (const [index, testCase] of problem.cases.entries()) {
		if (!SLUG.test(testCase.id ?? '')) fail(dir, `case ${index} needs an id like "example_1"`);
		if (seen.has(testCase.id)) fail(dir, `duplicate case id "${testCase.id}"`);
		seen.add(testCase.id);
		if (JSON.stringify(Object.keys(testCase.input ?? {}).sort()) !== JSON.stringify(names)) {
			fail(dir, `case "${testCase.id}" input must have exactly the keys ${names.join(', ')}`);
		}
		if ('expected' in testCase === 'digest' in testCase) {
			fail(dir, `case "${testCase.id}" needs exactly one of expected or digest`);
		}
	}
	return { problem, hints };
}

// The Python test file for a question that keeps its tests in problem.json: the cases and one
// test_NN_<id> per case, so the IDE shows them like any other tests. Examples
// come first, so "Run" (the first few tests) is a quick check and "Submit" runs everything.
// The shared runtime (cases-runtime.py) is not repeated here: buildTestHarness adds it once.
/**
 * @param {string} raw
 * @param {string} dir
 */
export function buildCasesTests(raw, dir) {
	const { problem } = parseProblem(raw, dir);
	const digits = String(problem.cases.length).length;
	const tests = problem.cases.map(
		(/** @type {any} */ testCase, /** @type {number} */ index) =>
			`test_${String(index + 1).padStart(Math.max(2, digits), '0')}_${testCase.id} = _make_test(${index})`
	);
	return `_PROBLEM = load_problem(${JSON.stringify(raw)})
_FUNCTION_NAME = _PROBLEM["function"]["name"]


def _make_test(index):
    def run():
        fn = globals().get(_FUNCTION_NAME)
        if not callable(fn):
            raise AssertionError("Define a function named " + _FUNCTION_NAME + ".")
        check_case(_PROBLEM, _PROBLEM["cases"][index], fn)

    return run


${tests.join('\n')}
`;
}
