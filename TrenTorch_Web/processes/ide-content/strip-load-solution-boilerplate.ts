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
// The fix for both: remove exactly the `from _load import load_solution`
// line, every `<var> = load_solution(...)` call (however many lines its
// arguments span), and every subsequent assignment whose right-hand side
// is purely attribute access off one of those `<var>` names (however many
// such aliasing lines follow, and however they're grouped into tuples) --
// and make sure every name that boilerplate would have bound already
// exists in the exec'd globals before the test functions that use it run
// (self-references are already covered, since the student's code execs
// first; cross-question references are covered by prepending the
// referenced track-mate's oracle solution ahead of the cleaned test code,
// see build-test-harness.ts).
//
// Critically, this must stop at the FIRST statement that isn't one of
// those two shapes, not at the first top-level `def` -- a number of real
// question files define genuine module-level fixtures (a shared test
// array, a couple of lambdas, even small helper classes) between the
// load_solution aliasing block and their first `def test_...`, and an
// earlier version of this function that scanned "import line through
// first `def`" silently deleted that fixture code, breaking every test
// that referenced it (an in-browser-only bug: standalone `pytest
// tests.py` never exhibited it, since nothing here runs there).
export function stripLoadSolutionBoilerplate(testsCode: string): {
	cleaned: string;
	dependencyPaths: string[];
	// Names bound to a whole module (`x = load_solution("...")`, nothing after
	// the call). Unlike an alias for one function, the tests may use these
	// as `x.something`, so the harness has to give them a value.
	// `self` is true when it loads the question's own solution (the student's
	// code), false when it loads another question's.
	moduleVars: { name: string; self: boolean; path?: string }[];
	// Literal solution paths the tests pass to load_solution, whether bound to a
	// module variable or called inside a test body. Each needs its own namespace.
	namespacePaths: string[];
	// Imports that give a dependency's function a new name, e.g.
	// `softmax_axis1 = load_solution("...").softmax`.
	renames: { target: string; attr: string }[];
} {
	const lines = testsCode.split('\n');
	const startIdx = lines.findIndex((line) =>
		line.trim().startsWith('from _load import load_solution')
	);
	if (startIdx === -1) {
		return {
			cleaned: testsCode,
			dependencyPaths: [],
			moduleVars: [],
			namespacePaths: [],
			renames: []
		};
	}

	const moduleVarNames = new Set<string>();
	const bareModuleVars = new Map<string, { self: boolean; path?: string }>();
	const renames: { target: string; attr: string }[] = [];
	// A removed alias that renames something (`a = dep.b`) is replaced by a
	// plain `a = b` at the same spot, so the new name stays bound.
	const rebindAtLine = new Map<number, string[]>();
	function recordRename(lineIdx: number, pairs: { target: string; attr: string }[]) {
		const changed = pairs.filter((p) => p.target !== p.attr);
		if (changed.length === 0) return;
		renames.push(...changed);
		rebindAtLine.set(
			lineIdx,
			changed.map((p) => `${p.target} = ${p.attr}`)
		);
	}
	const removedLineIdx = new Set<number>([startIdx]);

	// Net count of ()/[]/{} across a line -- used to find where a
	// statement that opens a paren on one line (load_solution's args, or a
	// parenthesized multi-line tuple of aliases) actually closes again.
	function bracketDelta(line: string): number {
		let delta = 0;
		for (const ch of line) {
			if (ch === '(' || ch === '[' || ch === '{') delta++;
			else if (ch === ')' || ch === ']' || ch === '}') delta--;
		}
		return delta;
	}

	let i = startIdx + 1;
	while (i < lines.length) {
		const line = lines[i];
		const trimmed = line.trim();
		// Blank lines and comments are harmless either way -- skip over
		// them without ending the scan, but don't remove them either
		// (leaving a stray blank line or comment behind costs nothing).
		if (trimmed === '' || trimmed.startsWith('#')) {
			i++;
			continue;
		}

		// Gather this statement's full span: start here, keep pulling in
		// lines while unclosed brackets remain open.
		let j = i;
		let balance = bracketDelta(line);
		while (balance > 0 && j + 1 < lines.length) {
			j++;
			balance += bracketDelta(lines[j]);
		}
		const statementLines = lines.slice(i, j + 1);
		const statementText = statementLines.join('\n');

		const loadCallMatch = /^\s*([A-Za-z_]\w*)\s*=\s*load_solution\s*\(/.exec(statementText);
		if (loadCallMatch) {
			const name = loadCallMatch[1];
			moduleVarNames.add(name);
			const tail = loadCallTail(statementText);
			if (tail === '') {
				const self =
					/load_solution\(\s*f["']/.test(statementText) || statementText.includes('__file__');
				const path = /load_solution\(\s*["']([^"']+)["']\s*\)/.exec(statementText)?.[1];
				bareModuleVars.set(name, { self, path: self ? undefined : path });
			} else {
				// `name = load_solution("...").attr`. When the name differs from
				// the attribute this is a rename (softmax_axis1 = ....softmax),
				// and deleting the line would leave `name` unbound.
				const attr = /^\.\s*([A-Za-z_]\w*)$/.exec(tail)?.[1];
				if (attr && attr !== name) recordRename(i, [{ target: name, attr }]);
			}
			for (let k = i; k <= j; k++) removedLineIdx.add(k);
			i = j + 1;
			continue;
		}

		const eqIdx = statementText.indexOf('=');
		const isAliasAssignment =
			eqIdx !== -1 && isPureModuleAttributeAlias(statementText, eqIdx, moduleVarNames);
		if (isAliasAssignment) {
			recordRename(i, moduleAliasPairs(statementText, eqIdx));
			for (let k = i; k <= j; k++) removedLineIdx.add(k);
			i = j + 1;
			continue;
		}

		// First statement that's neither a load_solution(...) call nor a
		// pure alias off an already-seen module var -- boilerplate ends
		// here, everything from this line on is real content and stays.
		break;
	}

	// load_solution() takes a full slash path from data/, e.g.
	// "01-classical-ml/01-linear-regression/01-hypothesis-function" --
	// kept whole (not just its last segment) since the same folder name
	// can legitimately exist under multiple tracks; questionsByFullPath
	// is keyed by this exact string. The self-reference form is an
	// f-string (load_solution(f"...{Path(__file__)...}")); skip anything
	// with a brace or __file__ in it -- the student's own code already
	// binds that name, so it needs no prelude.
	const removedText = [...removedLineIdx]
		.sort((a, b) => a - b)
		.map((idx) => lines[idx])
		.join('\n');
	const dependencyPaths = [
		...new Set(
			[...removedText.matchAll(/load_solution\(\s*f?["']([^"']+)["']\s*\)/g)]
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
	const cleaned = lines
		.flatMap((line, idx) => (removedLineIdx.has(idx) ? (rebindAtLine.get(idx) ?? []) : [line]))
		.filter((line) => !/^\s*sys\.path\.insert\s*\(/.test(line))
		.join('\n');

	// A test body can also load a solution itself, e.g.
	// `load_solution("00-.../01-entropy").entropy(...)`. The module-level scan
	// above never sees those, so without this the dependency's code was never
	// prepended and the call crashed in the browser.
	const inBodyPaths = [...cleaned.matchAll(/load_solution\(\s*["']([^"']+)["']\s*\)/g)].map(
		(m) => m[1]
	);
	return {
		cleaned,
		dependencyPaths: [...new Set([...dependencyPaths, ...inBodyPaths])],
		moduleVars: [...bareModuleVars].map(([name, info]) => ({ name, ...info })),
		namespacePaths: [
			...new Set([
				...inBodyPaths,
				...[...bareModuleVars.values()].flatMap((info) => (info.path ? [info.path] : []))
			])
		],
		renames
	};
}

// The text after the closing bracket of the load_solution(...) call, minus any
// trailing comment. '' means the statement is just `name = load_solution(...)`,
// which binds a whole module. `.attr` means it binds one attribute of it.
function loadCallTail(statementText: string): string | null {
	const open = statementText.indexOf('(', statementText.indexOf('load_solution'));
	if (open === -1) return null;
	let depth = 0;
	for (let k = open; k < statementText.length; k++) {
		const ch = statementText[k];
		if (ch === '(' || ch === '[' || ch === '{') depth++;
		else if (ch === ')' || ch === ']' || ch === '}') {
			depth--;
			if (depth === 0)
				return statementText
					.slice(k + 1)
					.replace(/#.*$/, '')
					.trim();
		}
	}
	return null;
}

// Pairs each name an alias statement binds with the attribute it reads, for
// statements already known to be pure module-attribute aliases:
// `a, b = m.x, m.y` gives [{a, x}, {b, y}].
function moduleAliasPairs(
	statementText: string,
	eqIdx: number
): { target: string; attr: string }[] {
	const targets = stripOuterParens(statementText.slice(0, eqIdx))
		.split(',')
		.map((s) => s.trim())
		.filter(Boolean);
	const values = stripOuterParens(statementText.slice(eqIdx + 1))
		.split(',')
		.map((s) => stripOuterParens(s))
		.filter(Boolean);
	if (targets.length !== values.length) return [];
	return targets.flatMap((target, n) => {
		const attr = /^[A-Za-z_]\w*\.([A-Za-z_]\w*)$/.exec(values[n])?.[1];
		return attr ? [{ target, attr }] : [];
	});
}

// True iff `statementText`'s left-hand side (before `eqIdx`) is one or
// more bare, comma-separated identifiers (optionally wrapped in parens
// for a tuple target), and its right-hand side is one or more
// comma-separated `<name>.<attr>` expressions where every `<name>` is
// already a known module variable -- the exact shape every real
// load_solution-derived alias line takes, however many names it binds or
// how it's wrapped across lines.
export function isPureModuleAttributeAlias(
	statementText: string,
	eqIdx: number,
	moduleVarNames: ReadonlySet<string>
): boolean {
	if (moduleVarNames.size === 0) return false;

	const lhs = statementText.slice(0, eqIdx).trim();
	const rhs = statementText.slice(eqIdx + 1).trim();

	const lhsTargets = stripOuterParens(lhs)
		.split(',')
		.map((s) => s.trim())
		.filter((s) => s.length > 0);
	if (lhsTargets.length === 0) return false;
	if (!lhsTargets.every((t) => /^[A-Za-z_]\w*$/.test(t))) return false;

	const rhsValues = stripOuterParens(rhs)
		.split(',')
		.map((s) => s.trim())
		.filter((s) => s.length > 0);
	if (rhsValues.length === 0) return false;
	return rhsValues.every((value) => {
		const stripped = stripOuterParens(value);
		const match = /^([A-Za-z_]\w*)\.[A-Za-z_]\w*$/.exec(stripped);
		return match !== null && moduleVarNames.has(match[1]);
	});
}

function stripOuterParens(text: string): string {
	let result = text.trim();
	while (result.startsWith('(') && result.endsWith(')')) {
		result = result.slice(1, -1).trim();
	}
	return result;
}
