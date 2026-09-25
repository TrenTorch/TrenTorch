export type Difficulty = 'Easy' | 'Medium' | 'Hard';

// Which real companies/roles this question's SUBJECT AREA is relevant to --
// topic-based relevance derived from public engineering blogs and
// aggregated interview-experience reports, not a claim that this exact
// question was asked verbatim at any of these companies. Attached per
// Part (see withCompanies below), since the source data ties one company
// list to a whole subject area, not to individual questions.
export interface CompanyTag {
	names: string[];
	roles: string;
}

export interface Question {
	slug: string;
	title: string;
	difficulty: Difficulty;
	topics: string[];
	companies?: CompanyTag;
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

// Stamps the same CompanyTag onto every question in every track of a Part
// -- the source data (trentorch_questions_company_tags.csv) ties one
// company list to a whole subject-area Part, not to individual questions,
// so this is applied once per Part rather than threaded through every
// mkTrack call.
function withCompanies(part: Part, companies: CompanyTag): Part {
	return {
		...part,
		tracks: part.tracks.map((track) => ({
			...track,
			questions: track.questions.map((question) => ({ ...question, companies }))
		}))
	};
}

const partPython: Part = {
	id: 'part-python',
	title: 'Python',
	tracks: [
		mkTrack(
			'Core Semantics',
			['Python Core Semantics'],
			[
				['What a Variable Is', 'Easy', 'python-what-a-variable-is'],
				['What a Function Is', 'Easy', 'python-what-a-function-is'],
				['What an Object Is', 'Easy', 'python-what-an-object-is'],
				['What a Variable Really Is (Pointer Model)', 'Easy', 'python-variable-pointer-model'],
				['Assignment', 'Easy', 'python-assignment'],
				['The id() Function', 'Easy', 'python-id-function'],
				['Reassignment vs Mutation', 'Medium', 'python-reassignment-vs-mutation'],
				['Identity (is) vs Equality (==)', 'Easy', 'python-identity-vs-equality'],
				['Mutable vs Immutable Types', 'Medium', 'python-mutable-vs-immutable-types'],
				['Function Arguments (Pointer Model)', 'Medium', 'python-function-arguments-pointer-model'],
				['The Mutable Default Argument Issue', 'Medium', 'python-mutable-default-argument'],
				['if / elif / else', 'Easy', 'python-if-elif-else'],
				['Truthy and Falsy Values', 'Easy', 'python-truthy-falsy'],
				['while Loops, break, continue, and Loop else', 'Medium', 'python-while-loops'],
				['for Loops', 'Medium', 'python-for-loops'],
				['Assemble: Full Variable/Mutation Trace', 'Hard', 'python-core-semantics-assemble']
			]
		),
		mkTrack(
			'Strings',
			['Python Strings'],
			[
				['String Objects, Indexing, and Slicing', 'Easy', 'python-strings-indexing-slicing'],
				['Why Strings Are Immutable', 'Easy', 'python-strings-why-immutable'],
				['Concatenation and Its Cost', 'Medium', 'python-strings-concatenation-cost'],
				['Case Methods', 'Easy', 'python-strings-case-methods'],
				['Searching and Checking Content', 'Medium', 'python-strings-searching-checking'],
				['Trimming and Replacing', 'Medium', 'python-strings-trimming-replacing'],
				['Splitting and Joining', 'Medium', 'python-strings-splitting-joining'],
				['Formatting: %, .format(), and f-strings', 'Medium', 'python-strings-formatting'],
				['Membership, Comparison, and Ordering', 'Medium', 'python-strings-membership-comparison'],
				['Text vs Bytes', 'Medium', 'python-strings-text-vs-bytes'],
				[
					'Assemble: Build a Formatted Report From Raw Text',
					'Hard',
					'python-strings-assemble-sales-report'
				]
			]
		),
		mkTrack(
			'Lists',
			['Python Lists'],
			[
				[
					'List Objects, Indexing, Slicing, and Slice Assignment',
					'Easy',
					'python-lists-indexing-slicing-assignment'
				],
				['Adding Elements: append, extend, insert', 'Easy', 'python-lists-adding-elements'],
				['Removing Elements: remove, pop, del, clear', 'Medium', 'python-lists-removing-elements'],
				['Searching and Counting: index, count, in', 'Easy', 'python-lists-searching-counting'],
				['Ordering: sort, sorted, reverse, and sort keys', 'Medium', 'python-lists-ordering-sort'],
				['Copying: Shallow vs Deep', 'Medium', 'python-lists-copying-shallow-deep'],
				['List Comprehensions', 'Medium', 'python-lists-list-comprehensions'],
				['Nested Lists and Addresses Across Levels', 'Hard', 'python-lists-nested-lists-addresses'],
				[
					'Assemble: In-Place Inventory Cleanup With Snapshots',
					'Hard',
					'python-lists-assemble-inventory-cleanup'
				]
			]
		),
		mkTrack(
			'Tuples',
			['Python Tuples'],
			[
				['Tuple Objects and Why They Are Immutable', 'Easy', 'python-tuples-objects-immutable'],
				['Packing and Unpacking, Including *', 'Medium', 'python-tuples-packing-unpacking'],
				['Tuples vs Lists: When Immutability Decides', 'Medium', 'python-tuples-vs-lists'],
				['Tuples as Dictionary Keys', 'Medium', 'python-tuples-as-dict-keys'],
				['Assemble: Analyze a Route of Grid Points', 'Hard', 'python-tuples-assemble-analyze-route']
			]
		),
		mkTrack(
			'Dictionaries',
			['Python Dictionaries'],
			[
				[
					'Dictionary Objects and How Key Lookup Works',
					'Medium',
					'python-dicts-objects-key-lookup'
				],
				[
					'Creating, Reading, and Updating; get() and Defaults',
					'Easy',
					'python-dicts-creating-reading-updating'
				],
				['Removing Entries: pop, popitem, del, clear', 'Medium', 'python-dicts-removing-entries'],
				['Iterating: keys(), values(), items()', 'Medium', 'python-dicts-iterating-views'],
				['update() and setdefault()', 'Medium', 'python-dicts-update-setdefault'],
				['Dictionary Comprehensions', 'Medium', 'python-dicts-comprehensions'],
				['Nested Dictionaries', 'Hard', 'python-dicts-nested-dictionaries'],
				['Assemble: Summarize Customer Orders', 'Hard', 'python-dicts-assemble-summarize-orders']
			]
		),
		mkTrack(
			'Sets',
			['Python Sets'],
			[
				['Set Objects and How They Store Unique Elements', 'Easy', 'python-sets-objects-unique'],
				['Adding and Removing Elements', 'Easy', 'python-sets-adding-removing-elements'],
				[
					'Set Operations: Union, Intersection, Difference, and Symmetric Difference',
					'Medium',
					'python-sets-operations'
				],
				['Set Comprehensions', 'Medium', 'python-sets-comprehensions'],
				[
					'When a Set Solves a Problem a List Structurally Cannot',
					'Medium',
					'python-sets-use-cases'
				],
				[
					'Assemble: Analyze Unique Events Across Datasets',
					'Hard',
					'python-sets-assemble-analyze-events'
				]
			]
		),
		mkTrack(
			'Functions',
			['Python Functions'],
			[
				[
					'Defining and Calling Functions, and Return Values',
					'Easy',
					'python-functions-defining-calling'
				],
				['Positional vs Keyword Arguments', 'Easy', 'python-functions-positional-vs-keyword'],
				[
					'Default Arguments and When Values Are Bound',
					'Medium',
					'python-functions-default-arguments'
				],
				['*args and **kwargs', 'Medium', 'python-functions-args-kwargs'],
				['Scope: Local vs Global', 'Medium', 'python-functions-scope-local-global'],
				['Docstrings and Function Annotations', 'Easy', 'python-functions-docstrings-annotations'],
				[
					'Assemble: Build a Configurable Data-Processing Pipeline',
					'Hard',
					'python-functions-assemble-pipeline'
				]
			]
		),
		mkTrack(
			'Functions as Values',
			['Python Functions as Values'],
			[
				[
					'Functions Are Objects and Can Be Assigned to Variables',
					'Easy',
					'python-functions-as-values-objects'
				],
				[
					'Passing a Function as an Argument',
					'Medium',
					'python-functions-as-values-passing-as-arguments'
				],
				['Closures and Retained Enclosing Scope', 'Medium', 'python-functions-as-values-closures'],
				['lambda Expressions', 'Easy', 'python-functions-as-values-lambda'],
				['Intro to Decorators', 'Medium', 'python-functions-as-values-intro-decorators'],
				[
					'Assemble: Build a Configurable Function Pipeline',
					'Hard',
					'python-functions-as-values-assemble-pipeline'
				]
			]
		),
		mkTrack(
			'Iteration Internals',
			['Python Iteration Internals'],
			[
				['Iterables vs Iterators', 'Easy', 'python-iteration-iterables-vs-iterators'],
				['iter(), next(), and StopIteration', 'Medium', 'python-iteration-iter-next-stopiteration'],
				['Generators and yield', 'Medium', 'python-iteration-generators-yield'],
				['map() and filter()', 'Medium', 'python-iteration-map-filter'],
				[
					'Generator Expressions vs List Comprehensions',
					'Medium',
					'python-iteration-generator-expressions-vs-comprehensions'
				],
				[
					'Assemble: Build a Lazy Data-Processing Pipeline',
					'Hard',
					'python-iteration-assemble-lazy-pipeline'
				]
			]
		),
		mkTrack(
			'Object-Oriented Programming',
			['Python OOP'],
			[
				['Classes and Instances', 'Easy', 'python-oop-classes-and-instances'],
				['__init__ and Instance Attributes', 'Easy', 'python-oop-init-instance-attributes'],
				['Why Methods Take self', 'Medium', 'python-oop-why-methods-take-self'],
				[
					'Class Attributes vs Instance Attributes',
					'Medium',
					'python-oop-class-vs-instance-attributes'
				],
				['Special (Dunder) Methods', 'Medium', 'python-oop-special-dunder-methods'],
				['Inheritance and Method Overriding', 'Medium', 'python-oop-inheritance-overriding'],
				['Assemble: A Small Matrix Class Hierarchy', 'Hard', 'python-oop-assemble-matrix-hierarchy']
			]
		),
		mkTrack(
			'Errors and Control Flow',
			['Python Errors and Control Flow'],
			[
				[
					'Exceptions: What Raising Does to Program Flow',
					'Easy',
					'python-errors-exceptions-and-flow'
				],
				['try / except / else / finally', 'Medium', 'python-errors-try-except-else-finally'],
				['Raising Your Own Exceptions', 'Medium', 'python-errors-raising-custom-exceptions'],
				['with Blocks and Context Managers', 'Medium', 'python-errors-with-context-managers'],
				[
					'Assemble: Run Jobs With Retries and Guaranteed Logging',
					'Hard',
					'python-errors-assemble-job-runner'
				]
			]
		),
		mkTrack(
			'Bridging to NumPy/ML',
			['Python NumPy Bridge'],
			[
				[
					'Why Plain Python Loops Are Slow: Interpreter Mechanics',
					'Medium',
					'python-numpy-bridge-interpreter-mechanics'
				],
				['Views vs Copies', 'Medium', 'python-numpy-bridge-views-vs-copies'],
				['Duck Typing', 'Medium', 'python-numpy-bridge-duck-typing'],
				[
					'Comprehensions and Functional Thinking as Vectorized Thinking',
					'Medium',
					'python-numpy-bridge-comprehensions-as-vectorized-thinking'
				],
				[
					'Assemble: A Vector With Shared-Memory Views',
					'Hard',
					'python-numpy-bridge-assemble-vector-views'
				]
			]
		)
	]
};

const partNumpy: Part = {
	id: 'part-numpy',
	title: 'NumPy',
	tracks: [
		mkTrack(
			'Array Fundamentals',
			['NumPy Core'],
			[
				['What an ndarray Is', 'Easy', 'numpy-what-an-ndarray-is'],
				['Creating Arrays From Python Data', 'Easy', 'numpy-creating-arrays-from-python-data'],
				['Creating Arrays With Generators', 'Easy', 'numpy-creating-arrays-with-generators'],
				['arange and linspace', 'Easy', 'numpy-arange-and-linspace'],
				['dtype', 'Medium', 'numpy-dtype'],
				['shape, ndim, size', 'Easy', 'numpy-shape-ndim-size'],
				[
					'Assemble: Build and Describe an Array From a Spec',
					'Hard',
					'numpy-assemble-build-and-describe'
				]
			]
		),
		mkTrack(
			'Indexing & Slicing',
			['NumPy Core'],
			[
				['Basic Indexing (1D and Multi-Dimensional)', 'Easy', 'numpy-basic-indexing'],
				['Slicing and What It Returns', 'Medium', 'numpy-slicing-and-views'],
				['Boolean Masking', 'Medium', 'numpy-boolean-masking'],
				['Fancy Indexing', 'Medium', 'numpy-fancy-indexing'],
				['np.where', 'Medium', 'numpy-np-where'],
				[
					'Assemble: Extract and Modify a Data Selection',
					'Hard',
					'numpy-assemble-extract-and-modify'
				]
			]
		),
		mkTrack(
			'Views vs Copies',
			['NumPy Core'],
			[
				['What a View Actually Is', 'Easy', 'numpy-what-a-view-is'],
				['Which Operations Return a View vs a Copy', 'Medium', 'numpy-view-vs-copy-classification'],
				['.copy() — Forcing an Independent Copy', 'Easy', 'numpy-forcing-a-copy'],
				['Mutating Through a View', 'Medium', 'numpy-mutating-through-a-view'],
				['The .base Attribute', 'Medium', 'numpy-the-base-attribute'],
				[
					'Assemble: Trace Ownership Through a Multi-Step Pipeline',
					'Hard',
					'numpy-assemble-trace-ownership'
				]
			]
		),
		mkTrack(
			'Shape Manipulation',
			['NumPy Core'],
			[
				['reshape', 'Medium', 'numpy-reshape'],
				['flatten vs ravel', 'Medium', 'numpy-flatten-vs-ravel'],
				['transpose / .T', 'Medium', 'numpy-transpose'],
				['newaxis / expand_dims', 'Easy', 'numpy-newaxis-expand-dims'],
				['squeeze', 'Easy', 'numpy-squeeze'],
				[
					'Combining Arrays: concatenate, stack, hstack, vstack',
					'Medium',
					'numpy-combining-arrays'
				],
				['Splitting Arrays: split, hsplit, vsplit', 'Medium', 'numpy-splitting-arrays'],
				[
					'Assemble: Reshape a Raw Batch Into Model-Ready Form',
					'Hard',
					'numpy-assemble-prepare-batch'
				]
			]
		),
		mkTrack(
			'Broadcasting',
			['NumPy Core'],
			[
				['The Problem Broadcasting Solves', 'Easy', 'numpy-the-broadcasting-problem'],
				['The Broadcasting Rule, Precisely', 'Medium', 'numpy-the-broadcasting-rule'],
				['Compatible Shape Examples', 'Medium', 'numpy-compatible-shape-examples'],
				[
					'Incompatible Shapes and Reading the Error',
					'Medium',
					'numpy-incompatible-shapes-and-errors'
				],
				['Practical Broadcasting Patterns', 'Medium', 'numpy-practical-broadcasting-patterns'],
				[
					'Assemble: Normalize a Batch Using Broadcasting Only',
					'Hard',
					'numpy-assemble-normalize-a-batch'
				]
			]
		),
		mkTrack(
			'Vectorized Operations & ufuncs',
			['NumPy Core'],
			[
				['Element-Wise Arithmetic', 'Easy', 'numpy-elementwise-arithmetic'],
				['Universal Functions (ufuncs)', 'Easy', 'numpy-universal-functions'],
				[
					'Why Vectorized Operations Are Faster Than a Loop',
					'Medium',
					'numpy-vectorized-vs-loop-speed'
				],
				['Boolean Comparisons and Combining Conditions', 'Medium', 'numpy-boolean-comparisons'],
				['Aggregations', 'Medium', 'numpy-aggregations'],
				['The axis Parameter', 'Medium', 'numpy-the-axis-parameter'],
				[
					'Assemble: Analyze a Dataset Using Vectorized Operations Only',
					'Hard',
					'numpy-assemble-analyze-a-dataset'
				]
			]
		),
		mkTrack(
			'Linear Algebra Basics',
			['NumPy Core'],
			[
				['Matrix Multiplication with @ / matmul', 'Medium', 'numpy-matrix-multiplication'],
				['np.dot', 'Easy', 'numpy-np-dot'],
				['Transpose in a Linear-Algebra Context', 'Medium', 'numpy-transpose-in-linear-algebra'],
				['np.linalg.norm', 'Medium', 'numpy-vector-norms'],
				['np.linalg.inv and np.linalg.det', 'Medium', 'numpy-inverse-and-determinant'],
				['np.linalg.solve', 'Medium', 'numpy-solving-linear-systems'],
				[
					'Assemble: Solve a Small Linear System End to End',
					'Hard',
					'numpy-assemble-solve-a-linear-system'
				]
			]
		),
		mkTrack(
			'Random & Sampling',
			['NumPy Random'],
			[
				['The Modern Random API: default_rng', 'Easy', 'numpy-default-rng'],
				['Seeding and Reproducibility', 'Medium', 'numpy-seeding-and-reproducibility'],
				['Uniform and Integer Random Arrays', 'Easy', 'numpy-uniform-and-integer-arrays'],
				[
					'Normal-Distribution Samples and Weight Initialization',
					'Medium',
					'numpy-normal-distribution-and-weight-init'
				],
				[
					'Assemble: Reproducible Synthetic Dataset with Initialized Weights',
					'Hard',
					'numpy-assemble-reproducible-synthetic-dataset'
				]
			]
		),
		mkTrack(
			'Performance & Memory',
			['NumPy Memory'],
			[
				['Strides', 'Medium', 'numpy-strides'],
				['Contiguous vs Non-Contiguous Arrays', 'Medium', 'numpy-contiguous-vs-non-contiguous'],
				[
					'Silent Copies From Non-Contiguous Layouts',
					'Hard',
					'numpy-silent-copies-from-non-contiguous-layouts'
				],
				[
					'Measuring Vectorized vs Loop-Based Performance',
					'Medium',
					'numpy-measuring-vectorized-vs-loop-performance'
				],
				['Assemble: Memory-Layout Audit of an Array', 'Hard', 'numpy-assemble-memory-layout-audit']
			]
		),
		mkTrack(
			'Bridging to PyTorch/Tensors',
			['NumPy Tensors'],
			[
				[
					'From ndarray to Tensor: Shape, Dtype, and Device',
					'Easy',
					'numpy-tensor-shape-dtype-device'
				],
				[
					'Everything Carries Over: Views, Broadcasting, Vectorization',
					'Medium',
					'numpy-tensor-views-broadcasting-vectorization'
				],
				['Where Tensors Diverge: Gradient Tracking', 'Medium', 'numpy-gradient-tracking'],
				[
					'Assemble: A Mini Linear Layer and Attention Weights with Tensor-Style Metadata',
					'Hard',
					'numpy-assemble-linear-layer-and-attention'
				]
			]
		)
	]
};

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
				['Single-Channel, Single-Filter 2D Convolution', 'Medium', 'vision-conv-single-filter'],
				['Padding: Same vs. Valid', 'Easy', 'vision-conv-padding'],
				['Stride: Skipping Positions to Downsample', 'Easy', 'vision-conv-stride'],
				['Convolution over Multi-Channel Input', 'Medium', 'vision-conv-multi-channel'],
				['Multiple Output Filters', 'Medium', 'vision-conv-multi-filter'],
				[
					'Stretch: im2col — Turning Convolution into One Matrix Multiply',
					'Hard',
					'vision-conv-im2col'
				]
			]
		),
		mkTrack(
			'Pooling',
			['Computer Vision'],
			[
				['Max Pooling: Downsampling by Keeping the Strongest Response', 'Easy', 'vision-pool-max'],
				[
					'Average Pooling: Downsampling by Smoothing Instead of Selecting',
					'Easy',
					'vision-pool-average'
				],
				[
					'Adaptive Average Pooling: The Modern Flatten Replacement',
					'Medium',
					'vision-pool-adaptive-average'
				]
			]
		),
		mkTrack(
			'CNN Architecture',
			['Computer Vision', 'Neural Networks'],
			[
				['Flatten: Bridging Convolutional and Linear Layers', 'Easy', 'vision-cnn-flatten'],
				['One CNN Block: Convolution, Activation, Pooling', 'Medium', 'vision-cnn-one-block'],
				['Stacking Multiple CNN Blocks', 'Medium', 'vision-cnn-stack-blocks'],
				['Full CNN Classifier', 'Hard', 'vision-cnn-full-classifier']
			]
		),
		mkTrack(
			'Modern CNN Concepts',
			['Computer Vision', 'Neural Networks'],
			[
				['Batch Normalization', 'Medium', 'vision-modern-batchnorm'],
				['Residual (Skip) Connection', 'Medium', 'vision-modern-residual-block'],
				['1x1 Convolution (Bottleneck)', 'Medium', 'vision-modern-pointwise-conv'],
				['Transposed Convolution', 'Medium', 'vision-modern-transposed-conv'],
				['Depthwise-Separable Convolution', 'Hard', 'vision-modern-depthwise-separable']
			]
		),
		mkTrack(
			'CNN Architecture History',
			['Computer Vision'],
			[
				[
					'Note: AlexNet — Dropout, and What Actually Changed from LeNet',
					'Easy',
					'vision-history-alexnet-dropout'
				],
				['VGG: Stacking Small 3x3 Convolutions', 'Medium', 'vision-history-vgg-stack'],
				[
					"DenseNet: Concatenating Every Previous Layer's Output",
					'Medium',
					'vision-history-densenet-block'
				],
				[
					'Note: EfficientNet — Compound Scaling',
					'Easy',
					'vision-history-efficientnet-compound-scaling'
				],
				['Dilated Convolution', 'Medium', 'vision-history-dilated-conv'],
				[
					'Note: Feature Pyramids — Combining Multiple Resolutions',
					'Easy',
					'vision-history-feature-pyramid-merge'
				]
			]
		),
		mkTrack(
			'Vision Transformer',
			['Computer Vision', 'Transformers'],
			[
				['Patchify an Image into Fixed-Size Patches', 'Medium', 'vision-vit-patchify'],
				['Patch Embedding', 'Easy', 'vision-vit-patch-embedding'],
				['Class Token + Position Embedding', 'Medium', 'vision-vit-cls-position-embedding'],
				['Feed Through the Transformer Block, Unmodified', 'Medium', 'vision-vit-encoder-block'],
				['Classification Head', 'Easy', 'vision-vit-classification-head'],
				['Stretch: InfoNCE Loss (CLIP-Style Contrastive Training)', 'Hard', 'vision-vit-info-nce'],
				[
					'Stretch: Triplet Loss (Metric/Representation Learning)',
					'Medium',
					'vision-vit-triplet-loss'
				]
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
				['Timing Decorator', 'Easy', 'systems-perf-timing-decorator'],
				['Parameter Counting', 'Easy', 'systems-perf-parameter-counting'],
				['Memory Footprint Estimation', 'Medium', 'systems-perf-memory-footprint-estimation'],
				['FLOPs Estimation (Linear/Conv)', 'Medium', 'systems-perf-flops-estimation'],
				[
					'Checkpointing: Save/Load Parameters to Disk, Resume Training',
					'Easy',
					'systems-perf-checkpointing'
				]
			]
		),
		mkTrack(
			'Quantization',
			['MLOps', 'Neural Networks'],
			[
				['Float32 to Int8 Mapping (Quantize)', 'Medium', 'systems-perf-quantize-float32-to-int8'],
				[
					'Int8 to Float32 Reconstruction (Dequantize)',
					'Medium',
					'systems-perf-dequantize-int8-to-float32'
				],
				[
					'Quantize a Full Weight Matrix, Measure Size/Accuracy Tradeoff',
					'Hard',
					'systems-perf-quantize-weight-matrix-tradeoff'
				]
			]
		),
		mkTrack(
			'Mixed Precision Training',
			['MLOps', 'Neural Networks'],
			[
				[
					'FP16/BF16 Representable Range vs FP32, Why Naive FP16 Training Underflows',
					'Medium',
					'systems-perf-fp16-bf16-representable-range'
				],
				[
					'Loss Scaling: Scale the Loss Before Backward, Unscale Gradients Before the Step',
					'Medium',
					'systems-perf-loss-scaling'
				],
				[
					'Autocast Concept: Which Ops Run in Reduced Precision, Which Stay in FP32',
					'Easy',
					'systems-perf-autocast-concept'
				]
			]
		),
		mkTrack(
			'Compression',
			['MLOps', 'Neural Networks'],
			[
				['Magnitude-Based Pruning, Single Step', 'Medium', 'systems-perf-magnitude-pruning'],
				['Stretch: Iterative Pruning Schedule', 'Hard', 'systems-perf-iterative-pruning-schedule'],
				[
					'Stretch: Basic Knowledge Distillation (Reuses KL Divergence)',
					'Hard',
					'systems-perf-knowledge-distillation'
				]
			]
		),
		mkTrack(
			'Acceleration',
			['MLOps'],
			[
				[
					'Vectorize a Naive Python Loop into NumPy Ops, Before/After Speed Comparison',
					'Easy',
					'systems-perf-vectorize-naive-loop'
				]
			]
		),
		mkTrack(
			'Kernels',
			['MLOps'],
			[
				[
					'Kernel Fusion: Fuse Two Elementwise Ops into One Pass, Measure the Win',
					'Medium',
					'systems-perf-kernel-fusion'
				],
				[
					'Memory-Bound vs Compute-Bound: The Roofline Model, Why Fusion Helps One but Not the Other',
					'Medium',
					'systems-perf-roofline-model'
				],
				[
					'Note: Real Kernels Are Written in CUDA/Triton, Not NumPy, What Changes and Why',
					'Easy',
					'systems-perf-real-kernels-cuda-triton'
				],
				[
					'Note: torch.compile / Graph Compilation, Why a JIT-Compiled Graph Beats Eager Mode',
					'Medium',
					'systems-perf-torch-compile-graph-compilation'
				],
				[
					'Note: TorchScript and ONNX Export, Why Production Serving Does Not Run Eager Python',
					'Easy',
					'systems-perf-torchscript-onnx-export'
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
				[
					'KV-cache for autoregressive generation (reuses Part 2 directly)',
					'Hard',
					'systems-distributed-kv-cache-autoregressive-generation'
				],
				[
					'Benchmark: with vs without cache',
					'Medium',
					'systems-distributed-benchmark-with-vs-without-cache'
				],
				[
					'Gradient checkpointing: recompute activations in backward instead of storing them',
					'Hard',
					'systems-distributed-gradient-checkpointing'
				]
			]
		),
		mkTrack(
			'Parallelism (concept only)',
			['MLOps'],
			[
				[
					'Data parallelism: a toy example splitting a batch across simulated workers, then averaging gradients',
					'Medium',
					'systems-distributed-data-parallelism-gradient-averaging'
				],
				[
					'Note: model/pipeline parallelism (why frontier training needs it, not implemented)',
					'Easy',
					'systems-distributed-pipeline-parallelism-bubble-fraction'
				],
				[
					'Note: torch.nn.DataParallel vs DistributedDataParallel, what the real APIs do differently',
					'Easy',
					'systems-distributed-dataparallel-vs-distributeddataparallel'
				],
				[
					'All-reduce, all-gather and reduce-scatter: the collectives distributed training is built from',
					'Medium',
					'systems-distributed-collective-communication-primitives'
				],
				[
					'Note: FSDP / ZeRO, sharding optimizer state and parameters across GPUs',
					'Medium',
					'systems-distributed-zero-optimizer-state-sharding'
				],
				[
					"Note: tensor parallelism, splitting one layer's matmul across GPUs",
					'Medium',
					'systems-distributed-tensor-parallel-matmul'
				],
				[
					'Note: sequence/context parallelism, splitting one long sequence across GPUs',
					'Medium',
					'systems-distributed-ring-attention-online-softmax'
				]
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
				[
					'Supervised fine-tuning: next-token loss, but only on the response tokens',
					'Medium',
					'rl-alignment-supervised-fine-tuning-response-loss-mask'
				],
				[
					'Instruction datasets: prompt/response pairs vs. raw next-token pretraining',
					'Easy',
					'rl-alignment-instruction-vs-pretraining-datasets'
				],
				[
					'Preference datasets: chosen vs. rejected response pairs',
					'Easy',
					'rl-alignment-preference-datasets-chosen-rejected'
				],
				[
					'Reward modeling: training a model to score a response instead of generate one',
					'Hard',
					'rl-alignment-reward-modeling-bradley-terry'
				],
				[
					'Note: RLHF, the full pretrain to SFT to reward model to PPO pipeline',
					'Easy',
					'rl-alignment-rlhf-pipeline-memory-cost'
				],
				[
					'Note: PPO, clipped policy updates for stable RL fine-tuning',
					'Medium',
					'rl-alignment-ppo-clipped-surrogate-objective'
				],
				[
					'DPO: optimizing the preference directly, no separate reward model or RL loop',
					'Hard',
					'rl-alignment-dpo-direct-preference-optimization'
				],
				[
					'Note: GRPO, group-relative advantage without a value network',
					'Medium',
					'rl-alignment-grpo-group-relative-advantage'
				],
				[
					'Rejection sampling: keep only the best of several sampled responses',
					'Easy',
					'rl-alignment-rejection-sampling-finetuning'
				],
				[
					"Best-of-N: sampling N responses and picking the reward model's favorite",
					'Easy',
					'rl-alignment-best-of-n-sampling'
				],
				[
					'Note: Constitutional AI, model-written critiques instead of human labels',
					'Easy',
					'rl-alignment-constitutional-ai-critique-revise'
				],
				[
					'Reward hacking: when optimizing the reward stops meaning what you wanted',
					'Medium',
					'rl-alignment-reward-hacking-goodharts-law'
				],
				[
					'Note: alignment tax, the capability cost of aligning a model',
					'Easy',
					'rl-alignment-alignment-tax'
				],
				[
					'QLoRA: LoRA on top of a quantized base model',
					'Hard',
					'rl-alignment-qlora-quantized-lora'
				],
				[
					'Note: adapter methods, prefix tuning and prompt tuning, other parameter-efficient approaches',
					'Easy',
					'rl-alignment-adapter-methods-prefix-prompt-tuning'
				]
			]
		),
		mkTrack(
			'Fine-tuning',
			['Reinforcement Learning', 'Neural Networks'],
			[
				[
					"LoRA: low-rank adapter matrices bolted onto Part 1's Linear layer",
					'Hard',
					'rl-alignment-lora-low-rank-adapters'
				],
				[
					'Compare: full fine-tune vs. LoRA, on parameter count and memory',
					'Medium',
					'rl-alignment-full-finetune-vs-lora-comparison'
				],
				[
					'KL Divergence (distillation, and the RLHF KL penalty term)',
					'Medium',
					'rl-alignment-kl-divergence-distillation-rlhf-penalty'
				],
				['Policy Gradient Loss', 'Medium', 'rl-alignment-policy-gradient-loss'],
				[
					'Generalized Advantage Estimation (pairs with Policy Gradient)',
					'Hard',
					'rl-alignment-generalized-advantage-estimation'
				]
			]
		),
		mkTrack(
			'Benchmarking and Capstone',
			['MLOps', 'Metrics & Evaluation'],
			[
				[
					'Build a benchmark harness (reuses Profiling)',
					'Medium',
					'rl-alignment-benchmark-harness'
				],
				[
					'Apply one optimization, measure real improvement',
					'Medium',
					'rl-alignment-apply-optimization-measure-improvement'
				],
				['Final capstone: submission/report', 'Hard', 'rl-alignment-capstone-report']
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
				[
					'Experiment tracking: logging hyperparameters, metrics and artifacts per run',
					'Easy',
					'production-ml-experiment-tracking'
				],
				[
					'Dataset versioning: why "the same CSV" is not reproducible without a hash',
					'Medium',
					'production-ml-dataset-versioning-hashing'
				],
				[
					'Model versioning and a model registry: promoting a run to a named, deployable version',
					'Easy',
					'production-ml-model-registry-versioning'
				],
				[
					'Reproducibility: pinning every source of randomness in a training run',
					'Medium',
					'production-ml-reproducibility-seeding'
				]
			]
		),
		mkTrack(
			'Deployment & Serving',
			['MLOps'],
			[
				[
					'Online vs. batch inference: request-by-request vs. scheduled bulk scoring',
					'Easy',
					'production-ml-online-vs-batch-inference'
				],
				[
					'Training pipelines: turning a notebook into a reproducible, scheduled DAG',
					'Medium',
					'production-ml-training-pipelines-dag'
				],
				[
					'Note: CI/CD for ML, testing a model like you would test code before it ships',
					'Easy',
					'production-ml-ci-cd-for-ml'
				],
				[
					'Canary deployment: rolling a new model out to a small slice of traffic first',
					'Medium',
					'production-ml-canary-deployment'
				],
				[
					'Shadow deployment: running a new model silently alongside the live one',
					'Medium',
					'production-ml-shadow-deployment'
				],
				[
					'A/B testing a model change, and rolling back when it loses',
					'Medium',
					'production-ml-ab-testing-rollback'
				]
			]
		),
		mkTrack(
			'Monitoring & Drift',
			['MLOps'],
			[
				[
					'Data drift: the input distribution shifting after deployment',
					'Medium',
					'production-ml-data-drift-psi'
				],
				[
					'Concept drift: the relationship between inputs and the target shifting',
					'Medium',
					'production-ml-concept-drift-sliding-window'
				],
				[
					'Model degradation over time, and deciding when to retrain',
					'Medium',
					'production-ml-model-degradation-retrain-trigger'
				],
				[
					'Retraining strategies: scheduled, triggered, and online learning',
					'Medium',
					'production-ml-retraining-strategies'
				]
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

// Source: trentorch_questions_company_tags.csv. Ten of the Parts above
// (not Math, Sequence Modeling, or RL & Alignment -- the CSV doesn't cover
// those) each get exactly one CompanyTag applied to every one of their
// questions via withCompanies below. "Classical ML" in the CSV maps only
// to partClassicalUnsupervised, not partClassicalLinear/partClassicalTrees
// -- confirmed by matching every CSV row's URL slug against this file's
// question slugs (231/231 matched, counts equal per Part).
const COMPANY_TAGS = {
	dlCore: {
		names: ['NVIDIA', 'Meta', 'Google DeepMind', 'OpenAI', 'Anthropic'],
		roles: 'core ML/AI Research & Framework Engineer interviews'
	},
	dlTraining: {
		names: ['NVIDIA', 'Google DeepMind', 'Meta', 'OpenAI', 'Anthropic', 'Snapchat'],
		roles: 'Deep Learning Engineer interviews'
	},
	dataFoundations: {
		names: ['Airbnb', 'Netflix', 'Spotify', 'Uber', 'PayPal', 'Zomato', 'Swiggy', 'OYO'],
		roles: 'Data Scientist / Analytics Engineer interviews (experimentation-heavy orgs)'
	},
	classicalUnsupervised: {
		names: ['Netflix', 'Spotify', 'Zomato', 'Swiggy', 'OYO', 'Airbnb', 'PayPal'],
		roles: 'ML Engineer / Data Scientist interviews (recommendation, ranking, fraud & risk)'
	},
	transformersLlm: {
		names: ['OpenAI', 'Anthropic', 'Google DeepMind', 'Meta', 'NVIDIA', 'Snapchat'],
		roles: 'LLM / Applied AI Engineer interviews'
	},
	productionMl: {
		names: ['Netflix', 'Airbnb', 'Spotify', 'Uber', 'Zomato', 'Swiggy', 'OYO', 'PayPal'],
		roles: 'ML Platform / MLOps Engineer interviews'
	},
	inference: {
		names: ['NVIDIA', 'OpenAI', 'Anthropic', 'Google', 'Meta', 'Snapchat', 'Netflix', 'Spotify'],
		roles: 'ML Systems / Inference Engineer interviews'
	},
	systemsPerf: {
		names: [
			'Tesla',
			'BMW',
			'SpaceX',
			'Rivian',
			'NVIDIA',
			'Qualcomm',
			'ARM',
			'Texas Instruments',
			'Jane Street',
			'Two Sigma',
			'Citadel',
			'D.E. Shaw',
			'Goldman Sachs',
			'JPMorgan',
			'Morgan Stanley'
		],
		roles: 'Performance/ML Systems & Embedded ML Engineer interviews'
	},
	vision: {
		names: [
			'Tesla',
			'BMW',
			'Rivian',
			'SpaceX',
			'Blue Origin',
			'NVIDIA',
			'Meta',
			'Google',
			'Qualcomm'
		],
		roles: 'Computer Vision / Perception Engineer interviews'
	},
	systemsDistributed: {
		names: [
			'NVIDIA',
			'Google',
			'Meta',
			'OpenAI',
			'Anthropic',
			'Tesla',
			'SpaceX',
			'Goldman Sachs',
			'JPMorgan',
			'Two Sigma',
			'Citadel'
		],
		roles: 'Distributed Training / ML Infrastructure Engineer interviews'
	}
} as const satisfies Record<string, CompanyTag>;

// Agentic Systems and Orchestration: four tracks, one per PR (#302, #304, #305, #307).
const partAgenticSystemsAndOrchestration: Part = {
	id: 'part-agentic-systems-and-orchestration',
	title: 'Agentic Systems and Orchestration',
	tracks: [
		mkTrack(
			'The Agent Loop',
			['Agents', 'Agent Loop'],
			[
				[
					'A Minimal ReAct Loop: Thought -> Action -> Observation',
					'Easy',
					'agentic-loop-minimal-react'
				],
				[
					'Stop an Agent Loop With a Step and Time Budget',
					'Easy',
					'agentic-loop-stop-step-time-budget'
				],
				[
					'Decompose a Goal Into an Ordered Sub-Task List',
					'Medium',
					'agentic-loop-decompose-goal-subtasks'
				],
				[
					'Self-Reflection: Critique the Last Step Before Continuing',
					'Medium',
					'agentic-loop-self-reflection-abandon'
				],
				[
					'Detect a Repeating Action and Break the Loop',
					'Medium',
					'agentic-loop-detect-repeating-action'
				]
			]
		),
		mkTrack(
			'Multi-Agent Orchestration',
			['Agents', 'Multi-Agent'],
			[
				[
					'Message-Passing Between Two Agents Over Shared State',
					'Easy',
					'agentic-orchestration-message-passing-shared-state'
				],
				[
					'A Handoff Mechanism: Route to the Right Agent',
					'Easy',
					'agentic-orchestration-handoff-route'
				]
			]
		),
		mkTrack(
			'Agent State and Durable Execution',
			['Agents', 'Agent State'],
			[
				['Idempotent Tool Execution Across Retries', 'Easy', 'agentic-state-idempotent-execution'],
				['Pause an Agent Run and Resume It Later', 'Medium', 'agentic-state-pause-resume-run'],
				[
					'Recover an Interrupted Agent From Its Last Checkpoint',
					'Medium',
					'agentic-state-recover-from-checkpoint'
				]
			]
		),
		mkTrack(
			'Agent Learning and Experience',
			['Agents', 'Agent Learning'],
			[
				[
					'Store Successful and Failed Agent Trajectories',
					'Easy',
					'agentic-learning-store-trajectories'
				],
				[
					'Retrieve Past Trajectories for a Similar Task',
					'Easy',
					'agentic-learning-retrieve-similar-trajectories'
				],
				[
					'Experience-Based Planning From Past Runs',
					'Easy',
					'agentic-learning-experience-based-planning'
				],
				[
					'Extract Reusable Lessons From a Failed Run',
					'Easy',
					'agentic-learning-extract-lesson-from-failure'
				],
				[
					'Compare an Agent With and Without Experience',
					'Medium',
					'agentic-learning-compare-with-without-experience'
				]
			]
		)
	]
};

// Reliability, Safety and Evaluation: three tracks, one per PR (#308, #309, #310).
const partReliabilitySafetyAndEvaluation: Part = {
	id: 'part-reliability-safety-and-evaluation',
	title: 'Reliability, Safety and Evaluation',
	tracks: [
		mkTrack(
			'Guardrails, Retry and Evaluation',
			['Agents', 'Guardrails'],
			[
				[
					'Enforce a Valid Output Format With Retry',
					'Easy',
					'agentic-guardrails-enforce-format-retry'
				],
				[
					'Detect a Hallucinated Claim Against Retrieved Context',
					'Medium',
					'agentic-guardrails-detect-hallucination'
				],
				['An LLM-as-Judge Scoring Harness', 'Medium', 'agentic-guardrails-llm-judge-harness']
			]
		),
		mkTrack(
			'Agent Security',
			['Agents', 'Agent Security'],
			[
				[
					"Sanitize a Tool's Output Before It Reaches the Model",
					'Easy',
					'agentic-security-sanitize-tool-output'
				],
				['Build an Audit Log of Agent Actions', 'Easy', 'agentic-security-audit-log']
			]
		),
		mkTrack(
			'Agent Observability',
			['Agents', 'Agent Observability'],
			[
				['Build a Trace of an Agent Run', 'Easy', 'agentic-observability-build-trace'],
				[
					'Compute the Total Cost of an Agent Run',
					'Easy',
					'agentic-observability-compute-run-cost'
				],
				[
					"Break Down a Run's Latency by Component",
					'Easy',
					'agentic-observability-latency-breakdown'
				],
				['Classify Failures Into Categories', 'Easy', 'agentic-observability-classify-failures'],
				[
					"Replay a Run's Steps Up to the First Failure",
					'Easy',
					'agentic-observability-replay-until-failure'
				]
			]
		)
	]
};

// Production and Advanced AI Systems: four tracks, one per PR (#312 to #315).
const partProductionAndAdvancedAiSystems: Part = {
	id: 'part-production-and-advanced-ai-systems',
	title: 'Production and Advanced AI Systems',
	tracks: [
		mkTrack(
			'Streaming and Real-Time Agents',
			['Agents', 'Streaming'],
			[
				[
					'Assemble a Streamed Response Into Display Snapshots',
					'Easy',
					'production-streaming-assemble-stream'
				],
				[
					'Detect a Tool Call Marker as It Streams In',
					'Easy',
					'production-streaming-detect-early-tool-call'
				],
				['Find Where a Stream Was Cancelled', 'Easy', 'production-streaming-find-cancel-point'],
				[
					'Handle User Input While an Agent Is Mid-Task',
					'Medium',
					'production-streaming-handle-interrupt-input'
				],
				[
					'Process an Event Queue That Arrives Out of Order',
					'Medium',
					'production-streaming-process-event-queue'
				]
			]
		),
		mkTrack(
			'Inference Optimization for Applications',
			['Systems & Performance', 'Inference'],
			[
				[
					'Simulate an LRU-Evicted Prefix Cache',
					'Medium',
					'production-inference-simulate-prefix-cache-lru'
				],
				[
					'Dynamic Windowed Batching of Inference Requests',
					'Medium',
					'production-inference-dynamic-windowed-batching'
				],
				[
					'Simulate Speculative Decoding',
					'Medium',
					'production-inference-simulate-speculative-decoding'
				],
				[
					'Compare Individual vs. Batched Processing Cost',
					'Easy',
					'production-inference-compare-batching-strategies'
				],
				[
					'Pick the Best Model That Fits a Latency Budget',
					'Easy',
					'production-inference-pick-model-under-budget'
				]
			]
		),
		mkTrack(
			'Multimodal Applications',
			['Agents', 'Multimodal'],
			[
				[
					'Unified Retrieval Across Text and Image-Caption Chunks',
					'Easy',
					'production-multimodal-unified-retrieval'
				],
				[
					'Chunk Multimodal Content Without Splitting Atomic Blocks',
					'Medium',
					'production-multimodal-atomic-chunking'
				],
				[
					'Route a Question to the Right Modality',
					'Easy',
					'production-multimodal-route-modality-for-question'
				],
				[
					'Extract a Parsed Table Into Structured Records',
					'Easy',
					'production-multimodal-table-to-dict'
				]
			]
		),
		mkTrack(
			'Synthetic Data and Self-Improvement',
			['Agents', 'Synthetic Data'],
			[
				[
					'Generate Synthetic Examples From Templates',
					'Easy',
					'production-synthetic-data-templated-pair-generation'
				],
				[
					'Filter Low-Quality Synthetic Examples',
					'Easy',
					'production-synthetic-data-quality-filter'
				],
				[
					'Simulate an Alternating Self-Play Transcript',
					'Easy',
					'production-synthetic-data-alternating-self-play'
				],
				[
					'Generate Single-Perturbation Adversarial Variants',
					'Easy',
					'production-synthetic-data-adversarial-variants'
				],
				[
					'Turn Eval Failures Into New Training Examples',
					'Easy',
					'production-synthetic-data-eval-failures-to-training-set'
				]
			]
		)
	]
};

export const curriculum: Part[] = [
	partPython,
	partNumpy,
	partMath,
	withCompanies(partDataFoundations, COMPANY_TAGS.dataFoundations),
	partClassicalLinear,
	partClassicalTrees,
	withCompanies(partClassicalUnsupervised, COMPANY_TAGS.classicalUnsupervised),
	withCompanies(partDlCore, COMPANY_TAGS.dlCore),
	withCompanies(partDlTraining, COMPANY_TAGS.dlTraining),
	partSeqModeling,
	withCompanies(partTransformersLlm, COMPANY_TAGS.transformersLlm),
	withCompanies(partVision, COMPANY_TAGS.vision),
	withCompanies(partSystemsPerf, COMPANY_TAGS.systemsPerf),
	withCompanies(partSystemsDistributed, COMPANY_TAGS.systemsDistributed),
	partRlAlignment,
	withCompanies(partProductionMl, COMPANY_TAGS.productionMl),
	withCompanies(partInference, COMPANY_TAGS.inference),
	partAgenticSystemsAndOrchestration,
	partReliabilitySafetyAndEvaluation,
	partProductionAndAdvancedAiSystems
];

/** `total` is always derived from the real curriculum data, never drifts
 * out of sync as questions get added. `completed` counts real solved
 * progress -- pass `solved.slugs` from the localStorage-backed store
 * (see processes/progress-tracking/solved.svelte.ts); omit it (or call with no
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
