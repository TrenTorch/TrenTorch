import { problemsetProblems, type ProblemsetDifficulty } from '$data/problemset';

export interface ProblemsetDifficultyProgress {
	difficulty: ProblemsetDifficulty;
	solved: number;
	total: number;
}

export interface ProblemsetProgressStats {
	solved: number;
	total: number;
	byDifficulty: ProblemsetDifficultyProgress[];
}

const difficulties: ProblemsetDifficulty[] = ['Beginner', 'Intermediate', 'Advanced'];

export function getProblemsetProgressStats(
	solvedSlugs: ReadonlySet<string>
): ProblemsetProgressStats {
	const byDifficulty: ProblemsetDifficultyProgress[] = difficulties.map((difficulty) => {
		const questions = problemsetProblems.filter((problem) => problem.difficulty === difficulty);
		return {
			difficulty,
			solved: questions.filter((problem) => solvedSlugs.has(problem.slug)).length,
			total: questions.length
		};
	});

	return {
		solved: byDifficulty.reduce((total, item) => total + item.solved, 0),
		total: problemsetProblems.length,
		byDifficulty
	};
}
