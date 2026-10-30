import { describe, it, expect } from 'vitest';
import { curriculum as generated } from 'virtual:curriculum/bundle';

const questionsOf = (roots: typeof generated.roots) =>
	roots.flatMap((root) =>
		root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
	);
const questions = questionsOf(generated.roots);
// DSA sheet questions keep their theory on a per-step page, not in the question itself.
const dsaSheetIds = new Set(
	questionsOf(generated.roots.filter((r) => r.id === 'dsa-sheet')).map((q) => q.id)
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
				(!q.theoryMarkdown.trim() && !dsaSheetIds.has(q.id)) ||
				!q.starterCode?.trim() ||
				!q.oracleSolutionCode.trim() ||
				!q.oracleExplanationMarkdown.trim() ||
				!q.testsCode.trim()
		);
		expect(incomplete.map((q) => q.id)).toEqual([]);
	});

	it('every extra-language solution is non-empty', () => {
		const bad = questions.filter(
			(q) =>
				q.languageSolutions &&
				Object.values(q.languageSolutions).some((code) => !code?.trim())
		);
		expect(bad.map((q) => q.id)).toEqual([]);
	});

	it('every difficulty is one the UI knows how to badge', () => {
		const allowed = new Set(['Beginner', 'Intermediate', 'Advanced', 'Mastery']);
		expect(questions.filter((q) => !allowed.has(q.difficulty)).map((q) => q.id)).toEqual([]);
	});

	it('every question has at least one tag', () => {
		expect(questions.filter((q) => q.tags.length === 0).map((q) => q.id)).toEqual([]);
	});
});
