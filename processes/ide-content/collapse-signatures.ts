// Authors write the signature in the statement fence with one parameter
// per line and the closing `)` on its own line. That reads fine in prose
// but lands in the editor as a five-line signature before the student has
// typed anything -- collapse each such `def name(\n  a,\n  b,\n) -> R:`
// back onto a single line. A signature that's already one line is left
// untouched (the inner `\n` in the pattern won't match).
export function collapseSignatures(code: string): string {
	return code.replace(
		/^(def \w+\()\n([\s\S]*?)\n(\)(?:\s*->[^\n:]+)?:)/gm,
		(_, open: string, params: string, close: string) => {
			const joined = params
				.split('\n')
				.map((line) => line.trim())
				.filter(Boolean)
				.join(' ')
				.replace(/,$/, '');
			return `${open}${joined}${close}`;
		}
	);
}
