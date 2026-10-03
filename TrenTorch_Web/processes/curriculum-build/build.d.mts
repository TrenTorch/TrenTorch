// Types for build.mjs. The script is plain JavaScript, so TypeScript reads
// these declarations instead of checking its body (see tsconfig.json).
import type { CurriculumBundle } from '../../data/curriculum/bundle-types';

export const DATA_DIR: string;

export function buildCurriculum(): {
	bundle: CurriculumBundle;
	catalogue: unknown;
	rootCount: number;
	questionCount: number;
};
