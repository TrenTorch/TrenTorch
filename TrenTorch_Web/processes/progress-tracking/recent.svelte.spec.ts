import { describe, expect, it } from 'vitest';
import { recent } from './recent.svelte';

describe('recent', () => {
	it('remembers the latest slug per area, independently', () => {
		recent.note('dsa', 'two-sum');
		recent.note('module', 'linear-regression');
		recent.note('dsa', 'valid-anagram');
		expect(recent.get('dsa')).toBe('valid-anagram');
		expect(recent.get('module')).toBe('linear-regression');
		expect(recent.get('paper')).toBeUndefined();
	});
});
