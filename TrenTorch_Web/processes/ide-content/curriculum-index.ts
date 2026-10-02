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
	// Raw, numeric-prefixed on-disk directory names -- see
	// processes/curriculum-build/build-question.mjs's comment on these
	// same fields for why they're needed alongside root/section/track.
	rootFolder: string;
	sectionFolder: string;
	trackFolder: string;
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

// Flat id -> question lookup, and a GLOBAL full-path -> question lookup
// for resolving a question's cross-question test dependencies -- see
// strip-load-solution-boilerplate.ts. The full path (rootFolder/
// sectionFolder/trackFolder/folder) is what a load_solution("...") call's string
// argument actually names, exactly mirroring data/app_data/_load.py's
// own resolution (see that file's docstring: paths are deliberately
// root/section/track/folder-qualified so no two tracks' "01-..." folders can
// ever collide with each other). A dependency lookup keyed by bare
// folder name alone -- and scoped to only the current question's own
// track -- silently fails the moment a question depends on a DIFFERENT
// track's solution (a common, deliberate pattern across this
// curriculum, e.g. an AdaBoost question depending on
// the decision-tree best-split question).
export const questionsById = new Map<string, GeneratedQuestion>();
export const questionsByFullPath = new Map<string, GeneratedQuestion>();

for (const root of curriculum.roots) {
	for (const section of root.sections) {
		for (const track of section.tracks) {
			for (const question of track.questions) {
				questionsById.set(question.id, question);
				questionsByFullPath.set(
					`${question.rootFolder}/${question.sectionFolder}/${question.trackFolder}/${question.folder}`,
					question
				);
			}
		}
	}
}
