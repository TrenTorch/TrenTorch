import type { Difficulty, Question } from '$data/questions';
import type { GeneratedQuestion } from '$processes/ide-content/curriculum-index';

// POTD entries reference real IDE content (data/app_data/...) directly,
// deliberately NOT data/questions.ts's hand-curated list -- a Problem of
// the Day is real, playable content that still shouldn't have to also be
// added to the main Questions page listing. GeneratedQuestion's
// Beginner/Intermediate/Advanced/Mastery scale and questions.ts's
// Easy/Medium/Hard scale are two different vocabularies used in two
// different parts of this codebase; this is the one place they meet.
const DIFFICULTY_MAP: Record<GeneratedQuestion['difficulty'], Difficulty> = {
	Beginner: 'Easy',
	Intermediate: 'Medium',
	Advanced: 'Hard',
	Mastery: 'Hard'
};

function humanize(kebabCase: string): string {
	return kebabCase
		.split('-')
		.map((word) => word[0].toUpperCase() + word.slice(1))
		.join(' ');
}

export interface PotdDisplayQuestion {
	question: Question;
	sectionLabel: string;
	trackLabel: string;
}

export function toDisplayQuestion(generated: GeneratedQuestion): PotdDisplayQuestion {
	return {
		question: {
			slug: generated.id,
			title: generated.title,
			difficulty: DIFFICULTY_MAP[generated.difficulty],
			topics: generated.tags
		},
		sectionLabel: humanize(generated.section),
		trackLabel: humanize(generated.track)
	};
}
