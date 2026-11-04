import { describe, expect, it } from 'vitest';
import { dsaResume } from './dsa-resume';

const qs = ['a', 'b', 'c'].map((id) => ({ id, title: id.toUpperCase() }));

describe('dsaResume', () => {
	it('starts a first-time visitor at the first question', () => {
		expect(dsaResume(qs, new Set(), undefined)).toEqual({ kind: 'start', question: qs[0] });
	});
	it('continues the last opened question while it is unsolved', () => {
		expect(dsaResume(qs, new Set(['a']), 'c')).toEqual({ kind: 'continue', question: qs[2] });
		expect(dsaResume(qs, new Set(), 'b')?.kind).toBe('continue');
	});
	it('offers the next unsolved one when nothing is half-done', () => {
		expect(dsaResume(qs, new Set(['a']), 'a')).toEqual({ kind: 'next', question: qs[1] });
		expect(dsaResume(qs, new Set(['a', 'c']), undefined)).toEqual({
			kind: 'next',
			question: qs[1]
		});
	});
	it('has nowhere to send a student who has solved everything', () => {
		expect(dsaResume(qs, new Set(['a', 'b', 'c']), 'c')).toBeNull();
	});
	it('ignores a last-opened id that is not on the sheet', () => {
		expect(dsaResume(qs, new Set(), 'zzz')?.kind).toBe('start');
	});
});
