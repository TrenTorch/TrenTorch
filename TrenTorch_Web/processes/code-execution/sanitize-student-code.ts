import { isPureModuleAttributeAlias } from '../ide-content/strip-load-solution-boilerplate';

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
// is provided by the harness (see buildTestHarness), which defines the
// dependency solutions, and any names the starter renames them to, before the
// student's code runs.
//
// The starters carry the same header, so it is not only pasted solutions:
// every student who leaves the starter as it is sends it. That includes
// module handles,
//
//   _cond_prob = load_solution("...")
//   marginal_x = _cond_prob.marginal_x
//
// where dropping only the first line leaves `marginal_x = _cond_prob.marginal_x`
// behind, which raises NameError as the code is defined, before any test runs.
// So aliases off a module handle that was just removed are dropped too.
//
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
	const lines = code.split('\n');
	const kept: string[] = [];
	// Names bound by a `name = load_solution(...)` line that has been removed.
	const removedModuleVars = new Set<string>();
	let i = 0;

	while (i < lines.length) {
		const line = lines[i];

		if (isBoilerplateStart(line)) {
			const moduleVar = /^\s*([A-Za-z_]\w*)\s*=\s*load_solution\s*\(/.exec(line)?.[1];
			if (moduleVar) removedModuleVars.add(moduleVar);
			let openParens = Math.max(0, parenDelta(line));
			i++;
			while (openParens > 0 && i < lines.length) {
				openParens += parenDelta(lines[i]);
				i++;
			}
			continue;
		}

		if (removedModuleVars.size > 0) {
			let end = i;
			let balance = parenDelta(line);
			while (balance > 0 && end + 1 < lines.length) {
				end++;
				balance += parenDelta(lines[end]);
			}
			const statement = lines.slice(i, end + 1).join('\n');
			const eqIdx = statement.indexOf('=');
			if (eqIdx !== -1 && isPureModuleAttributeAlias(statement, eqIdx, removedModuleVars)) {
				i = end + 1;
				continue;
			}
		}

		kept.push(line);
		i++;
	}

	return kept.join('\n');
}
