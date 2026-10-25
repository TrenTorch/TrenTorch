// Types for build.mjs. The script is plain JavaScript, so TypeScript reads
// these declarations instead of checking its body (see tsconfig.json).
import type {
	CurriculumBundle,
	DsaSheet,
	ProblemsetSource
} from '../../data/curriculum/bundle-types';

export const DATA_DIR: string;

export function buildCurriculum(): {
	bundle: CurriculumBundle;
	catalogue: unknown;
	problemset: ProblemsetSource[];
	dsaSheet: DsaSheet;
	rootCount: number;
	questionCount: number;
};
