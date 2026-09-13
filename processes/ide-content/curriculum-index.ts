// Shared index over the compiled curriculum -- see
// data/curriculum/generated-curriculum.json and data/app_data/README.md
// for where that file comes from (processes/curriculum-build/build.mjs,
// compiled from real .py/.md files authored under data/app_data/). Built
// once at module load (ES modules are cached singletons), then reused by
// every function under processes/ide-content/ that needs to look a
// question up by id or resolve a track-mate's oracle solution.
import generatedCurriculum from '$data/curriculum/generated-curriculum.json';
import type { QuestionMetadata } from '$data/curriculum/types';

export interface GeneratedQuestion {
	id: string;
	title: string;
	tags: string[];
	difficulty: QuestionMetadata['difficulty'];
	section: string;
	track: string;
	folder: string;
	order: number;
	statementMarkdown: string;
	theoryMarkdown: string;
	// Hand-authored student stub (data/<...>/starter.py). Optional: older
	// questions don't have one and fall back to a signature derived from
	// the statement fence -- see extractStarterCode.
	starterCode?: string;
	oracleSolutionCode: string;
	oracleExplanationMarkdown: string;
	testsCode: string;
}

interface GeneratedTrack {
	id: string;
	questions: GeneratedQuestion[];
}

interface GeneratedSection {
	id: string;
	tracks: GeneratedTrack[];
}

const curriculum = generatedCurriculum as { sections: GeneratedSection[] };

// Flat id -> question lookup, and id -> (track-mates, keyed by folder
// name) for resolving a question's cross-question test dependencies --
// see strip-load-solution-boilerplate.ts.
export const questionsById = new Map<string, GeneratedQuestion>();
export const trackMatesByQuestionId = new Map<string, Map<string, GeneratedQuestion>>();

for (const section of curriculum.sections) {
	for (const track of section.tracks) {
		const byFolder = new Map(track.questions.map((q) => [q.folder, q]));
		for (const question of track.questions) {
			questionsById.set(question.id, question);
			trackMatesByQuestionId.set(question.id, byFolder);
		}
	}
}
