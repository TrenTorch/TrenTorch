export const MAX_CODE_LENGTH = 50000;
export const MAX_DESCRIPTION_LENGTH = 30000;

// Question ids become folder names in the user's repo, so only plain slugs.
export const isSafeQuestionId = (id: unknown): id is string =>
	typeof id === 'string' && /^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$/.test(id) && !id.includes('..');

export interface SolutionInput {
	questionId: string;
	title: string;
	difficulty: string;
	tags: string[];
	description: string;
	code: string;
}

export function parseSolutionInput(body: unknown): SolutionInput | null {
	if (typeof body !== 'object' || body === null) return null;
	const b = body as Record<string, unknown>;
	if (!isSafeQuestionId(b.questionId)) return null;
	if (typeof b.code !== 'string' || b.code.length === 0 || b.code.length > MAX_CODE_LENGTH) {
		return null;
	}
	if (typeof b.description !== 'string' || b.description.length > MAX_DESCRIPTION_LENGTH) {
		return null;
	}
	const title = typeof b.title === 'string' ? b.title.slice(0, 200) : b.questionId;
	const difficulty = typeof b.difficulty === 'string' ? b.difficulty.slice(0, 40) : '';
	const tags = Array.isArray(b.tags)
		? b.tags
				.filter((t): t is string => typeof t === 'string')
				.slice(0, 20)
				.map((t) => t.slice(0, 40))
		: [];
	return {
		questionId: b.questionId,
		title,
		difficulty,
		tags,
		description: b.description,
		code: b.code
	};
}

export function buildReadme(input: SolutionInput): string {
	const meta = [input.difficulty, ...input.tags].filter(Boolean).join(' | ');
	return `# ${input.title}\n\n${meta ? `${meta}\n\n` : ''}${input.description.trim()}\n`;
}

export function solutionFiles(input: SolutionInput): { path: string; content: string }[] {
	return [
		{ path: `${input.questionId}/solution.py`, content: `${input.code.trimEnd()}\n` },
		{ path: `${input.questionId}/README.md`, content: buildReadme(input) }
	];
}
