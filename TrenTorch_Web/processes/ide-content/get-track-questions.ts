import { curriculum } from '$data/questions';
import { problemsetModules, problemsetProblems } from '$data/problemset';
import { potdEntries } from '$data/potd';
import { questionsById } from './curriculum-index';

export interface TrackQuestion {
	id: string;
	title: string;
}

export interface TrackQuestions {
	/** Id of the Part (the /questions/[partId] page) the question belongs to. */
	partId: string | null;
	/** The track's own title, from its meta.json. */
	track: string | null;
	questions: TrackQuestion[];
}

// Every question in the same track as `id`, in the order /questions lists
// them -- the IDE header's quick-nav drawer shows these. Read from the same
// catalogue the Questions pages use, so the drawer, its title and the back
// arrow's destination can never disagree with them. Scoped to one track
// rather than the whole curriculum so each prerendered page only carries
// that track's titles.
export function getTrackQuestions(id: string): TrackQuestions {
	for (const part of curriculum) {
		for (const track of part.tracks) {
			if (!track.questions.some((q) => q.slug === id)) continue;
			return {
				partId: part.id,
				track: track.name,
				questions: track.questions.map(({ slug, title }) => ({ id: slug, title }))
			};
		}
	}
	return { partId: null, track: null, questions: [] };
}

export interface SourceList {
	/** Heading under "Problems": the module or "Problem of the Day". */
	label: string;
	questions: (TrackQuestion & { date?: string })[];
}

// The Problemset page's own grouping: the question's module, in the order the page lists
// them. Null when the question is not a Problemset problem.
export function getProblemsetList(id: string): SourceList | null {
	const problem = problemsetProblems.find((p) => p.slug === id);
	if (!problem) return null;
	const module = problemsetModules.find((m) => m.id === problem.moduleId);
	return {
		label: module ? `Problemset · ${module.title}` : 'Problemset',
		questions: problemsetProblems
			.filter((p) => p.moduleId === problem.moduleId)
			.map(({ slug, title }) => ({ id: slug, title }))
	};
}

// Every Problem of the Day, newest first, when `id` is one. Carries the dates because
// "today" is the visitor's, not the build's: the header drops the ones not yet released.
export function getPotdList(id: string): SourceList | null {
	if (!potdEntries.some((e) => e.questionId === id)) return null;
	const questions = [...potdEntries]
		.sort((a, b) => b.date.localeCompare(a.date))
		.flatMap((e) => {
			const q = questionsById.get(e.questionId);
			return q ? [{ id: q.id, title: q.title, date: e.date }] : [];
		});
	return { label: 'Problem of the Day', questions };
}
