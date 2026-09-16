import { describe, it, expect } from 'vitest';
import { quizBank, assembleQuiz } from './roadmap-quiz';

describe('roadmap quiz', () => {
	it('every question has a valid correctIndex into its own options', () => {
		for (const questions of Object.values(quizBank)) {
			for (const q of questions) {
				expect(q.correctIndex).toBeGreaterThanOrEqual(0);
				expect(q.correctIndex).toBeLessThan(q.options.length);
			}
		}
	});

	it('assembleQuiz with no domains returns just the general baseline', () => {
		expect(assembleQuiz([])).toEqual(quizBank.general);
	});

	it('assembleQuiz adds exactly one question per selected domain', () => {
		const quiz = assembleQuiz(['ds', 'ml']);
		expect(quiz).toHaveLength(quizBank.general.length + 2);
	});

	it('ignores unknown domain ids', () => {
		const quiz = assembleQuiz(['not-a-real-domain']);
		expect(quiz).toEqual(quizBank.general);
	});
});
