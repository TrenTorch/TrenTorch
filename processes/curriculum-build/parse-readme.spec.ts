import { describe, it, expect } from 'vitest';
import { parseReadme } from './parse-readme.mjs';

const VALID = `---
name: example-question
title: Example Question
tags: [foo, bar]
difficulty: easy
---

## Statement

Do the thing.

## Theory

Why the thing works.

## Explanation

How the reference solution does the thing.
`;

describe('parseReadme', () => {
	it('parses a well-formed README into meta + three sections', () => {
		const result = parseReadme(VALID, '/fake/path');
		expect(result.meta).toEqual({
			name: 'example-question',
			title: 'Example Question',
			tags: ['foo', 'bar'],
			difficulty: 'easy'
		});
		expect(result.statementMarkdown).toBe('Do the thing.');
		expect(result.theoryMarkdown).toBe('Why the thing works.');
		expect(result.explanationMarkdown).toBe('How the reference solution does the thing.');
	});

	it('throws when the frontmatter block is missing', () => {
		expect(() =>
			parseReadme('## Statement\nx\n## Theory\ny\n## Explanation\nz', '/fake/path')
		).toThrow(/frontmatter/);
	});

	it('throws when a required frontmatter field is missing', () => {
		const missingDifficulty = VALID.replace('difficulty: easy\n', '');
		expect(() => parseReadme(missingDifficulty, '/fake/path')).toThrow(/difficulty/);
	});

	it('throws when sections are out of order', () => {
		const reordered = VALID.replace(
			'## Statement\n\nDo the thing.\n\n## Theory',
			'## Theory\n\nDo the thing.\n\n## Statement'
		);
		expect(() => parseReadme(reordered, '/fake/path')).toThrow(/Statement.*Theory.*Explanation/s);
	});

	it('swallows any content after ## Explanation into explanationMarkdown verbatim', () => {
		// parseReadme has no notion of a fourth section -- everything from
		// "## Explanation" to end-of-file is captured as-is. Anything an
		// author doesn't want shipped (e.g. a "Notes for the Judge" aside)
		// has to never be written in the source README, since the parser
		// itself won't strip it. See no-forbidden-sections.spec.ts for the
		// actual guard against that mistake.
		const withTrailingAside = VALID + '\n### Notes for the Judge\n\nDo not ship this.\n';
		const result = parseReadme(withTrailingAside, '/fake/path');
		expect(result.explanationMarkdown).toContain('Notes for the Judge');
	});
});
