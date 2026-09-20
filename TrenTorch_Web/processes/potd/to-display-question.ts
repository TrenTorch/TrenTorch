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

const POTD_DATE_FORMAT = new Intl.DateTimeFormat('en-US', {
	month: 'long',
	day: 'numeric',
	year: 'numeric'
});

// Date-only ISO strings are parsed as UTC by `new Date(string)`, which shifts
// the displayed calendar day for users west of UTC. POTD dates represent the
// student's local calendar, so construct local midnight explicitly instead.
export function parseLocalDateString(dateString: string): Date {
	const [year, month, day] = dateString.split('-').map(Number);
	return new Date(year, month - 1, day);
}

export interface PotdDisplayQuestion {
	question: Question;
	sectionLabel: string;
	trackLabel: string;
}

// `date` (the PotdEntry's own 'YYYY-MM-DD') is optional only so this stays
// usable for a hypothetical non-dated caller -- every real POTD call site
// passes it, so every POTD question's displayed title carries the exact
// date it ran, not just the section header grouping it sits under.
export function toDisplayQuestion(
	generated: GeneratedQuestion,
	date?: string
): PotdDisplayQuestion {
	const title = date
		? `${generated.title} (${POTD_DATE_FORMAT.format(parseLocalDateString(date))})`
		: generated.title;
	return {
		question: {
			slug: generated.id,
			title,
			difficulty: DIFFICULTY_MAP[generated.difficulty],
			topics: generated.tags
		},
		sectionLabel: humanize(generated.section),
		trackLabel: humanize(generated.track)
	};
}
