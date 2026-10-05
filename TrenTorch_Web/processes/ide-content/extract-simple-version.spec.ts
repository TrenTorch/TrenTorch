import { describe, it, expect } from 'vitest';
import { questionsById } from './curriculum-index';
import { extractSimpleVersion } from './extract-simple-version';

describe('extractSimpleVersion', () => {
	it('returns only the section under the heading, stopping at the next heading', () => {
		const theory =
			'### The simple version\n\nFirst idea.\n\nSecond idea.\n\n### The formula\n\nx = y';
		expect(extractSimpleVersion(theory)).toBe('First idea.\n\nSecond idea.');
	});

	it('handles Windows line endings and a section that runs to the end', () => {
		expect(extractSimpleVersion('### The simple version\r\n\r\nJust this.\r\n')).toBe('Just this.');
	});

	it('returns null when there is no such section or it is empty', () => {
		expect(extractSimpleVersion('### The formula\n\nx = y')).toBeNull();
		expect(extractSimpleVersion('### The simple version\n\n### The formula\n\nx')).toBeNull();
	});

	it('finds it for almost every authored question, without pulling in later sections', () => {
		let found = 0;
		// Problemset questions are short drills with their own README shape.
		const authored = [...questionsById.values()].filter((q) => q.kind !== 'problemset');
		for (const question of authored) {
			const section = extractSimpleVersion(question.theoryMarkdown);
			if (!section) continue;
			found++;
			expect(section).not.toMatch(/^###\s/m);
			expect(section.length).toBeLessThan(2500);
		}
		// The Python part (91 questions) and the NumPy part (61) don't use this
		// heading in their theory (a different author, a different README
		// convention), while every other part does, so about 72% of questions have
		// it. The threshold sits just under that. GuidePane.svelte already handles
		// a missing section: it just renders no "simple version" callout for
		// those questions.
		expect(found).toBeGreaterThan(authored.length * 0.7);
	});
});
