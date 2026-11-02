import { describe, expect, it } from 'vitest';
import { highlightPython } from './highlight-python';

const kinds = (line: string) =>
	highlightPython(line)[0]
		.filter((t) => t.kind !== 'plain')
		.map((t) => `${t.kind}:${t.text}`);

describe('highlightPython', () => {
	it('colours imports, the function name after def, and keywords', () => {
		expect(kinds('import numpy as np')).toEqual(['keyword:import', 'keyword:as']);
		expect(kinds('def softmax(x):')).toEqual(['keyword:def', 'function:softmax']);
		expect(kinds('    return x')).toEqual(['keyword:return']);
	});

	it('colours numbers, strings and comments, and leaves a hash inside a string alone', () => {
		expect(kinds('y = 1.5e-3')).toEqual(['number:1.5e-3']);
		expect(kinds("s = 'a # b'")).toEqual(["string:'a # b'"]);
		expect(kinds('x = 1  # one')).toEqual(['number:1', 'comment:# one']);
	});

	it('knows a few built-ins as functions, but not a name that merely contains one', () => {
		expect(kinds('m = max(a, b)')).toEqual(['function:max']);
		expect(kinds('maximum = 3')).toEqual(['number:3']);
	});

	it('keeps every character: joining the tokens gives the line back', () => {
		const code = 'def f(a, b=2):\n    """doc"""\n    return a + b  # sum\n\n';
		const joined = highlightPython(code)
			.map((line) => line.map((t) => t.text).join(''))
			.join('\n');
		expect(joined).toBe(code);
	});

	it('does not mistake a name after a parenthesis for the function after def', () => {
		expect(kinds('x = f(def_)')).toEqual([]);
		expect(kinds('def  g():')).toEqual(['keyword:def', 'function:g']);
	});

	it('keeps colouring a docstring as a string over several lines, and picks code up again after it', () => {
		const lines = highlightPython(
			'def f(x):\n    """The sum is\n    in a loop for x\n    """\n    return x'
		);
		expect(lines[1].map((t) => t.kind)).toEqual(['plain', 'string']);
		expect(lines[2].map((t) => t.kind)).toEqual(['string']);
		expect(lines[3].map((t) => t.kind)).toEqual(['string']);
		expect(lines[4].map((t) => t.kind)).toEqual(['plain', 'keyword', 'plain']);
	});

	it('closes a one-line docstring and goes on', () => {
		const [line] = highlightPython('    """doc""" if x else 1');
		expect(line.map((t) => `${t.kind}:${t.text}`)).toContain('keyword:if');
		expect(line[1]).toEqual({ text: '"""doc"""', kind: 'string' });
	});
});
