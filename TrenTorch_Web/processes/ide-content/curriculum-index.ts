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
	root: string;
	section: string;
	track: string;
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
	// Optional id of a client-side widget (platform/widgets/) to mount in
	// the Theory tab -- see README.md frontmatter's `widget` field.
	widgetId?: string;
}

interface GeneratedTrack {
	id: string;
	questions: GeneratedQuestion[];
}

interface GeneratedSection {
	id: string;
	tracks: GeneratedTrack[];
}

interface GeneratedRoot {
	id: string;
	sections: GeneratedSection[];
}

const curriculum = generatedCurriculum as { roots: GeneratedRoot[] };

// Flat id -> question lookup. It is also how a load_solution("<id>") call in a
// question's tests or solution is resolved: a question names another one by
// the `name` in its README, never by where that question sits on disk, so
// moving or renumbering folders cannot break a dependency (see
// strip-load-solution-boilerplate.ts and data/app_data/_load.py).
export const questionsById = new Map<string, GeneratedQuestion>();

for (const root of curriculum.roots) {
	for (const section of root.sections) {
		for (const track of section.tracks) {
			for (const question of track.questions) {
				questionsById.set(question.id, question);
			}
		}
	}
}
