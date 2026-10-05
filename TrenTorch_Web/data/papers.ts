export type PaperKind = 'foundational' | 'breakthrough';

export interface PaperImplementation {
	slug: string;
	title: string;
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
}

export interface Paper {
	slug: string;
	title: string;
	authors: string;
	year: number;
	kind: PaperKind;
	summary: string;
	arxivId: string;
	implementations: PaperImplementation[];
}

export interface PaperTopic {
	slug: string;
	title: string;
	description: string;
	papers: Paper[];
}

export const paperTopics: PaperTopic[] = [
	{
		slug: 'neural-network-foundations',
		title: 'Neural Network Foundations',
		description:
			'Backpropagation, convolutions and the architectures that made deep learning work.',
		papers: []
	},
	{
		slug: 'optimization-and-training',
		title: 'Optimization and Training',
		description: 'Optimizers, normalization and the tricks that make large models train stably.',
		papers: [
			{
				slug: 'adam',
				title: 'Adam: A Method for Stochastic Optimization',
				authors: 'Diederik P. Kingma, Jimmy Ba',
				year: 2014,
				kind: 'breakthrough',
				summary:
					'Adam adapts a learning rate for every parameter by tracking running averages of the gradient and its square. It became the default optimizer for most deep learning.',
				arxivId: '1412.6980',
				implementations: [
					{
						slug: 'research-adam-moment-updates',
						title: 'Updating the two running moments',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-adam-single-step',
						title: 'One full update with bias correction',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-adam-minimize',
						title: 'Running the full optimization loop',
						difficulty: 'Intermediate'
					}
				]
			}
		]
	},
	{
		slug: 'classical-ml-and-learning-theory',
		title: 'Classical ML and Learning Theory',
		description: 'Ensembles, margins and the theory behind generalization.',
		papers: []
	},
	{
		slug: 'unsupervised-and-representation-learning',
		title: 'Unsupervised and Representation Learning',
		description: 'Autoencoders, word embeddings and contrastive learning.',
		papers: []
	},
	{
		slug: 'sequence-models-and-attention',
		title: 'Sequence Models and Attention',
		description: 'Recurrent models, sequence-to-sequence learning and the birth of attention.',
		papers: []
	},
	{
		slug: 'transformers-and-llms',
		title: 'Transformers and LLMs',
		description: 'The transformer, pretraining at scale and instruction following.',
		papers: []
	},
	{
		slug: 'computer-vision',
		title: 'Computer Vision',
		description: 'Residual networks, vision transformers and diffusion models for images.',
		papers: []
	},
	{
		slug: 'reinforcement-learning-and-alignment',
		title: 'Reinforcement Learning and Alignment',
		description: 'Policy gradients, PPO and preference-based fine-tuning.',
		papers: []
	},
	{
		slug: 'agentic-systems',
		title: 'Agentic Systems',
		description: 'Reasoning and acting with language models, tool use and self-correction.',
		papers: []
	},
	{
		slug: 'inference-distributed-and-production',
		title: 'Inference, Distributed and Production',
		description: 'Memory-efficient attention, large-model serving and distributed training.',
		papers: []
	}
];

export const papers: Paper[] = paperTopics.flatMap((topic) => topic.papers);

export function getPaper(slug: string): Paper | undefined {
	return papers.find((paper) => paper.slug === slug);
}
