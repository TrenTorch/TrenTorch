export type Difficulty = 'Easy' | 'Medium' | 'Hard';

// Which real companies/roles this question's SUBJECT AREA is relevant to --
// topic-based relevance derived from public engineering blogs and
// aggregated interview-experience reports, not a claim that this exact
// question was asked verbatim at any of these companies. Attached per
// Track (a `companies` entry in a meta.json), since the source data ties one company
// list to a whole subject area, not to individual questions.
export interface CompanyTag {
	names: string[];
	roles: string;
}

export interface Question {
	slug: string;
	title: string;
	difficulty: Difficulty;
	topics: string[];
	companies?: CompanyTag;
}

export interface Track {
	name: string;
	questions: Question[];
}

// The grouping layer between a root Part and its Tracks, e.g.
// Python -> "Semantics" -> [Basics, Strings, Lists, ...]. `tracks` on Part
// stays the flat list of every Track (so progress/SEO/search code needs no
// changes); `sections` is the same Tracks grouped for display.
export interface Section {
	name: string;
	tracks: Track[];
	questions: Question[];
}

export interface Part {
	id: string;
	title: string;
	tracks: Track[];
	sections?: Section[];
}

// The curriculum is generated, not written here: `npm run curriculum:build`
// walks data/app_data (each folder's meta.json for titles, topics and company
// tags; each question's README for its name, title and difficulty) and emits
// this slim catalogue. To add, move or rename anything, change the folders.
// The IDE's heavier content bundle (statements, solutions, tests) is a separate
// file, so none of it ships with the pages that only list questions.
import catalogue from './curriculum/generated-catalogue.json';

interface CatalogueTrack {
	name: string;
	topics: string[];
	companies?: CompanyTag;
	questions: { slug: string; title: string; difficulty: Difficulty }[];
}

interface Catalogue {
	parts: {
		id: string;
		title: string;
		sections: { name: string; tracks: CatalogueTrack[] }[];
	}[];
}

function toTrack({ name, topics, companies, questions }: CatalogueTrack): Track {
	return {
		name,
		questions: questions.map((question) => ({
			...question,
			topics,
			...(companies ? { companies } : {})
		}))
	};
}

export const curriculum: Part[] = (catalogue as Catalogue).parts.map((part) => {
	const sections = part.sections.map((section) => {
		const tracks = section.tracks.map(toTrack);
		return { name: section.name, tracks, questions: tracks.flatMap((track) => track.questions) };
	});
	return {
		id: part.id,
		title: part.title,
		sections,
		tracks: sections.flatMap((section) => section.tracks)
	};
});

/** `total` is always derived from the real curriculum data, never drifts
 * out of sync as questions get added. `completed` counts real solved
 * progress -- pass `solved.slugs` from the localStorage-backed store
 * (see processes/progress-tracking/solved.svelte.ts); omit it (or call with no
 * argument) to get 0 completed, e.g. for a server-rendered first paint
 * before the client-only store has hydrated. Intersected against real
 * slugs rather than just `solvedSlugs.size`, so a stale slug left over
 * from a since-renamed/removed question never inflates the count. */
export function getProgressStats(solvedSlugs: ReadonlySet<string> = new Set()): {
	completed: number;
	total: number;
} {
	const allSlugs = curriculum.flatMap((part) =>
		part.tracks.flatMap((track) => track.questions.map((q) => q.slug))
	);
	const completed = allSlugs.filter((slug) => solvedSlugs.has(slug)).length;
	return { completed, total: allSlugs.length };
}

/** How many *real* questions are attempted but not yet solved. Same
 * defensive intersection as getProgressStats: attempted.svelte.ts is
 * additive-only and never drops a slug, so a since-renamed or removed
 * question's slug can sit in that store indefinitely -- counting
 * `attemptedSlugs.size` directly (minus solved) would let a stale slug
 * inflate "in progress" even though no real question backs it, and the
 * Continue-where-you-left-off list (which looks each slug up via
 * findQuestionBySlug) would silently show fewer items than the count
 * implies. Intersecting against real slugs first keeps the two in sync. */
export function getInProgressCount(
	solvedSlugs: ReadonlySet<string>,
	attemptedSlugs: ReadonlySet<string>
): number {
	const allSlugs = curriculum.flatMap((part) =>
		part.tracks.flatMap((track) => track.questions.map((q) => q.slug))
	);
	return allSlugs.filter((slug) => attemptedSlugs.has(slug) && !solvedSlugs.has(slug)).length;
}

/** One row of curriculum-wide progress, one entry per Part, in curriculum
 * order. Used to render a real per-Part progress list (solved out of that
 * Part's own total) instead of a plain question-count-per-Part chart. */
export interface PartProgress {
	id: string;
	title: string;
	solved: number;
	total: number;
}

export function getPartProgress(solvedSlugs: ReadonlySet<string> = new Set()): PartProgress[] {
	return curriculum.map((part) => {
		const slugs = part.tracks.flatMap((track) => track.questions.map((q) => q.slug));
		return {
			id: part.id,
			title: part.title,
			solved: slugs.filter((slug) => solvedSlugs.has(slug)).length,
			total: slugs.length
		};
	});
}

/** Same idea, one row per Difficulty instead of per Part. */
export interface DifficultyProgress {
	difficulty: Difficulty;
	solved: number;
	total: number;
}

export function getDifficultyProgress(
	solvedSlugs: ReadonlySet<string> = new Set()
): DifficultyProgress[] {
	const allQuestions = curriculum.flatMap((part) => part.tracks.flatMap((t) => t.questions));
	const order: Difficulty[] = ['Easy', 'Medium', 'Hard'];
	return order.map((difficulty) => {
		const inThisDifficulty = allQuestions.filter((q) => q.difficulty === difficulty);
		return {
			difficulty,
			solved: inThisDifficulty.filter((q) => solvedSlugs.has(q.slug)).length,
			total: inThisDifficulty.length
		};
	});
}

/** A question plus which Part/Track it lives under, looked up by slug --
 * for anything that needs to show a real question's context (title,
 * difficulty, where it sits in the curriculum) given only a slug, e.g. a
 * "continue where you left off" list built from the attempted store. */
export interface QuestionWithLocation {
	question: Question;
	partTitle: string;
	trackName: string;
}

export function findQuestionBySlug(slug: string): QuestionWithLocation | undefined {
	for (const part of curriculum) {
		for (const track of part.tracks) {
			const question = track.questions.find((q) => q.slug === slug);
			if (question) return { question, partTitle: part.title, trackName: track.name };
		}
	}
	return undefined;
}
