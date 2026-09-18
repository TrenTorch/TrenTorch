// Every data/<...>/solution.py ships with a dev-only header so it runs as a
// standalone `pytest` file on disk:
//
//   import sys
//   from pathlib import Path
//   sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
//   from _load import load_solution
//   linear_forward = load_solution("...").linear_forward
//
// Those files are public under data/, so a student copy-pasting one in to
// check their work against it is an obvious move -- and `__file__` doesn't
// exist when the worker exec()s a code string, so it crashes on the very
// first line. Strip that header from student submissions the same way the
// test harness already strips it from tests.py: the sys.path / _load lines
// are meaningless in-browser, and any `name = load_solution(...)` binding
// is either provided by the harness prelude (Submit) or resolves to a
// clear NameError the student can act on (Run).
// A boilerplate statement (sys.path.insert(...) or `name = load_solution(...)`)
// isn't always one line -- a long folder path routinely pushes it past the
// line-length a formatter wraps at, e.g.:
//
//   predict_tree = load_solution(
//       "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
//   ).predict_tree
//
// A naive per-line filter only drops the opening line, leaving the argument
// and closing `).attr` lines behind -- syntactically orphaned fragments that
// crash with IndentationError the moment Pyodide execs the "sanitized"
// result. Track paren balance instead: once a boilerplate line opens more
// parens than it closes, keep consuming (and dropping) lines until the
// statement's own parens balance back out.
function parenDelta(line: string): number {
	let delta = 0;
	for (const ch of line) {
		if (ch === '(') delta++;
		else if (ch === ')') delta--;
	}
	return delta;
}

function isBoilerplateStart(line: string): boolean {
	return (
		/^\s*sys\.path\.insert\s*\(/.test(line) ||
		/^\s*from\s+_load\s+import\b/.test(line) ||
		/^\s*\S+\s*=\s*load_solution\s*\(/.test(line)
	);
}

export function sanitizeStudentCode(code: string): string {
	const kept: string[] = [];
	let openParens = 0;

	for (const line of code.split('\n')) {
		if (openParens > 0) {
			openParens += parenDelta(line);
			continue;
		}
		if (isBoilerplateStart(line)) {
			openParens = Math.max(0, parenDelta(line));
			continue;
		}
		kept.push(line);
	}

	return kept.join('\n');
}
