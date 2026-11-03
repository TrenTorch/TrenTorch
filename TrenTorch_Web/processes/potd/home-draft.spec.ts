import { describe, expect, it } from 'vitest';
import { mergeDraft, stripHint } from './home-draft';
import { previewParts } from './home-preview';

const long = Array.from({ length: 40 }, (_, i) => `line${i} = ${i}`).join('\n');

describe('stripHint', () => {
	it('drops a trailing hint, and only that', () => {
		expect(stripHint('a = 1\n    # ...')).toBe('a = 1');
		expect(stripHint('a = 1\n    # ...\nb = 2')).toBe('a = 1\n    # ...\nb = 2');
	});
});

describe('mergeDraft', () => {
	it('puts the unseen rest of the starter after the edited window', () => {
		const { code: shown, lines: shownLines } = previewParts(long);
		const text = stripHint(shown).replace('line0 = 0', 'line0 = 99');
		const merged = mergeDraft(long, { id: 'q', text, shownLines });
		const lines = merged.trimEnd().split('\n');
		expect(lines[0]).toBe('line0 = 99');
		expect(lines).toHaveLength(40);
		expect(lines.at(-1)).toBe('line39 = 39');
	});

	it('keeps just the edit when the window showed the whole starter', () => {
		const starter = 'def f(x):\n    return x';
		expect(mergeDraft(starter, { id: 'q', text: 'def f(x):\n    return 2', shownLines: 2 })).toBe(
			'def f(x):\n    return 2\n'
		);
	});
});

it('puts a joined signature back in place of the lines it replaced', () => {
	const starter = 'def f(\n    a: int,\n    b: int,\n) -> int:\n    return a\n    # more\n' + long;
	const { code, lines } = previewParts(starter);
	expect(code.split('\n')[0]).toBe('def f(a: int, b: int) -> int:');
	const merged = mergeDraft(starter, { id: 'q', text: stripHint(code), shownLines: lines });
	expect(merged.startsWith('def f(\n    a: int,\n    b: int,\n) -> int:\n    return a')).toBe(true);
	expect(merged.trimEnd().split('\n').at(-1)).toBe('line39 = 39');
	expect(merged.match(/line0 = 0/g)).toHaveLength(1);
});

it('keeps a signature the visitor changed as they wrote it', () => {
	const starter = 'def f(\n    a: int,\n    b: int,\n) -> int:\n    return a';
	const { code, lines } = previewParts(starter);
	const text = stripHint(code).replace('b: int', 'b: float');
	expect(mergeDraft(starter, { id: 'q', text, shownLines: lines })).toBe(
		'def f(a: int, b: float) -> int:\n    return a\n'
	);
});

describe('a draft made on top of code already saved in the IDE', () => {
	const saved = `import numpy as np\n\n${Array.from({ length: 30 }, (_, i) => `x${i} = ${i}`).join('\n')}\n`;
	it('keeps that code and appends only what the window never showed', () => {
		const { code, lines } = previewParts(saved);
		const text = stripHint(code).replace('x0 = 0', 'x0 = 100');
		const merged = mergeDraft(saved, { id: 'q', text, shownLines: lines, base: saved });
		expect(merged).toBe(saved.replace('x0 = 0', 'x0 = 100'));
	});
});
