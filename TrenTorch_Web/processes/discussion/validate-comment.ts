export const MAX_COMMENT_CHARACTERS = 2000;
export const MAX_COMMENT_LINES = 30;
export const MAX_CODE_BLOCK_LINES = 6;

function isNonEmptyDatabaseLine(line: string): boolean {
	return line.replace(/^ +| +$/g, '') !== '';
}

// This mirrors the database trigger for immediate feedback; the trigger remains authoritative.
export function validateComment(content: string): string | null {
	const characterCount = [...content].length;
	if (characterCount === 0) return 'Comments cannot be empty.';
	if (characterCount > MAX_COMMENT_CHARACTERS) {
		return `Comments must be ${MAX_COMMENT_CHARACTERS} characters or fewer.`;
	}

	const body = content.replace(/\r/g, '');
	const lines = body.split('\n');
	if (lines.length > MAX_COMMENT_LINES) {
		return `Comments must be ${MAX_COMMENT_LINES} lines or fewer.`;
	}

	const fencedBlocks = /(```|~~~)[^\n]*\n([\s\S]*?)(?:\1|$)/g;
	for (const match of body.matchAll(fencedBlocks)) {
		const nonEmptyLines = match[2].split('\n').filter(isNonEmptyDatabaseLine).length;
		if (nonEmptyLines > MAX_CODE_BLOCK_LINES) {
			return `Code blocks must have ${MAX_CODE_BLOCK_LINES} non-empty lines or fewer.`;
		}
	}

	let indentedRun = 0;
	for (const line of lines) {
		if (/^( {4}|\t)/.test(line) && isNonEmptyDatabaseLine(line)) {
			indentedRun += 1;
			if (indentedRun > MAX_CODE_BLOCK_LINES) {
				return `Code blocks must have ${MAX_CODE_BLOCK_LINES} non-empty lines or fewer.`;
			}
		} else {
			indentedRun = 0;
		}
	}

	return null;
}
