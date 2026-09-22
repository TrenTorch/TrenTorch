import { describe, it, expect } from 'vitest';
import generated from './generated-curriculum.json';

const questions = generated.sections.flatMap((section) =>
	section.tracks.flatMap((track) => track.questions)
);

describe('generated curriculum bundle', () => {
	it('has no duplicate question ids', () => {
		const ids = questions.map((q) => q.id);
		expect(new Set(ids).size).toBe(ids.length);
	});

	it('every question ships every authored part', () => {
		const incomplete = questions.filter(
			(q) =>
				!q.statementMarkdown.trim() ||
				!q.theoryMarkdown.trim() ||
				!q.starterCode.trim() ||
				!q.oracleSolutionCode.trim() ||
				!q.oracleExplanationMarkdown.trim() ||
				!q.testsCode.trim()
		);
		expect(incomplete.map((q) => q.id)).toEqual([]);
	});

	it('every difficulty is one the UI knows how to badge', () => {
		const allowed = new Set(['Beginner', 'Intermediate', 'Advanced', 'Mastery']);
		expect(questions.filter((q) => !allowed.has(q.difficulty)).map((q) => q.id)).toEqual([]);
	});

	it('every question has at least one tag', () => {
		expect(questions.filter((q) => q.tags.length === 0).map((q) => q.id)).toEqual([]);
	});
});
