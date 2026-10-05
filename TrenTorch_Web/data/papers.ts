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
		papers: [
			{
				slug: 'dropout',
				title: 'Improving Neural Networks by Preventing Co-adaptation of Feature Detectors',
				authors:
					'Geoffrey Hinton, Nitish Srivastava, Alex Krizhevsky, Ilya Sutskever, Ruslan Salakhutdinov',
				year: 2012,
				kind: 'foundational',
				summary:
					'Dropout randomly removes units during training, which stops neurons from relying on each other and reduces overfitting.',
				arxivId: '1207.0580',
				implementations: [
					{
						slug: 'research-dropout-forward',
						title: 'The forward pass with inverted scaling',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-dropout-backward',
						title: 'Backpropagating through the mask',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-dropout-expectation',
						title: 'Averaging over masks recovers the input',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'he-initialization',
				title:
					'Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification',
				authors: 'Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Proposes a weight initialization scaled for ReLU networks, and the parametric ReLU, so very deep rectifier networks train from scratch.',
				arxivId: '1502.01852',
				implementations: [
					{
						slug: 'research-he-init-std',
						title: 'The standard deviation rule',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-he-init-sample',
						title: 'Sampling a weight matrix',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-prelu-forward',
						title: 'Learning the negative slope',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'batch-normalization',
				title:
					'Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift',
				authors: 'Sergey Ioffe, Christian Szegedy',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Normalizes each feature across a mini-batch and learns a scale and shift, which stabilizes training and allows much higher learning rates.',
				arxivId: '1502.03167',
				implementations: [
					{
						slug: 'research-batchnorm-train',
						title: 'The training-time forward pass',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-batchnorm-inference',
						title: 'Inference with running statistics',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-batchnorm-running-stats',
						title: 'Updating running statistics',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'layer-normalization',
				title: 'Layer Normalization',
				authors: 'Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton',
				year: 2016,
				kind: 'foundational',
				summary:
					'Normalizes across the features of each example instead of across the batch, so it works with small batches and in sequence models.',
				arxivId: '1607.06450',
				implementations: [
					{
						slug: 'research-layernorm-normalize',
						title: 'Normalizing across features',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-layernorm-affine',
						title: 'The learned scale and shift',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-layernorm-per-example-stats',
						title: 'Per-example statistics',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'highway-networks',
				title: 'Training Very Deep Networks',
				authors: 'Rupesh Kumar Srivastava, Klaus Greff, Jürgen Schmidhuber',
				year: 2015,
				kind: 'foundational',
				summary:
					'Highway networks use learned gates to decide how much of each layer to transform and how much to carry through, making very deep networks trainable.',
				arxivId: '1505.00387',
				implementations: [
					{
						slug: 'research-highway-gate',
						title: 'The transform gate',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-highway-combine',
						title: 'Mixing transform and carry',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-highway-layer',
						title: 'A full highway layer',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'gelu',
				title: 'Gaussian Error Linear Units (GELUs)',
				authors: 'Dan Hendrycks, Kevin Gimpel',
				year: 2016,
				kind: 'breakthrough',
				summary:
					'GELU gates each input by its Gaussian cumulative probability, a smooth version of ReLU that became the default in transformer models.',
				arxivId: '1606.08415',
				implementations: [
					{
						slug: 'research-gelu-exact',
						title: 'The exact Gaussian-gated activation',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-gelu-tanh',
						title: 'The tanh approximation',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-gelu-derivative', title: 'The derivative', difficulty: 'Advanced' }
				]
			},
			{
				slug: 'swish',
				title: 'Searching for Activation Functions',
				authors: 'Prajit Ramachandran, Barret Zoph, Quoc V. Le',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'An automated search found x * sigmoid(beta * x), called Swish, which often beats ReLU on deep networks.',
				arxivId: '1710.05941',
				implementations: [
					{
						slug: 'research-swish-forward',
						title: 'A self-gated activation',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-swish-derivative',
						title: 'The derivative with beta',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-swish-vs-relu-gap',
						title: 'How close is it to ReLU?',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'weight-normalization',
				title:
					'Weight Normalization: A Simple Reparameterization to Accelerate Training of Deep Neural Networks',
				authors: 'Tim Salimans, Diederik P. Kingma',
				year: 2016,
				kind: 'foundational',
				summary:
					'Separates each weight vector into a length and a direction, so the two can be optimized independently.',
				arxivId: '1602.07868',
				implementations: [
					{
						slug: 'research-weight-norm',
						title: 'Reparameterizing the weights',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-weight-norm-row-norms', title: 'Row norms', difficulty: 'Beginner' },
					{
						slug: 'research-weight-norm-linear',
						title: 'A weight-normalized linear layer',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'network-in-network',
				title: 'Network In Network',
				authors: 'Min Lin, Qiang Chen, Shuicheng Yan',
				year: 2013,
				kind: 'foundational',
				summary:
					'Replaces linear filters with small networks applied at each position, using 1x1 convolutions and global average pooling.',
				arxivId: '1312.4400',
				implementations: [
					{
						slug: 'research-nin-conv1x1',
						title: 'The 1x1 convolution',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-nin-conv2d-valid',
						title: 'A valid 2D convolution',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-nin-global-average-pool',
						title: 'Global average pooling',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'maxout-networks',
				title: 'Maxout Networks',
				authors:
					'Ian J. Goodfellow, David Warde-Farley, Mehdi Mirza, Aaron Courville, Yoshua Bengio',
				year: 2013,
				kind: 'foundational',
				summary:
					'Each maxout unit outputs the maximum of several learned linear functions, a learnable activation that works well with dropout.',
				arxivId: '1302.4389',
				implementations: [
					{ slug: 'research-maxout-forward', title: 'The maxout unit', difficulty: 'Intermediate' },
					{
						slug: 'research-maxout-argmax',
						title: 'Which piece wins?',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-maxout-relu', title: 'ReLU is a maxout', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'mixup',
				title: 'mixup: Beyond Empirical Risk Minimization',
				authors: 'Hongyi Zhang, Moustapha Cisse, Yann N. Dauphin, David Lopez-Paz',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Trains on convex combinations of pairs of examples and their labels, smoothing decision boundaries between classes.',
				arxivId: '1710.09412',
				implementations: [
					{
						slug: 'research-mixup-inputs',
						title: 'Blending two training examples',
						difficulty: 'Beginner'
					},
					{ slug: 'research-mixup-targets', title: 'Blending the labels', difficulty: 'Beginner' },
					{ slug: 'research-mixup-loss', title: 'The mixed loss', difficulty: 'Intermediate' }
				]
			},
			{
				slug: 'identity-mappings-resnet',
				title: 'Identity Mappings in Deep Residual Networks',
				authors: 'Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun',
				year: 2016,
				kind: 'breakthrough',
				summary:
					'Analyzes residual blocks and shows that an identity shortcut keeps the gradient path clear, which is why very deep residual networks train.',
				arxivId: '1603.05027',
				implementations: [
					{
						slug: 'research-residual-forward',
						title: 'The residual block',
						difficulty: 'Beginner'
					},
					{ slug: 'research-residual-stack', title: 'Stacking blocks', difficulty: 'Intermediate' },
					{
						slug: 'research-residual-gradient',
						title: 'The gradient through the shortcut',
						difficulty: 'Advanced'
					}
				]
			}
		]
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
