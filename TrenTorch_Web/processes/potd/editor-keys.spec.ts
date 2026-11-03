import { describe, expect, it } from 'vitest';
import {
	affectedRange,
	blocksEdit,
	editForKey,
	exceedsLines,
	lockedRange,
	windowGrowth,
	type Edit
} from './editor-keys';

const apply = (value: string, e: Edit) => value.slice(0, e.from) + e.insert + value.slice(e.to);

describe('Tab', () => {
	it('indents to the next multiple of four at the caret', () => {
		const e = editForKey('ab', 2, 2, 'Tab')!;
		expect(apply('ab', e)).toBe('ab  ');
		expect(e.selStart).toBe(4);
	});
	it('indents every selected line, and dedents them with Shift', () => {
		const v = 'a\n    b\nc';
		const indented = editForKey(v, 0, v.length, 'Tab')!;
		expect(apply(v, indented)).toBe('    a\n        b\n    c');
		const back = editForKey(apply(v, indented), 0, apply(v, indented).length, 'Tab', true)!;
		expect(apply(apply(v, indented), back)).toBe(v);
	});
	it('dedents the caret line on Shift+Tab', () => {
		const e = editForKey('    x = 1', 6, 6, 'Tab', true)!;
		expect(apply('    x = 1', e)).toBe('x = 1');
		expect(e.selStart).toBe(2);
	});
});

describe('Enter', () => {
	it('keeps the indent of the line', () => {
		expect(apply('    x = 1', editForKey('    x = 1', 9, 9, 'Enter')!)).toBe('    x = 1\n    ');
	});
	it('goes one level deeper after a colon', () => {
		expect(apply('def f():', editForKey('def f():', 8, 8, 'Enter')!)).toBe('def f():\n    ');
	});
});

describe('the locked signature line', () => {
	const sig = 'def f(a, b) -> int:';
	const value = `import numpy as np\n\n${sig}\n    return a`;
	const first = value.indexOf(sig);
	const last = first + sig.length;

	it('finds the line', () => {
		expect(lockedRange(value, sig)).toEqual([first, last]);
		expect(lockedRange(value, null)).toBeNull();
	});
	it('refuses typing, pasting and deleting on the line', () => {
		expect(blocksEdit(value, sig, first + 4, first + 4, 'x')).toBe(true);
		expect(blocksEdit(value, sig, first, first, 'x')).toBe(true);
		expect(blocksEdit(value, sig, last, last, 'x')).toBe(true);
		expect(blocksEdit(value, sig, first + 2, first + 6, '')).toBe(true);
		expect(
			blocksEdit(
				value,
				sig,
				...affectedRange(value, first + 3, first + 3, 'deleteContentBackward'),
				''
			)
		).toBe(true);
	});
	it('refuses joining it to a neighbour', () => {
		// Backspace at the start of the line, and delete at its end, would both remove a line break.
		expect(
			blocksEdit(value, sig, ...affectedRange(value, first, first, 'deleteContentBackward'), '')
		).toBe(true);
		expect(
			blocksEdit(value, sig, ...affectedRange(value, last, last, 'deleteContentForward'), '')
		).toBe(true);
	});
	it('allows a new line just before or after it, and edits elsewhere', () => {
		expect(blocksEdit(value, sig, first, first, '\n')).toBe(false);
		expect(blocksEdit(value, sig, last, last, '\n    ')).toBe(false);
		expect(blocksEdit(value, sig, 2, 2, 'x')).toBe(false);
		expect(blocksEdit(value, sig, value.length, value.length, 'x')).toBe(false);
		const bodyStart = last + 1;
		expect(
			blocksEdit(
				value,
				sig,
				...affectedRange(value, bodyStart + 6, bodyStart + 6, 'deleteWordBackward'),
				''
			)
		).toBe(false);
	});
});

describe('the window size', () => {
	const lines = (n: number) => Array.from({ length: n }, (_, i) => `l${i}`).join('\n');
	it('refuses a new line past the limit, but not an edit that adds none', () => {
		const full = lines(35);
		expect(exceedsLines(full, full.length, full.length, '\n')).toBe(true);
		expect(exceedsLines(full, 0, 0, 'x')).toBe(false);
		expect(exceedsLines(full, 0, full.length, 'a\nb')).toBe(false);
		const room = lines(34);
		expect(exceedsLines(room, room.length, room.length, '\n')).toBe(false);
		expect(exceedsLines(room, room.length, room.length, '\n\n')).toBe(true);
	});
	it('does not trap a longer-than-limit window: deleting is always fine', () => {
		const over = lines(40);
		expect(exceedsLines(over, 0, 10, '')).toBe(false);
	});
	it('widens from 25 lines to 20% at 35', () => {
		expect(windowGrowth(10)).toBe(1);
		expect(windowGrowth(25)).toBe(1);
		expect(windowGrowth(30)).toBeCloseTo(1.1);
		expect(windowGrowth(35)).toBeCloseTo(1.2);
		expect(windowGrowth(60)).toBeCloseTo(1.2);
	});
});
