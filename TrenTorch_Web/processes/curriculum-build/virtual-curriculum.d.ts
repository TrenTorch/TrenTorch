// Types for the virtual modules served by vite-plugin-curriculum.mjs.
// Ambient so that svelte-check and the TypeScript language service see them
// without a file-level import.

declare module 'virtual:curriculum/bundle' {
	import type { CurriculumBundle } from '$data/curriculum/bundle-types';
	export const curriculum: CurriculumBundle;
}

declare module 'virtual:curriculum/dsa-sheet' {
	import type { DsaSheet } from '$data/curriculum/bundle-types';
	export const dsaSheet: DsaSheet;
}

declare module 'virtual:curriculum/problemset' {
	import type { ProblemsetSource } from '$data/curriculum/bundle-types';
	export const problemsetSources: ProblemsetSource[];
}

declare module 'virtual:curriculum/catalogue' {
	// Shape is validated where it is read: data/questions.ts (Catalogue).
	export const catalogue: unknown;
}
