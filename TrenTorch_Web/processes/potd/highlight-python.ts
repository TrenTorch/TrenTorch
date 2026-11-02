// A small, forgiving colouring of Python for the home page's code preview. It does not parse: it only
// recognises what reads well in a few lines (comments, strings, numbers, keywords, the name after `def`,
// a few built-ins). The real editor uses CodeMirror; this exists so the landing page ships none of it.

export type TokenKind = 'keyword' | 'function' | 'number' | 'comment' | 'string' | 'plain';
export interface Token {
	text: string;
	kind: TokenKind;
}

const KEYWORDS = new Set(
	(
		'and as assert break class continue def del elif else except finally for from global if import in is ' +
		'lambda nonlocal not or pass raise return try while with yield True False None'
	).split(' ')
);
const BUILTINS = new Set(
	'abs all any enumerate float int len list map max min print range reversed round set sorted sum tuple zip dict isinstance'.split(
		' '
	)
);

const PATTERN =
	/(#.*$)|("""|''')|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+(?:\.\d+)?(?:e[-+]?\d+)?\b)|([A-Za-z_]\w*)|(\s+|.)/gy;

/** Whether a line starts inside a triple-quoted string, and which quote closes it. */
type Open = '"""' | "'''" | null;

/** One line of code as tokens, and the triple quote still open at its end. A `def` makes the next name a function. */
function tokenizeLine(line: string, open: Open): { tokens: Token[]; open: Open } {
	const tokens: Token[] = [];
	const push = (text: string, kind: TokenKind) => {
		const last = tokens[tokens.length - 1];
		// Neighbouring pieces of the same kind read as one.
		if (last && last.kind === kind) last.text += text;
		else tokens.push({ text, kind });
	};
	let afterDef = false;
	let at = 0;
	if (open) {
		// Inside a docstring: everything is string up to the closing quote.
		const end = line.indexOf(open);
		if (end < 0) return { tokens: line ? [{ text: line, kind: 'string' }] : [], open };
		push(line.slice(0, end + 3), 'string');
		at = end + 3;
		open = null;
	}
	PATTERN.lastIndex = at;
	let match: RegExpExecArray | null;
	while (PATTERN.lastIndex < line.length && (match = PATTERN.exec(line))) {
		const [text, comment, triple, string, number, word] = match;
		if (triple) {
			// A docstring that opens here; it may close on this same line.
			const end = line.indexOf(triple, PATTERN.lastIndex);
			if (end < 0) {
				push(line.slice(PATTERN.lastIndex - 3), 'string');
				return { tokens, open: triple as Open };
			}
			push(line.slice(PATTERN.lastIndex - 3, end + 3), 'string');
			PATTERN.lastIndex = end + 3;
			continue;
		}
		let kind: TokenKind = 'plain';
		if (comment) kind = 'comment';
		else if (string) kind = 'string';
		else if (number) kind = 'number';
		else if (word) {
			if (afterDef) kind = 'function';
			else if (KEYWORDS.has(word)) kind = 'keyword';
			else if (BUILTINS.has(word)) kind = 'function';
			afterDef = word === 'def' && !afterDef;
		} else if (text.trim()) afterDef = false;
		push(text, kind);
	}
	return { tokens, open };
}

export function highlightPython(code: string): Token[][] {
	let open: Open = null;
	return code.split('\n').map((line) => {
		const result = tokenizeLine(line, open);
		open = result.open;
		return result.tokens;
	});
}
