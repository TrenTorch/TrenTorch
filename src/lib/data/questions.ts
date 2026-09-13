export type Difficulty = 'Easy' | 'Medium' | 'Hard';

export interface Question {
	slug: string;
	title: string;
	difficulty: Difficulty;
	topics: string[];
}

export interface Track {
	name: string;
	questions: Question[];
}

export interface Part {
	id: string;
	title: string;
	tracks: Track[];
}

function slugify(title: string): string {
	return title
		.toLowerCase()
		.replace(/[()/]/g, '')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/(^-|-$)/g, '');
}

function mkTrack(
	name: string,
	topics: string[],
	items: [title: string, difficulty: Difficulty, explicitSlug?: string][]
): Track {
	// Slugified from "track name + title", not title alone: several tracks
	// share generic titles like "Full training loop" or "Stack multiple
	// blocks", which collided into the same slug when only the title was
	// used (caught by questions.spec.ts's uniqueness check).
	//
	// A question can pass an explicit third element instead, when its slug
	// needs to match a real IDE content id exactly (e.g. one of Maanas's
	// authored questions under data/) rather than whatever this function
	// would derive on its own.
	return {
		name,
		questions: items.map(([title, difficulty, explicitSlug]) => ({
			slug: explicitSlug ?? slugify(`${name} ${title}`),
			title,
			difficulty,
			topics
		}))
	};
}

const partMath: Part = {
	id: 'part-math',
	title: 'Math & Statistics for ML',
	tracks: [
		mkTrack(
			'Linear Algebra',
			['Linear Algebra'],
			[
				[
					'Vectors, matrices and tensors: shapes and basic operations',
					'Easy',
					'math-vectors-matrices-tensors'
				],
				['Dot product and vector norms (L1, L2, L-infinity)', 'Easy', 'math-dot-product-norms'],
				['Matrix multiplication from first principles', 'Medium', 'math-matrix-multiplication'],
				['Transpose, and its role in reshaping without copying data', 'Easy', 'math-transpose'],
				['Matrix inverse, and when it does not exist', 'Medium', 'math-matrix-inverse'],
				['Eigenvalues and eigenvectors of a small matrix', 'Hard', 'math-eigenvalues-eigenvectors'],
				['Singular Value Decomposition (SVD)', 'Hard', 'math-svd'],
				[
					'Positive-definite matrices, and why they matter for optimization',
					'Medium',
					'math-positive-definite-matrices'
				]
			]
		),
		mkTrack(
			'Calculus',
			['Calculus'],
			[
				[
					'Derivatives from first principles: the limit definition, computed numerically',
					'Easy',
					'math-derivatives-first-principles'
				],
				['Partial derivatives of a multivariate function', 'Easy', 'math-partial-derivatives'],
				["Chain rule: composing two functions' derivatives by hand", 'Medium', 'math-chain-rule'],
				[
					'Jacobian: the matrix of all partial derivatives of a vector-valued function',
					'Hard',
					'math-jacobian'
				],
				[
					'Hessian: second-order partial derivatives, and what its eigenvalues tell you',
					'Hard',
					'math-hessian'
				],
				[
					'Directional derivatives, and the gradient as steepest ascent',
					'Medium',
					'math-directional-derivatives'
				]
			]
		),
		mkTrack(
			'Probability',
			['Probability & Statistics'],
			[
				[
					'Sampling from a random variable and estimating its distribution',
					'Easy',
					'math-sampling-estimating-distribution'
				],
				['Expectation and variance from a sample', 'Easy', 'math-expectation-variance'],
				[
					'Covariance and correlation between two variables',
					'Medium',
					'math-covariance-correlation'
				],
				[
					'Conditional probability from a joint distribution',
					'Medium',
					'math-conditional-probability'
				],
				["Bayes' theorem: updating a belief given evidence", 'Medium', 'math-bayes-theorem'],
				[
					'Likelihood vs. probability: the same formula, two different questions',
					'Medium',
					'math-likelihood-vs-probability'
				],
				[
					'Maximum likelihood estimation for a simple distribution',
					'Hard',
					'math-maximum-likelihood-estimation'
				],
				['MAP estimation: maximum likelihood plus a prior', 'Hard', 'math-map-estimation']
			]
		),
		mkTrack(
			'Information Theory',
			['Information Theory'],
			[
				['Entropy of a discrete distribution', 'Easy', 'math-entropy'],
				[
					"Cross-entropy, and why it's the loss Classification already uses",
					'Medium',
					'math-cross-entropy'
				],
				['KL divergence between two distributions', 'Medium', 'math-kl-divergence'],
				['Mutual information between two variables', 'Hard', 'math-mutual-information']
			]
		)
	]
};

const partDataFoundations: Part = {
	id: 'part-data-foundations',
	title: 'Data & Statistics Foundations',
	tracks: [
		mkTrack(
			'Data Preprocessing',
			['Data Processing'],
			[
				[
					'Detecting and counting missing values in a dataset',
					'Easy',
					'math-detecting-missing-values'
				],
				[
					'Imputing missing numeric values with a column mean/median',
					'Easy',
					'math-imputing-missing-values'
				],
				['One-hot encoding a categorical column', 'Medium', 'math-one-hot-encoding'],
				[
					'Feature scaling: standardization vs min-max normalization',
					'Medium',
					'math-feature-scaling'
				]
			]
		),
		mkTrack(
			'Exploratory Data Analysis',
			['Data Processing'],
			[
				['Detecting outliers with IQR and z-score', 'Easy', 'math-outlier-detection'],
				[
					"Summarizing a feature's distribution: mean, median, skew",
					'Easy',
					'math-summarizing-distribution'
				],
				[
					'Correlation matrix, and why correlation is not causation',
					'Medium',
					'math-correlation-matrix'
				],
				[
					'Data leakage: a feature that accidentally encodes the label',
					'Hard',
					'math-data-leakage'
				],
				[
					"Feature engineering: deriving a feature that makes the model's job easier",
					'Medium',
					'math-feature-engineering'
				],
				['Stratified sampling for an imbalanced dataset', 'Medium', 'math-stratified-sampling']
			]
		),
		mkTrack(
			'Statistical Inference',
			['Probability & Statistics'],
			[
				['Confidence interval for a sample mean', 'Medium', 'math-confidence-interval'],
				['Bootstrap confidence intervals', 'Medium', 'math-bootstrap-confidence-intervals'],
				[
					'Hypothesis testing: a two-sample t-test from scratch',
					'Hard',
					'math-hypothesis-testing-t-test'
				],
				[
					'A/B testing: is the difference between two groups real or noise',
					'Medium',
					'math-ab-testing'
				],
				[
					'Statistical significance and p-values, and what they do not mean',
					'Easy',
					'math-statistical-significance-p-values'
				]
			]
		)
	]
};

const partClassicalLinear: Part = {
	id: 'part-classical-linear',
	title: 'Classical ML: Linear Models',
	tracks: [
		mkTrack(
			'Linear Regression',
			['Regression', 'Optimization'],
			[
				// Slugs pinned to match data/classical-ml/linear-regression/ exactly
				// (Maanas's real, authored IDE content) instead of this file's usual
				// auto-derived slug, so these rows open real content, not a "not
				// published yet" placeholder.
				['Hypothesis Function', 'Easy', 'linear-regression-hypothesis-function'],
				['Mean Squared Error Loss', 'Easy', 'linear-regression-mse-loss'],
				['Gradient of MSE with Respect to w and b', 'Medium', 'linear-regression-mse-gradient'],
				['One Gradient-Descent Update', 'Easy', 'linear-regression-gd-step'],
				['Full Linear Regression Training Loop', 'Medium', 'linear-regression-training-loop'],
				['Stretch: L2 Regularization (Ridge)', 'Medium', 'linear-regression-ridge-gradient'],
				[
					'Production Engineering: Mini-Batch Training',
					'Hard',
					'linear-regression-production-mini-batch'
				],
				['Stretch: L1 Loss (MAE), contrasted against MSE', 'Easy', 'linear-regression-l1-loss-mae'],
				[
					'Stretch: Huber Loss, quadratic near zero and linear far from it',
					'Medium',
					'linear-regression-huber-loss'
				],
				[
					'Generalization: train/val split and the generalization gap',
					'Medium',
					'linear-regression-generalization-train-val-split'
				]
			]
		),
		mkTrack(
			'Classification (Logistic Regression)',
			['Classification', 'Optimization'],
			[
				['Sigmoid Function', 'Easy', 'classification-sigmoid'],
				['Binary Cross-Entropy Loss', 'Easy', 'classification-bce-loss'],
				['Gradient of BCE', 'Medium', 'classification-bce-gradient'],
				['Decision Boundary / Thresholding', 'Easy', 'classification-decision-boundary'],
				['Full Training Loop', 'Medium', 'classification-training-loop'],
				['Stretch: Softmax + Categorical Cross-Entropy', 'Medium', 'classification-softmax-cce'],
				['Linear Discriminant Analysis (LDA)', 'Hard', 'classification-lda'],
				['Stretch: Class Imbalance Handling', 'Medium', 'classification-weighted-bce'],
				[
					'Production Engineering: Fused, Numerically-Stable Loss',
					'Hard',
					'classification-production-bce-with-logits'
				],
				[
					'LogSoftmax + NLLLoss: the two pieces CrossEntropyLoss actually fuses',
					'Medium',
					'classification-logsoftmax-nllloss'
				],
				[
					'Production Engineering: detecting train/serve distribution shift',
					'Hard',
					'classification-distribution-shift-detection'
				],
				[
					'Multiclass via One-vs-Rest, contrasted against Softmax',
					'Medium',
					'classification-one-vs-rest'
				]
			]
		),
		mkTrack(
			'Regularized Linear Models',
			['Regression', 'Classic ML'],
			[
				[
					'Linear Regression: closed form (Normal Equation)',
					'Medium',
					'regularized-linear-models-normal-equation'
				],
				['Ridge Regression (L2)', 'Medium', 'regularized-linear-models-ridge-regression'],
				[
					'Lasso Regression (L1), contrasted against Ridge',
					'Medium',
					'regularized-linear-models-lasso-regression'
				],
				[
					'Elastic Net: combining L1 and L2 penalties',
					'Medium',
					'regularized-linear-models-elastic-net'
				],
				[
					'Polynomial features: expanding inputs before a linear model',
					'Medium',
					'regularized-linear-models-polynomial-features'
				],
				[
					'Note: Generalized Linear Models, one framework behind Linear and Logistic Regression',
					'Easy'
				]
			]
		),
		mkTrack(
			'Support Vector Machines',
			['Classic ML', 'Loss Functions'],
			[
				['Hinge loss', 'Easy', 'support-vector-machines-hinge-loss'],
				['Margin maximization intuition', 'Easy', 'support-vector-machines-margin-maximization'],
				[
					'Linear SVM via gradient descent on hinge loss',
					'Medium',
					'support-vector-machines-linear-svm-gradient-descent'
				],
				['Stretch: kernel trick (conceptual)', 'Hard']
			]
		)
	]
};

const partClassicalTrees: Part = {
	id: 'part-classical-trees',
	title: 'Classical ML: Trees & Ensembles',
	tracks: [
		mkTrack(
			'Decision Trees',
			['Classic ML'],
			[
				['Gini Impurity for a split', 'Easy', 'decision-trees-gini-impurity'],
				['Information Gain for a split', 'Easy', 'decision-trees-information-gain'],
				[
					'Decision Tree best split (assemble a minimal tree)',
					'Hard',
					'decision-trees-best-split-minimal-tree'
				],
				['Pruning (pre-pruning, post-pruning)', 'Medium', 'decision-trees-pruning'],
				[
					'Regression trees: splitting on variance reduction instead of Gini',
					'Medium',
					'decision-trees-regression-trees'
				],
				['Feature importance from a fitted tree', 'Medium', 'decision-trees-feature-importance']
			]
		),
		mkTrack(
			'Ensembles',
			['Classic ML'],
			[
				[
					'Random Forest: majority vote aggregation',
					'Medium',
					'ensembles-random-forest-majority-vote'
				],
				['Stretch: bagging concept', 'Easy', 'ensembles-bagging'],
				[
					'Gradient Boosting: fit one tree to the negative gradient of the loss',
					'Medium',
					'ensembles-gradient-boosting-negative-gradient'
				],
				['Full boosting loop: assemble a minimal booster', 'Hard', 'ensembles-full-boosting-loop'],
				[
					'Random Forest regression, and out-of-bag error estimation',
					'Medium',
					'ensembles-random-forest-regression-oob'
				],
				['AdaBoost: reweighting misclassified samples each round', 'Medium', 'ensembles-adaboost'],
				[
					'Stretch: regularized boosting (shrinkage + L2 leaf penalty, XGBoost-style)',
					'Hard',
					'ensembles-regularized-boosting'
				],
				[
					'Note: histogram-based boosting (LightGBM-style binning), why it is faster at scale',
					'Easy',
					'ensembles-histogram-boosting'
				]
			]
		),
		mkTrack(
			'Instance-Based and Probabilistic',
			['Classic ML'],
			[
				['KNN: distance and neighbor lookup', 'Easy', 'instance-based-probabilistic-knn'],
				[
					'Naive Bayes: Bernoulli log-likelihood',
					'Medium',
					'instance-based-probabilistic-naive-bayes-bernoulli'
				],
				[
					'Stretch: Gaussian Naive Bayes',
					'Medium',
					'instance-based-probabilistic-gaussian-naive-bayes'
				],
				['Nearest centroid classifier', 'Easy', 'instance-based-probabilistic-nearest-centroid'],
				[
					'Note: Gaussian Processes, a distribution over functions instead of over parameters',
					'Medium',
					'instance-based-probabilistic-gaussian-processes'
				]
			]
		)
	]
};

const partClassicalUnsupervised: Part = {
	id: 'part-classical-unsupervised',
	title: 'Classical ML: Unsupervised & Evaluation',
	tracks: [
		mkTrack(
			'Unsupervised',
			['Classic ML'],
			[
				['K-Means: assignment step', 'Easy', 'unsupervised-kmeans-assignment'],
				['K-Means: centroid update', 'Easy', 'unsupervised-kmeans-centroid-update'],
				['PCA: projection', 'Medium', 'unsupervised-pca-projection'],
				['Gaussian Mixture Clustering', 'Hard', 'unsupervised-gaussian-mixture'],
				['Stretch: EM Algorithm', 'Hard', 'unsupervised-em-algorithm'],
				[
					'Isolation Forest: anomaly detection via random splits',
					'Medium',
					'unsupervised-isolation-forest'
				],
				['DBSCAN: density-based clustering', 'Medium', 'unsupervised-dbscan'],
				[
					'Hierarchical clustering: agglomerative merge order',
					'Medium',
					'unsupervised-hierarchical-clustering'
				],
				[
					'Note: t-SNE and UMAP, nonlinear dimensionality reduction for visualization',
					'Easy',
					'unsupervised-tsne-umap'
				]
			]
		),
		mkTrack(
			'Evaluation and Model Selection',
			['Metrics & Evaluation'],
			[
				[
					'Train/test split, k-fold cross-validation, bootstrapping',
					'Easy',
					'evaluation-splitting-and-resampling'
				],
				['Precision, Recall, F1, ROC, AUC', 'Medium', 'evaluation-classification-metrics'],
				['Bias-variance tradeoff', 'Medium', 'evaluation-bias-variance-tradeoff'],
				['Grid search over a hyperparameter grid', 'Easy', 'evaluation-grid-search'],
				['Random search, contrasted against grid search', 'Medium', 'evaluation-random-search'],
				[
					'Note: Bayesian optimization for hyperparameter search',
					'Medium',
					'evaluation-bayesian-optimization'
				],
				[
					'Early stopping: halting training at the best validation checkpoint',
					'Medium',
					'evaluation-early-stopping'
				],
				[
					'Learning curves: training/validation error vs. dataset size',
					'Medium',
					'evaluation-learning-curves'
				],
				[
					'Validation curves: training/validation error vs. one hyperparameter',
					'Medium',
					'evaluation-validation-curves'
				],
				[
					'Calibration: does a predicted probability of 0.8 mean 80% of the time',
					'Hard',
					'evaluation-calibration'
				],
				[
					'Threshold optimization for imbalanced classification',
					'Medium',
					'evaluation-threshold-optimization'
				],
				[
					'Nested cross-validation, and why plain CV leaks hyperparameter choices',
					'Hard',
					'evaluation-nested-cross-validation'
				],
				[
					'Model selection under class imbalance',
					'Medium',
					'evaluation-model-selection-class-imbalance'
				]
			]
		),
		mkTrack(
			'Tabular Foundation Models',
			['Transformers', 'Classic ML'],
			[
				[
					'Row-wise attention over table cells',
					'Hard',
					'tabular-foundation-models-row-wise-attention'
				],
				[
					'Column-wise attention over table cells',
					'Hard',
					'tabular-foundation-models-column-wise-attention'
				],
				[
					'Combine into a TabPFN-style two-way attention block',
					'Hard',
					'tabular-foundation-models-two-way-attention-block'
				],
				[
					'In-context prediction: single forward pass, no per-dataset training loop',
					'Medium',
					'tabular-foundation-models-in-context-prediction'
				],
				[
					'Contrast note: why no positional encoding here, unlike Part 2',
					'Easy',
					'tabular-foundation-models-no-positional-encoding'
				]
			]
		)
	]
};

const partDlCore: Part = {
	id: 'part-dl-core',
	title: 'Deep Learning: Core Mechanics',
	tracks: [
		mkTrack(
			'Tensors',
			['Linear Algebra'],
			[
				['Tensor creation / dtype', 'Easy', 'dl-core-tensor-creation-dtype'],
				['Elementwise ops', 'Easy', 'dl-core-elementwise-ops'],
				['Broadcasting rules', 'Medium', 'dl-core-broadcasting-rules'],
				['Matmul', 'Medium', 'dl-core-matmul'],
				['Reshape / transpose', 'Easy', 'dl-core-reshape-transpose'],
				['Reduction ops (sum, mean, max)', 'Easy', 'dl-core-reduction-ops'],
				['Indexing / slicing', 'Easy', 'dl-core-indexing-slicing']
			]
		),
		mkTrack(
			'Activations (fwd + bwd each)',
			['Activation Functions', 'Neural Networks'],
			[
				['ReLU fwd/bwd', 'Easy', 'dl-core-relu'],
				['Sigmoid fwd/bwd', 'Easy', 'dl-core-sigmoid'],
				['Tanh fwd/bwd', 'Easy', 'dl-core-tanh'],
				['Softmax fwd/bwd', 'Medium', 'dl-core-softmax'],
				['GELU fwd/bwd', 'Medium', 'dl-core-gelu'],
				['Swish (SiLU) fwd/bwd', 'Medium', 'dl-core-swish'],
				['LeakyReLU fwd/bwd', 'Easy', 'dl-core-leaky-relu'],
				['Mish fwd/bwd', 'Medium', 'dl-core-mish']
			]
		),
		mkTrack(
			'Loss Functions',
			['Loss Functions'],
			[
				['MSE', 'Easy', 'dl-core-mse-loss'],
				['Cross-Entropy', 'Medium', 'dl-core-cross-entropy-loss'],
				['Binary Cross-Entropy', 'Medium', 'dl-core-binary-cross-entropy-loss']
			]
		),
		mkTrack(
			'Autograd (micrograd-style progressive build)',
			['Neural Networks'],
			[
				['Backward for addition', 'Easy', 'dl-core-backward-addition'],
				['Backward for multiplication', 'Easy', 'dl-core-backward-multiplication'],
				['Backward for matmul', 'Medium', 'dl-core-backward-matmul'],
				['Graph node (value + grad + backward fn)', 'Medium', 'dl-core-graph-node'],
				['Topological sort for backward pass', 'Hard', 'dl-core-topological-sort'],
				['Assemble minimal autograd engine', 'Hard', 'dl-core-minimal-autograd-engine'],
				[
					'Numerical gradient checking: verify an analytical gradient via finite differences',
					'Medium',
					'dl-core-numerical-gradient-checking'
				]
			]
		)
	]
};

const partDlTraining: Part = {
	id: 'part-dl-training',
	title: 'Deep Learning: Training & Theory',
	tracks: [
		mkTrack(
			'Optimizers',
			['Optimization'],
			[
				['SGD', 'Easy', 'dl-training-sgd'],
				['SGD + Momentum', 'Medium', 'dl-training-sgd-momentum'],
				['Adam: bias-corrected moment estimates', 'Medium', 'dl-training-adam-bias-correction'],
				['Adam: full update rule', 'Medium', 'dl-training-adam-full-update'],
				['AdamW: decoupled weight decay', 'Medium', 'dl-training-adamw-decoupled-weight-decay'],
				['Muon', 'Hard', 'dl-training-muon'],
				['Gradient clipping (global norm)', 'Easy', 'dl-training-gradient-clipping'],
				[
					'Learning rate scheduling: warmup and cosine decay',
					'Medium',
					'dl-training-lr-warmup-cosine-decay'
				],
				[
					'OneCycleLR schedule, contrasted against warmup + cosine decay',
					'Medium',
					'dl-training-onecyclelr'
				],
				[
					'Stretch: optimizer survey (RMSprop, Adagrad, NAdam, RAdam, AdaDelta, Nesterov momentum)',
					'Medium'
				],
				['Note: L-BFGS and why second-order methods do not scale to deep nets', 'Easy']
			]
		),
		mkTrack(
			'Layers',
			['Neural Networks'],
			[
				['Linear fwd', 'Easy', 'dl-training-linear-forward'],
				['Linear bwd', 'Medium', 'dl-training-linear-backward'],
				['Dropout fwd/bwd', 'Easy', 'dl-training-dropout'],
				[
					'Weight initialization: Xavier/Glorot, He/Kaiming',
					'Medium',
					'dl-training-weight-initialization'
				],
				[
					'Minimal Module base class (parameter collection)',
					'Medium',
					'dl-training-module-base-class'
				],
				[
					'Sequential container: stack layers, one forward pass through all of them',
					'Easy',
					'dl-training-sequential-container'
				],
				[
					'LazyLinear: infer in_features from the first real forward call',
					'Medium',
					'dl-training-lazylinear'
				]
			]
		),
		mkTrack(
			'Training Loop',
			['Neural Networks', 'Data Processing'],
			[
				[
					'Dataset/DataLoader abstraction (indexing, batching, shuffling)',
					'Medium',
					'dl-training-dataset-dataloader'
				],
				[
					'Assemble full loop (data, forward, loss, backward, optimizer step)',
					'Medium',
					'dl-training-assemble-training-loop'
				],
				['Train/eval mode switching', 'Easy', 'dl-training-train-eval-mode'],
				['Basic metric tracking (loss curve)', 'Easy', 'dl-training-metric-tracking']
			]
		),
		mkTrack(
			'Regularization',
			['Neural Networks'],
			[
				[
					'Early stopping: monitor validation loss, restore the best checkpoint',
					'Medium',
					'dl-training-early-stopping'
				],
				[
					'Data augmentation: label-preserving input transformations',
					'Easy',
					'dl-training-data-augmentation'
				],
				[
					'Label smoothing: softening one-hot targets before cross-entropy',
					'Medium',
					'dl-training-label-smoothing'
				]
			]
		),
		mkTrack(
			'Why Deep Networks Work',
			['Neural Networks'],
			[
				[
					'Universal approximation: why one wide hidden layer can fit any function, in principle',
					'Medium',
					'dl-training-universal-approximation'
				],
				[
					'Representation learning: why depth learns hierarchical features, not one big lookup',
					'Easy',
					'dl-training-representation-learning'
				],
				[
					'Vanishing and exploding gradients: why a deep, badly-initialized net fails to train',
					'Hard',
					'dl-training-vanishing-exploding-gradients'
				],
				[
					'Internal covariate shift, and what BatchNorm was actually designed to fix',
					'Medium',
					'dl-training-batchnorm'
				],
				[
					'Overparameterization and double descent: more parameters than data can still generalize',
					'Hard',
					'dl-training-overparameterization-double-descent'
				],
				[
					'Note: optimization landscape vs. generalization, they are not the same problem',
					'Medium'
				],
				[
					'Note: neural tangent kernel, an infinitely-wide network behaves like a fixed kernel',
					'Hard'
				],
				['Note: scaling laws, why bigger models trained on more data reliably get better', 'Easy']
			]
		)
	]
};

const partSeqModeling: Part = {
	id: 'part-seq-modeling',
	title: 'Sequence Modeling & Attention',
	tracks: [
		mkTrack(
			'Tokenization',
			['NLP'],
			[
				['Whitespace/character tokenizer', 'Easy', 'seq-tokenization-whitespace-char'],
				[
					'Vocabulary building + unknown-token handling',
					'Easy',
					'seq-tokenization-vocabulary-building'
				],
				['BPE: single merge step', 'Medium', 'seq-tokenization-bpe-single-merge'],
				['Stretch: BPE, full training loop', 'Hard', 'seq-tokenization-bpe-full-training-loop'],
				['Encode/decode round-trip', 'Easy', 'seq-tokenization-encode-decode-roundtrip']
			]
		),
		mkTrack(
			'Embeddings',
			['NLP', 'Transformers'],
			[
				['Token embedding lookup', 'Easy', 'seq-embeddings-token-embedding-lookup'],
				[
					'Embedding backward (scatter-add gradient)',
					'Medium',
					'seq-embeddings-embedding-backward'
				],
				[
					'Sinusoidal positional encoding',
					'Medium',
					'seq-embeddings-sinusoidal-positional-encoding'
				],
				['Learned positional embedding', 'Easy', 'seq-embeddings-learned-positional-embedding'],
				[
					'Combine token and positional embeddings',
					'Easy',
					'seq-embeddings-combine-token-positional'
				],
				['RoPE (Rotary Position Embeddings)', 'Hard', 'seq-embeddings-rope']
			]
		),
		mkTrack(
			'Recurrent Neural Networks',
			['NLP', 'Neural Networks'],
			[
				['Vanilla RNN cell, forward', 'Easy', 'seq-rnn-cell-forward'],
				['Vanilla RNN cell, backward', 'Medium', 'seq-rnn-cell-backward'],
				[
					'Backprop through time (BPTT): vanishing and exploding gradient intuition',
					'Hard',
					'seq-rnn-bptt-vanishing-exploding'
				],
				['LSTM cell, forward (gating mechanism)', 'Medium', 'seq-rnn-lstm-cell-forward'],
				['GRU cell, forward (simplified gating)', 'Medium', 'seq-rnn-gru-cell-forward'],
				['Stretch: bidirectional RNN', 'Medium', 'seq-rnn-bidirectional'],
				[
					'Sequence-to-sequence / encoder-decoder: the bottleneck problem attention was invented to solve',
					'Medium',
					'seq-rnn-seq2seq-bottleneck'
				]
			]
		),
		mkTrack(
			'Attention',
			['Transformers'],
			[
				['Scaled dot-product attention, forward', 'Medium', 'seq-attention-scaled-dot-product'],
				['Causal mask', 'Easy', 'seq-attention-causal-mask'],
				[
					'Softmax (reuses Part 1, the first cross-part reuse)',
					'Easy',
					'seq-attention-softmax-last-axis'
				],
				[
					'Multi-Head Attention: splitting into heads, per-head attention',
					'Medium',
					'seq-attention-mha-split-heads'
				],
				[
					'Multi-Head Attention: concatenating heads plus output projection',
					'Medium',
					'seq-attention-mha-concat-output-projection'
				],
				['Stretch: Grouped-Query Attention (GQA)', 'Hard', 'seq-attention-grouped-query-attention']
			]
		)
	]
};

const partTransformersLlm: Part = {
	id: 'part-transformers-llm',
	title: 'Transformers & LLMs',
	tracks: [
		mkTrack(
			'Transformer Block',
			['Transformers'],
			[
				['Layer Normalization, forward', 'Medium', 'txf-block-layer-norm-forward'],
				['Stretch: RMSNorm (alternative to LayerNorm)', 'Easy', 'txf-block-rmsnorm'],
				['Residual/skip connection', 'Easy', 'txf-block-residual-connection'],
				[
					'Feed-forward sublayer (reuses Part 1 Linear + activation)',
					'Easy',
					'txf-block-feedforward-sublayer'
				],
				['Stretch: SwiGLU-gated FFN', 'Medium', 'txf-block-swiglu-ffn'],
				[
					'Assemble one full block (attention, norm, residual, FFN, norm, residual)',
					'Hard',
					'txf-block-assemble-full-block'
				],
				['Stack multiple blocks', 'Medium', 'txf-block-stack-blocks']
			]
		),
		mkTrack(
			'Modern Transformer Architecture',
			['Transformers'],
			[
				[
					'Encoder vs. decoder vs. encoder-decoder: three ways to arrange the same block',
					'Easy',
					'txf-modern-encoder-decoder-arrangements'
				],
				[
					'Pre-norm vs. post-norm: where LayerNorm sits, and why it changes trainability',
					'Medium',
					'txf-modern-pre-norm-vs-post-norm'
				],
				[
					"Attention's quadratic complexity, and why context length is expensive",
					'Medium',
					'txf-modern-attention-quadratic-complexity'
				],
				[
					'Note: FlashAttention, the same math computed without materializing the full attention matrix',
					'Medium',
					'txf-modern-flash-attention'
				],
				[
					'Sliding-window / local attention: bounding context to a fixed window',
					'Medium',
					'txf-modern-sliding-window-attention'
				],
				[
					'ALiBi: a positional bias baked into attention scores instead of the embeddings',
					'Medium',
					'txf-modern-alibi'
				],
				[
					'Note: attention sinks, why the first few tokens matter disproportionately',
					'Easy',
					'txf-modern-attention-sinks'
				],
				[
					'RoPE scaling: extending a model past its trained context length',
					'Hard',
					'txf-modern-rope-scaling'
				],
				[
					'Untied embeddings, contrasted against weight tying',
					'Easy',
					'txf-modern-untied-embeddings'
				],
				['Logit scaling before the final softmax', 'Easy', 'txf-modern-logit-scaling']
			]
		),
		mkTrack(
			'Language Model Assembly',
			['Transformers', 'NLP'],
			[
				['Output projection to vocab logits', 'Easy', 'txf-lm-output-projection'],
				['Weight tying (share input/output embedding matrix)', 'Medium', 'txf-lm-weight-tying'],
				[
					'Next-token Cross-Entropy loss (reuses Part 1 loss)',
					'Medium',
					'txf-lm-next-token-cross-entropy'
				],
				[
					'Full forward pass (tokens to embeddings to blocks to logits)',
					'Hard',
					'txf-lm-full-forward-pass'
				],
				[
					'Training loop for next-token prediction (reuses Part 1 loop)',
					'Hard',
					'txf-lm-training-loop'
				],
				[
					'Perplexity (exp of loss), the standard LM evaluation metric',
					'Easy',
					'txf-lm-perplexity'
				],
				['Greedy decoding / generation', 'Medium', 'txf-lm-greedy-decoding'],
				['Stretch: temperature + top-k sampling', 'Medium', 'txf-lm-temperature-topk-sampling'],
				['Beam search decoding, contrasted against greedy', 'Hard', 'txf-lm-beam-search-decoding']
			]
		),
		mkTrack(
			'LLM Engineering',
			['Transformers', 'NLP'],
			[
				[
					'Mixture of Experts: top-k gating, route each token to its best expert FFN',
					'Hard',
					'txf-llmeng-mixture-of-experts'
				],
				[
					'Speculative decoding: draft-and-verify loop, accept/reject against a larger model',
					'Hard',
					'txf-llmeng-speculative-decoding'
				],
				[
					'Capstone: wire tokenization, embeddings, attention and the training loop into one tiny end-to-end LLM',
					'Hard',
					'txf-llmeng-capstone-tiny-llm'
				],
				[
					'Deduplication: removing near-identical documents before training',
					'Medium',
					'txf-llmeng-deduplication'
				],
				[
					'Data filtering and contamination: keeping eval data out of the training set',
					'Medium',
					'txf-llmeng-data-filtering-contamination'
				],
				[
					'Sequence packing: concatenating short examples to fill a fixed context window',
					'Medium',
					'txf-llmeng-sequence-packing'
				],
				[
					'Gradient accumulation: simulating a larger batch size than memory allows',
					'Medium',
					'txf-llmeng-gradient-accumulation'
				],
				[
					'Resume-from-checkpoint: restoring optimizer state, not just weights',
					'Medium',
					'txf-llmeng-resume-from-checkpoint'
				],
				[
					'Reading a loss curve: spotting training instability before it diverges',
					'Medium',
					'txf-llmeng-reading-loss-curves'
				],
				[
					'Compute-optimal training: Chinchilla-style scaling laws',
					'Hard',
					'txf-llmeng-chinchilla-scaling-laws'
				]
			]
		)
	]
};

const partVision: Part = {
	id: 'part-vision',
	title: 'Vision Modeling',
	tracks: [
		mkTrack(
			'Convolutions',
			['Computer Vision'],
			[
				['Single-channel, single-filter 2D conv', 'Medium'],
				['Padding (same vs valid)', 'Easy'],
				['Stride', 'Easy'],
				['Multi-channel input', 'Medium'],
				['Multiple output filters', 'Medium'],
				['Stretch: im2col optimization', 'Hard']
			]
		),
		mkTrack(
			'Pooling',
			['Computer Vision'],
			[
				['Max pooling, forward', 'Easy'],
				['Average pooling, forward', 'Easy'],
				['Adaptive average pooling (global average pool), the modern flatten replacement', 'Medium']
			]
		),
		mkTrack(
			'CNN Architecture',
			['Computer Vision', 'Neural Networks'],
			[
				['Flatten (bridges to Part 1 Linear layers)', 'Easy'],
				['One CNN block (conv + activation + pool)', 'Medium'],
				['Stack multiple blocks', 'Medium'],
				['Full CNN classifier (reuses Part 0 classification loss/loop)', 'Hard']
			]
		),
		mkTrack(
			'Modern CNN Concepts',
			['Computer Vision', 'Neural Networks'],
			[
				['Batch Normalization, forward', 'Medium'],
				["Residual/skip connection (reuses Part 2's residual concept)", 'Easy'],
				['1x1 convolution: channel-wise mixing without spatial mixing (bottleneck)', 'Medium'],
				['Transposed convolution (upsampling), contrasted against regular convolution', 'Hard'],
				['Depthwise-separable convolution: the efficiency trick behind MobileNet', 'Hard']
			]
		),
		mkTrack(
			'CNN Architecture History',
			['Computer Vision'],
			[
				['Note: AlexNet, what actually changed from LeNet (ReLU, dropout, scale)', 'Easy'],
				['VGG: stacking small 3x3 convs instead of one large one', 'Medium'],
				["DenseNet: concatenating every previous layer's output instead of adding", 'Medium'],
				[
					'Note: EfficientNet, scaling depth/width/resolution together instead of one at a time',
					'Easy'
				],
				['Dilated convolution: expanding receptive field without more parameters', 'Medium'],
				['Note: feature pyramids, combining multiple resolutions for detection', 'Easy']
			]
		),
		mkTrack(
			'Vision Transformer',
			['Computer Vision', 'Transformers'],
			[
				['Patchify an image into fixed-size patches', 'Medium'],
				['Patch embedding (linear projection, reuses Part 1)', 'Easy'],
				['Class token + position embedding', 'Medium'],
				["Feed through Part 2's transformer block, unmodified", 'Medium'],
				['Classification head', 'Easy'],
				['Stretch: InfoNCE loss (CLIP-style image-text contrastive training)', 'Hard'],
				['Stretch: Triplet loss (metric/representation learning)', 'Medium']
			]
		)
	]
};

const partSystemsPerf: Part = {
	id: 'part-systems-perf',
	title: 'Systems: Performance & Efficiency',
	tracks: [
		mkTrack(
			'Profiling (inference/analysis tooling)',
			['MLOps'],
			[
				['Timing decorator', 'Easy'],
				['Parameter counting', 'Easy'],
				['Memory footprint estimation', 'Medium'],
				['FLOPs estimation (Linear/Conv)', 'Medium'],
				['Checkpointing: save/load parameters to disk, resume training', 'Easy']
			]
		),
		mkTrack(
			'Quantization',
			['MLOps', 'Neural Networks'],
			[
				['Float32 to Int8 mapping (quantize)', 'Medium'],
				['Int8 to Float32 reconstruction (dequantize)', 'Medium'],
				['Quantize a full weight matrix, measure size/accuracy tradeoff', 'Hard']
			]
		),
		mkTrack(
			'Mixed Precision Training',
			['MLOps', 'Neural Networks'],
			[
				['FP16/BF16 representable range vs FP32, why naive fp16 training underflows', 'Medium'],
				[
					'Loss scaling: scale the loss before backward, unscale gradients before the step',
					'Medium'
				],
				['Autocast concept: which ops run in reduced precision, which stay in fp32', 'Easy']
			]
		),
		mkTrack(
			'Compression',
			['MLOps', 'Neural Networks'],
			[
				['Magnitude-based pruning, single step', 'Medium'],
				['Stretch: iterative pruning schedule', 'Hard'],
				['Stretch: basic knowledge distillation (reuses KL Divergence)', 'Hard']
			]
		),
		mkTrack(
			'Acceleration',
			['MLOps'],
			[['Vectorize a naive Python loop into NumPy ops, before/after speed comparison', 'Easy']]
		),
		mkTrack(
			'Kernels',
			['MLOps'],
			[
				['Kernel fusion: fuse two elementwise ops into one pass, measure the win', 'Medium'],
				[
					'Memory-bound vs compute-bound: the roofline model, why fusion helps one but not the other',
					'Medium'
				],
				['Note: real kernels are written in CUDA/Triton, not NumPy, what changes and why', 'Easy'],
				[
					'Note: torch.compile / graph compilation, why a JIT-compiled graph beats eager mode',
					'Medium'
				],
				[
					'Note: TorchScript and ONNX export, why production serving does not run eager Python',
					'Easy'
				]
			]
		)
	]
};

const partSystemsDistributed: Part = {
	id: 'part-systems-distributed',
	title: 'Systems: Memory & Distributed Training',
	tracks: [
		mkTrack(
			'Memoization',
			['Transformers', 'MLOps'],
			[
				['KV-cache for autoregressive generation (reuses Part 2 directly)', 'Hard'],
				['Benchmark: with vs without cache', 'Medium'],
				[
					'Gradient checkpointing: recompute activations in backward instead of storing them',
					'Hard'
				]
			]
		),
		mkTrack(
			'Parallelism (concept only)',
			['MLOps'],
			[
				[
					'Data parallelism: a toy example splitting a batch across simulated workers, then averaging gradients',
					'Medium'
				],
				[
					'Note: model/pipeline parallelism (why frontier training needs it, not implemented)',
					'Easy'
				],
				[
					'Note: torch.nn.DataParallel vs DistributedDataParallel, what the real APIs do differently',
					'Easy'
				],
				[
					'All-reduce, all-gather and reduce-scatter: the collectives distributed training is built from',
					'Medium'
				],
				['Note: FSDP / ZeRO, sharding optimizer state and parameters across GPUs', 'Medium'],
				["Note: tensor parallelism, splitting one layer's matmul across GPUs", 'Medium'],
				['Note: sequence/context parallelism, splitting one long sequence across GPUs', 'Medium']
			]
		)
	]
};

const partRlAlignment: Part = {
	id: 'part-rl-alignment',
	title: 'Reinforcement Learning & Alignment',
	tracks: [
		mkTrack(
			'Reinforcement Learning',
			['Reinforcement Learning'],
			[
				[
					'Value iteration on a small Markov Decision Process',
					'Medium',
					'rl-alignment-value-iteration-mdp'
				],
				['Tabular Q-learning', 'Medium', 'rl-alignment-tabular-q-learning']
			]
		),
		mkTrack(
			'Post-Training & Alignment',
			['Reinforcement Learning', 'NLP'],
			[
				['Supervised fine-tuning: next-token loss, but only on the response tokens', 'Medium'],
				['Instruction datasets: prompt/response pairs vs. raw next-token pretraining', 'Easy'],
				['Preference datasets: chosen vs. rejected response pairs', 'Easy'],
				['Reward modeling: training a model to score a response instead of generate one', 'Hard'],
				['Note: RLHF, the full pretrain to SFT to reward model to PPO pipeline', 'Easy'],
				['Note: PPO, clipped policy updates for stable RL fine-tuning', 'Medium'],
				['DPO: optimizing the preference directly, no separate reward model or RL loop', 'Hard'],
				['Note: GRPO, group-relative advantage without a value network', 'Medium'],
				['Rejection sampling: keep only the best of several sampled responses', 'Easy'],
				["Best-of-N: sampling N responses and picking the reward model's favorite", 'Easy'],
				['Note: Constitutional AI, model-written critiques instead of human labels', 'Easy'],
				['Reward hacking: when optimizing the reward stops meaning what you wanted', 'Medium'],
				['Note: alignment tax, the capability cost of aligning a model', 'Easy'],
				['QLoRA: LoRA on top of a quantized base model', 'Hard'],
				[
					'Note: adapter methods, prefix tuning and prompt tuning, other parameter-efficient approaches',
					'Easy'
				]
			]
		),
		mkTrack(
			'Fine-tuning',
			['Reinforcement Learning', 'Neural Networks'],
			[
				["LoRA: low-rank adapter matrices bolted onto Part 1's Linear layer", 'Hard'],
				['Compare: full fine-tune vs. LoRA, on parameter count and memory', 'Medium'],
				['KL Divergence (distillation, and the RLHF KL penalty term)', 'Medium'],
				['Policy Gradient Loss', 'Medium'],
				['Generalized Advantage Estimation (pairs with Policy Gradient)', 'Hard']
			]
		),
		mkTrack(
			'Benchmarking and Capstone',
			['MLOps', 'Metrics & Evaluation'],
			[
				['Build a benchmark harness (reuses Profiling)', 'Medium'],
				['Apply one optimization, measure real improvement', 'Medium'],
				['Final capstone: submission/report', 'Hard']
			]
		)
	]
};

const partProductionMl: Part = {
	id: 'part-production-ml',
	title: 'Production ML',
	tracks: [
		mkTrack(
			'Experiment Tracking & Versioning',
			['MLOps'],
			[
				['Experiment tracking: logging hyperparameters, metrics and artifacts per run', 'Easy'],
				['Dataset versioning: why "the same CSV" is not reproducible without a hash', 'Medium'],
				[
					'Model versioning and a model registry: promoting a run to a named, deployable version',
					'Easy'
				],
				['Reproducibility: pinning every source of randomness in a training run', 'Medium']
			]
		),
		mkTrack(
			'Deployment & Serving',
			['MLOps'],
			[
				['Online vs. batch inference: request-by-request vs. scheduled bulk scoring', 'Easy'],
				['Training pipelines: turning a notebook into a reproducible, scheduled DAG', 'Medium'],
				['Note: CI/CD for ML, testing a model like you would test code before it ships', 'Easy'],
				['Canary deployment: rolling a new model out to a small slice of traffic first', 'Medium'],
				['Shadow deployment: running a new model silently alongside the live one', 'Medium'],
				['A/B testing a model change, and rolling back when it loses', 'Medium']
			]
		),
		mkTrack(
			'Monitoring & Drift',
			['MLOps'],
			[
				['Data drift: the input distribution shifting after deployment', 'Medium'],
				['Concept drift: the relationship between inputs and the target shifting', 'Medium'],
				['Model degradation over time, and deciding when to retrain', 'Medium'],
				['Retraining strategies: scheduled, triggered, and online learning', 'Medium']
			]
		)
	]
};

const partInference: Part = {
	id: 'part-inference',
	title: 'Inference',
	tracks: [
		mkTrack(
			'Attention Mechanisms',
			['Transformers', 'Inference'],
			[
				[
					'Scaled Dot-Product Attention: the core operation every transformer runs',
					'Medium',
					'inf-attn-scaled-dot-product'
				],
				['Multi-Head Attention: splitting into independent heads', 'Medium', 'inf-attn-multi-head'],
				[
					'Multi-Query Attention: sharing one KV head across all query heads',
					'Medium',
					'inf-attn-multi-query'
				],
				[
					'Grouped-Query Attention: the middle ground between MHA and MQA',
					'Medium',
					'inf-attn-grouped-query'
				],
				[
					'Multi-Head Latent Attention: compressing KV into a shared low-rank latent',
					'Hard',
					'inf-attn-multi-head-latent'
				]
			]
		),
		mkTrack(
			'KV Cache and Decoding',
			['Transformers', 'Inference'],
			[
				['Rotary Position Embeddings at a single decode step', 'Medium', 'inf-kv-rope-decoding'],
				[
					'Autoregressive Generation with a KV Cache: prefill then decode',
					'Medium',
					'inf-kv-autoregressive-cache'
				],
				['KV Cache Memory Footprint Across Attention Variants', 'Easy', 'inf-kv-memory-footprint'],
				['PagedAttention Block Allocation (as used in vLLM)', 'Hard', 'inf-kv-paged-attention'],
				['Prefix Cache Lookup and Reuse', 'Medium', 'inf-kv-prefix-cache']
			]
		),
		mkTrack(
			'Quantization and Numerical Efficiency',
			['Inference', 'MLOps'],
			[
				['Symmetric INT8 Quantization', 'Easy', 'inf-quant-int8-symmetric'],
				['Per-Channel Weight Quantization for Linear Layers', 'Medium', 'inf-quant-per-channel'],
				[
					'Group-Wise INT4 Weight Quantization (GPTQ/AWQ-style)',
					'Hard',
					'inf-quant-int4-groupwise'
				],
				['Block-Wise FP8 (E4M3-style) Quantization', 'Hard', 'inf-quant-fp8-blockwise'],
				['Prefill and Decode Analysis with the Roofline Model', 'Medium', 'inf-quant-roofline']
			]
		),
		mkTrack(
			'Batching and Serving Metrics',
			['Inference', 'MLOps'],
			[
				['Calculate P50, P95, and P99 Inference Latency', 'Easy', 'inf-batch-latency-percentiles'],
				[
					'Compute TTFT, TPOT, ITL, and Token Throughput',
					'Easy',
					'inf-batch-serving-metrics-ttft-tpot-itl'
				],
				[
					'Implement Dynamic (Static-Window) Request Batching',
					'Medium',
					'inf-batch-dynamic-request-batching'
				],
				['Simulate Continuous (Iteration-Level) Batching', 'Hard', 'inf-batch-continuous-batching'],
				['Simulate Chunked Prefill Scheduling', 'Hard', 'inf-batch-chunked-prefill']
			]
		)
	]
};

export const curriculum: Part[] = [
	partMath,
	partDataFoundations,
	partClassicalLinear,
	partClassicalTrees,
	partClassicalUnsupervised,
	partDlCore,
	partDlTraining,
	partSeqModeling,
	partTransformersLlm,
	partVision,
	partSystemsPerf,
	partSystemsDistributed,
	partRlAlignment,
	partProductionMl,
	partInference
];

/** `total` is always derived from the real curriculum data, never drifts
 * out of sync as questions get added. `completed` counts real solved
 * progress -- pass `solved.slugs` from the localStorage-backed store
 * (see src/lib/stores/solved.svelte.ts); omit it (or call with no
 * argument) to get 0 completed, e.g. for a server-rendered first paint
 * before the client-only store has hydrated. Intersected against real
 * slugs rather than just `solvedSlugs.size`, so a stale slug left over
 * from a since-renamed/removed question never inflates the count. */
export function getProgressStats(solvedSlugs: ReadonlySet<string> = new Set()): {
	completed: number;
	total: number;
} {
	const allSlugs = curriculum.flatMap((part) =>
		part.tracks.flatMap((track) => track.questions.map((q) => q.slug))
	);
	const completed = allSlugs.filter((slug) => solvedSlugs.has(slug)).length;
	return { completed, total: allSlugs.length };
}

/** How many *real* questions are attempted but not yet solved. Same
 * defensive intersection as getProgressStats: attempted.svelte.ts is
 * additive-only and never drops a slug, so a since-renamed or removed
 * question's slug can sit in that store indefinitely -- counting
 * `attemptedSlugs.size` directly (minus solved) would let a stale slug
 * inflate "in progress" even though no real question backs it, and the
 * Continue-where-you-left-off list (which looks each slug up via
 * findQuestionBySlug) would silently show fewer items than the count
 * implies. Intersecting against real slugs first keeps the two in sync. */
export function getInProgressCount(
	solvedSlugs: ReadonlySet<string>,
	attemptedSlugs: ReadonlySet<string>
): number {
	const allSlugs = curriculum.flatMap((part) =>
		part.tracks.flatMap((track) => track.questions.map((q) => q.slug))
	);
	return allSlugs.filter((slug) => attemptedSlugs.has(slug) && !solvedSlugs.has(slug)).length;
}

/** One row of curriculum-wide progress, one entry per Part, in curriculum
 * order. Used to render a real per-Part progress list (solved out of that
 * Part's own total) instead of a plain question-count-per-Part chart. */
export interface PartProgress {
	id: string;
	title: string;
	solved: number;
	total: number;
}

export function getPartProgress(solvedSlugs: ReadonlySet<string> = new Set()): PartProgress[] {
	return curriculum.map((part) => {
		const slugs = part.tracks.flatMap((track) => track.questions.map((q) => q.slug));
		return {
			id: part.id,
			title: part.title,
			solved: slugs.filter((slug) => solvedSlugs.has(slug)).length,
			total: slugs.length
		};
	});
}

/** Same idea, one row per Difficulty instead of per Part. */
export interface DifficultyProgress {
	difficulty: Difficulty;
	solved: number;
	total: number;
}

export function getDifficultyProgress(
	solvedSlugs: ReadonlySet<string> = new Set()
): DifficultyProgress[] {
	const allQuestions = curriculum.flatMap((part) => part.tracks.flatMap((t) => t.questions));
	const order: Difficulty[] = ['Easy', 'Medium', 'Hard'];
	return order.map((difficulty) => {
		const inThisDifficulty = allQuestions.filter((q) => q.difficulty === difficulty);
		return {
			difficulty,
			solved: inThisDifficulty.filter((q) => solvedSlugs.has(q.slug)).length,
			total: inThisDifficulty.length
		};
	});
}

/** A question plus which Part/Track it lives under, looked up by slug --
 * for anything that needs to show a real question's context (title,
 * difficulty, where it sits in the curriculum) given only a slug, e.g. a
 * "continue where you left off" list built from the attempted store. */
export interface QuestionWithLocation {
	question: Question;
	partTitle: string;
	trackName: string;
}

export function findQuestionBySlug(slug: string): QuestionWithLocation | undefined {
	for (const part of curriculum) {
		for (const track of part.tracks) {
			const question = track.questions.find((q) => q.slug === slug);
			if (question) return { question, partTitle: part.title, trackName: track.name };
		}
	}
	return undefined;
}
