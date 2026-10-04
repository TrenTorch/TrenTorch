import { questionsById } from '$processes/ide-content/curriculum-index';
import type { QuestionMetadata } from '$data/curriculum/types';
import { curriculum as learningCurriculum } from './questions';

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
}

export interface ProblemsetModule {
	id: string;
	title: string;
	description: string;
	learningPartId: string;
}

const moduleDetails: Record<string, Omit<ProblemsetModule, 'id' | 'learningPartId'>> = {
	'part-math': {
		title: 'Mathematics & Statistics',
		description: 'Linear algebra, calculus, probability, and statistical foundations'
	},
	'part-data-foundations': {
		title: 'Data & Statistics',
		description: 'Data analysis, preprocessing, inference, and experiments'
	},
	'part-classical-linear': {
		title: 'Classical ML',
		description: 'Supervised learning, models, and evaluation'
	},
	'part-classical-trees': {
		title: 'Trees & Ensembles',
		description: 'Decision trees, bagging, and boosting'
	},
	'part-classical-unsupervised': {
		title: 'Unsupervised ML',
		description: 'Clustering, dimensionality reduction, and anomaly detection'
	},
	'part-dl-core': {
		title: 'Deep Learning',
		description: 'Neural networks, layers, activations, and losses'
	},
	'part-dl-training': {
		title: 'DL Training',
		description: 'Optimization, regularization, and training dynamics'
	},
	'part-seq-modeling': {
		title: 'Sequence Models',
		description: 'Recurrent networks, attention, and sequence learning'
	},
	'part-transformers-llm': {
		title: 'Transformers & LLMs',
		description: 'Transformer blocks, language modeling, and LLM engineering'
	}
};

const learningParts = new Map(learningCurriculum.map((part) => [part.id, part]));
const problemsetQuestions = [...questionsById.values()]
	.filter((question) => question.kind === 'problemset')
	.sort((a, b) => a.order - b.order);

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
