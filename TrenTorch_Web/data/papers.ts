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
				title: 'Improving neural networks by preventing co-adaptation of feature detectors',
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
				title: 'Highway Networks',
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
			},
			{
				slug: 'adamw',
				title: 'Decoupled Weight Decay Regularization',
				authors: 'Ilya Loshchilov, Frank Hutter',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Shows that L2 regularization is not equivalent to weight decay under Adam, and decouples decay from the adaptive gradient step, which generalizes better.',
				arxivId: '1711.05101',
				implementations: [
					{
						slug: 'research-adamw-decoupled-update',
						title: 'The decoupled update',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-adamw-bias-correction',
						title: 'Bias correction',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-adamw-effective-decay',
						title: 'The effective decay per step',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'lars',
				title: 'Large Batch Training of Convolutional Networks',
				authors: 'Yang You, Igor Gitman, Boris Ginsburg',
				year: 2017,
				kind: 'foundational',
				summary:
					'Scales the learning rate of each layer by a trust ratio of its weight norm to its gradient norm, which keeps very large batches stable.',
				arxivId: '1708.03888',
				implementations: [
					{
						slug: 'research-lars-trust-ratio',
						title: 'The layer trust ratio',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-lars-update',
						title: 'The layer-wise update',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-lars-layer-norms', title: 'Per-layer norms', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'lamb',
				title: 'Large Batch Optimization for Deep Learning: Training BERT in 76 minutes',
				authors: 'Yang You, Jing Li, Sashank Reddi, et al.',
				year: 2019,
				kind: 'breakthrough',
				summary:
					'Combines Adam-style moment estimates with the LARS layer trust ratio, enabling very large batch training of BERT.',
				arxivId: '1904.00962',
				implementations: [
					{
						slug: 'research-lamb-trust-ratio',
						title: 'The LAMB trust ratio',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-lamb-update',
						title: 'The layer-wise update',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-lamb-adam-direction',
						title: 'The Adam direction',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'lookahead',
				title: 'Lookahead Optimizer: k steps forward, 1 step back',
				authors: 'Michael R. Zhang, James Lucas, Geoffrey Hinton, Jimmy Ba',
				year: 2019,
				kind: 'foundational',
				summary:
					'Wraps any inner optimizer with slow weights that take a step toward the fast weights every k steps, smoothing the optimization path.',
				arxivId: '1907.08610',
				implementations: [
					{
						slug: 'research-lookahead-slow-sync',
						title: 'The slow weight sync',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-lookahead-sync-steps',
						title: 'When syncs happen',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-lookahead-trajectory',
						title: 'The slow trajectory',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'adafactor',
				title: 'Adafactor: Adaptive Learning Rates with Sublinear Memory Cost',
				authors: 'Noam Shazeer, Mitchell Stern',
				year: 2018,
				kind: 'breakthrough',
				summary:
					'Factors the second-moment statistics into row and column vectors, cutting optimizer memory from linear in the parameter count to roughly its square root.',
				arxivId: '1804.04235',
				implementations: [
					{
						slug: 'research-adafactor-factored-moment',
						title: 'The factored second moment',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-adafactor-factored-memory',
						title: 'Memory saved by factoring',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-adafactor-relative-step',
						title: 'The relative step size',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'shampoo',
				title: 'Shampoo: Preconditioned Stochastic Tensor Optimization',
				authors: 'Vineet Gupta, Tomer Koren, Yoram Singer',
				year: 2018,
				kind: 'foundational',
				summary:
					'Preconditions each matrix gradient on both sides with running gram matrices, approximating full-matrix adaptive methods at modest cost.',
				arxivId: '1802.09568',
				implementations: [
					{
						slug: 'research-shampoo-accumulate',
						title: 'Accumulating preconditioners',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-shampoo-diagonal-precondition',
						title: 'Diagonal preconditioning',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-shampoo-inverse-root',
						title: 'The inverse root',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'sophia',
				title:
					'Sophia: A Scalable Stochastic Second-order Optimizer for Language Model Pre-training',
				authors: 'Hong Liu, Zhiyuan Li, David Hall, Percy Liang, Tengyu Ma',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Uses a cheap diagonal Hessian estimate to scale momentum, and clips each coordinate step, which speeds up language model pretraining.',
				arxivId: '2305.14342',
				implementations: [
					{
						slug: 'research-sophia-clipped-step',
						title: 'The clipped step',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-sophia-hutchinson',
						title: 'The Hutchinson diagonal estimate',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-sophia-clip-fraction',
						title: 'How often steps are clipped',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'large-minibatch-sgd',
				title: 'Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour',
				authors: 'Priya Goyal, Piotr Dollar, Ross Girshick, et al.',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Trains ImageNet with minibatch 8192 by scaling the learning rate linearly with batch size and warming it up gradually.',
				arxivId: '1706.02677',
				implementations: [
					{
						slug: 'research-goyal-scaled-lr',
						title: 'The linear scaling rule',
						difficulty: 'Beginner'
					},
					{ slug: 'research-goyal-warmup', title: 'Gradual warmup', difficulty: 'Beginner' },
					{
						slug: 'research-goyal-worker-count',
						title: 'Workers per batch',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'cyclical-learning-rates',
				title: 'Cyclical Learning Rates for Training Neural Networks',
				authors: 'Leslie N. Smith',
				year: 2015,
				kind: 'foundational',
				summary:
					'Cycles the learning rate between bounds on a triangular schedule and proposes a short LR range test to find those bounds.',
				arxivId: '1506.01186',
				implementations: [
					{
						slug: 'research-clr-triangular-lr',
						title: 'The triangular schedule',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-clr-cycle-index', title: 'The cycle index', difficulty: 'Beginner' },
					{ slug: 'research-clr-range-test', title: 'The LR range test', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'sgdr',
				title: 'SGDR: Stochastic Gradient Descent with Warm Restarts',
				authors: 'Ilya Loshchilov, Frank Hutter',
				year: 2016,
				kind: 'foundational',
				summary:
					'Anneals the learning rate with a cosine within each cycle and restarts it periodically, with cycle lengths that grow over training.',
				arxivId: '1608.03983',
				implementations: [
					{
						slug: 'research-sgdr-cosine-lr',
						title: 'The cosine learning rate',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-sgdr-cycle-position',
						title: 'Finding the cycle position',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-sgdr-cycles-total',
						title: 'Total steps across cycles',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'gradient-clipping',
				title: 'On the difficulty of training recurrent neural networks',
				authors: 'Razvan Pascanu, Tomas Mikolov, Yoshua Bengio',
				year: 2013,
				kind: 'foundational',
				summary:
					'Explains exploding and vanishing gradients in recurrent networks and proposes clipping the gradient norm to a threshold as a remedy.',
				arxivId: '1211.5063',
				implementations: [
					{ slug: 'research-clip-by-norm', title: 'Clipping by norm', difficulty: 'Beginner' },
					{ slug: 'research-clip-scale', title: 'The clip scale', difficulty: 'Beginner' },
					{
						slug: 'research-clip-exploding-steps',
						title: 'Counting exploding steps',
						difficulty: 'Beginner'
					}
				]
			}
		]
	},
	{
		slug: 'classical-ml-and-learning-theory',
		title: 'Classical ML and Learning Theory',
		description: 'Ensembles, margins and the theory behind generalization.',
		papers: [
			{
				slug: 'xgboost',
				title: 'XGBoost: A Scalable Tree Boosting System',
				authors: 'Tianqi Chen, Carlos Guestrin',
				year: 2016,
				kind: 'breakthrough',
				summary:
					'A gradient boosting system that uses second-order gradients and regularized leaf weights, and became the default for tabular machine learning.',
				arxivId: '1603.02754',
				implementations: [
					{
						slug: 'research-xgboost-leaf-weight',
						title: 'The optimal leaf weight',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-xgboost-split-gain',
						title: 'The split gain',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-xgboost-logistic-grads',
						title: 'Gradients and hessians for logistic loss',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'catboost',
				title: 'CatBoost: unbiased boosting with categorical features',
				authors:
					'Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush, Andrey Gulin',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Encodes categorical features using only earlier samples, avoiding target leakage, and builds symmetric oblivious trees.',
				arxivId: '1706.09516',
				implementations: [
					{
						slug: 'research-catboost-ordered-encoding',
						title: 'Ordered target encoding',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-catboost-target-statistic',
						title: 'The target statistic formula',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-catboost-oblivious-leaf',
						title: 'Oblivious tree leaf index',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'deep-forest',
				title: 'Deep Forest',
				authors: 'Zhi-Hua Zhou, Ji Feng',
				year: 2017,
				kind: 'foundational',
				summary:
					'A cascade of random forests, where each layer passes class vectors to the next, as an alternative to deep neural networks.',
				arxivId: '1702.08835',
				implementations: [
					{
						slug: 'research-deep-forest-class-distribution',
						title: 'The class vector',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-deep-forest-cascade-augment',
						title: 'Augmenting features with class vectors',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-deep-forest-cascade-predict',
						title: 'Predicting from averaged forests',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'distillation',
				title: 'Distilling the Knowledge in a Neural Network',
				authors: 'Geoffrey Hinton, Oriol Vinyals, Jeff Dean',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'A small student network learns to match the softened outputs of a large teacher, transferring what the teacher knows beyond the hard labels.',
				arxivId: '1503.02531',
				implementations: [
					{
						slug: 'research-distill-softmax-temperature',
						title: 'Softmax with temperature',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-distill-soft-target-ce',
						title: 'The soft-target loss',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-distill-combined-loss',
						title: 'The combined loss',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'rethinking-generalization',
				title: 'Understanding deep learning requires rethinking generalization',
				authors: 'Chiyuan Zhang, Samy Bengio, Moritz Hardt, Benjamin Recht, Oriol Vinyals',
				year: 2016,
				kind: 'foundational',
				summary:
					'Shows that large networks can fit random labels perfectly, so standard complexity measures cannot explain why they generalize on real data.',
				arxivId: '1611.03530',
				implementations: [
					{
						slug: 'research-generalization-shuffle-labels',
						title: 'Shuffling the labels',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-generalization-gap',
						title: 'The generalization gap',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-generalization-error-rate',
						title: 'The error rate',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'neural-tangent-kernel',
				title: 'Neural Tangent Kernel: Convergence and Generalization in Neural Networks',
				authors: 'Arthur Jacot, Franck Gabriel, Clement Hongler',
				year: 2018,
				kind: 'breakthrough',
				summary:
					'Shows that infinitely wide networks trained by gradient descent behave like kernel regression with a fixed kernel, giving a theory of their training dynamics.',
				arxivId: '1806.07572',
				implementations: [
					{
						slug: 'research-ntk-linear-kernel',
						title: 'The linear kernel matrix',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ntk-kernel-ridge',
						title: 'Kernel ridge prediction',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-ntk-arc-cosine',
						title: 'The ReLU arc-cosine kernel',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'deep-double-descent',
				title: 'Deep Double Descent: Where Bigger Models and More Data Hurt',
				authors:
					'Preetum Nakkiran, Gal Kaplun, Yamini Bansal, Tristan Yang, Boaz Barak, Ilya Sutskever',
				year: 2019,
				kind: 'breakthrough',
				summary:
					'Shows test error can peak near the interpolation threshold and then fall again as models grow, so bigger models can generalize better.',
				arxivId: '1912.02292',
				implementations: [
					{
						slug: 'research-double-descent-min-norm',
						title: 'The minimum-norm interpolator',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-double-descent-ridge',
						title: 'The ridge solution',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-double-descent-regime',
						title: 'Which regime is it in?',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'lottery-ticket',
				title: 'The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks',
				authors: 'Jonathan Frankle, Michael Carbin',
				year: 2018,
				kind: 'breakthrough',
				summary:
					'Finds sparse subnetworks that train to full accuracy when reset to their original initialization, suggesting that large networks contain small trainable winners.',
				arxivId: '1803.03635',
				implementations: [
					{
						slug: 'research-lottery-magnitude-mask',
						title: 'The magnitude pruning mask',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-lottery-apply-mask',
						title: 'Applying the mask',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-lottery-remaining-fraction',
						title: 'Iterative pruning',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'scikit-learn',
				title: 'Scikit-learn: Machine Learning in Python',
				authors: 'Fabian Pedregosa, Gael Varoquaux, Alexandre Gramfort, et al.',
				year: 2011,
				kind: 'foundational',
				summary:
					'Describes the scikit-learn library: a consistent API for estimators, cross-validation and preprocessing that much of applied machine learning is built on.',
				arxivId: '1201.0490',
				implementations: [
					{
						slug: 'research-sklearn-kfold',
						title: 'K-fold cross-validation splits',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-sklearn-cv-mean',
						title: 'Averaging cross-validation scores',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-sklearn-standard-scale',
						title: 'Standardizing features',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'shap',
				title: 'A Unified Approach to Interpreting Model Predictions',
				authors: 'Scott M. Lundberg, Su-In Lee',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Unifies several explanation methods under Shapley values, which split a prediction fairly among input features.',
				arxivId: '1705.07874',
				implementations: [
					{
						slug: 'research-shap-exact-shapley',
						title: 'Exact Shapley values',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-shap-additivity',
						title: 'Checking additivity',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-shap-linear',
						title: 'Linear model attributions',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'smote',
				title: 'SMOTE: Synthetic Minority Over-sampling Technique',
				authors: 'Nitesh V. Chawla, Kevin W. Bowyer, Lawrence O. Hall, W. Philip Kegelmeyer',
				year: 2002,
				kind: 'foundational',
				summary:
					'Balances imbalanced datasets by creating new minority-class samples between existing ones and their nearest neighbors.',
				arxivId: '1106.1813',
				implementations: [
					{
						slug: 'research-smote-point',
						title: 'Interpolating between two points',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-smote-nearest',
						title: 'Finding nearest neighbors',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-smote-oversample',
						title: 'Oversampling a minority class',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'bayesian-optimization',
				title: 'A Tutorial on Bayesian Optimization',
				authors: 'Peter I. Frazier',
				year: 2018,
				kind: 'foundational',
				summary:
					'A tutorial on tuning expensive functions by fitting a probabilistic surrogate and choosing points with acquisition functions such as expected improvement.',
				arxivId: '1807.02811',
				implementations: [
					{
						slug: 'research-ei-expected-improvement',
						title: 'Expected improvement',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-bo-lower-confidence-bound',
						title: 'Lower confidence bound',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-bo-probability-improvement',
						title: 'Probability of improvement',
						difficulty: 'Advanced'
					}
				]
			}
		]
	},
	{
		slug: 'unsupervised-and-representation-learning',
		title: 'Unsupervised and Representation Learning',
		description: 'Autoencoders, word embeddings and contrastive learning.',
		papers: [
			{
				slug: 'vae',
				title: 'Auto-Encoding Variational Bayes',
				authors: 'Diederik P. Kingma, Max Welling',
				year: 2013,
				kind: 'breakthrough',
				summary:
					'Trains a latent-variable model with a learned encoder by optimizing a lower bound on the likelihood, using a reparameterized sample.',
				arxivId: '1312.6114',
				implementations: [
					{
						slug: 'research-vae-reparameterize',
						title: 'The reparameterization trick',
						difficulty: 'Beginner'
					},
					{ slug: 'research-vae-kl', title: 'The KL to the prior', difficulty: 'Intermediate' },
					{
						slug: 'research-vae-elbo',
						title: 'The evidence lower bound',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'word2vec',
				title: 'Efficient Estimation of Word Representations in Vector Space',
				authors: 'Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean',
				year: 2013,
				kind: 'breakthrough',
				summary:
					'Introduces CBOW and skip-gram, two simple architectures that learn word vectors from very large corpora.',
				arxivId: '1301.3781',
				implementations: [
					{
						slug: 'research-w2v-skipgram-pairs',
						title: 'Building skip-gram pairs',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-w2v-cbow-mean',
						title: 'The CBOW context average',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-w2v-skipgram-prob',
						title: 'The skip-gram softmax',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'negative-sampling',
				title: 'Distributed Representations of Words and Phrases and their Compositionality',
				authors: 'Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean',
				year: 2013,
				kind: 'foundational',
				summary:
					'Adds negative sampling, subsampling of frequent words and phrase vectors to word2vec, making training much faster and the vectors better.',
				arxivId: '1310.4546',
				implementations: [
					{
						slug: 'research-ns-loss',
						title: 'The per-pair negative sampling loss',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-ns-subsample',
						title: 'Subsampling frequent words',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ns-unigram-noise',
						title: 'The noise distribution',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'gan',
				title: 'Generative Adversarial Networks',
				authors: 'Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, et al.',
				year: 2014,
				kind: 'breakthrough',
				summary:
					'Trains a generator and a discriminator against each other, so the generator learns to produce samples the discriminator cannot tell from real data.',
				arxivId: '1406.2661',
				implementations: [
					{
						slug: 'research-gan-discriminator-loss',
						title: 'The discriminator loss',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-gan-generator-loss',
						title: 'The non-saturating generator loss',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-gan-optimal-discriminator',
						title: 'The optimal discriminator',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'adversarial-autoencoders',
				title: 'Adversarial Autoencoders',
				authors: 'Alireza Makhzani, Jonathon Shlens, Navdeep Jaitly, Ian Goodfellow, Brendan Frey',
				year: 2015,
				kind: 'foundational',
				summary:
					'Uses a discriminator to match the distribution of an autoencoder code to a chosen prior, turning the autoencoder into a generative model.',
				arxivId: '1511.05644',
				implementations: [
					{
						slug: 'research-aae-recon-mse',
						title: 'The reconstruction loss',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-aae-prior-sample',
						title: 'Sampling the prior',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-aae-encoder-loss',
						title: 'The encoder fooling loss',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'simclr',
				title: 'A Simple Framework for Contrastive Learning of Visual Representations',
				authors: 'Ting Chen, Simon Kornblith, Mohammad Norouzi, Geoffrey Hinton',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Shows that strong augmentations, a projection head and a large batch with the NT-Xent loss give representations competitive with supervised learning.',
				arxivId: '2002.05709',
				implementations: [
					{ slug: 'research-simclr-cosine', title: 'Cosine similarity', difficulty: 'Beginner' },
					{
						slug: 'research-simclr-nt-xent',
						title: 'The NT-Xent loss for one anchor',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-simclr-l2-normalize',
						title: 'L2 normalization of projections',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'moco',
				title: 'Momentum Contrast for Unsupervised Visual Representation Learning',
				authors: 'Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, Ross Girshick',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Keeps a large queue of negative keys produced by a momentum-updated encoder, which allows many negatives without a huge batch.',
				arxivId: '1911.05722',
				implementations: [
					{
						slug: 'research-moco-momentum-update',
						title: 'The momentum encoder update',
						difficulty: 'Beginner'
					},
					{ slug: 'research-moco-info-nce', title: 'InfoNCE with a queue', difficulty: 'Advanced' },
					{ slug: 'research-moco-enqueue', title: 'The key queue', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'byol',
				title: 'Bootstrap your own latent: A new approach to self-supervised Learning',
				authors: 'Jean-Bastien Grill, Florian Strub, Florent Altche, et al.',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Learns representations without negative pairs by predicting a slowly moving target network, avoiding collapse through the asymmetry of the predictor.',
				arxivId: '2006.07733',
				implementations: [
					{
						slug: 'research-byol-loss',
						title: 'The normalized regression loss',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-byol-ema-update',
						title: 'The target network update',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-byol-symmetric-loss',
						title: 'The symmetrized loss',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'cpc',
				title: 'Representation Learning with Contrastive Predictive Coding',
				authors: 'Aaron van den Oord, Yazhe Li, Oriol Vinyals',
				year: 2018,
				kind: 'foundational',
				summary:
					'Predicts future latent codes from the present context with a contrastive loss, which lower-bounds the mutual information between them.',
				arxivId: '1807.03748',
				implementations: [
					{ slug: 'research-cpc-loss', title: 'The contrastive loss', difficulty: 'Intermediate' },
					{
						slug: 'research-cpc-bilinear-score',
						title: 'The bilinear compatibility score',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-cpc-mi-bound',
						title: 'The mutual information bound',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'vq-vae',
				title: 'Neural Discrete Representation Learning',
				authors: 'Aaron van den Oord, Oriol Vinyals, Koray Kavukcuoglu',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Quantizes encoder outputs to a learned discrete codebook, giving a VAE-style model with discrete latents that models images and speech well.',
				arxivId: '1711.00937',
				implementations: [
					{
						slug: 'research-vq-nearest-code',
						title: 'Choosing the nearest code',
						difficulty: 'Beginner'
					},
					{ slug: 'research-vq-quantize', title: 'Looking up the code', difficulty: 'Beginner' },
					{
						slug: 'research-vq-loss',
						title: 'The vector-quantization loss',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'deep-infomax',
				title: 'Learning deep representations by mutual information estimation and maximization',
				authors: 'R Devon Hjelm, Alex Fedorov, Samuel Lavoie-Marchildon, et al.',
				year: 2019,
				kind: 'foundational',
				summary:
					'Maximizes mutual information between local features and global summaries of an input, using a discriminator and a Jensen-Shannon estimate.',
				arxivId: '1808.06670',
				implementations: [
					{
						slug: 'research-dim-jsd-estimate',
						title: 'The Jensen-Shannon MI estimate',
						difficulty: 'Advanced'
					},
					{ slug: 'research-dim-softplus', title: 'The softplus function', difficulty: 'Beginner' },
					{
						slug: 'research-dim-discriminator-score',
						title: 'The bilinear discriminator',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'glow',
				title: 'Glow: Generative Flow with Invertible 1x1 Convolutions',
				authors: 'Diederik P. Kingma, Prafulla Dhariwal',
				year: 2018,
				kind: 'foundational',
				summary:
					'A normalizing flow built from actnorm, invertible 1x1 convolutions and affine coupling layers, giving exact likelihoods and invertible generation.',
				arxivId: '1807.03039',
				implementations: [
					{
						slug: 'research-glow-actnorm',
						title: 'Activation normalization',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-glow-logdet-1x1',
						title: 'The log-determinant of a 1x1 convolution',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-glow-affine-coupling',
						title: 'The affine coupling layer',
						difficulty: 'Advanced'
					}
				]
			}
		]
	},
	{
		slug: 'sequence-models-and-attention',
		title: 'Sequence Models and Attention',
		description: 'Recurrent models, sequence-to-sequence learning and the birth of attention.',
		papers: [
			{
				slug: 'rnn-regularization',
				title: 'Recurrent Neural Network Regularization',
				authors: 'Wojciech Zaremba, Ilya Sutskever, Oriol Vinyals',
				year: 2014,
				kind: 'foundational',
				summary:
					'Shows that dropout must skip the recurrent connections, applying it only between layers and to the output, which makes LSTM language models generalize.',
				arxivId: '1409.2329',
				implementations: [
					{
						slug: 'research-zaremba-perplexity',
						title: 'Perplexity from the loss',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-zaremba-nonrecurrent-dropout',
						title: 'Dropout on non-recurrent connections',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-zaremba-bptt-chunks',
						title: 'Truncated backpropagation chunks',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'pointer-networks',
				title: 'Pointer Networks',
				authors: 'Oriol Vinyals, Meire Fortunato, Navdeep Jaitly',
				year: 2015,
				kind: 'foundational',
				summary:
					'Outputs positions in the input rather than words from a fixed vocabulary, using attention as a pointer, so the output set changes with each input.',
				arxivId: '1506.03134',
				implementations: [
					{
						slug: 'research-ptr-pointer-distribution',
						title: 'The pointer distribution',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-ptr-select-input',
						title: 'Selecting the pointed input',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ptr-pointer-sequence',
						title: 'A sequence of pointers',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'luong-attention',
				title: 'Effective Approaches to Attention-based Neural Machine Translation',
				authors: 'Minh-Thang Luong, Hieu Pham, Christopher D. Manning',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Compares dot, general and concat alignment scores, and introduces local attention that looks only at a window of source positions.',
				arxivId: '1508.04025',
				implementations: [
					{ slug: 'research-luong-dot-score', title: 'The dot score', difficulty: 'Beginner' },
					{
						slug: 'research-luong-general-score',
						title: 'The general score',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-luong-local-window', title: 'The local window', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'show-attend-tell',
				title: 'Show, Attend and Tell: Neural Image Caption Generation with Visual Attention',
				authors: 'Kelvin Xu, Jimmy Ba, Ryan Kiros, et al.',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Generates image captions with soft and hard attention over convolutional feature maps, with a regularizer that spreads attention across the image.',
				arxivId: '1502.03044',
				implementations: [
					{
						slug: 'research-sat-soft-context',
						title: 'The soft attention context',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-sat-doubly-stochastic',
						title: 'The doubly stochastic penalty',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-sat-hard-sample',
						title: 'Sampling hard attention',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'neural-turing-machines',
				title: 'Neural Turing Machines',
				authors: 'Alex Graves, Greg Wayne, Ivo Danihelka',
				year: 2014,
				kind: 'breakthrough',
				summary:
					'Couples a neural controller to an external memory it reads and writes with differentiable content and location addressing.',
				arxivId: '1410.5401',
				implementations: [
					{
						slug: 'research-ntm-content-weights',
						title: 'Content addressing',
						difficulty: 'Advanced'
					},
					{ slug: 'research-ntm-read', title: 'Reading the memory', difficulty: 'Beginner' },
					{ slug: 'research-ntm-write', title: 'Erase and add write', difficulty: 'Intermediate' }
				]
			},
			{
				slug: 'memory-networks',
				title: 'Memory Networks',
				authors: 'Jason Weston, Sumit Chopra, Antoine Bordes',
				year: 2014,
				kind: 'foundational',
				summary:
					'Stores facts as memory embeddings, matches a question against them, and reasons over several hops to answer.',
				arxivId: '1410.3916',
				implementations: [
					{
						slug: 'research-memnet-match',
						title: 'Matching the question to memory',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-memnet-read',
						title: 'Reading the output memory',
						difficulty: 'Beginner'
					},
					{ slug: 'research-memnet-hop', title: 'The multi-hop update', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'wavenet',
				title: 'WaveNet: A Generative Model for Raw Audio',
				authors: 'Aaron van den Oord, Sander Dieleman, Heiga Zen, et al.',
				year: 2016,
				kind: 'breakthrough',
				summary:
					'Models raw audio sample by sample with stacked dilated causal convolutions, whose exponentially growing receptive field covers long context.',
				arxivId: '1609.03499',
				implementations: [
					{
						slug: 'research-wavenet-receptive-field',
						title: 'The dilated receptive field',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-wavenet-mu-law-encode',
						title: 'Mu-law companding',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-wavenet-mu-law-decode',
						title: 'Mu-law expansion',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'temporal-convolutional-networks',
				title:
					'An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling',
				authors: 'Shaojie Bai, J. Zico Kolter, Vladlen Koltun',
				year: 2018,
				kind: 'foundational',
				summary:
					'Shows that a simple temporal convolutional network with causal, dilated convolutions and residual blocks matches or beats recurrent networks on many sequence tasks.',
				arxivId: '1803.01271',
				implementations: [
					{
						slug: 'research-tcn-receptive-field',
						title: 'The TCN receptive field',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-tcn-causal-padding', title: 'Causal padding', difficulty: 'Beginner' },
					{
						slug: 'research-tcn-causal-conv1d',
						title: 'A causal 1D convolution',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'listen-attend-spell',
				title: 'Listen, Attend and Spell',
				authors: 'William Chan, Navdeep Jaitly, Quoc V. Le, Oriol Vinyals',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'An end-to-end speech recognizer with a pyramidal listener that shortens the input, and an attention speller that outputs characters with beam search.',
				arxivId: '1508.01211',
				implementations: [
					{
						slug: 'research-las-pyramid-length',
						title: 'The pyramidal length',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-las-sequence-nll',
						title: 'Character negative log-likelihood',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-las-top-k-beams',
						title: 'Beam search pruning',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'adaptive-computation-time',
				title: 'Adaptive Computation Time for Recurrent Neural Networks',
				authors: 'Alex Graves',
				year: 2016,
				kind: 'foundational',
				summary:
					'Lets a recurrent network learn how many computation steps to spend on each input, using a differentiable halting probability and a ponder cost.',
				arxivId: '1603.08983',
				implementations: [
					{ slug: 'research-act-remainder', title: 'The remainder', difficulty: 'Intermediate' },
					{ slug: 'research-act-ponder-cost', title: 'The ponder cost', difficulty: 'Beginner' },
					{ slug: 'research-act-output', title: 'The weighted output', difficulty: 'Advanced' }
				]
			},
			{
				slug: 'mamba',
				title: 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces',
				authors: 'Albert Gu, Tri Dao',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Makes state space model parameters depend on the input, so the model can select what to keep, while a hardware-aware scan keeps training linear in length.',
				arxivId: '2312.00752',
				implementations: [
					{
						slug: 'research-mamba-zoh-discretize',
						title: 'Zero-order-hold discretization',
						difficulty: 'Advanced'
					},
					{ slug: 'research-mamba-ssm-scan', title: 'The recurrent scan', difficulty: 'Advanced' },
					{
						slug: 'research-mamba-selective-step',
						title: 'The selective step size',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 's4',
				title: 'Efficiently Modeling Long Sequences with Structured State Spaces',
				authors: 'Albert Gu, Karan Goel, Christopher Re',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Parameterizes a state space model so it runs as a convolution for training and a recurrence for generation, making very long sequences tractable.',
				arxivId: '2111.00396',
				implementations: [
					{
						slug: 'research-s4-ssm-kernel',
						title: 'The SSM convolution kernel',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-s4-causal-conv',
						title: 'Causal convolution by the kernel',
						difficulty: 'Advanced'
					},
					{ slug: 'research-s4-recurrent-ssm', title: 'The recurrent form', difficulty: 'Advanced' }
				]
			}
		]
	},
	{
		slug: 'transformers-and-llms',
		title: 'Transformers and LLMs',
		description: 'The transformer, pretraining at scale and instruction following.',
		papers: [
			{
				slug: 'bahdanau-attention',
				title: 'Neural Machine Translation by Jointly Learning to Align and Translate',
				authors: 'Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio',
				year: 2014,
				kind: 'foundational',
				summary:
					'Lets the decoder look back at every encoder state at each step, using a learned alignment score. This is the first attention mechanism for translation.',
				arxivId: '1409.0473',
				implementations: [
					{
						slug: 'research-bahdanau-additive-scores',
						title: 'Additive alignment scores',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-bahdanau-attention-weights',
						title: 'Turning scores into weights',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-bahdanau-context-vector',
						title: 'The context vector',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'seq2seq',
				title: 'Sequence to Sequence Learning with Neural Networks',
				authors: 'Ilya Sutskever, Oriol Vinyals, Quoc V. Le',
				year: 2014,
				kind: 'foundational',
				summary:
					'An LSTM encoder reads the source sentence and an LSTM decoder writes the translation. Reversing the source made training much easier.',
				arxivId: '1409.3215',
				implementations: [
					{
						slug: 'research-seq2seq-reverse-source',
						title: 'Reversing the source sentence',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-seq2seq-teacher-forcing',
						title: 'Teacher-forced decoder inputs',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-seq2seq-sequence-nll',
						title: 'The sequence negative log-likelihood',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'gru',
				title:
					'Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation',
				authors:
					'Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Dzmitry Bahdanau, Fethi Bougares, Holger Schwenk, Yoshua Bengio',
				year: 2014,
				kind: 'foundational',
				summary:
					'Introduces the gated recurrent unit (GRU), a simpler gated recurrent cell with an update gate and a reset gate.',
				arxivId: '1406.1078',
				implementations: [
					{ slug: 'research-gru-update-gate', title: 'The update gate', difficulty: 'Beginner' },
					{
						slug: 'research-gru-candidate',
						title: 'The candidate state',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-gru-step', title: 'One full GRU step', difficulty: 'Advanced' }
				]
			},
			{
				slug: 'attention-is-all-you-need',
				title: 'Attention Is All You Need',
				authors:
					'Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Introduces the transformer, which replaces recurrence with multi-head self-attention and positional encodings.',
				arxivId: '1706.03762',
				implementations: [
					{
						slug: 'research-scaled-dot-attention',
						title: 'Scaled dot-product attention',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-multihead-split',
						title: 'Splitting into heads',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-sinusoidal-positional-encoding',
						title: 'Sinusoidal positions',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'bert',
				title: 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding',
				authors: 'Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova',
				year: 2018,
				kind: 'breakthrough',
				summary:
					'Pretrains a bidirectional transformer by predicting masked tokens, then fine-tunes it on many language understanding tasks.',
				arxivId: '1810.04805',
				implementations: [
					{
						slug: 'research-bert-masking-action',
						title: 'The 80/10/10 masking rule',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-bert-masked-lm-loss',
						title: 'The masked language model loss',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-bert-input-embedding',
						title: 'Summing token, segment and position embeddings',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'gpt-3',
				title: 'Language Models are Few-Shot Learners',
				authors: 'Tom B. Brown, Benjamin Mann, Nick Ryder, et al.',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Shows that a large autoregressive language model can perform new tasks from a few examples in the prompt, with no gradient updates.',
				arxivId: '2005.14165',
				implementations: [
					{
						slug: 'research-gpt3-few-shot-prompt',
						title: 'Building a few-shot prompt',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-causal-mask',
						title: 'The causal attention mask',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-gpt3-continuation-logprob',
						title: 'Scoring a continuation',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'scaling-laws',
				title: 'Scaling Laws for Neural Language Models',
				authors: 'Jared Kaplan, Sam McCandlish, Tom Henighan, et al.',
				year: 2020,
				kind: 'foundational',
				summary:
					'Shows that language model loss follows smooth power laws in model size, data and compute, which makes large training runs predictable.',
				arxivId: '2001.08361',
				implementations: [
					{
						slug: 'research-scaling-power-law-loss',
						title: 'The power-law loss',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-scaling-fit-exponent',
						title: 'Fitting the exponent',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-scaling-ratio',
						title: 'Predicting the gain from growth',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'chinchilla',
				title: 'Training Compute-Optimal Large Language Models',
				authors: 'Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, et al.',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Argues that many large models were undertrained: for a fixed compute budget, model size and token count should grow together, at about twenty tokens per parameter.',
				arxivId: '2203.15556',
				implementations: [
					{
						slug: 'research-chinchilla-flops',
						title: 'Estimating training FLOPs',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-chinchilla-optimal-tokens',
						title: 'The compute-optimal token count',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-chinchilla-optimal-params',
						title: 'Choosing model size for a budget',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'roformer',
				title: 'RoFormer: Enhanced Transformer with Rotary Position Embedding',
				authors: 'Jianlin Su, Yu Lu, Shengfeng Pan, Ahmed Murtadha, Bo Wen, Yunfeng Liu',
				year: 2021,
				kind: 'foundational',
				summary:
					'Encodes position by rotating query and key vectors, so attention scores depend on the relative distance between tokens.',
				arxivId: '2104.09864',
				implementations: [
					{
						slug: 'research-rope-frequencies',
						title: 'The rotary frequencies',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-rope-rotate',
						title: 'Rotating a vector by position',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-rope-relative-dot',
						title: 'The dot product depends only on relative position',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'instructgpt',
				title: 'Training language models to follow instructions with human feedback',
				authors: 'Long Ouyang, Jeff Wu, Xu Jiang, et al.',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Fine-tunes a language model with a reward model trained on human rankings, and a PPO policy update with a KL penalty to the original model.',
				arxivId: '2203.02155',
				implementations: [
					{
						slug: 'research-reward-pairwise-loss',
						title: 'The pairwise reward loss',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-kl-penalized-reward',
						title: 'The KL-penalized reward',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-ppo-clipped-surrogate',
						title: 'The PPO clipped objective',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'llama',
				title: 'LLaMA: Open and Efficient Foundation Language Models',
				authors: 'Hugo Touvron, Thibaut Lavril, Gautier Izacard, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'A family of openly released language models trained on public data, using RMSNorm, SwiGLU and rotary embeddings.',
				arxivId: '2302.13971',
				implementations: [
					{ slug: 'research-llama-rmsnorm', title: 'RMS normalization', difficulty: 'Beginner' },
					{
						slug: 'research-llama-swiglu',
						title: 'The SwiGLU feed-forward gate',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-llama-hidden-dim',
						title: 'Choosing the feed-forward width',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'switch-transformer',
				title:
					'Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity',
				authors: 'William Fedus, Barret Zoph, Noam Shazeer',
				year: 2021,
				kind: 'breakthrough',
				summary:
					'Routes each token to a single expert, so the parameter count grows with the number of experts while compute per token stays constant.',
				arxivId: '2101.03961',
				implementations: [
					{ slug: 'research-switch-routing', title: 'Top-1 routing', difficulty: 'Intermediate' },
					{
						slug: 'research-switch-load-balancing',
						title: 'The load-balancing loss',
						difficulty: 'Advanced'
					},
					{ slug: 'research-switch-capacity', title: 'Expert capacity', difficulty: 'Beginner' }
				]
			}
		]
	},
	{
		slug: 'computer-vision',
		title: 'Computer Vision',
		description: 'Residual networks, vision transformers and diffusion models for images.',
		papers: [
			{
				slug: 'resnet',
				title: 'Deep Residual Learning for Image Recognition',
				authors: 'Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Learns residual functions with identity shortcuts, which makes networks of 100 layers and more trainable and wins ImageNet 2015.',
				arxivId: '1512.03385',
				implementations: [
					{
						slug: 'research-resnet-conv-output-size',
						title: 'The convolution output size',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-resnet-projection-shortcut',
						title: 'When the shortcut needs a projection',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-resnet-depth-count',
						title: 'Counting layers in a basic-block network',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'googlenet',
				title: 'Going Deeper with Convolutions',
				authors: 'Christian Szegedy, Wei Liu, Yangqing Jia, et al.',
				year: 2014,
				kind: 'foundational',
				summary:
					'Introduces the inception module, parallel convolutions of several sizes with 1x1 reductions, and auxiliary classifiers for deep networks.',
				arxivId: '1409.4842',
				implementations: [
					{
						slug: 'research-googlenet-conv-params',
						title: 'Counting convolution parameters',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-googlenet-inception-channels',
						title: 'Output channels of an inception module',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-googlenet-aux-loss',
						title: 'The auxiliary classifier loss',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'vgg',
				title: 'Very Deep Convolutional Networks for Large-Scale Image Recognition',
				authors: 'Karen Simonyan, Andrew Zisserman',
				year: 2014,
				kind: 'foundational',
				summary:
					'Shows that stacks of small 3x3 convolutions in very deep networks outperform shallower designs with larger filters.',
				arxivId: '1409.1556',
				implementations: [
					{
						slug: 'research-vgg-receptive-field',
						title: 'Receptive field of stacked 3x3 convolutions',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-vgg-conv-macs',
						title: 'Multiply-accumulates of a convolution',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-vgg-stacked-params',
						title: 'Parameters of a stack of convolutions',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'zeiler-visualization',
				title: 'Visualizing and Understanding Convolutional Networks',
				authors: 'Matthew D. Zeiler, Rob Fergus',
				year: 2013,
				kind: 'foundational',
				summary:
					'Projects learned features back onto input pixels with a deconvolutional network, showing what each layer of a CNN responds to.',
				arxivId: '1311.2901',
				implementations: [
					{
						slug: 'research-zeiler-receptive-field',
						title: 'The receptive field',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-zeiler-max-switches',
						title: 'Max-pooling switches',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-zeiler-unpool',
						title: 'Unpooling with switches',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'vit',
				title: 'An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale',
				authors: 'Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, et al.',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Applies a standard transformer directly to sequences of image patches, matching CNNs when pre-trained on large datasets.',
				arxivId: '2010.11929',
				implementations: [
					{
						slug: 'research-vit-num-patches',
						title: 'Counting image patches',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-vit-patchify',
						title: 'Patchifying an image',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-vit-seq-length',
						title: 'The sequence length with a class token',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'clip',
				title: 'Learning Transferable Visual Models From Natural Language Supervision',
				authors: 'Alec Radford, Jong Wook Kim, Chris Hallacy, et al.',
				year: 2021,
				kind: 'breakthrough',
				summary:
					'Trains image and text encoders on 400 million web pairs with a contrastive loss, enabling zero-shot classification from class names.',
				arxivId: '2103.00020',
				implementations: [
					{
						slug: 'research-clip-logits',
						title: 'The similarity matrix',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-clip-symmetric-loss',
						title: 'The symmetric contrastive loss',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-clip-zero-shot',
						title: 'Zero-shot classification',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'ddpm',
				title: 'Denoising Diffusion Probabilistic Models',
				authors: 'Jonathan Ho, Ajay Jain, Pieter Abbeel',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Trains a network to predict the noise added to images at many levels, then generates images by reversing the noising process step by step.',
				arxivId: '2006.11239',
				implementations: [
					{
						slug: 'research-ddpm-forward-noise',
						title: 'Adding noise in one step',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-ddpm-linear-schedule',
						title: 'The linear noise schedule',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-ddpm-noise-loss',
						title: 'The noise prediction loss',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'latent-diffusion',
				title: 'High-Resolution Image Synthesis with Latent Diffusion Models',
				authors: 'Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Bjorn Ommer',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Runs diffusion in the compressed latent space of an autoencoder and adds text conditioning, making high-resolution generation practical.',
				arxivId: '2112.10752',
				implementations: [
					{
						slug: 'research-ldm-latent-shape',
						title: 'The latent grid size',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ldm-compression-ratio',
						title: 'The compression ratio',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-ldm-cfg-combine',
						title: 'Classifier-free guidance',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'faster-rcnn',
				title: 'Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks',
				authors: 'Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Shares convolutional features between a region proposal network and the detector, making two-stage detection fast enough for near real-time use.',
				arxivId: '1506.01497',
				implementations: [
					{ slug: 'research-frcnn-iou', title: 'Intersection over union', difficulty: 'Beginner' },
					{
						slug: 'research-frcnn-box-targets',
						title: 'Bounding box regression targets',
						difficulty: 'Advanced'
					},
					{ slug: 'research-frcnn-nms', title: 'Non-maximum suppression', difficulty: 'Advanced' }
				]
			},
			{
				slug: 'unet',
				title: 'U-Net: Convolutional Networks for Biomedical Image Segmentation',
				authors: 'Olaf Ronneberger, Philipp Fischer, Thomas Brox',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'An encoder-decoder network with skip connections that passes fine detail to the decoder, the standard architecture for image segmentation.',
				arxivId: '1505.04597',
				implementations: [
					{
						slug: 'research-unet-crop',
						title: 'Center-cropping skip connections',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-unet-upsample',
						title: 'Nearest-neighbour upsampling',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-unet-skip-concat',
						title: 'Concatenating skip connections',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'squeeze-excitation',
				title: 'Squeeze-and-Excitation Networks',
				authors: 'Jie Hu, Li Shen, Gang Sun',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Adds a lightweight block that summarizes each channel and learns per-channel gates, improving accuracy with little extra cost.',
				arxivId: '1709.01507',
				implementations: [
					{ slug: 'research-se-squeeze', title: 'The squeeze step', difficulty: 'Beginner' },
					{
						slug: 'research-se-excitation',
						title: 'The excitation gate',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-se-recalibrate',
						title: 'Recalibrating the features',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'yolo',
				title: 'You Only Look Once: Unified, Real-Time Object Detection',
				authors: 'Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi',
				year: 2016,
				kind: 'breakthrough',
				summary:
					'Frames detection as a single regression over a grid of cells, predicting boxes and class scores in one network pass for real-time speed.',
				arxivId: '1506.02640',
				implementations: [
					{
						slug: 'research-yolo-cell-index',
						title: 'Assigning an object to a grid cell',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-yolo-decode-xy',
						title: 'Decoding the box centre',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-yolo-confidence',
						title: 'The confidence score',
						difficulty: 'Beginner'
					}
				]
			}
		]
	},
	{
		slug: 'reinforcement-learning-and-alignment',
		title: 'Reinforcement Learning and Alignment',
		description: 'Policy gradients, PPO and preference-based fine-tuning.',
		papers: [
			{
				slug: 'dqn',
				title: 'Playing Atari with Deep Reinforcement Learning',
				authors: 'Volodymyr Mnih, Koray Kavukcuoglu, David Silver, et al.',
				year: 2013,
				kind: 'breakthrough',
				summary:
					'Learns control policies directly from pixels with a convolutional Q-network, using experience replay and a target network.',
				arxivId: '1312.5602',
				implementations: [
					{ slug: 'research-dqn-td-target', title: 'The Bellman target', difficulty: 'Beginner' },
					{
						slug: 'research-dqn-epsilon-schedule',
						title: 'Annealing exploration',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-dqn-clipped-td-error',
						title: 'Clipping the TD error',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'double-dqn',
				title: 'Deep Reinforcement Learning with Double Q-learning',
				authors: 'Hado van Hasselt, Arthur Guez, David Silver',
				year: 2015,
				kind: 'foundational',
				summary:
					'Decouples action selection from action evaluation in the Q-learning target, which removes much of the overestimation bias of DQN.',
				arxivId: '1509.06461',
				implementations: [
					{
						slug: 'research-double-dqn-target',
						title: 'The decoupled target',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-double-dqn-greedy-action',
						title: 'The greedy action',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-double-dqn-overestimation-gap',
						title: 'Measuring overestimation',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'dueling',
				title: 'Dueling Network Architectures for Deep Reinforcement Learning',
				authors: 'Ziyu Wang, Tom Schaul, Matteo Hessel, et al.',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Splits the Q-network into a state value and a per-action advantage, which learns faster when many actions do not matter much.',
				arxivId: '1511.06581',
				implementations: [
					{
						slug: 'research-dueling-q',
						title: 'Combining value and advantage',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-dueling-centered-advantage',
						title: 'Centering the advantages',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-dueling-q-argmax',
						title: 'The greedy action is unchanged',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'gae',
				title: 'High-Dimensional Continuous Control Using Generalized Advantage Estimation',
				authors: 'John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, Pieter Abbeel',
				year: 2015,
				kind: 'foundational',
				summary:
					'Estimates advantages as an exponentially weighted sum of TD residuals, trading bias against variance with a single parameter lambda.',
				arxivId: '1506.02438',
				implementations: [
					{
						slug: 'research-gae-td-residuals',
						title: 'One-step TD residuals',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-gae-advantages',
						title: 'Combining residuals with lambda',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-gae-discounted-returns',
						title: 'Discounted returns',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'trpo',
				title: 'Trust Region Policy Optimization',
				authors: 'John Schulman, Sergey Levine, Philipp Moritz, Michael Jordan, Pieter Abbeel',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Maximizes a surrogate objective subject to a KL-divergence trust region, which gives monotone improvement for policy gradient updates.',
				arxivId: '1502.05477',
				implementations: [
					{
						slug: 'research-trpo-surrogate',
						title: 'The surrogate objective',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-trpo-gaussian-kl',
						title: 'KL between Gaussians',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-trpo-step-size',
						title: 'The trust-region step size',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'ppo',
				title: 'Proximal Policy Optimization Algorithms',
				authors: 'John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Replaces the TRPO constraint with a clipped objective that is simple to implement and is the default policy-gradient method for language model fine-tuning.',
				arxivId: '1707.06347',
				implementations: [
					{
						slug: 'research-ppo-probability-ratio',
						title: 'The probability ratio',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ppo-objective-batch',
						title: 'The clipped objective over a batch',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-ppo-total-loss',
						title: 'The combined training loss',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'a3c',
				title: 'Asynchronous Methods for Deep Reinforcement Learning',
				authors: 'Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, et al.',
				year: 2016,
				kind: 'breakthrough',
				summary:
					'Trains an actor-critic with many asynchronous workers, using n-step returns and an entropy bonus, without a replay buffer.',
				arxivId: '1602.01783',
				implementations: [
					{
						slug: 'research-a3c-n-step-return',
						title: 'The n-step return',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-a3c-policy-gradient-loss',
						title: 'The policy gradient loss',
						difficulty: 'Beginner'
					},
					{ slug: 'research-a3c-entropy', title: 'Policy entropy', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'ddpg',
				title: 'Continuous control with deep reinforcement learning',
				authors: 'Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, et al.',
				year: 2015,
				kind: 'breakthrough',
				summary:
					'Extends deterministic policy gradients with deep networks, target networks and temporally correlated exploration noise for continuous actions.',
				arxivId: '1509.02971',
				implementations: [
					{
						slug: 'research-ddpg-soft-update',
						title: 'Soft target updates',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ddpg-critic-target',
						title: 'The critic target',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ddpg-ou-step',
						title: 'The Ornstein-Uhlenbeck exploration step',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'alphazero',
				title:
					'Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm',
				authors: 'David Silver, Thomas Hubert, Julian Schrittwieser, et al.',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Combines a neural network with Monte Carlo tree search, trained purely by self-play, and learns chess, shogi and Go from the rules alone.',
				arxivId: '1712.01815',
				implementations: [
					{ slug: 'research-alphazero-puct', title: 'The PUCT score', difficulty: 'Advanced' },
					{
						slug: 'research-alphazero-visit-distribution',
						title: 'The visit distribution',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-alphazero-dirichlet-mix',
						title: 'Mixing in Dirichlet noise',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'preferences',
				title: 'Deep reinforcement learning from human preferences',
				authors: 'Paul F. Christiano, Jan Leike, Tom B. Brown, et al.',
				year: 2017,
				kind: 'breakthrough',
				summary:
					'Learns a reward function from pairwise human comparisons of short behaviour clips, then trains an agent on the learned reward.',
				arxivId: '1706.03741',
				implementations: [
					{
						slug: 'research-preference-probability',
						title: 'The preference probability',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-preference-segment-return',
						title: 'Segment returns',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-preference-reward-nll',
						title: 'The reward model loss',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'summarize',
				title: 'Learning to summarize from human feedback',
				authors: 'Nisan Stiennon, Long Ouyang, Jeff Wu, et al.',
				year: 2020,
				kind: 'breakthrough',
				summary:
					'Fine-tunes a summarizer with a reward model trained on human comparisons and a KL penalty to a supervised reference model.',
				arxivId: '2009.01325',
				implementations: [
					{
						slug: 'research-summarize-per-token-kl',
						title: 'The sequence KL estimate',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-summarize-best-of-n',
						title: 'Best-of-N selection',
						difficulty: 'Beginner'
					},
					{ slug: 'research-summarize-win-rate', title: 'The win rate', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'dpo',
				title: 'Direct Preference Optimization: Your Language Model is Secretly a Reward Model',
				authors: 'Rafael Rafailov, Archit Sharma, Eric Mitchell, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Shows that preference fine-tuning can be done with a simple classification loss on policy log-ratios, with no reward model and no RL loop.',
				arxivId: '2305.18290',
				implementations: [
					{
						slug: 'research-dpo-logit',
						title: 'The implicit reward margin',
						difficulty: 'Advanced'
					},
					{ slug: 'research-dpo-loss', title: 'The preference loss', difficulty: 'Advanced' },
					{
						slug: 'research-dpo-implicit-reward',
						title: 'The implicit reward',
						difficulty: 'Intermediate'
					}
				]
			}
		]
	},
	{
		slug: 'agentic-systems',
		title: 'Agentic Systems',
		description: 'Reasoning and acting with language models, tool use and self-correction.',
		papers: [
			{
				slug: 'react',
				title: 'ReAct: Synergizing Reasoning and Acting in Language Models',
				authors: 'Shunyu Yao, Jeffrey Zhao, Dian Yu, et al.',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Interleaves reasoning traces with actions that query external sources, so the model can plan and gather information as it goes.',
				arxivId: '2210.03629',
				implementations: [
					{
						slug: 'research-react-parse-action',
						title: 'Parsing an action',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-react-prompt',
						title: 'Building the trace prompt',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-react-first-finish',
						title: 'Detecting the finish action',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'chain-of-thought',
				title: 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models',
				authors: 'Jason Wei, Xuezhi Wang, Dale Schuurmans, et al.',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Shows that prompting with worked examples that include intermediate reasoning steps greatly improves multi-step reasoning in large models.',
				arxivId: '2201.11903',
				implementations: [
					{
						slug: 'research-cot-prompt',
						title: 'Few-shot prompt with reasoning',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-cot-extract-answer',
						title: 'Extracting the final answer',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-cot-answers-match',
						title: 'Matching numeric answers',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'toolformer',
				title: 'Toolformer: Language Models Can Teach Themselves to Use Tools',
				authors: 'Timo Schick, Jane Dwivedi-Yu, Roberto Dessi, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Trains a language model to insert API calls into its own text, keeping only those calls that reduce the loss on the following words.',
				arxivId: '2302.04761',
				implementations: [
					{
						slug: 'research-toolformer-call-format',
						title: 'Formatting an API call',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-toolformer-insert-call',
						title: 'Inserting a call into text',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-toolformer-keep-call',
						title: 'Keeping useful calls',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'reflexion',
				title: 'Reflexion: Language Agents with Verbal Reinforcement Learning',
				authors: 'Noah Shinn, Federico Cassano, Edward Berman, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Agents write verbal reflections on failed attempts and keep them in memory, improving on later trials without updating model weights.',
				arxivId: '2303.11366',
				implementations: [
					{
						slug: 'research-reflexion-add-memory',
						title: 'Keeping a bounded memory',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-reflexion-prompt',
						title: 'The reflection prompt',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-reflexion-success-rate',
						title: 'Measuring success across trials',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'self-consistency',
				title: 'Self-Consistency Improves Chain of Thought Reasoning in Language Models',
				authors: 'Xuezhi Wang, Jason Wei, Dale Schuurmans, et al.',
				year: 2022,
				kind: 'foundational',
				summary:
					'Samples several reasoning paths and returns the most consistent answer, a simple improvement over greedy chain-of-thought decoding.',
				arxivId: '2203.11171',
				implementations: [
					{ slug: 'research-sc-majority-vote', title: 'Majority vote', difficulty: 'Intermediate' },
					{ slug: 'research-sc-agreement-rate', title: 'Agreement rate', difficulty: 'Beginner' },
					{
						slug: 'research-sc-normalize-answer',
						title: 'Normalizing answers',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'tree-of-thoughts',
				title: 'Tree of Thoughts: Deliberate Problem Solving with Large Language Models',
				authors: 'Shunyu Yao, Dian Yu, Jeffrey Zhao, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Frames reasoning as a search over thought trees, with the model proposing and evaluating partial solutions, plus breadth-first or depth-first search.',
				arxivId: '2305.10601',
				implementations: [
					{
						slug: 'research-tot-select-top-b',
						title: 'Keeping the best thoughts',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-tot-prune', title: 'Pruning weak branches', difficulty: 'Beginner' },
					{
						slug: 'research-tot-total-thoughts',
						title: 'The cost of a breadth search',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'voyager',
				title: 'Voyager: An Open-Ended Embodied Agent with Large Language Models',
				authors: 'Guanzhi Wang, Yuqi Xie, Yunfan Jiang, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'A lifelong learning agent that writes code, stores verified skills in a growing library and proposes its own curriculum of tasks.',
				arxivId: '2305.16291',
				implementations: [
					{
						slug: 'research-voyager-add-skill',
						title: 'Adding a skill to the library',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-voyager-retrieve-skill',
						title: 'Retrieving a skill',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-voyager-next-task',
						title: 'Choosing the next task',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'generative-agents',
				title: 'Generative Agents: Interactive Simulacra of Human Behavior',
				authors: "Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, et al.",
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Simulates believable agents with a memory stream, reflection and planning, retrieving memories by recency, importance and relevance.',
				arxivId: '2304.03442',
				implementations: [
					{ slug: 'research-ga-recency-score', title: 'The recency score', difficulty: 'Beginner' },
					{
						slug: 'research-ga-retrieval-score',
						title: 'The combined retrieval score',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-ga-top-k',
						title: 'Retrieving the top memories',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'mrkl',
				title:
					'MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning',
				authors: 'Ehud Karpas, Omri Abend, Yonatan Belinkov, et al.',
				year: 2022,
				kind: 'foundational',
				summary:
					'Routes parts of a query to specialized modules such as calculators and knowledge bases, with the language model coordinating them.',
				arxivId: '2205.00445',
				implementations: [
					{
						slug: 'research-mrkl-route-query',
						title: 'Routing a query to an expert',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-mrkl-arithmetic',
						title: 'An arithmetic expert',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-mrkl-dispatch',
						title: 'Dispatching to experts',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'self-refine',
				title: 'Self-Refine: Iterative Refinement with Self-Feedback',
				authors: 'Aman Madaan, Niket Tandon, Prakhar Gupta, et al.',
				year: 2023,
				kind: 'foundational',
				summary:
					'A single language model drafts, critiques its own output and revises it in a loop, without extra training or external supervision.',
				arxivId: '2303.17651',
				implementations: [
					{
						slug: 'research-selfrefine-loop',
						title: 'The refinement loop',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-selfrefine-first-ok',
						title: 'The first accepted round',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-selfrefine-prompt',
						title: 'The refinement prompt',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'gorilla',
				title: 'Gorilla: Large Language Model Connected with Massive APIs',
				authors: 'Shishir G. Patil, Tianjun Zhang, Xin Wang, Joseph E. Gonzalez',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Fine-tunes a model to call APIs correctly and pairs it with a retriever over API documentation, reducing hallucinated calls.',
				arxivId: '2305.15334',
				implementations: [
					{
						slug: 'research-gorilla-retrieve-api',
						title: 'Retrieving the right API',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-gorilla-name-match',
						title: 'Checking the called API name',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-gorilla-hallucinated',
						title: 'Detecting hallucinated APIs',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'hugginggpt',
				title: 'HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face',
				authors: 'Yongliang Shen, Kaitao Song, Xu Tan, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Uses a language model to plan a task graph, dispatches each subtask to a specialist model on Hugging Face, and combines their results.',
				arxivId: '2303.17580',
				implementations: [
					{
						slug: 'research-hugginggpt-topo-order',
						title: 'Ordering the subtasks',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-hugginggpt-valid-plan',
						title: 'Checking a plan',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-hugginggpt-resolve-args',
						title: 'Resolving task placeholders',
						difficulty: 'Intermediate'
					}
				]
			}
		]
	},
	{
		slug: 'inference-distributed-and-production',
		title: 'Inference, Distributed and Production',
		description: 'Memory-efficient attention, large-model serving and distributed training.',
		papers: [
			{
				slug: 'flashattention',
				title: 'FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness',
				authors: 'Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Re',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Computes exact attention in tiles held in fast on-chip memory, cutting memory traffic and making long sequences practical.',
				arxivId: '2205.14135',
				implementations: [
					{
						slug: 'research-flash-online-softmax-merge',
						title: 'Merging softmax blocks',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-flash-causal-block-skip',
						title: 'Skipping masked blocks',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-flash-hbm-bytes',
						title: 'Memory traffic of naive attention',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'flashattention-2',
				title: 'FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning',
				authors: 'Tri Dao',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Reduces non-matmul work and partitions attention across the GPU more effectively, roughly doubling the speed of the first version.',
				arxivId: '2307.08691',
				implementations: [
					{
						slug: 'research-fa2-deferred-normalization',
						title: 'Deferred normalization',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-fa2-attention-flops',
						title: 'Attention FLOPs',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-fa2-num-blocks',
						title: 'Partitioning work into blocks',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'megatron-lm',
				title:
					'Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism',
				authors: 'Mohammad Shoeybi, Mostofa Patwary, Raul Puri, et al.',
				year: 2019,
				kind: 'breakthrough',
				summary:
					'Splits transformer weight matrices across GPUs in a column and row pattern, so each block needs one all-reduce, enabling billion-parameter training.',
				arxivId: '1909.08053',
				implementations: [
					{
						slug: 'research-megatron-column-shard',
						title: 'Column-parallel weight shards',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-megatron-row-allreduce',
						title: 'Summing row-parallel partial outputs',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-megatron-tp-matmul',
						title: 'Tensor-parallel matrix multiply',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'zero',
				title: 'ZeRO: Memory Optimizations Toward Training Trillion Parameter Models',
				authors: 'Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, Yuxiong He',
				year: 2019,
				kind: 'breakthrough',
				summary:
					'Partitions optimizer states, gradients and parameters across data-parallel GPUs, removing the memory redundancy of standard data parallelism.',
				arxivId: '1910.02054',
				implementations: [
					{
						slug: 'research-zero-memory-per-gpu',
						title: 'Memory per GPU',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-zero-shard-size', title: 'The shard size', difficulty: 'Beginner' },
					{
						slug: 'research-zero-partition-bounds',
						title: 'Partition bounds',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'vllm',
				title: 'Efficient Memory Management for Large Language Model Serving with PagedAttention',
				authors: 'Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Stores the KV cache in fixed-size blocks like virtual memory pages, which nearly eliminates fragmentation and raises serving throughput.',
				arxivId: '2309.06180',
				implementations: [
					{
						slug: 'research-vllm-num-blocks',
						title: 'Blocks for a sequence',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-vllm-kv-cache-bytes',
						title: 'KV cache size',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-vllm-block-lookup',
						title: 'Finding a token’s block',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'gpipe',
				title: 'GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism',
				authors: 'Yanping Huang, Youlong Cheng, Ankur Bapna, et al.',
				year: 2018,
				kind: 'foundational',
				summary:
					'Splits a model into pipeline stages across devices and processes micro-batches so that all stages stay busy with gradient accumulation.',
				arxivId: '1811.06965',
				implementations: [
					{
						slug: 'research-gpipe-bubble-fraction',
						title: 'The pipeline bubble',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-gpipe-micro-batch-size',
						title: 'Micro-batch size',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-gpipe-schedule-steps',
						title: 'Steps in a pipeline schedule',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'speculative-decoding',
				title: 'Fast Inference from Transformers via Speculative Decoding',
				authors: 'Yaniv Leviathan, Matan Kalman, Yossi Matias',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'A small draft model proposes tokens that the large model verifies in parallel, with an acceptance rule that keeps the output distribution exact.',
				arxivId: '2211.17192',
				implementations: [
					{
						slug: 'research-spec-acceptance',
						title: 'The acceptance probability',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-spec-expected-tokens',
						title: 'Expected accepted tokens',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-spec-residual',
						title: 'The residual distribution',
						difficulty: 'Advanced'
					}
				]
			},
			{
				slug: 'multi-query-attention',
				title: 'Fast Transformer Decoding: One Write-Head is All You Need',
				authors: 'Noam Shazeer',
				year: 2019,
				kind: 'foundational',
				summary:
					'Shares one key and value head across all query heads, shrinking the decoder cache and speeding up incremental generation.',
				arxivId: '1911.02150',
				implementations: [
					{ slug: 'research-mqa-kv-elems', title: 'KV cache elements', difficulty: 'Beginner' },
					{
						slug: 'research-mqa-attention',
						title: 'Shared keys and values',
						difficulty: 'Advanced'
					},
					{
						slug: 'research-mqa-saving-ratio',
						title: 'The cache saving ratio',
						difficulty: 'Beginner'
					}
				]
			},
			{
				slug: 'gqa',
				title:
					'GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints',
				authors: 'Joshua Ainslie, James Lee-Thorp, Michiel de Jong, et al.',
				year: 2023,
				kind: 'breakthrough',
				summary:
					'Groups query heads to share key-value heads, a middle ground between multi-head and multi-query attention that keeps most of the quality.',
				arxivId: '2305.13245',
				implementations: [
					{
						slug: 'research-gqa-group-index',
						title: 'Which group is a head in?',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-gqa-expand-kv',
						title: 'Expanding key-value heads',
						difficulty: 'Intermediate'
					},
					{ slug: 'research-gqa-groups-valid', title: 'Valid group counts', difficulty: 'Beginner' }
				]
			},
			{
				slug: 'lora',
				title: 'LoRA: Low-Rank Adaptation of Large Language Models',
				authors: 'Edward J. Hu, Yelong Shen, Phillip Wallis, et al.',
				year: 2021,
				kind: 'breakthrough',
				summary:
					'Freezes the pretrained weights and trains a low-rank update, cutting fine-tuning memory and storage while adding no inference latency once merged.',
				arxivId: '2106.09685',
				implementations: [
					{ slug: 'research-lora-delta', title: 'The low-rank update', difficulty: 'Intermediate' },
					{
						slug: 'research-lora-param-count',
						title: 'Trainable parameter count',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-lora-forward',
						title: 'The adapted forward pass',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'gptq',
				title: 'GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers',
				authors: 'Elias Frantar, Saleh Ashkboos, Torsten Hoefler, Dan Alistarh',
				year: 2022,
				kind: 'breakthrough',
				summary:
					'Quantizes model weights to three or four bits after training, using approximate second-order information to correct rounding errors layer by layer.',
				arxivId: '2210.17323',
				implementations: [
					{
						slug: 'research-gptq-quantize',
						title: 'Symmetric quantization',
						difficulty: 'Intermediate'
					},
					{
						slug: 'research-gptq-dequantize',
						title: 'Dequantizing weights',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-gptq-error',
						title: 'Measuring quantization error',
						difficulty: 'Intermediate'
					}
				]
			},
			{
				slug: 'fsdp',
				title: 'PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel',
				authors: 'Yanli Zhao, Andrew Gu, Rohan Varma, et al.',
				year: 2023,
				kind: 'foundational',
				summary:
					'Describes PyTorch’s fully sharded data parallelism, which shards parameters, gradients and optimizer states across ranks and gathers them only when needed.',
				arxivId: '2304.11277',
				implementations: [
					{
						slug: 'research-fsdp-shard-numel',
						title: 'Elements per shard',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-fsdp-memory-per-rank',
						title: 'Memory per rank',
						difficulty: 'Beginner'
					},
					{
						slug: 'research-fsdp-padded-numel',
						title: 'Padded flat parameters',
						difficulty: 'Intermediate'
					}
				]
			}
		]
	}
];

export const papers: Paper[] = paperTopics.flatMap((topic) => topic.papers);

export function getPaper(slug: string): Paper | undefined {
	return papers.find((paper) => paper.slug === slug);
}
