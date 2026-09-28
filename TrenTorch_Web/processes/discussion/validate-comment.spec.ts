import { describe, expect, it } from 'vitest';
import { validateComment } from './validate-comment';

describe('validateComment', () => {
	it('rejects empty content and accepts the character and line limits', () => {
		expect(validateComment('')).toBe('Comments cannot be empty.');
		expect(validateComment('a'.repeat(2000))).toBeNull();
		expect(validateComment('😀'.repeat(2000))).toBeNull();
		expect(validateComment('a'.repeat(2001))).toContain('2000 characters');
		expect(validateComment(Array.from({ length: 30 }, () => 'line').join('\n'))).toBeNull();
		expect(validateComment(Array.from({ length: 31 }, () => 'line').join('\n'))).toContain(
			'30 lines'
		);
	});

	it('rejects oversized fenced, tilde, unclosed, and indented code blocks', () => {
		const eightLines = Array.from({ length: 8 }, () => 'code').join('\n');
		expect(validateComment(`\`\`\`python\n${eightLines}\n\`\`\``)).toContain('6 non-empty lines');
		expect(validateComment(`~~~python\n${eightLines}\n~~~`)).toContain('6 non-empty lines');
		expect(validateComment(`\`\`\`\n${eightLines}`)).toContain('6 non-empty lines');
		expect(
			validateComment(Array.from({ length: 8 }, (_, index) => `    code${index}`).join('\n'))
		).toContain('6 non-empty lines');
		expect(validateComment(Array.from({ length: 8 }, () => '\t').join('\n'))).toContain(
			'6 non-empty lines'
		);
	});

	it('accepts six-line and blank-line-separated code blocks', () => {
		const sixLines = Array.from({ length: 6 }, () => 'code').join('\n');
		expect(validateComment(`\`\`\`python\n${sixLines}\n\`\`\``)).toBeNull();
		expect(
			validateComment(['    one', '    two', '', '    three', '    four'].join('\n'))
		).toBeNull();
	});
});
