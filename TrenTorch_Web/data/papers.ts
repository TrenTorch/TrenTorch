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
		papers: []
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
