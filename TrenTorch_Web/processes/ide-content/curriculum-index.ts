// Shared index over the compiled curriculum. The bundle is compiled in memory
// from the real .py/.md files under data/app_data/ (see data/app_data/README.md
// and processes/curriculum-build/build.mjs) and served as the virtual module
// `virtual:curriculum/bundle`. Built once at module load (ES modules are
// cached singletons), then reused by every function under processes/ide-content/
// that needs to look a question up by id or resolve a track-mate's oracle solution.
import { curriculum } from 'virtual:curriculum/bundle';
import type { GeneratedQuestion } from '$data/curriculum/bundle-types';

export type { GeneratedQuestion } from '$data/curriculum/bundle-types';

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
