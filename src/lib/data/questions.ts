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

function mkTrack(name: string, topics: string[], items: [string, Difficulty][]): Track {
	// Slugified from "track name + title", not title alone: several tracks
	// share generic titles like "Full training loop" or "Stack multiple
	// blocks", which collided into the same slug when only the title was
	// used (caught by questions.spec.ts's uniqueness check).
	return {
		name,
		questions: items.map(([title, difficulty]) => ({
			slug: slugify(`${name} ${title}`),
			title,
			difficulty,
			topics
		}))
	};
}

const part0: Part = {
	id: 'part-0',
	title: 'Classical ML',
	tracks: [
		mkTrack(
			'Linear Regression',
			['Regression', 'Optimization'],
			[
				['Hypothesis function (y = wx + b)', 'Easy'],
				['Mean Squared Error loss', 'Easy'],
				['Gradient of MSE w.r.t. w, b', 'Medium'],
				['One gradient-descent update step', 'Medium'],
				['Full training loop', 'Medium'],
				['Stretch: L2 regularization (Ridge)', 'Medium']
			]
		),
		mkTrack(
			'Classification (Logistic Regression)',
			['Classification', 'Optimization'],
			[
				['Sigmoid function', 'Easy'],
				['Binary Cross-Entropy loss', 'Easy'],
				['Gradient of BCE', 'Medium'],
				['Decision boundary / thresholding', 'Easy'],
				['Full training loop', 'Medium'],
				['Stretch: Softmax + Categorical Cross-Entropy (multi-class)', 'Medium'],
				['Linear Discriminant Analysis (LDA)', 'Medium'],
				['Stretch: class imbalance handling', 'Medium']
			]
		),
		mkTrack(
			'Regularized Linear Models',
			['Regression', 'Classic ML'],
			[
				['Linear Regression: closed form (Normal Equation)', 'Medium'],
				['Ridge Regression (L2)', 'Medium'],
				['Lasso Regression (L1), contrasted against Ridge', 'Medium']
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
				['Pruning (pre-pruning, post-pruning)', 'Medium']
			]
		),
		mkTrack(
			'Ensembles',
			['Classic ML'],
			[
				['Random Forest: majority vote aggregation', 'Medium'],
				['Stretch: bagging concept', 'Easy'],
				['Gradient Boosting: fit one tree to the negative gradient of the loss', 'Medium'],
				['Full boosting loop: assemble a minimal booster', 'Hard']
			]
		),
		mkTrack(
			'Instance-Based and Probabilistic',
			['Classic ML'],
			[
				['KNN: distance and neighbor lookup', 'Easy'],
				['Naive Bayes: Bernoulli log-likelihood', 'Medium'],
				['Stretch: Gaussian Naive Bayes', 'Medium']
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
				['Stretch: EM Algorithm', 'Hard']
			]
		),
		mkTrack(
			'Evaluation and Model Selection',
			['Metrics & Evaluation'],
			[
				['Train/test split, k-fold cross-validation, bootstrapping', 'Easy'],
				['Precision, Recall, F1, ROC, AUC', 'Medium'],
				['Bias-variance tradeoff', 'Medium']
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
				['Swish (SiLU) fwd/bwd', 'Medium']
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
				['Assemble minimal autograd engine', 'Hard']
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
				[
					'Stretch: optimizer survey (RMSprop, Adagrad, NAdam, RAdam, AdaDelta, Nesterov momentum)',
					'Medium'
				]
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
				['Minimal Module base class (parameter collection)', 'Medium']
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
				['Stretch: temperature + top-k sampling', 'Medium']
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
				['Average pooling, forward', 'Easy']
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
				["Residual/skip connection (reuses Part 2's residual concept)", 'Easy']
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
				['FLOPs estimation (Linear/Conv)', 'Medium']
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
			[
				['Vectorize a naive Python loop into NumPy ops, before/after speed comparison', 'Easy'],
				['Kernel fusion concept (simplified combined-op example)', 'Medium']
			]
		),
		mkTrack(
			'Memoization',
			['Transformers', 'MLOps'],
			[
				['KV-cache for autoregressive generation (reuses Part 2 directly)', 'Hard'],
				['Benchmark: with vs without cache', 'Medium']
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

export const curriculum: Part[] = [part0, part1, part2, part3, part4];

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
