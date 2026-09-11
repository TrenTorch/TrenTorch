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
				['Vectors, matrices and tensors: shapes and basic operations', 'Easy'],
				['Dot product and vector norms (L1, L2, L-infinity)', 'Easy'],
				['Matrix multiplication from first principles', 'Medium'],
				['Transpose, and its role in reshaping without copying data', 'Easy'],
				['Matrix inverse, and when it does not exist', 'Medium'],
				['Eigenvalues and eigenvectors of a small matrix', 'Hard'],
				['Singular Value Decomposition (SVD)', 'Hard'],
				['Positive-definite matrices, and why they matter for optimization', 'Medium']
			]
		),
		mkTrack(
			'Calculus',
			['Calculus'],
			[
				['Derivatives from first principles: the limit definition, computed numerically', 'Easy'],
				['Partial derivatives of a multivariate function', 'Easy'],
				["Chain rule: composing two functions' derivatives by hand", 'Medium'],
				['Jacobian: the matrix of all partial derivatives of a vector-valued function', 'Hard'],
				['Hessian: second-order partial derivatives, and what its eigenvalues tell you', 'Hard'],
				['Directional derivatives, and the gradient as steepest ascent', 'Medium']
			]
		),
		mkTrack(
			'Probability',
			['Probability & Statistics'],
			[
				['Sampling from a random variable and estimating its distribution', 'Easy'],
				['Expectation and variance from a sample', 'Easy'],
				['Covariance and correlation between two variables', 'Medium'],
				['Conditional probability from a joint distribution', 'Medium'],
				["Bayes' theorem: updating a belief given evidence", 'Medium'],
				['Likelihood vs. probability: the same formula, two different questions', 'Medium'],
				['Maximum likelihood estimation for a simple distribution', 'Hard'],
				['MAP estimation: maximum likelihood plus a prior', 'Hard']
			]
		),
		mkTrack(
			'Information Theory',
			['Information Theory'],
			[
				['Entropy of a discrete distribution', 'Easy'],
				["Cross-entropy, and why it's the loss Classification already uses", 'Medium'],
				['KL divergence between two distributions', 'Medium'],
				['Mutual information between two variables', 'Hard']
			]
		)
	]
};

const part0: Part = {
	id: 'part-0',
	title: 'Classical ML',
	tracks: [
		mkTrack(
			'Data Preprocessing',
			['Data Processing'],
			[
				['Detecting and counting missing values in a dataset', 'Easy'],
				['Imputing missing numeric values with a column mean/median', 'Easy'],
				['One-hot encoding a categorical column', 'Medium'],
				['Feature scaling: standardization vs min-max normalization', 'Medium']
			]
		),
		mkTrack(
			'Exploratory Data Analysis',
			['Data Processing'],
			[
				['Detecting outliers with IQR and z-score', 'Easy'],
				["Summarizing a feature's distribution: mean, median, skew", 'Easy'],
				['Correlation matrix, and why correlation is not causation', 'Medium'],
				['Data leakage: a feature that accidentally encodes the label', 'Hard'],
				["Feature engineering: deriving a feature that makes the model's job easier", 'Medium'],
				['Stratified sampling for an imbalanced dataset', 'Medium']
			]
		),
		mkTrack(
			'Statistical Inference',
			['Probability & Statistics'],
			[
				['Confidence interval for a sample mean', 'Medium'],
				['Bootstrap confidence intervals', 'Medium'],
				['Hypothesis testing: a two-sample t-test from scratch', 'Hard'],
				['A/B testing: is the difference between two groups real or noise', 'Medium'],
				['Statistical significance and p-values, and what they do not mean', 'Easy']
			]
		),
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
				['Stretch: L1 Loss (MAE), contrasted against MSE', 'Easy'],
				['Stretch: Huber Loss, quadratic near zero and linear far from it', 'Medium'],
				['Generalization: train/val split and the generalization gap', 'Medium']
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
				['LogSoftmax + NLLLoss: the two pieces CrossEntropyLoss actually fuses', 'Medium'],
				['Production Engineering: detecting train/serve distribution shift', 'Hard'],
				['Multiclass via One-vs-Rest, contrasted against Softmax', 'Medium']
			]
		),
		mkTrack(
			'Regularized Linear Models',
			['Regression', 'Classic ML'],
			[
				['Linear Regression: closed form (Normal Equation)', 'Medium'],
				['Ridge Regression (L2)', 'Medium'],
				['Lasso Regression (L1), contrasted against Ridge', 'Medium'],
				['Elastic Net: combining L1 and L2 penalties', 'Medium'],
				['Polynomial features: expanding inputs before a linear model', 'Medium'],
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
				['Hinge loss', 'Easy'],
				['Margin maximization intuition', 'Easy'],
				['Linear SVM via gradient descent on hinge loss', 'Medium'],
				['Stretch: kernel trick (conceptual)', 'Hard']
			]
		),
		mkTrack(
			'Decision Trees',
			['Classic ML'],
			[
				['Gini Impurity for a split', 'Easy'],
				['Information Gain for a split', 'Easy'],
				['Decision Tree best split (assemble a minimal tree)', 'Hard'],
				['Pruning (pre-pruning, post-pruning)', 'Medium'],
				['Regression trees: splitting on variance reduction instead of Gini', 'Medium'],
				['Feature importance from a fitted tree', 'Medium']
			]
		),
		mkTrack(
			'Ensembles',
			['Classic ML'],
			[
				['Random Forest: majority vote aggregation', 'Medium'],
				['Stretch: bagging concept', 'Easy'],
				['Gradient Boosting: fit one tree to the negative gradient of the loss', 'Medium'],
				['Full boosting loop: assemble a minimal booster', 'Hard'],
				['Random Forest regression, and out-of-bag error estimation', 'Medium'],
				['AdaBoost: reweighting misclassified samples each round', 'Medium'],
				['Stretch: regularized boosting (shrinkage + L2 leaf penalty, XGBoost-style)', 'Hard'],
				[
					'Note: histogram-based boosting (LightGBM-style binning), why it is faster at scale',
					'Easy'
				]
			]
		),
		mkTrack(
			'Instance-Based and Probabilistic',
			['Classic ML'],
			[
				['KNN: distance and neighbor lookup', 'Easy'],
				['Naive Bayes: Bernoulli log-likelihood', 'Medium'],
				['Stretch: Gaussian Naive Bayes', 'Medium'],
				['Nearest centroid classifier', 'Easy'],
				[
					'Note: Gaussian Processes, a distribution over functions instead of over parameters',
					'Medium'
				]
			]
		),
		mkTrack(
			'Unsupervised',
			['Classic ML'],
			[
				['K-Means: assignment step', 'Easy'],
				['K-Means: centroid update', 'Easy'],
				['PCA: projection', 'Medium'],
				['Gaussian Mixture Clustering', 'Hard'],
				['Stretch: EM Algorithm', 'Hard'],
				['Isolation Forest: anomaly detection via random splits', 'Medium'],
				['DBSCAN: density-based clustering', 'Medium'],
				['Hierarchical clustering: agglomerative merge order', 'Medium'],
				['Note: t-SNE and UMAP, nonlinear dimensionality reduction for visualization', 'Easy']
			]
		),
		mkTrack(
			'Evaluation and Model Selection',
			['Metrics & Evaluation'],
			[
				['Train/test split, k-fold cross-validation, bootstrapping', 'Easy'],
				['Precision, Recall, F1, ROC, AUC', 'Medium'],
				['Bias-variance tradeoff', 'Medium'],
				['Grid search over a hyperparameter grid', 'Easy'],
				['Random search, contrasted against grid search', 'Medium'],
				['Note: Bayesian optimization for hyperparameter search', 'Medium'],
				['Early stopping: halting training at the best validation checkpoint', 'Medium'],
				['Learning curves: training/validation error vs. dataset size', 'Medium'],
				['Validation curves: training/validation error vs. one hyperparameter', 'Medium'],
				['Calibration: does a predicted probability of 0.8 mean 80% of the time', 'Hard'],
				['Threshold optimization for imbalanced classification', 'Medium'],
				['Nested cross-validation, and why plain CV leaks hyperparameter choices', 'Hard'],
				['Model selection under class imbalance', 'Medium']
			]
		),
		mkTrack(
			'Tabular Foundation Models',
			['Transformers', 'Classic ML'],
			[
				['Row-wise attention over table cells', 'Hard'],
				['Column-wise attention over table cells', 'Hard'],
				['Combine into a TabPFN-style two-way attention block', 'Hard'],
				['In-context prediction: single forward pass, no per-dataset training loop', 'Medium'],
				['Contrast note: why no positional encoding here, unlike Part 2', 'Easy']
			]
		)
	]
};

const part1: Part = {
	id: 'part-1',
	title: 'Deep Learning Foundations',
	tracks: [
		mkTrack(
			'Tensors',
			['Linear Algebra'],
			[
				['Tensor creation / dtype', 'Easy'],
				['Elementwise ops', 'Easy'],
				['Broadcasting rules', 'Medium'],
				['Matmul', 'Medium'],
				['Reshape / transpose', 'Easy'],
				['Reduction ops (sum, mean, max)', 'Easy'],
				['Indexing / slicing', 'Easy']
			]
		),
		mkTrack(
			'Activations (fwd + bwd each)',
			['Activation Functions', 'Neural Networks'],
			[
				['ReLU fwd/bwd', 'Easy'],
				['Sigmoid fwd/bwd', 'Easy'],
				['Tanh fwd/bwd', 'Easy'],
				['Softmax fwd/bwd', 'Medium'],
				['GELU fwd/bwd', 'Medium'],
				['Swish (SiLU) fwd/bwd', 'Medium'],
				['LeakyReLU fwd/bwd', 'Easy'],
				['Mish fwd/bwd', 'Medium']
			]
		),
		mkTrack(
			'Loss Functions',
			['Loss Functions'],
			[
				['MSE', 'Easy'],
				['Cross-Entropy', 'Medium'],
				['Binary Cross-Entropy', 'Medium']
			]
		),
		mkTrack(
			'Autograd (micrograd-style progressive build)',
			['Neural Networks'],
			[
				['Backward for addition', 'Easy'],
				['Backward for multiplication', 'Easy'],
				['Backward for matmul', 'Medium'],
				['Graph node (value + grad + backward fn)', 'Medium'],
				['Topological sort for backward pass', 'Hard'],
				['Assemble minimal autograd engine', 'Hard'],
				[
					'Numerical gradient checking: verify an analytical gradient via finite differences',
					'Medium'
				]
			]
		),
		mkTrack(
			'Optimizers',
			['Optimization'],
			[
				['SGD', 'Easy'],
				['SGD + Momentum', 'Medium'],
				['Adam: bias-corrected moment estimates', 'Medium'],
				['Adam: full update rule', 'Medium'],
				['AdamW: decoupled weight decay', 'Medium'],
				['Muon', 'Hard'],
				['Gradient clipping (global norm)', 'Easy'],
				['Learning rate scheduling: warmup and cosine decay', 'Medium'],
				['OneCycleLR schedule, contrasted against warmup + cosine decay', 'Medium'],
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
				['Linear fwd', 'Easy'],
				['Linear bwd', 'Medium'],
				['Dropout fwd/bwd', 'Easy'],
				['Weight initialization: Xavier/Glorot, He/Kaiming', 'Medium'],
				['Minimal Module base class (parameter collection)', 'Medium'],
				['Sequential container: stack layers, one forward pass through all of them', 'Easy'],
				['LazyLinear: infer in_features from the first real forward call', 'Medium']
			]
		),
		mkTrack(
			'Training Loop',
			['Neural Networks', 'Data Processing'],
			[
				['Dataset/DataLoader abstraction (indexing, batching, shuffling)', 'Medium'],
				['Assemble full loop (data, forward, loss, backward, optimizer step)', 'Medium'],
				['Train/eval mode switching', 'Easy'],
				['Basic metric tracking (loss curve)', 'Easy']
			]
		),
		mkTrack(
			'Regularization',
			['Neural Networks'],
			[
				['Early stopping: monitor validation loss, restore the best checkpoint', 'Medium'],
				['Data augmentation: label-preserving input transformations', 'Easy'],
				['Label smoothing: softening one-hot targets before cross-entropy', 'Medium']
			]
		),
		mkTrack(
			'Why Deep Networks Work',
			['Neural Networks'],
			[
				[
					'Universal approximation: why one wide hidden layer can fit any function, in principle',
					'Medium'
				],
				[
					'Representation learning: why depth learns hierarchical features, not one big lookup',
					'Easy'
				],
				[
					'Vanishing and exploding gradients: why a deep, badly-initialized net fails to train',
					'Hard'
				],
				['Internal covariate shift, and what BatchNorm was actually designed to fix', 'Medium'],
				[
					'Overparameterization and double descent: more parameters than data can still generalize',
					'Hard'
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

const part2: Part = {
	id: 'part-2',
	title: 'Language Modeling',
	tracks: [
		mkTrack(
			'Tokenization',
			['NLP'],
			[
				['Whitespace/character tokenizer', 'Easy'],
				['Vocabulary building + unknown-token handling', 'Easy'],
				['BPE: single merge step', 'Medium'],
				['Stretch: BPE, full training loop', 'Hard'],
				['Encode/decode round-trip', 'Easy']
			]
		),
		mkTrack(
			'Embeddings',
			['NLP', 'Transformers'],
			[
				['Token embedding lookup', 'Easy'],
				['Embedding backward (scatter-add gradient)', 'Medium'],
				['Sinusoidal positional encoding', 'Medium'],
				['Learned positional embedding', 'Easy'],
				['Combine token and positional embeddings', 'Easy'],
				['RoPE (Rotary Position Embeddings)', 'Hard']
			]
		),
		mkTrack(
			'Recurrent Neural Networks',
			['NLP', 'Neural Networks'],
			[
				['Vanilla RNN cell, forward', 'Easy'],
				['Vanilla RNN cell, backward', 'Medium'],
				['Backprop through time (BPTT): vanishing and exploding gradient intuition', 'Hard'],
				['LSTM cell, forward (gating mechanism)', 'Medium'],
				['GRU cell, forward (simplified gating)', 'Medium'],
				['Stretch: bidirectional RNN', 'Medium'],
				[
					'Sequence-to-sequence / encoder-decoder: the bottleneck problem attention was invented to solve',
					'Medium'
				]
			]
		),
		mkTrack(
			'Attention',
			['Transformers'],
			[
				['Scaled dot-product attention, forward', 'Medium'],
				['Causal mask', 'Easy'],
				['Softmax (reuses Part 1, the first cross-part reuse)', 'Easy'],
				['Multi-Head Attention: splitting into heads, per-head attention', 'Medium'],
				['Multi-Head Attention: concatenating heads plus output projection', 'Medium'],
				['Stretch: Grouped-Query Attention (GQA)', 'Hard']
			]
		),
		mkTrack(
			'Transformer Block',
			['Transformers'],
			[
				['Layer Normalization, forward', 'Medium'],
				['Stretch: RMSNorm (alternative to LayerNorm)', 'Easy'],
				['Residual/skip connection', 'Easy'],
				['Feed-forward sublayer (reuses Part 1 Linear + activation)', 'Easy'],
				['Stretch: SwiGLU-gated FFN', 'Medium'],
				['Assemble one full block (attention, norm, residual, FFN, norm, residual)', 'Hard'],
				['Stack multiple blocks', 'Medium']
			]
		),
		mkTrack(
			'Modern Transformer Architecture',
			['Transformers'],
			[
				['Encoder vs. decoder vs. encoder-decoder: three ways to arrange the same block', 'Easy'],
				['Pre-norm vs. post-norm: where LayerNorm sits, and why it changes trainability', 'Medium'],
				["Attention's quadratic complexity, and why context length is expensive", 'Medium'],
				[
					'Note: FlashAttention, the same math computed without materializing the full attention matrix',
					'Medium'
				],
				['Sliding-window / local attention: bounding context to a fixed window', 'Medium'],
				[
					'ALiBi: a positional bias baked into attention scores instead of the embeddings',
					'Medium'
				],
				['Note: attention sinks, why the first few tokens matter disproportionately', 'Easy'],
				['RoPE scaling: extending a model past its trained context length', 'Hard'],
				['Untied embeddings, contrasted against weight tying', 'Easy'],
				['Logit scaling before the final softmax', 'Easy']
			]
		),
		mkTrack(
			'Language Model Assembly',
			['Transformers', 'NLP'],
			[
				['Output projection to vocab logits', 'Easy'],
				['Weight tying (share input/output embedding matrix)', 'Medium'],
				['Next-token Cross-Entropy loss (reuses Part 1 loss)', 'Medium'],
				['Full forward pass (tokens to embeddings to blocks to logits)', 'Hard'],
				['Training loop for next-token prediction (reuses Part 1 loop)', 'Hard'],
				['Perplexity (exp of loss), the standard LM evaluation metric', 'Easy'],
				['Greedy decoding / generation', 'Medium'],
				['Stretch: temperature + top-k sampling', 'Medium'],
				['Beam search decoding, contrasted against greedy', 'Hard']
			]
		),
		mkTrack(
			'LLM Engineering',
			['Transformers', 'NLP'],
			[
				['Mixture of Experts: top-k gating, route each token to its best expert FFN', 'Hard'],
				[
					'Speculative decoding: draft-and-verify loop, accept/reject against a larger model',
					'Hard'
				],
				[
					'Capstone: wire tokenization, embeddings, attention and the training loop into one tiny end-to-end LLM',
					'Hard'
				],
				['Deduplication: removing near-identical documents before training', 'Medium'],
				['Data filtering and contamination: keeping eval data out of the training set', 'Medium'],
				['Sequence packing: concatenating short examples to fill a fixed context window', 'Medium'],
				['Gradient accumulation: simulating a larger batch size than memory allows', 'Medium'],
				['Resume-from-checkpoint: restoring optimizer state, not just weights', 'Medium'],
				['Reading a loss curve: spotting training instability before it diverges', 'Medium'],
				['Compute-optimal training: Chinchilla-style scaling laws', 'Hard']
			]
		)
	]
};

const part3: Part = {
	id: 'part-3',
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

const part4: Part = {
	id: 'part-4',
	title: 'Systems / Optimization',
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
		),
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
		),
		mkTrack(
			'Reinforcement Learning',
			['Reinforcement Learning'],
			[
				['Value iteration on a small Markov Decision Process', 'Medium'],
				['Tabular Q-learning', 'Medium']
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

const part5: Part = {
	id: 'part-5',
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

export const curriculum: Part[] = [partMath, part0, part1, part2, part3, part4, part5];

/** Placeholder until real progress persistence exists (localStorage or a
 * backend, once the schema work happens). Completed is hardcoded to 0 for
 * now, total is derived from the real data so it never drifts out of sync
 * as questions get added. */
export function getProgressStats(): { completed: number; total: number } {
	const total = curriculum.flatMap((part) =>
		part.tracks.flatMap((track) => track.questions)
	).length;
	return { completed: 0, total };
}
