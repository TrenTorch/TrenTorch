import { dsaSheet } from 'virtual:curriculum/dsa-sheet';
import type { DsaSheetQuestion, DsaSheetStep } from './curriculum/bundle-types';

// The DSA sheet for the /dsa page. A slim virtual module (titles only), so the page does not pull
// the full question bundle into the browser.
export type { DsaSheetQuestion, DsaSheetStep, DsaSheetTopic } from './curriculum/bundle-types';

export const dsaSteps: DsaSheetStep[] = dsaSheet.steps;
export const dsaQuestions: DsaSheetQuestion[] = dsaSteps.flatMap((step) =>
	step.topics.flatMap((topic) => topic.questions)
);
