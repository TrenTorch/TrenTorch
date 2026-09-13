// tests.py is real pytest, written to run standalone via `pytest
// tests.py` against the oracle solution.py sitting next to it -- see
// data/app_data/README.md. Two things about that don't hold once this same file
// runs inside a single Pyodide exec against a *student's* code instead:
//
// 1. `from _load import load_solution` -- there's no filesystem, so no
//    `_load` module exists to import at all.
// 2. `<name> = load_solution(...).{name}` -- re-binds a name that's
//    either the student's own submission (self-reference, via
//    `Path(__file__)...`) or a track-mate's oracle solution (a literal
//    folder-name string). Either way it needs a real value, which
//    `load_solution` can't produce here.
//
// The fix for both: strip the whole `from _load import load_solution`
// through the load_solution(...) assignments block (bounded by the
// first `def`, so it survives however many lines a given assignment
// spans), and instead make sure every name it would have bound already
// exists in the exec'd globals before the test functions that use it
// run -- self-references are already covered (the student's code execs
// first), and cross-question references are covered by prepending the
// referenced track-mate's oracle solution ahead of the cleaned test
// code (see build-test-harness.ts).
export function stripLoadSolutionBoilerplate(testsCode: string): {
	cleaned: string;
	dependencyPaths: string[];
} {
	const lines = testsCode.split('\n');
	const startIdx = lines.findIndex((line) =>
		line.trim().startsWith('from _load import load_solution')
	);
	if (startIdx === -1) {
		return { cleaned: testsCode, dependencyPaths: [] };
	}

	let endIdx = lines.findIndex((line, i) => i > startIdx && /^def\s/.test(line));
	if (endIdx === -1) endIdx = lines.length;

	const boilerplate = lines.slice(startIdx, endIdx).join('\n');
	// load_solution() takes a full slash path from data/, e.g.
	// "01-classical-ml/01-linear-regression/01-hypothesis-function" --
	// kept whole (not just its last segment) since the same folder name
	// can legitimately exist under multiple tracks; questionsByFullPath
	// is keyed by this exact string. The self-reference form is an
	// f-string (load_solution(f"...{Path(__file__)...}")); skip anything
	// with a brace or __file__ in it -- the student's own code already
	// binds that name, so it needs no prelude.
	const dependencyPaths = [
		...new Set(
			[...boilerplate.matchAll(/load_solution\(\s*f?["']([^"']+)["']\s*\)/g)]
				.map((m) => m[1])
				.filter((arg) => !arg.includes('{') && !arg.includes('__file__'))
		)
	];

	// The `_load` scaffold has one more line that lives *above* the import
	// it's bounded by: `sys.path.insert(0, str(Path(__file__)...))`, there
	// only so `from _load import ...` resolves when pytest runs the file
	// from disk. In-browser there's no `__file__` in the exec globals, so
	// left in it raises NameError before any test runs -- drop it (and any
	// other bare sys.path.insert, which is never legitimate in a harness
	// that runs as a single in-memory exec).
	const cleaned = [...lines.slice(0, startIdx), ...lines.slice(endIdx)]
		.filter((line) => !/^\s*sys\.path\.insert\s*\(/.test(line))
		.join('\n');
	return { cleaned, dependencyPaths };
}
