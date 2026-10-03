// The slim catalogue the /questions, /potd and progress pages read: titles and
// the root -> section -> track -> question hierarchy, with none of the
// statement/theory/solution text that the IDE bundle carries. Everything in it
// comes from the folders and their meta.json / README.md files, so there is
// nothing to keep in sync by hand.

/**
 * @typedef {{ title: string, topics?: string[], companies?: { names: string[], roles: string } }} Meta
 * @typedef {{ id: string, title: string, difficulty: string }} BuiltQuestion
 * @typedef {{ id: string, meta: Meta, questions: BuiltQuestion[] }} BuiltTrack
 * @typedef {{ id: string, meta: Meta, tracks: BuiltTrack[] }} BuiltSection
 * @typedef {{ id: string, meta: Meta, sections: BuiltSection[] }} BuiltRoot
 */

// README difficulty has four levels, the catalogue shows three.
/** @type {Record<string, 'Easy' | 'Medium' | 'Hard'>} */
const DIFFICULTY = { Beginner: 'Easy', Intermediate: 'Medium', Advanced: 'Hard', Mastery: 'Hard' };

// `topics` and `companies` are set on the highest folder they are shared by
// and inherited by everything below: the nearest meta.json going down wins.
// With no `topics` anywhere on the way, a track falls back to its root's title.
/**
 * @param {'topics' | 'companies'} key
 * @param {{ meta: Meta }[]} levels root first, track last
 */
function inherit(key, ...levels) {
	for (const level of [...levels].reverse()) {
		if (level.meta[key] !== undefined) return level.meta[key];
	}
	return undefined;
}

/**
 * The list pages key sections and tracks by title, and the IDE and the tests
 * look a question up by id, so none of these may repeat. Fail the build, naming
 * both places, instead of shipping a page Svelte refuses to render.
 * @param {BuiltRoot[]} roots
 */
export function assertUnique(roots) {
	/** @type {Map<string, string>} */
	const questions = new Map();
	for (const root of roots) {
		const sections = new Set();
		const tracks = new Map();
		for (const section of root.sections) {
			if (sections.has(section.meta.title)) {
				throw new Error(`${root.id}: two sections are titled "${section.meta.title}"`);
			}
			sections.add(section.meta.title);
			for (const track of section.tracks) {
				const where = `${root.id}/${section.id}/${track.id}`;
				if (tracks.has(track.meta.title)) {
					throw new Error(
						`${root.id}: two tracks are titled "${track.meta.title}" (${tracks.get(track.meta.title)} and ${where})`
					);
				}
				tracks.set(track.meta.title, where);
				for (const question of track.questions) {
					if (questions.has(question.id)) {
						throw new Error(
							`duplicate question name "${question.id}" (${questions.get(question.id)} and ${where})`
						);
					}
					questions.set(question.id, where);
				}
			}
		}
	}
}

/** @param {BuiltRoot[]} roots */
export function buildCatalogue(roots) {
	assertUnique(roots);
	return {
		parts: roots.map((root) => ({
			id: `part-${root.id}`,
			title: root.meta.title,
			sections: root.sections.map((section) => ({
				name: section.meta.title,
				tracks: section.tracks.map((track) => {
					const topics = inherit('topics', root, section, track) ?? [root.meta.title];
					const companies = inherit('companies', root, section, track);
					return {
						name: track.meta.title,
						topics,
						...(companies ? { companies } : {}),
						questions: track.questions.map((question) => {
							const difficulty = DIFFICULTY[question.difficulty];
							if (!difficulty) {
								throw new Error(`${question.id}: unknown difficulty "${question.difficulty}"`);
							}
							return { slug: question.id, title: question.title, difficulty };
						})
					};
				})
			}))
		}))
	};
}
