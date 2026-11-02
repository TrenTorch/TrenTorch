import { problemsetSources } from 'virtual:curriculum/problemset';
import type { QuestionMetadata } from '$data/curriculum/types';
import { curriculum as learningCurriculum } from './questions';
import { potdEntries } from './potd';
import type { PotdSummary } from '$processes/potd/potd-summary';

export type ProblemsetDifficulty = Exclude<QuestionMetadata['difficulty'], 'Mastery'>;
export type ProblemsetKind = 'direct' | 'case-study';

export interface ProblemsetProblem {
	slug: string;
	title: string;
	difficulty: ProblemsetDifficulty;
	kind: ProblemsetKind;
	moduleId: string;
	topic: string;
	caseCompany: string | null;
	tools: string[];
	order: number;
	// Set only for Problem of the Day picks: the local calendar day they ran.
	potdDate?: string;
}

export interface ProblemsetModule {
	id: string;
	title: string;
	description: string;
	learningPartId: string;
}

const moduleDetails: Record<string, Omit<ProblemsetModule, 'id' | 'learningPartId'>> = {
	'part-mathematics': {
		title: 'Mathematics & Statistics',
		description: 'Linear algebra, calculus, probability, and statistical foundations'
	},
	'part-data-science': {
		title: 'Data Science',
		description: 'Data processing, analysis, and experiments'
	},
	'part-classical-ml': {
		title: 'Classical ML',
		description: 'Supervised and unsupervised models, trees, ensembles, and evaluation'
	},
	'part-deep-learning': {
		title: 'Deep Learning',
		description: 'Neural networks, layers, activations, losses, and optimization'
	},
	'part-language-modelling-attention-llms': {
		title: 'Transformers & LLMs',
		description: 'Attention, transformer blocks, language modeling, and NLP'
	}
};

const learningParts = new Map(learningCurriculum.map((part) => [part.id, part]));
// Read from the slim virtual module, not the full question index: this file is imported by pages that
// run in the browser, and the full index would put every question's text into their JavaScript.
const problemsetQuestions = [...problemsetSources].sort((a, b) => a.order - b.order);

export const problemsetProblems: ProblemsetProblem[] = problemsetQuestions.map((question) => {
	const relatedModule = question.relatedModule;
	if (!relatedModule || question.difficulty === 'Mastery') {
		throw new Error(`Problemset question "${question.id}" is missing valid module metadata.`);
	}
	const relatedPart = learningParts.get(relatedModule.partId);
	if (
		!relatedPart ||
		!relatedPart.tracks.some((track) =>
			track.questions.some((moduleQuestion) =>
				moduleQuestion.topics.includes(relatedModule.topicTag)
			)
		)
	) {
		throw new Error(
			`Problemset question "${question.id}" references an unknown module/topic pair: ` +
				`${relatedModule.partId}|${relatedModule.topicTag}`
		);
	}

	const problemNumber = Number(question.id.match(/^problem-(\d+)-/)?.[1]);
	return {
		slug: question.id,
		title: question.title,
		difficulty: question.difficulty,
		kind: question.caseCompany ? 'case-study' : 'direct',
		moduleId: relatedModule.partId,
		topic: question.topic ?? relatedModule.topicTag,
		caseCompany: question.caseCompany ?? null,
		tools: question.tools ?? [],
		order: Number.isFinite(problemNumber) && problemNumber > 0 ? problemNumber : question.order
	};
});

export const problemsetModules: ProblemsetModule[] = [
	...new Set(
		problemsetQuestions
			.map((question) => question.relatedModule?.partId)
			.filter((partId): partId is string => Boolean(partId))
	)
].map((partId) => {
	const details = moduleDetails[partId];
	if (!details) throw new Error(`No Problemset module display metadata for "${partId}".`);
	return { id: partId, learningPartId: partId, ...details };
});

// Problem of the Day picks, so the Past POTD filter can list them. A pick belongs
// to no module, so it has an empty moduleId and its date is kept for the filter.
//
// Built from the summaries the page's server load provides, not from the curriculum index: importing
// the index here would put every question's text into the browser's JavaScript.
export function buildPotdProblems(summaries: PotdSummary[]): ProblemsetProblem[] {
	const byId = new Map(summaries.map((summary) => [summary.id, summary]));
	return potdEntries.flatMap((entry) => {
		const question = byId.get(entry.questionId);
		if (!question || question.difficulty === 'Mastery') return [];
		return [
			{
				slug: question.id,
				title: question.title,
				difficulty: question.difficulty,
				kind: question.caseCompany ? 'case-study' : 'direct',
				moduleId: '',
				topic: question.topic ?? question.tags[0] ?? 'potd',
				caseCompany: question.caseCompany ?? null,
				tools: question.tools ?? [],
				order: 0,
				potdDate: entry.date
			}
		];
	});
}
