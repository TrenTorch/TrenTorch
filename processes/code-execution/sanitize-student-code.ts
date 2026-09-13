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
export function sanitizeStudentCode(code: string): string {
	return code
		.split('\n')
		.filter(
			(line) =>
				!/^\s*sys\.path\.insert\s*\(/.test(line) &&
				!/^\s*from\s+_load\s+import\b/.test(line) &&
				!/^\s*\S+\s*=\s*load_solution\s*\(/.test(line)
		)
		.join('\n');
}
