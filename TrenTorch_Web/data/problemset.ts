export type ProblemsetDifficulty = 'Easy' | 'Medium' | 'Hard';
export type ProblemsetKind = 'direct' | 'case-study';

export interface ProblemsetProblem {
	slug: string;
	title: string;
	difficulty: ProblemsetDifficulty;
	kind: ProblemsetKind;
	moduleId: string;
	topic: string;
	caseCompany: string | null;
}

export interface ProblemsetModule {
	id: string;
	title: string;
	description: string;
	learningPartId: string;
}

export const problemsetModules: ProblemsetModule[] = [
	{
		id: 'maths-stats-for-ml',
		title: 'Maths & Statistics for ML',
		description: 'Linear algebra, calculus, probability, and information theory',
		learningPartId: 'part-math'
	},
	{
		id: 'data-stats-for-ds',
		title: 'Data & Stats for Data Science',
		description: 'Data analysis, inference, and experiment design',
		learningPartId: 'part-data-foundations'
	},
	{
		id: 'classical-ml',
		title: 'Classical ML',
		description: 'Core supervised learning algorithms and evaluation',
		learningPartId: 'part-classical-linear'
	},
	{
		id: 'classical-ml-trees-ensembles',
		title: 'Classical ML: Trees & Ensembles',
		description: 'Decision trees, bagging, and boosting',
		learningPartId: 'part-classical-trees'
	},
	{
		id: 'unsupervised-ml',
		title: 'Unsupervised ML',
		description: 'Clustering, dimensionality reduction, and anomaly detection',
		learningPartId: 'part-classical-unsupervised'
	},
	{
		id: 'dl-core',
		title: 'DL Core',
		description: 'Neural network components and architecture fundamentals',
		learningPartId: 'part-dl-core'
	},
	{
		id: 'dl-training-theory',
		title: 'DL Training & Theory',
		description: 'Optimization, generalization, and training dynamics',
		learningPartId: 'part-dl-training'
	},
	{
		id: 'sequence-models-attention',
		title: 'Sequence Models & Attention',
		description: 'Sequence modeling, attention, and decoding',
		learningPartId: 'part-seq-modeling'
	},
	{
		id: 'transformer-llm',
		title: 'Transformer & LLM',
		description: 'Transformer architecture, language modeling, and prompting',
		learningPartId: 'part-transformers-llm'
	}
];

export const problemsetProblems: ProblemsetProblem[] = [
	{
		slug: 'problem-1-compute-a-stable-l2-norm',
		title: 'Compute a Stable L2 Norm',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: null
	},
	{
		slug: 'problem-2-normalize-a-vector',
		title: 'Normalize a Vector',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: null
	},
	{
		slug: 'problem-3-cosine-similarity',
		title: 'Cosine Similarity',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: 'Google'
	},
	{
		slug: 'problem-4-matrix-vector-product',
		title: 'Matrix-Vector Product',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: null
	},
	{
		slug: 'problem-5-matrix-transpose',
		title: 'Matrix Transpose',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: null
	},
	{
		slug: 'problem-6-frobenius-norm',
		title: 'Frobenius Norm',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: 'Amazon'
	},
	{
		slug: 'problem-7-gram-matrix',
		title: 'Gram Matrix',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: null
	},
	{
		slug: 'problem-8-solve-a-2-2-linear-system',
		title: 'Solve a 2×2 Linear System',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'linear-algebra',
		caseCompany: null
	},
	{
		slug: 'problem-9-power-iteration',
		title: 'Power Iteration',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'eigenvalues',
		caseCompany: 'Zomato'
	},
	{
		slug: 'problem-10-low-rank-reconstruction',
		title: 'Low-Rank Reconstruction',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'svd',
		caseCompany: 'Stripe'
	},
	{
		slug: 'problem-11-finite-difference-derivative',
		title: 'Finite Difference Derivative',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'calculus',
		caseCompany: 'Airbnb'
	},
	{
		slug: 'problem-12-gradient-of-a-quadratic',
		title: 'Gradient of a Quadratic',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'calculus',
		caseCompany: 'Meta'
	},
	{
		slug: 'problem-13-jacobian-by-finite-differences',
		title: 'Jacobian by Finite Differences',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'calculus',
		caseCompany: 'Apple'
	},
	{
		slug: 'problem-14-hessian-diagonal',
		title: 'Hessian Diagonal',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'calculus',
		caseCompany: 'OpenAI'
	},
	{
		slug: 'problem-15-directional-derivative',
		title: 'Directional Derivative',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'calculus',
		caseCompany: 'Datadog'
	},
	{
		slug: 'problem-16-monte-carlo-expectation',
		title: 'Monte Carlo Expectation',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'probability',
		caseCompany: 'Snowflake'
	},
	{
		slug: 'problem-17-bernoulli-mean-and-variance',
		title: 'Bernoulli Mean and Variance',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'probability',
		caseCompany: 'DoorDash'
	},
	{
		slug: 'problem-18-conditional-probability-table',
		title: 'Conditional Probability Table',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'probability',
		caseCompany: 'Flipkart'
	},
	{
		slug: 'problem-19-bayes-posterior',
		title: 'Bayes Posterior',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'bayesian-inference',
		caseCompany: 'Swiggy'
	},
	{
		slug: 'problem-20-mle-of-gaussian-mean',
		title: 'MLE of Gaussian Mean',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'estimation',
		caseCompany: null
	},
	{
		slug: 'problem-21-map-bernoulli-estimate',
		title: 'MAP Bernoulli Estimate',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'maths-stats-for-ml',
		topic: 'bayesian-inference',
		caseCompany: 'Atlassian'
	},
	{
		slug: 'problem-22-entropy-of-a-distribution',
		title: 'Entropy of a Distribution',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'maths-stats-for-ml',
		topic: 'information-theory',
		caseCompany: null
	},
	{
		slug: 'problem-23-mean-imputation',
		title: 'Mean Imputation',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'data-cleaning',
		caseCompany: null
	},
	{
		slug: 'problem-24-median-imputation',
		title: 'Median Imputation',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'data-cleaning',
		caseCompany: 'TikTok'
	},
	{
		slug: 'problem-25-one-hot-encode-categories',
		title: 'One-Hot Encode Categories',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'data-cleaning',
		caseCompany: null
	},
	{
		slug: 'problem-26-min-max-scaling',
		title: 'Min-Max Scaling',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'data-cleaning',
		caseCompany: null
	},
	{
		slug: 'problem-27-z-score-scaling',
		title: 'Z-Score Scaling',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'data-cleaning',
		caseCompany: 'Salesforce'
	},
	{
		slug: 'problem-28-robust-scaling',
		title: 'Robust Scaling',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'data-cleaning',
		caseCompany: null
	},
	{
		slug: 'problem-29-iqr-outlier-flagging',
		title: 'IQR Outlier Flagging',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'eda',
		caseCompany: 'Pinterest'
	},
	{
		slug: 'problem-30-correlation-matrix',
		title: 'Correlation Matrix',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'eda',
		caseCompany: 'Dropbox'
	},
	{
		slug: 'problem-31-stratified-split',
		title: 'Stratified Split',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'sampling',
		caseCompany: 'Lyft'
	},
	{
		slug: 'problem-32-bootstrap-mean',
		title: 'Bootstrap Mean',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'sampling',
		caseCompany: 'Instacart'
	},
	{
		slug: 'problem-33-two-sample-difference-in-means',
		title: 'Two-Sample Difference in Means',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'hypothesis-testing',
		caseCompany: 'Walmart'
	},
	{
		slug: 'problem-34-welch-t-statistic',
		title: 'Welch t Statistic',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'hypothesis-testing',
		caseCompany: 'PayPal'
	},
	{
		slug: 'problem-35-confidence-interval-for-mean',
		title: 'Confidence Interval for Mean',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'confidence-intervals',
		caseCompany: 'JPMorgan Chase'
	},
	{
		slug: 'problem-36-a-b-conversion-rate',
		title: 'A/B Conversion Rate',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'ab-testing',
		caseCompany: 'Goldman Sachs'
	},
	{
		slug: 'problem-37-pooled-proportion-test-statistic',
		title: 'Pooled Proportion Test Statistic',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'ab-testing',
		caseCompany: 'Coinbase'
	},
	{
		slug: 'problem-38-sample-size-for-proportion',
		title: 'Sample Size for Proportion',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'experiment-design',
		caseCompany: 'Palantir'
	},
	{
		slug: 'problem-39-leakage-detector',
		title: 'Leakage Detector',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'data-leakage',
		caseCompany: 'Tesla'
	},
	{
		slug: 'problem-40-group-aggregation',
		title: 'Group Aggregation',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'data-wrangling',
		caseCompany: null
	},
	{
		slug: 'problem-41-winsorize-values',
		title: 'Winsorize Values',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'eda',
		caseCompany: null
	},
	{
		slug: 'problem-42-time-series-lag-feature',
		title: 'Time-Series Lag Feature',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'data-stats-for-ds',
		topic: 'time-series',
		caseCompany: 'Meesho'
	},
	{
		slug: 'problem-43-rolling-mean',
		title: 'Rolling Mean',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'time-series',
		caseCompany: null
	},
	{
		slug: 'problem-44-inferential-regression-slope',
		title: 'Inferential Regression Slope',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'data-stats-for-ds',
		topic: 'regression-for-inference',
		caseCompany: null
	},
	{
		slug: 'problem-45-linear-regression-prediction',
		title: 'Linear Regression Prediction',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'linear-regression',
		caseCompany: 'Myntra'
	},
	{
		slug: 'problem-46-linear-regression-normal-equation',
		title: 'Linear Regression Normal Equation',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'linear-regression',
		caseCompany: null
	},
	{
		slug: 'problem-47-mean-squared-error',
		title: 'Mean Squared Error',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'metrics',
		caseCompany: null
	},
	{
		slug: 'problem-48-mean-absolute-error',
		title: 'Mean Absolute Error',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'metrics',
		caseCompany: 'Reddit'
	},
	{
		slug: 'problem-49-logistic-sigmoid',
		title: 'Logistic Sigmoid',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'logistic-regression',
		caseCompany: 'Discord'
	},
	{
		slug: 'problem-50-binary-cross-entropy',
		title: 'Binary Cross-Entropy',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'logistic-regression',
		caseCompany: 'Zoom'
	},
	{
		slug: 'problem-51-logistic-gradient',
		title: 'Logistic Gradient',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'logistic-regression',
		caseCompany: 'Cloudflare'
	},
	{
		slug: 'problem-52-ridge-objective',
		title: 'Ridge Objective',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'regularization',
		caseCompany: 'Twilio'
	},
	{
		slug: 'problem-53-lasso-soft-threshold',
		title: 'Lasso Soft Threshold',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'regularization',
		caseCompany: 'MongoDB'
	},
	{
		slug: 'problem-54-elastic-net-penalty',
		title: 'Elastic-Net Penalty',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'regularization',
		caseCompany: 'Databricks'
	},
	{
		slug: 'problem-55-linear-svm-hinge-loss',
		title: 'Linear SVM Hinge Loss',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'svm',
		caseCompany: 'Oracle'
	},
	{
		slug: 'problem-56-svm-subgradient-step',
		title: 'SVM Subgradient Step',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'svm',
		caseCompany: 'Intel'
	},
	{
		slug: 'problem-57-knn-classification',
		title: 'KNN Classification',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'knn',
		caseCompany: 'Netflix'
	},
	{
		slug: 'problem-58-knn-regression',
		title: 'KNN Regression',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'knn',
		caseCompany: 'Uber'
	},
	{
		slug: 'problem-59-precision-recall',
		title: 'Precision Recall',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'metrics',
		caseCompany: 'Google'
	},
	{
		slug: 'problem-60-f1-score',
		title: 'F1 Score',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'metrics',
		caseCompany: 'Microsoft'
	},
	{
		slug: 'problem-61-confusion-matrix',
		title: 'Confusion Matrix',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'metrics',
		caseCompany: null
	},
	{
		slug: 'problem-62-roc-curve-points',
		title: 'ROC Curve Points',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'metrics',
		caseCompany: null
	},
	{
		slug: 'problem-63-k-fold-indices',
		title: 'K-Fold Indices',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'cross-validation',
		caseCompany: 'Spotify'
	},
	{
		slug: 'problem-64-stratified-k-fold',
		title: 'Stratified K-Fold',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'cross-validation',
		caseCompany: null
	},
	{
		slug: 'problem-65-bias-variance-decomposition',
		title: 'Bias-Variance Decomposition',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'bias-variance',
		caseCompany: null
	},
	{
		slug: 'problem-66-polynomial-features',
		title: 'Polynomial Features',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml',
		topic: 'feature-engineering',
		caseCompany: 'Stripe'
	},
	{
		slug: 'problem-67-standardize-then-train',
		title: 'Standardize Then Train',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'feature-engineering',
		caseCompany: null
	},
	{
		slug: 'problem-68-calibration-bins',
		title: 'Calibration Bins',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'classical-ml',
		topic: 'model-evaluation',
		caseCompany: null
	},
	{
		slug: 'problem-69-gini-impurity',
		title: 'Gini Impurity',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'decision-trees',
		caseCompany: 'Apple'
	},
	{
		slug: 'problem-70-entropy-impurity',
		title: 'Entropy Impurity',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'decision-trees',
		caseCompany: 'OpenAI'
	},
	{
		slug: 'problem-71-best-binary-split',
		title: 'Best Binary Split',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'decision-trees',
		caseCompany: 'Datadog'
	},
	{
		slug: 'problem-72-decision-stump',
		title: 'Decision Stump',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'decision-trees',
		caseCompany: 'Snowflake'
	},
	{
		slug: 'problem-73-tree-leaf-majority',
		title: 'Tree Leaf Majority',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'decision-trees',
		caseCompany: 'DoorDash'
	},
	{
		slug: 'problem-74-bootstrap-sample',
		title: 'Bootstrap Sample',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'bagging',
		caseCompany: 'Flipkart'
	},
	{
		slug: 'problem-75-random-feature-subset',
		title: 'Random Feature Subset',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'random-forest',
		caseCompany: 'Swiggy'
	},
	{
		slug: 'problem-76-random-forest-vote',
		title: 'Random Forest Vote',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'random-forest',
		caseCompany: 'Razorpay'
	},
	{
		slug: 'problem-77-bagging-regression-mean',
		title: 'Bagging Regression Mean',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'bagging',
		caseCompany: 'Atlassian'
	},
	{
		slug: 'problem-78-adaboost-weight-update',
		title: 'AdaBoost Weight Update',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'boosting',
		caseCompany: 'LinkedIn'
	},
	{
		slug: 'problem-79-adaboost-alpha',
		title: 'AdaBoost Alpha',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'boosting',
		caseCompany: 'ByteDance'
	},
	{
		slug: 'problem-80-gradient-boosting-residual',
		title: 'Gradient Boosting Residual',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'gradient-boosting',
		caseCompany: null
	},
	{
		slug: 'problem-81-gradient-boosting-update',
		title: 'Gradient Boosting Update',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'gradient-boosting',
		caseCompany: 'NVIDIA'
	},
	{
		slug: 'problem-82-xgboost-style-leaf-weight',
		title: 'XGBoost-Style Leaf Weight',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'regularized-boosting',
		caseCompany: null
	},
	{
		slug: 'problem-83-xgboost-split-gain',
		title: 'XGBoost Split Gain',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'regularized-boosting',
		caseCompany: null
	},
	{
		slug: 'problem-84-feature-importance-from-splits',
		title: 'Feature Importance from Splits',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'feature-importance',
		caseCompany: 'Shopify'
	},
	{
		slug: 'problem-85-out-of-bag-mask',
		title: 'Out-of-Bag Mask',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'out-of-bag',
		caseCompany: null
	},
	{
		slug: 'problem-86-oob-accuracy',
		title: 'OOB Accuracy',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'out-of-bag',
		caseCompany: null
	},
	{
		slug: 'problem-87-stacked-predictions',
		title: 'Stacked Predictions',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'stacking',
		caseCompany: 'Lyft'
	},
	{
		slug: 'problem-88-blended-prediction',
		title: 'Blended Prediction',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'classical-ml-trees-ensembles',
		topic: 'blending',
		caseCompany: null
	},
	{
		slug: 'problem-89-k-means-assignment',
		title: 'K-Means Assignment',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'k-means-clustering',
		caseCompany: 'Walmart'
	},
	{
		slug: 'problem-90-k-means-centroid-update',
		title: 'K-Means Centroid Update',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'k-means-clustering',
		caseCompany: 'PayPal'
	},
	{
		slug: 'problem-91-k-means-one-iteration',
		title: 'K-Means One Iteration',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'k-means-clustering',
		caseCompany: 'JPMorgan Chase'
	},
	{
		slug: 'problem-92-k-means-inertia',
		title: 'K-Means Inertia',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'clustering-evaluation',
		caseCompany: 'Goldman Sachs'
	},
	{
		slug: 'problem-93-hierarchical-single-link-distance',
		title: 'Hierarchical Single-Link Distance',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'hierarchical-clustering',
		caseCompany: 'Coinbase'
	},
	{
		slug: 'problem-94-complete-link-distance',
		title: 'Complete-Link Distance',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'hierarchical-clustering',
		caseCompany: 'Palantir'
	},
	{
		slug: 'problem-95-dbscan-core-point',
		title: 'DBSCAN Core Point',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'dbscan',
		caseCompany: 'Tesla'
	},
	{
		slug: 'problem-96-dbscan-region-query',
		title: 'DBSCAN Region Query',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'dbscan',
		caseCompany: 'Waymo'
	},
	{
		slug: 'problem-97-gaussian-log-likelihood',
		title: 'Gaussian Log Likelihood',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'gaussian-mixture',
		caseCompany: 'Grab'
	},
	{
		slug: 'problem-98-gmm-responsibility',
		title: 'GMM Responsibility',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'gaussian-mixture',
		caseCompany: 'Meesho'
	},
	{
		slug: 'problem-99-pca-centering',
		title: 'PCA Centering',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'pca',
		caseCompany: 'Ola'
	},
	{
		slug: 'problem-100-pca-covariance',
		title: 'PCA Covariance',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'unsupervised-ml',
		topic: 'pca',
		caseCompany: null
	},
	{
		slug: 'problem-101-pca-projection',
		title: 'PCA Projection',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'unsupervised-ml',
		topic: 'pca',
		caseCompany: null
	},
	{
		slug: 'problem-102-pca-reconstruction',
		title: 'PCA Reconstruction',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'pca',
		caseCompany: 'CRED'
	},
	{
		slug: 'problem-103-explained-variance-ratio',
		title: 'Explained Variance Ratio',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'unsupervised-ml',
		topic: 'pca',
		caseCompany: null
	},
	{
		slug: 'problem-104-silhouette-score-one-point',
		title: 'Silhouette Score One Point',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'unsupervised-ml',
		topic: 'clustering-metrics',
		caseCompany: null
	},
	{
		slug: 'problem-105-apriori-candidate-join',
		title: 'Apriori Candidate Join',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'association-rules',
		caseCompany: 'Discord'
	},
	{
		slug: 'problem-106-support-counting',
		title: 'Support Counting',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'unsupervised-ml',
		topic: 'association-rules',
		caseCompany: null
	},
	{
		slug: 'problem-107-anomaly-z-score',
		title: 'Anomaly Z-Score',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'unsupervised-ml',
		topic: 'anomaly-detection',
		caseCompany: null
	},
	{
		slug: 'problem-108-isolation-path-length',
		title: 'Isolation Path Length',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'unsupervised-ml',
		topic: 'anomaly-detection',
		caseCompany: 'Twilio'
	},
	{
		slug: 'problem-109-relu-activation',
		title: 'ReLU Activation',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'activation-functions',
		caseCompany: 'MongoDB'
	},
	{
		slug: 'problem-110-relu-backward',
		title: 'ReLU Backward',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'activation-functions',
		caseCompany: 'Databricks'
	},
	{
		slug: 'problem-111-sigmoid-activation',
		title: 'Sigmoid Activation',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'activation-functions',
		caseCompany: 'Oracle'
	},
	{
		slug: 'problem-112-tanh-activation',
		title: 'Tanh Activation',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'activation-functions',
		caseCompany: 'Intel'
	},
	{
		slug: 'problem-113-softmax-vector',
		title: 'Softmax Vector',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'activation-functions',
		caseCompany: 'Netflix'
	},
	{
		slug: 'problem-114-cross-entropy-from-logits',
		title: 'Cross-Entropy from Logits',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'loss-functions',
		caseCompany: 'Uber'
	},
	{
		slug: 'problem-115-mse-loss',
		title: 'MSE Loss',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'loss-functions',
		caseCompany: 'Google'
	},
	{
		slug: 'problem-116-linear-layer-forward',
		title: 'Linear Layer Forward',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'forward-pass',
		caseCompany: 'Microsoft'
	},
	{
		slug: 'problem-117-linear-layer-backward',
		title: 'Linear Layer Backward',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'backpropagation',
		caseCompany: 'AWS'
	},
	{
		slug: 'problem-118-two-layer-mlp-forward',
		title: 'Two-Layer MLP Forward',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'forward-pass',
		caseCompany: 'Amazon'
	},
	{
		slug: 'problem-119-two-layer-mlp-backward',
		title: 'Two-Layer MLP Backward',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'backpropagation',
		caseCompany: 'Spotify'
	},
	{
		slug: 'problem-120-xavier-initialization',
		title: 'Xavier Initialization',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'weight-initialization',
		caseCompany: 'Cloudflare'
	},
	{
		slug: 'problem-121-he-initialization',
		title: 'He Initialization',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'dl-core',
		topic: 'weight-initialization',
		caseCompany: null
	},
	{
		slug: 'problem-122-batch-normalization-forward',
		title: 'Batch Normalization Forward',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'dl-core',
		topic: 'normalization',
		caseCompany: null
	},
	{
		slug: 'problem-123-layer-normalization',
		title: 'Layer Normalization',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'normalization',
		caseCompany: 'Airbnb'
	},
	{
		slug: 'problem-124-convolution-output-shape',
		title: 'Convolution Output Shape',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'dl-core',
		topic: 'cnn-basics',
		caseCompany: null
	},
	{
		slug: 'problem-125-naive-2d-convolution',
		title: 'Naive 2D Convolution',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'dl-core',
		topic: 'cnn-basics',
		caseCompany: null
	},
	{
		slug: 'problem-126-max-pooling-2d',
		title: 'Max Pooling 2D',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'cnn-basics',
		caseCompany: 'OpenAI'
	},
	{
		slug: 'problem-127-average-pooling-2d',
		title: 'Average Pooling 2D',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'dl-core',
		topic: 'cnn-basics',
		caseCompany: null
	},
	{
		slug: 'problem-128-rnn-step',
		title: 'RNN Step',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'dl-core',
		topic: 'rnn-basics',
		caseCompany: null
	},
	{
		slug: 'problem-129-rnn-sequence-forward',
		title: 'RNN Sequence Forward',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'rnn-basics',
		caseCompany: 'DoorDash'
	},
	{
		slug: 'problem-130-autoencoder-reconstruction',
		title: 'Autoencoder Reconstruction',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'autoencoders',
		caseCompany: 'Flipkart'
	},
	{
		slug: 'problem-131-encoder-bottleneck',
		title: 'Encoder Bottleneck',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'autoencoders',
		caseCompany: 'Swiggy'
	},
	{
		slug: 'problem-132-universal-approximation-toy-basis',
		title: 'Universal Approximation Toy Basis',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'universal-approximation',
		caseCompany: 'Razorpay'
	},
	{
		slug: 'problem-133-softmax-temperature',
		title: 'Softmax Temperature',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-core',
		topic: 'attention---activations',
		caseCompany: 'Atlassian'
	},
	{
		slug: 'problem-134-sgd-update',
		title: 'SGD Update',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'optimizers',
		caseCompany: 'LinkedIn'
	},
	{
		slug: 'problem-135-momentum-update',
		title: 'Momentum Update',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'optimizers',
		caseCompany: 'ByteDance'
	},
	{
		slug: 'problem-136-adam-first-step',
		title: 'Adam First Step',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'optimizers',
		caseCompany: 'TikTok'
	},
	{
		slug: 'problem-137-adamw-decoupled-decay',
		title: 'AdamW Decoupled Decay',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'optimizers',
		caseCompany: 'NVIDIA'
	},
	{
		slug: 'problem-138-exponential-lr-schedule',
		title: 'Exponential LR Schedule',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'learning-rate-schedules',
		caseCompany: 'Adobe'
	},
	{
		slug: 'problem-139-cosine-lr-schedule',
		title: 'Cosine LR Schedule',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'learning-rate-schedules',
		caseCompany: 'Salesforce'
	},
	{
		slug: 'problem-140-warmup-schedule',
		title: 'Warmup Schedule',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'dl-training-theory',
		topic: 'learning-rate-schedules',
		caseCompany: null
	},
	{
		slug: 'problem-141-dropout-mask',
		title: 'Dropout Mask',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'regularization',
		caseCompany: 'Pinterest'
	},
	{
		slug: 'problem-142-weight-decay-penalty',
		title: 'Weight Decay Penalty',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'dl-training-theory',
		topic: 'regularization',
		caseCompany: null
	},
	{
		slug: 'problem-143-early-stopping',
		title: 'Early Stopping',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'dl-training-theory',
		topic: 'regularization',
		caseCompany: null
	},
	{
		slug: 'problem-144-gradient-clipping-by-norm',
		title: 'Gradient Clipping by Norm',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'gradient-stability',
		caseCompany: 'Instacart'
	},
	{
		slug: 'problem-145-detect-vanishing-gradients',
		title: 'Detect Vanishing Gradients',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'dl-training-theory',
		topic: 'gradient-stability',
		caseCompany: null
	},
	{
		slug: 'problem-146-detect-exploding-gradients',
		title: 'Detect Exploding Gradients',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'dl-training-theory',
		topic: 'gradient-stability',
		caseCompany: null
	},
	{
		slug: 'problem-147-train-validation-gap',
		title: 'Train/Validation Gap',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'generalization',
		caseCompany: 'JPMorgan Chase'
	},
	{
		slug: 'problem-148-grid-search-selection',
		title: 'Grid Search Selection',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'dl-training-theory',
		topic: 'hyperparameter-tuning',
		caseCompany: null
	},
	{
		slug: 'problem-149-random-search-sampler',
		title: 'Random Search Sampler',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'hyperparameter-tuning',
		caseCompany: 'Coinbase'
	},
	{
		slug: 'problem-150-mini-batch-iterator',
		title: 'Mini-Batch Iterator',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'batch-dynamics',
		caseCompany: 'Palantir'
	},
	{
		slug: 'problem-151-gradient-accumulation',
		title: 'Gradient Accumulation',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'batch-dynamics',
		caseCompany: 'Tesla'
	},
	{
		slug: 'problem-152-transfer-learning-freeze',
		title: 'Transfer Learning Freeze',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'transfer-learning',
		caseCompany: 'Waymo'
	},
	{
		slug: 'problem-153-fine-tuning-lr-groups',
		title: 'Fine-Tuning LR Groups',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'fine-tuning',
		caseCompany: 'Grab'
	},
	{
		slug: 'problem-154-mixed-precision-loss-scale',
		title: 'Mixed Precision Loss Scale',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'numerical-stability',
		caseCompany: 'Meesho'
	},
	{
		slug: 'problem-155-stable-logsumexp',
		title: 'Stable LogSumExp',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'dl-training-theory',
		topic: 'numerical-stability',
		caseCompany: 'Ola'
	},
	{
		slug: 'problem-156-vanilla-rnn-sequence',
		title: 'Vanilla RNN Sequence',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'rnn-lstm-gru',
		caseCompany: 'PhonePe'
	},
	{
		slug: 'problem-157-lstm-cell',
		title: 'LSTM Cell',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'rnn-lstm-gru',
		caseCompany: 'Myntra'
	},
	{
		slug: 'problem-158-gru-cell',
		title: 'GRU Cell',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'rnn-lstm-gru',
		caseCompany: 'CRED'
	},
	{
		slug: 'problem-159-bidirectional-rnn-merge',
		title: 'Bidirectional RNN Merge',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'bidirectional-rnns',
		caseCompany: 'Booking.com'
	},
	{
		slug: 'problem-160-seq2seq-encoder-state',
		title: 'Seq2Seq Encoder State',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'sequence-models-attention',
		topic: 'seq2seq',
		caseCompany: null
	},
	{
		slug: 'problem-161-teacher-forcing-step',
		title: 'Teacher Forcing Step',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'sequence-models-attention',
		topic: 'teacher-forcing',
		caseCompany: null
	},
	{
		slug: 'problem-162-beam-search-top-k',
		title: 'Beam Search Top-K',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'beam-search',
		caseCompany: 'Zoom'
	},
	{
		slug: 'problem-163-length-normalized-beam-search',
		title: 'Length-Normalized Beam Search',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'sequence-models-attention',
		topic: 'beam-search',
		caseCompany: null
	},
	{
		slug: 'problem-164-scaled-dot-product-attention',
		title: 'Scaled Dot-Product Attention',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'sequence-models-attention',
		topic: 'attention-mechanism',
		caseCompany: null
	},
	{
		slug: 'problem-165-masked-attention',
		title: 'Masked Attention',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'attention-mechanism',
		caseCompany: 'MongoDB'
	},
	{
		slug: 'problem-166-causal-mask',
		title: 'Causal Mask',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'sequence-models-attention',
		topic: 'attention-mechanism',
		caseCompany: null
	},
	{
		slug: 'problem-167-attention-weighted-sum',
		title: 'Attention Weighted Sum',
		difficulty: 'Hard',
		kind: 'direct',
		moduleId: 'sequence-models-attention',
		topic: 'attention-mechanism',
		caseCompany: null
	},
	{
		slug: 'problem-168-additive-attention-score',
		title: 'Additive Attention Score',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'attention-mechanism',
		caseCompany: 'Intel'
	},
	{
		slug: 'problem-169-attention-padding-mask',
		title: 'Attention Padding Mask',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'sequence-padding',
		caseCompany: 'Netflix'
	},
	{
		slug: 'problem-170-sequence-padding',
		title: 'Sequence Padding',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'sequence-padding',
		caseCompany: 'Uber'
	},
	{
		slug: 'problem-171-sequence-mask',
		title: 'Sequence Mask',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'sequence-masking',
		caseCompany: 'Google'
	},
	{
		slug: 'problem-172-positional-encoding',
		title: 'Positional Encoding',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'positional-encoding',
		caseCompany: 'Microsoft'
	},
	{
		slug: 'problem-173-learned-positional-embeddings',
		title: 'Learned Positional Embeddings',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'positional-encoding',
		caseCompany: 'AWS'
	},
	{
		slug: 'problem-174-packed-sequence-lengths',
		title: 'Packed Sequence Lengths',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'sequence-padding',
		caseCompany: 'Amazon'
	},
	{
		slug: 'problem-175-masked-mean-pooling',
		title: 'Masked Mean Pooling',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'sequence-padding',
		caseCompany: 'Spotify'
	},
	{
		slug: 'problem-176-vocabulary-frequency-count',
		title: 'Vocabulary Frequency Count',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'sequence-modeling',
		caseCompany: 'Cloudflare'
	},
	{
		slug: 'problem-177-unknown-token-mapping',
		title: 'Unknown Token Mapping',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'sequence-models-attention',
		topic: 'tokenization',
		caseCompany: 'Zomato'
	},
	{
		slug: 'problem-178-multi-head-attention-split',
		title: 'Multi-Head Attention Split',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'multi-head-attention',
		caseCompany: 'Stripe'
	},
	{
		slug: 'problem-179-multi-head-attention-merge',
		title: 'Multi-Head Attention Merge',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'multi-head-attention',
		caseCompany: 'Airbnb'
	},
	{
		slug: 'problem-180-transformer-residual-block',
		title: 'Transformer Residual Block',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'transformer-architecture',
		caseCompany: 'Meta'
	},
	{
		slug: 'problem-181-transformer-feed-forward',
		title: 'Transformer Feed-Forward',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'transformer-architecture',
		caseCompany: null
	},
	{
		slug: 'problem-182-pre-norm-transformer-block',
		title: 'Pre-Norm Transformer Block',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'layer-norm-and-residuals',
		caseCompany: null
	},
	{
		slug: 'problem-183-post-norm-transformer-block',
		title: 'Post-Norm Transformer Block',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'layer-norm-and-residuals',
		caseCompany: 'Datadog'
	},
	{
		slug: 'problem-184-bpe-pair-counting',
		title: 'BPE Pair Counting',
		difficulty: 'Easy',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'tokenization',
		caseCompany: null
	},
	{
		slug: 'problem-185-bpe-merge',
		title: 'BPE Merge',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'tokenization',
		caseCompany: null
	},
	{
		slug: 'problem-186-wordpiece-score',
		title: 'WordPiece Score',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'tokenization',
		caseCompany: 'Flipkart'
	},
	{
		slug: 'problem-187-causal-lm-shift',
		title: 'Causal LM Shift',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'pretraining-objectives',
		caseCompany: null
	},
	{
		slug: 'problem-188-masked-lm-labels',
		title: 'Masked LM Labels',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'pretraining-objectives',
		caseCompany: null
	},
	{
		slug: 'problem-189-perplexity-from-nll',
		title: 'Perplexity from NLL',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'llm-evaluation',
		caseCompany: 'Atlassian'
	},
	{
		slug: 'problem-190-top-k-sampling',
		title: 'Top-K Sampling',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'generation',
		caseCompany: 'LinkedIn'
	},
	{
		slug: 'problem-191-top-p-sampling',
		title: 'Top-P Sampling',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'generation',
		caseCompany: 'ByteDance'
	},
	{
		slug: 'problem-192-temperature-sampling',
		title: 'Temperature Sampling',
		difficulty: 'Hard',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'generation',
		caseCompany: 'TikTok'
	},
	{
		slug: 'problem-193-greedy-decoding',
		title: 'Greedy Decoding',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'generation',
		caseCompany: 'NVIDIA'
	},
	{
		slug: 'problem-194-kv-cache-append',
		title: 'KV Cache Append',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'inference',
		caseCompany: 'Adobe'
	},
	{
		slug: 'problem-195-lora-update',
		title: 'LoRA Update',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'fine-tuning-and-peft',
		caseCompany: 'Salesforce'
	},
	{
		slug: 'problem-196-lora-parameter-count',
		title: 'LoRA Parameter Count',
		difficulty: 'Easy',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'fine-tuning-and-peft',
		caseCompany: 'Shopify'
	},
	{
		slug: 'problem-197-prompt-token-budget',
		title: 'Prompt Token Budget',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'prompting',
		caseCompany: 'Pinterest'
	},
	{
		slug: 'problem-198-in-context-majority-vote',
		title: 'In-Context Majority Vote',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'in-context-learning',
		caseCompany: 'Dropbox'
	},
	{
		slug: 'problem-199-rlhf-reward-normalization',
		title: 'RLHF Reward Normalization',
		difficulty: 'Medium',
		kind: 'case-study',
		moduleId: 'transformer-llm',
		topic: 'rlhf-intuition',
		caseCompany: 'Lyft'
	},
	{
		slug: 'problem-200-benchmark-accuracy',
		title: 'Benchmark Accuracy',
		difficulty: 'Medium',
		kind: 'direct',
		moduleId: 'transformer-llm',
		topic: 'llm-evaluation',
		caseCompany: null
	}
];
