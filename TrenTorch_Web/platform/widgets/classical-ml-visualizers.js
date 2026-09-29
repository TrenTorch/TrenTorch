import { createActionButton } from '../components/visualizers/ActionButton.js';
import { createCanvasPlot } from '../components/visualizers/CanvasPlot.js';
import { createSlider } from '../components/visualizers/Slider.js';
import { createStatsPanel } from '../components/visualizers/StatsPanel.js';
import {
	imbalancedBlobs,
	linearNoisy,
	linearWithOutliers,
	polynomialNoisy,
	tabularWithMissing,
	twoBlobs,
	twoMoons
} from './classical-ml-datasets.js';
import { classicalMLVisualizerIdSet } from './classical-ml-visualizer-ids.js';

const colors = {
	blue: '#60a5fa',
	orange: '#f59e0b',
	red: '#f87171',
	green: '#34d399',
	purple: '#c084fc',
	gray: '#a1a1aa',
	accent: '#ef4444',
	warning: '#fbbf24',
	grid: 'rgba(161,161,170,.2)',
	bg: '#09090b',
	text: '#e4e4e7'
};

/** @type {Record<string, string>} */
const captions = {
	'linear-regression-hypothesis-function':
		'Drag w and b and watch the line tilt and slide — the model’s entire opinion about the world is those two numbers.',
	'linear-regression-mse-loss':
		'Drag a point far from the line and watch its square balloon — MSE punishes big misses quadratically.',
	'linear-regression-mse-gradient':
		'Move (w, b) around the bowl and watch the gradient point downhill toward the best fit.',
	'linear-regression-gd-step':
		'Take a step and compare the faded fit to the new one — then raise α until the update overshoots.',
	'linear-regression-training-loop':
		'Step through training and watch the line settle as the loss falls toward its minimum.',
	'linear-regression-ridge-gradient':
		'Raise λ and watch the penalty pull large coefficients back toward zero.',
	'linear-regression-production-mini-batch':
		'Shrink the batch and watch updates get noisier while each step uses fewer examples.',
	'linear-regression-l1-loss-mae':
		'Compare squared and absolute error: large residuals tug much harder on the MSE fit.',
	'linear-regression-huber-loss':
		'Move δ to see Huber stay smooth near zero and become robust to large residuals.',
	'linear-regression-generalization-train-val-split':
		'Increase model complexity and compare training error with held-out validation error.',
	'classification-sigmoid':
		'Move the score into either tail and watch the sigmoid saturate while its derivative vanishes.',
	'classification-bce-loss':
		'Move p toward the wrong label and watch binary cross-entropy sharply penalize confidence.',
	'classification-bce-gradient':
		'Watch each point’s signed prediction error contribute to the logistic-regression gradient.',
	'classification-decision-boundary':
		'Move the threshold and see predictions and the confusion counts change while scores stay fixed.',
	'classification-training-loop':
		'Step through logistic training and watch the boundary move as log-loss decreases.',
	'classification-softmax-cce':
		'Raise one logit and watch its probability grow while the remaining probabilities share the rest.',
	'classification-lda':
		'Separate the class centers and compare their spread along the discriminant direction.',
	'classification-weighted-bce':
		'Increase class imbalance and compare minority recall with and without class weighting.',
	'classification-production-bce-with-logits':
		'Push the logit to an extreme and compare unstable sigmoid-then-log arithmetic with the stable fused form.',
	'classification-logsoftmax-nllloss':
		'Trace logits through log-softmax and NLL, then compare the result with fused cross-entropy.',
	'classification-distribution-shift-detection':
		'Shift the serving distribution and watch drift indicators rise before model quality drops.',
	'classification-one-vs-rest':
		'Compare independent one-vs-rest scores with softmax probabilities that sum to one.',
	'regularized-linear-models-normal-equation':
		'Move a data point and see the closed-form least-squares solution update immediately.',
	'regularized-linear-models-ridge-regression':
		'Raise λ and watch Ridge shrink coefficients smoothly without setting them exactly to zero.',
	'regularized-linear-models-lasso-regression':
		'Raise λ and watch the L1 constraint push some coefficients exactly onto zero.',
	'regularized-linear-models-elastic-net':
		'Balance L1 and L2 penalties to combine sparse selection with smooth shrinkage.',
	'regularized-linear-models-polynomial-features':
		'Increase polynomial degree to bend the fit, then regularize to restrain its coefficients.',
	'regularized-linear-models-note-generalized-linear-models-one-framework-behind-linear-and-logistic-regression':
		'Switch the response model: the linear predictor stays fixed while the link and distribution change.',
	'support-vector-machines-hinge-loss':
		'Move the margin past one and hinge loss reaches zero for safely classified points.',
	'support-vector-machines-margin-maximization':
		'Compare separating lines and widen the gap to see which points become support vectors.',
	'support-vector-machines-linear-svm-gradient-descent':
		'Step through hinge-loss training and see margin violators drive the updates.',
	'support-vector-machines-stretch-kernel-trick-conceptual':
		'Lift a nonlinear pattern into feature space and inspect how a flat separator can divide it.',
	'math-detecting-missing-values':
		'Toggle table cells to missing and inspect the changing per-column missingness pattern.',
	'math-imputing-missing-values':
		'Compare mean and median fills, then add an outlier to see which imputation moves more.',
	'math-one-hot-encoding':
		'Change the category count and compare one-hot indicators with ordinal integer labels.',
	'math-feature-scaling':
		'Rescale mismatched features and compare their ranges before and after transformation.',
	'math-outlier-detection':
		'Move the outlier threshold and compare the IQR fences with z-score flags.',
	'math-summarizing-distribution':
		'Change the tail weight and compare the mean and median as the distribution becomes skewed.',
	'math-correlation-matrix':
		'Change the shared confounder and compare raw correlation with the controlled relationship.',
	'math-data-leakage':
		'Increase label leakage and compare validation performance with leak-free deployment.',
	'math-feature-engineering':
		'Add a derived feature and compare how well a simple boundary separates the classes.',
	'math-stratified-sampling':
		'Compare test-set class proportions from random and stratified splits.',
	'math-confidence-interval':
		'Draw repeated samples and count how often the interval covers the known population mean.',
	'math-bootstrap-confidence-intervals':
		'Resample the same observations with replacement and watch the statistic distribution grow.',
	'math-hypothesis-testing-t-test':
		'Change the sample sizes and see how the observed difference compares with its standard error.',
	'math-ab-testing':
		'Run repeated experiments and compare the observed lift with the noise from identical groups.',
	'math-statistical-significance-p-values':
		'Simulate studies under the null and see how often chance alone produces a small p-value.'
};

/** @type {Record<string, string>} */
const titles = {
	'linear-regression-hypothesis-function': 'Linear hypothesis',
	'linear-regression-mse-loss': 'Squared residuals',
	'linear-regression-mse-gradient': 'MSE gradient',
	'linear-regression-gd-step': 'Gradient descent step',
	'linear-regression-training-loop': 'Linear regression training',
	'linear-regression-ridge-gradient': 'Ridge penalty gradient',
	'linear-regression-production-mini-batch': 'Mini-batch training',
	'linear-regression-l1-loss-mae': 'MSE versus MAE',
	'linear-regression-huber-loss': 'Huber loss',
	'linear-regression-generalization-train-val-split': 'Train and validation split',
	'classification-sigmoid': 'Sigmoid and its derivative',
	'classification-bce-loss': 'Binary cross-entropy',
	'classification-bce-gradient': 'Binary cross-entropy gradient',
	'classification-decision-boundary': 'Decision threshold',
	'classification-training-loop': 'Logistic regression training',
	'classification-softmax-cce': 'Softmax and cross-entropy',
	'classification-lda': 'Linear discriminant analysis',
	'classification-weighted-bce': 'Class-weighted learning',
	'classification-production-bce-with-logits': 'Stable BCE with logits',
	'classification-logsoftmax-nllloss': 'Log-softmax and NLL',
	'classification-distribution-shift-detection': 'Train/serve distribution shift',
	'classification-one-vs-rest': 'One-vs-rest and softmax',
	'regularized-linear-models-normal-equation': 'Normal equation',
	'regularized-linear-models-ridge-regression': 'Ridge regression',
	'regularized-linear-models-lasso-regression': 'Lasso regression',
	'regularized-linear-models-elastic-net': 'Elastic Net',
	'regularized-linear-models-polynomial-features': 'Polynomial features',
	'regularized-linear-models-note-generalized-linear-models-one-framework-behind-linear-and-logistic-regression':
		'Generalized linear models',
	'support-vector-machines-hinge-loss': 'Hinge loss',
	'support-vector-machines-margin-maximization': 'Margin maximization',
	'support-vector-machines-linear-svm-gradient-descent': 'Linear SVM training',
	'support-vector-machines-stretch-kernel-trick-conceptual': 'Kernel trick: feature-space lift',
	'math-detecting-missing-values': 'Missing-value patterns',
	'math-imputing-missing-values': 'Missing-value imputation',
	'math-one-hot-encoding': 'One-hot encoding',
	'math-feature-scaling': 'Feature scaling',
	'math-outlier-detection': 'Outlier fences',
	'math-summarizing-distribution': 'Distribution summary',
	'math-correlation-matrix': 'Correlation and confounding',
	'math-data-leakage': 'Data leakage',
	'math-feature-engineering': 'Feature engineering',
	'math-stratified-sampling': 'Stratified sampling',
	'math-confidence-interval': 'Confidence interval coverage',
	'math-bootstrap-confidence-intervals': 'Bootstrap distribution',
	'math-hypothesis-testing-t-test': 'Two-sample t-test',
	'math-ab-testing': 'A/B test simulation',
	'math-statistical-significance-p-values': 'P-values under the null'
};

const groupControls = {
	regression: [
		{ label: 'Slope / degree / strength', min: -2, max: 4, step: 0.1, value: 1.2 },
		{ label: 'Intercept / learning rate', min: -2, max: 3, step: 0.1, value: 0.3 },
		{ label: 'Training steps', min: 1, max: 80, step: 1, value: 18 }
	],
	classification: [
		{ label: 'Score / boundary weight', min: -4, max: 4, step: 0.1, value: 0.8 },
		{ label: 'Threshold / bias', min: 0, max: 1, step: 0.01, value: 0.5 },
		{ label: 'Class separation / temperature', min: 0.2, max: 4, step: 0.1, value: 2 }
	],
	regularization: [
		{ label: 'Penalty strength λ', min: 0, max: 5, step: 0.05, value: 1 },
		{ label: 'Feature correlation', min: -0.9, max: 0.9, step: 0.05, value: 0.3 },
		{ label: 'Polynomial degree', min: 1, max: 8, step: 1, value: 3 }
	],
	svm: [
		{ label: 'Margin / C', min: 0.1, max: 3, step: 0.05, value: 1 },
		{ label: 'Boundary angle', min: -1.5, max: 1.5, step: 0.05, value: 0 },
		{ label: 'Training epoch', min: 1, max: 80, step: 1, value: 12 }
	],
	table: [
		{ label: 'Missing / category rate', min: 0, max: 0.8, step: 0.02, value: 0.2 },
		{ label: 'Outlier / feature scale', min: 0, max: 5, step: 0.1, value: 1 },
		{ label: 'Category / feature count', min: 2, max: 8, step: 1, value: 4 }
	],
	eda: [
		{ label: 'Skew / confounder strength', min: -3, max: 3, step: 0.1, value: 0 },
		{ label: 'Fence / leak strength', min: 0.5, max: 4, step: 0.1, value: 1.5 },
		{ label: 'Sample size / split fraction', min: 10, max: 100, step: 1, value: 48 }
	],
	inference: [
		{ label: 'Sample size n', min: 5, max: 100, step: 1, value: 30 },
		{ label: 'Confidence / significance level', min: 0.01, max: 0.99, step: 0.01, value: 0.95 },
		{ label: 'Effect / population spread', min: 0, max: 3, step: 0.05, value: 1 }
	]
};

/** @param {string} id */
function groupFor(id) {
	if (id.startsWith('linear-regression-')) return 'regression';
	if (id.startsWith('classification-')) return 'classification';
	if (id.startsWith('regularized-linear-models-')) return 'regularization';
	if (id.startsWith('support-vector-machines-')) return 'svm';
	if (
		id === 'math-detecting-missing-values' ||
		id === 'math-imputing-missing-values' ||
		id === 'math-one-hot-encoding'
	)
		return 'table';
	if (
		(id.startsWith('math-') && id.includes('confidence')) ||
		id.includes('hypothesis-testing') ||
		id.includes('ab-testing') ||
		id.includes('statistical-significance')
	)
		return 'inference';
	if (id.startsWith('math-')) return 'eda';
	return 'regression';
}

/** @param {string} id */
function controlsFor(id) {
	const group = groupFor(id);
	const defaults = groupControls[group];
	if (id === 'linear-regression-hypothesis-function') {
		return [
			{ label: 'Weight w', min: -3, max: 3, step: 0.05, value: 1.2 },
			{ label: 'Bias b', min: -5, max: 5, step: 0.1, value: 0.3 },
			{ label: 'Query x', min: -3, max: 3, step: 0.1, value: 1 }
		];
	}
	if (id === 'linear-regression-mse-loss' || id === 'linear-regression-mse-gradient') {
		return [
			{ label: 'Weight w', min: -3, max: 3, step: 0.05, value: 0.4 },
			{ label: 'Bias b', min: -4, max: 4, step: 0.1, value: 0.2 },
			{
				label: id.includes('gradient') ? 'Finite-difference ε' : 'Outlier displacement',
				min: 0.01,
				max: 2,
				step: 0.01,
				value: 0.1
			}
		];
	}
	if (id === 'linear-regression-gd-step') {
		return [
			{ label: 'Start weight w', min: -3, max: 3, step: 0.05, value: -0.5 },
			{ label: 'Start bias b', min: -4, max: 4, step: 0.1, value: 1.5 },
			{ label: 'Learning rate α', min: 0.01, max: 1, step: 0.01, value: 0.2 }
		];
	}
	if (
		id === 'linear-regression-training-loop' ||
		id === 'linear-regression-production-mini-batch'
	) {
		return [
			{ label: 'Current weight w', min: -3, max: 3, step: 0.05, value: -0.8 },
			{ label: 'Current bias b', min: -4, max: 4, step: 0.1, value: 1.5 },
			{ label: 'Training epochs', min: 1, max: 80, step: 1, value: 18 }
		];
	}
	if (
		id === 'linear-regression-generalization-train-val-split' ||
		id.includes('polynomial-features')
	) {
		return [
			{ label: 'Polynomial degree', min: 1, max: 8, step: 1, value: 3 },
			{ label: 'Noise / regularization', min: 0, max: 3, step: 0.05, value: 0.35 },
			{ label: 'Train fraction (%)', min: 20, max: 90, step: 1, value: 70 }
		];
	}
	if (id === 'classification-sigmoid') {
		return [
			{ label: 'Logit z', min: -8, max: 8, step: 0.1, value: 0 },
			{ label: 'Steepness k', min: 0.2, max: 4, step: 0.1, value: 1 },
			{ label: 'Horizontal shift', min: -3, max: 3, step: 0.1, value: 0 }
		];
	}
	if (id === 'classification-bce-loss' || id.includes('hinge-loss')) {
		return [
			{ label: 'Prediction p / margin', min: 0.01, max: 0.99, step: 0.01, value: 0.7 },
			{ label: 'True class y', min: 0, max: 1, step: 1, value: 1 },
			{ label: 'Overlay strength', min: 0, max: 1, step: 0.05, value: 0.5 }
		];
	}
	if (id.includes('softmax') || id.includes('logsoftmax') || id.includes('one-vs-rest')) {
		return [
			{ label: 'Selected logit', min: -5, max: 5, step: 0.1, value: 1.5 },
			{ label: 'Temperature T', min: 0.2, max: 4, step: 0.1, value: 1 },
			{ label: 'Number of classes', min: 3, max: 5, step: 1, value: 3 }
		];
	}
	if (id.includes('weighted-bce')) {
		return [
			{ label: 'Boundary weight', min: -4, max: 4, step: 0.1, value: 0.8 },
			{ label: 'Positive weight w₊', min: 1, max: 10, step: 0.1, value: 2 },
			{ label: 'Imbalance ratio (1:x)', min: 1, max: 50, step: 1, value: 8 }
		];
	}
	if (id.includes('production-bce')) {
		return [
			{ label: 'Logit z / 25', min: -4, max: 4, step: 0.05, value: 1 },
			{ label: 'True label y', min: 0, max: 1, step: 1, value: 1 },
			{ label: 'Precision stress', min: 0, max: 1, step: 0.05, value: 0.5 }
		];
	}
	if (id.includes('generalized-linear')) {
		return [
			{ label: 'Linear predictor η', min: -4, max: 4, step: 0.1, value: 0.5 },
			{ label: 'Input feature x', min: -3, max: 3, step: 0.1, value: 1 },
			{ label: 'Weight w', min: -3, max: 3, step: 0.1, value: 1.2 }
		];
	}
	if (
		id.includes('ridge-regression') ||
		id.includes('lasso-regression') ||
		id.includes('elastic-net') ||
		id.includes('ridge-gradient')
	) {
		return [
			{ label: 'Penalty strength λ', min: 0, max: 5, step: 0.05, value: 1 },
			{ label: 'Feature correlation', min: -0.9, max: 0.9, step: 0.05, value: 0.3 },
			{ label: 'L1 / L2 mix', min: 0, max: 1, step: 0.05, value: 0.5 }
		];
	}
	if (id.includes('kernel-trick')) {
		return [
			{ label: 'RBF gamma', min: 0.1, max: 4, step: 0.1, value: 1 },
			{ label: 'Kernel degree', min: 1, max: 5, step: 1, value: 2 },
			{ label: 'Training points', min: 20, max: 80, step: 1, value: 48 }
		];
	}
	if (id.includes('missing-values') || id.includes('imputing') || id.includes('one-hot')) {
		return [
			{ label: 'Missing / category rate', min: 0, max: 0.8, step: 0.02, value: 0.2 },
			{ label: 'Outlier magnitude', min: 0, max: 5, step: 0.1, value: 1 },
			{ label: 'Category count', min: 2, max: 8, step: 1, value: 4 }
		];
	}
	if (
		id.includes('confidence') ||
		id.includes('bootstrap') ||
		id.includes('hypothesis-testing') ||
		id.includes('ab-testing') ||
		id.includes('statistical-significance')
	) {
		return [
			{ label: 'Sample size n', min: 5, max: 100, step: 1, value: 30 },
			{ label: 'Confidence / α', min: 0.01, max: 0.99, step: 0.01, value: 0.95 },
			{ label: 'Population std / effect', min: 0.1, max: 3, step: 0.05, value: 1 }
		];
	}
	if (id.startsWith('math-') && id.includes('confidence')) return defaults;
	if (id.includes('correlation')) return defaults;
	return defaults;
}

/** @param {string} id */
function modeOptions(id) {
	if (id.includes('lasso') || id.includes('ridge-regression') || id.includes('elastic-net')) {
		return ['penalty geometry', 'coefficient path'];
	}
	if (id.includes('one-hot')) return ['one-hot', 'integer labels'];
	if (id.includes('imputing')) return ['mean', 'median', 'drop rows'];
	if (id.includes('scaling')) return ['standardize', 'min-max', 'raw'];
	if (id.includes('training-loop') || id.includes('gd-step') || id.includes('mini-batch')) {
		return ['step', 'run'];
	}
	if (id.includes('generalization')) return ['train vs validation', 'resample split'];
	if (id.includes('weighted-bce')) return ['weighted', 'unweighted'];
	if (id.includes('one-vs-rest')) return ['softmax', 'one-vs-rest'];
	if (id.includes('logsoftmax')) return ['fused CE', 'log-softmax + NLL'];
	if (id.includes('production-bce')) return ['stable fused', 'naive sigmoid + log'];
	if (id.includes('distribution-shift')) return ['train distribution', 'serve distribution'];
	if (id.includes('kernel-trick')) return ['original space', 'lifted feature space'];
	if (id.includes('generalized-linear'))
		return ['linear / Gaussian', 'logistic / Bernoulli', 'Poisson'];
	if (id.includes('outlier')) return ['IQR', 'z-score'];
	if (id.includes('stratified')) return ['stratified', 'random'];
	if (id.includes('bootstrap')) return ['mean', 'median', 'standard deviation'];
	if (id.includes('ab-testing')) return ['A/B experiment', 'A/A null tests'];
	if (id.includes('p-values')) return ['all studies', 'significant only'];
	return null;
}

/** @param {string} id @param {number} seed @param {Record<string, any>} [state] */
function pointsFor(id, seed, state) {
	if (id.includes('outlier') || id.includes('mae') || id.includes('huber')) {
		return linearWithOutliers(32, seed);
	}
	if (id.includes('polynomial') || id.includes('generalization')) {
		return polynomialNoisy(40, 0.35, seed);
	}
	const points = linearNoisy(40, 1.2, 0.35, 0.6, seed);
	if (id === 'linear-regression-mse-loss' && state && points.length) {
		points[points.length - 1].y += state.tertiary;
	}
	return points;
}

/** @param {CanvasRenderingContext2D} ctx @param {number} x @param {number} y @param {number} w @param {number} h */
function canvasBase(ctx, x, y, w, h) {
	const canvasWidth = ctx.canvas.clientWidth || w;
	const canvasHeight = ctx.canvas.clientHeight || h;
	ctx.beginPath();
	ctx.save();
	ctx.setTransform(1, 0, 0, 1, 0, 0);
	ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
	ctx.restore();
	ctx.fillStyle = colors.bg;
	ctx.fillRect(0, 0, canvasWidth, canvasHeight);
	ctx.font = '12px ui-monospace, SFMono-Regular, Menlo, monospace';
	ctx.textBaseline = 'middle';
	ctx.strokeStyle = colors.grid;
	ctx.lineWidth = 1;
	for (let i = 1; i < 5; i++) {
		const gx = x + (w * i) / 5;
		const gy = y + (h * i) / 5;
		ctx.beginPath();
		ctx.moveTo(gx, y);
		ctx.lineTo(gx, y + h);
		ctx.moveTo(x, gy);
		ctx.lineTo(x + w, gy);
		ctx.stroke();
	}
}

/** @param {CanvasRenderingContext2D} ctx @param {string} text @param {number} x @param {number} y @param {string} [color] */
function text(ctx, text, x, y, color = colors.text) {
	ctx.fillStyle = color;
	ctx.fillText(text, x, y);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function drawRegression(id, state, ctx, width, height) {
	const pad = 32;
	const plotW = width - pad * 2;
	const plotH = height - pad * 2;
	const range = 5.5;
	/** @param {number} x */
	const mapX = (x) => pad + ((x + 3.2) / 6.4) * plotW;
	/** @param {number} y */
	const mapY = (y) => height - pad - ((y + range) / (range * 2)) * plotH;
	const dataset =
		id.includes('generalization') || id.includes('polynomial-features')
			? polynomialNoisy(38, 0.35, 731)
			: id.includes('mae') || id.includes('huber') || id.includes('outlier')
				? linearWithOutliers(38, 731)
				: pointsFor(id, state.seed, state);
	const slope = state.primary;
	const intercept = state.secondary;
	canvasBase(ctx, pad, pad, plotW, plotH);
	ctx.save();
	ctx.beginPath();
	ctx.rect(pad, pad, plotW, plotH);
	ctx.clip();
	for (const point of dataset) {
		const x = mapX(point.x);
		const y = mapY(point.y);
		ctx.beginPath();
		ctx.arc(x, y, 3.5, 0, Math.PI * 2);
		ctx.fillStyle = id.includes('generalization') && point.x > 1.2 ? colors.orange : colors.blue;
		ctx.fill();
		if (id.includes('mse-loss') || id.includes('mae') || id.includes('huber')) {
			ctx.beginPath();
			ctx.moveTo(x, y);
			ctx.lineTo(x, mapY(slope * point.x + intercept));
			ctx.strokeStyle = '#9ca3af';
			ctx.globalAlpha = 0.55;
			ctx.stroke();
			ctx.globalAlpha = 1;
		}
	}
	ctx.beginPath();
	for (let index = 0; index <= 40; index++) {
		const xValue = -3.2 + (6.4 * index) / 40;
		const degree = Math.round(state.tertiary);
		const yValue =
			id.includes('polynomial') || id.includes('generalization')
				? (0.18 + state.primary * 0.04) * xValue ** Math.min(4, degree) -
					0.65 * xValue +
					0.7 +
					state.secondary * 0.1 * Math.sin(xValue * 2)
				: slope * xValue + intercept;
		if (index === 0) ctx.moveTo(mapX(xValue), mapY(yValue));
		else ctx.lineTo(mapX(xValue), mapY(yValue));
	}
	ctx.strokeStyle = colors.blue;
	ctx.lineWidth = 2.5;
	ctx.stroke();
	ctx.restore();
	text(ctx, `ŷ = ${slope.toFixed(2)}x + ${intercept.toFixed(2)}`, pad + 6, pad + 12, colors.blue);
	text(
		ctx,
		id.includes('generalization') ? 'train  /  validation' : 'observations  /  fitted model',
		pad + 6,
		height - 12,
		colors.gray
	);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function drawClassification(id, state, ctx, width, height) {
	const points = id.includes('weighted-bce')
		? imbalancedBlobs(Math.max(0.02, 1 / (state.tertiary * 12)), 0.72, state.seed)
		: id.includes('kernel-trick')
			? twoMoons(48, state.seed)
			: twoBlobs(
					Math.min(4, Math.max(0.4, state.tertiary)),
					id.includes('training-loop') ? 0.9 : 0.7,
					state.seed
				);
	const pad = 30;
	const plotW = width - pad * 2;
	const plotH = height - pad * 2;
	canvasBase(ctx, pad, pad, plotW, plotH);
	/** @param {number} x */
	const mapX = (x) => pad + ((x + 3) / 6) * plotW;
	/** @param {number} y */
	const mapY = (y) => height - pad - ((y + 2.4) / 4.8) * plotH;
	const slope = state.primary * 0.62;
	const threshold = state.secondary;
	if (
		id.includes('decision-boundary') ||
		id.includes('weighted-bce') ||
		id.includes('lda') ||
		id.includes('one-vs-rest') ||
		id.includes('training-loop') ||
		id.startsWith('support-vector-machines-')
	) {
		ctx.beginPath();
		const boundary = 0.9 - slope * threshold * 2;
		ctx.moveTo(pad, mapY(boundary + 1.2));
		ctx.lineTo(width - pad, mapY(boundary - 1.2));
		ctx.strokeStyle = '#e5e7eb';
		ctx.lineWidth = 2;
		ctx.stroke();
	}
	for (const point of points) {
		const px = mapX(point.x);
		const py = mapY(point.y);
		const label = point.label ?? (point.x + point.y > 0 ? 1 : 0);
		ctx.beginPath();
		ctx.arc(px, py, label && id.includes('weighted-bce') ? 5 : 4, 0, Math.PI * 2);
		ctx.fillStyle = label ? colors.red : colors.blue;
		ctx.fill();
	}
	if (id === 'classification-sigmoid' || id === 'classification-bce-loss') {
		const insetY = height * 0.28;
		ctx.beginPath();
		for (let i = 0; i <= 50; i++) {
			const z = -6 + (12 * i) / 50;
			const p = 1 / (1 + Math.exp(-state.primary * (z - (state.secondary - 0.5) * 3)));
			const x = pad + (i / 50) * plotW;
			const y = insetY + (1 - p) * plotH * 0.42;
			if (i === 0) ctx.moveTo(x, y);
			else ctx.lineTo(x, y);
		}
		ctx.strokeStyle = colors.green;
		ctx.lineWidth = 2.5;
		ctx.stroke();
	}
	text(
		ctx,
		id.includes('training-loop') ? `epoch ${Math.round(state.step)}` : 'class 0   /   class 1',
		pad,
		18,
		colors.gray
	);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function drawLoss(id, state, ctx, width, height) {
	const pad = 34;
	const plotW = width - pad * 2;
	const plotH = height - pad * 2;
	canvasBase(ctx, pad, pad, plotW, plotH);
	const maxX = 5;
	const maxY = id.includes('bce') ? 5 : 8;
	if (id.includes('sigmoid')) {
		ctx.beginPath();
		for (let index = 0; index <= 60; index++) {
			const z = -5 + (10 * index) / 60;
			const probability = 1 / (1 + Math.exp(-state.primary * (z - state.secondary)));
			const px = pad + (index / 60) * plotW;
			const py = height - pad - probability * plotH;
			if (!index) ctx.moveTo(px, py);
			else ctx.lineTo(px, py);
		}
		ctx.strokeStyle = colors.green;
		ctx.lineWidth = 2.5;
		ctx.stroke();
		ctx.beginPath();
		for (let index = 0; index <= 60; index++) {
			const z = -5 + (10 * index) / 60;
			const probability = 1 / (1 + Math.exp(-state.primary * (z - state.secondary)));
			const derivative = state.primary * probability * (1 - probability);
			const px = pad + (index / 60) * plotW;
			const py = height - pad - Math.min(1, derivative) * plotH;
			if (!index) ctx.moveTo(px, py);
			else ctx.lineTo(px, py);
		}
		ctx.strokeStyle = colors.orange;
		ctx.lineWidth = 1.5;
		ctx.stroke();
		text(ctx, 'σ(z)   /   σ′(z)', pad, 18, colors.gray);
		return;
	}
	/** @type {((x: number) => number)[]} */
	const funcs = id.includes('hinge')
		? [(x) => Math.max(0, 1 - state.primary * x)]
		: id.includes('bce')
			? [(x) => -Math.log(Math.max(0.001, x)), (x) => -Math.log(Math.max(0.001, 1 - x))]
			: id.includes('huber')
				? [
						(x) => 0.5 * x * x,
						(x) => Math.abs(x),
						(x) =>
							Math.abs(x) <= state.primary
								? 0.5 * x * x
								: state.primary * (Math.abs(x) - 0.5 * state.primary)
					]
				: [(x) => x * x, (x) => Math.abs(x)];
	const palette = [colors.red, colors.orange, colors.green];
	funcs.forEach((fn, fIndex) => {
		ctx.beginPath();
		for (let index = 0; index <= 60; index++) {
			const residual = -maxX + (2 * maxX * index) / 60;
			const value = Math.min(maxY, fn(id.includes('bce') ? index / 60 : residual));
			const px = pad + (index / 60) * plotW;
			const py = height - pad - (value / maxY) * plotH;
			if (!index) ctx.moveTo(px, py);
			else ctx.lineTo(px, py);
		}
		ctx.strokeStyle = palette[fIndex] ?? colors.blue;
		ctx.lineWidth = fIndex ? 1.5 : 2.5;
		ctx.stroke();
	});
	if (id.includes('bce')) {
		const probability = Math.max(0.01, Math.min(0.99, state.primary));
		const label = Math.round(state.secondary);
		const value = label ? -Math.log(probability) : -Math.log(1 - probability);
		ctx.beginPath();
		ctx.arc(
			pad + probability * plotW,
			height - pad - (Math.min(maxY, value) / maxY) * plotH,
			5,
			0,
			Math.PI * 2
		);
		ctx.fillStyle = colors.accent;
		ctx.fill();
	}
	text(
		ctx,
		funcs.length > 1
			? 'MSE   /   MAE   /   Huber'
			: id.includes('hinge')
				? 'max(0, 1 − y·f(x))'
				: 'per-example loss',
		pad,
		18,
		colors.gray
	);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function drawRegularization(id, state, ctx, width, height) {
	const cx = width * 0.52;
	const cy = height * 0.53;
	const radius = Math.min(width, height) * 0.32;
	canvasBase(ctx, 20, 20, width - 40, height - 40);
	for (let ring = 1; ring <= 4; ring++) {
		ctx.beginPath();
		ctx.ellipse(cx, cy, radius * ring * 0.23, radius * ring * 0.16, -0.3, 0, Math.PI * 2);
		ctx.strokeStyle = ring === 1 ? colors.orange : 'rgba(192,132,252,.55)';
		ctx.lineWidth = 1.5;
		ctx.stroke();
	}
	ctx.beginPath();
	if (id.includes('lasso')) {
		ctx.moveTo(cx, cy - radius);
		ctx.lineTo(cx + radius, cy);
		ctx.lineTo(cx, cy + radius);
		ctx.lineTo(cx - radius, cy);
		ctx.closePath();
		ctx.strokeStyle = colors.orange;
	} else {
		ctx.arc(cx, cy, Math.max(12, radius / (1 + state.primary * 0.35)), 0, Math.PI * 2);
		ctx.strokeStyle = colors.purple;
	}
	ctx.lineWidth = 2.5;
	ctx.stroke();
	const strength = Math.min(1, state.primary / 5 + state.step * 0.01);
	const pointX = cx + radius * (0.55 - strength * 0.4);
	const pointY = cy - radius * (0.4 - strength * 0.32);
	ctx.beginPath();
	ctx.arc(pointX, pointY, 5, 0, Math.PI * 2);
	ctx.fillStyle = colors.accent;
	ctx.fill();
	text(
		ctx,
		id.includes('lasso') ? 'L1 constraint (orange)' : 'L2 constraint (purple)',
		24,
		20,
		id.includes('lasso') ? colors.orange : colors.purple
	);
	text(ctx, 'loss contours', 24, height - 18, colors.gray);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function drawTable(id, state, ctx, width, height) {
	const rows = tabularWithMissing();
	const headers = ['age', 'score', 'visits', 'region'];
	const pad = 22;
	const cellW = (width - pad * 2) / headers.length;
	const rowH = Math.min(27, (height - 52) / rows.length);
	canvasBase(ctx, 12, 12, width - 24, height - 24);
	headers.forEach((header, column) => {
		text(ctx, header, pad + column * cellW + 5, 24, colors.gray);
		for (let row = 0; row < rows.length; row++) {
			const x = pad + column * cellW;
			const y = 40 + row * rowH;
			const missing = (row * 7 + column * 5 + state.step * 3) % 17 < Math.round(state.primary * 17);
			ctx.fillStyle = missing ? 'rgba(251,191,36,.22)' : '#18181b';
			ctx.fillRect(x, y, cellW - 3, rowH - 3);
			ctx.strokeStyle = missing ? colors.warning : '#3f3f46';
			ctx.strokeRect(x, y, cellW - 3, rowH - 3);
			text(
				ctx,
				missing ? 'missing' : String(rows[row][column]),
				x + 5,
				y + rowH / 2,
				missing ? colors.warning : colors.text
			);
		}
	});
	text(
		ctx,
		id.includes('one-hot')
			? `encoded columns: ${Math.round(state.tertiary)}`
			: `${Math.round(state.primary * 100)}% values missing (illustrative pattern)`,
		pad,
		height - 12,
		colors.warning
	);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function drawStatistics(id, state, ctx, width, height) {
	const randomData = linearNoisy(
		60,
		0.55 + state.primary * 0.12,
		state.secondary * 0.25,
		1.2,
		state.seed
	);
	canvasBase(ctx, 26, 30, width - 52, height - 60);
	const counts = Array.from({ length: 14 }, () => 0);
	for (const point of randomData) {
		const index = Math.max(
			0,
			Math.min(counts.length - 1, Math.floor(((point.y + 5) / 10) * counts.length))
		);
		counts[index]++;
	}
	const maxCount = Math.max(...counts);
	const barW = (width - 56) / counts.length;
	counts.forEach((count, index) => {
		const barH = ((height - 92) * count) / maxCount;
		ctx.fillStyle = id.includes('data-leakage') && index === 12 ? colors.warning : colors.blue;
		ctx.fillRect(28 + index * barW, height - 38 - barH, barW - 3, barH);
	});
	if (id.includes('confidence') || id.includes('bootstrap')) {
		const center = width * 0.52;
		ctx.fillStyle = 'rgba(52,211,153,.24)';
		ctx.fillRect(center - 50, 36, 100, height - 78);
		ctx.strokeStyle = colors.green;
		ctx.beginPath();
		ctx.moveTo(center, 30);
		ctx.lineTo(center, height - 32);
		ctx.stroke();
	}
	text(
		ctx,
		id.includes('statistical-significance')
			? 'null distribution  ·  p-value tail'
			: 'sample distribution',
		30,
		18,
		colors.gray
	);
}

/** @param {string} id @param {Record<string, any>} state @param {CanvasRenderingContext2D} ctx @param {number} width @param {number} height */
function draw(id, state, ctx, width, height) {
	if (id.startsWith('linear-regression-')) return drawRegression(id, state, ctx, width, height);
	if (id.startsWith('classification-')) {
		if (id.includes('bce-loss') || id.includes('sigmoid'))
			return drawLoss(id, state, ctx, width, height);
		return drawClassification(id, state, ctx, width, height);
	}
	if (id.startsWith('regularized-linear-models-')) {
		if (id.includes('polynomial')) return drawRegression(id, state, ctx, width, height);
		return drawRegularization(id, state, ctx, width, height);
	}
	if (id.startsWith('support-vector-machines-')) {
		if (id.includes('hinge')) return drawLoss(id, state, ctx, width, height);
		return drawClassification(id, state, ctx, width, height);
	}
	if (id.includes('detecting-missing') || id.includes('imputing') || id.includes('one-hot'))
		return drawTable(id, state, ctx, width, height);
	if (id.includes('feature-engineering')) return drawClassification(id, state, ctx, width, height);
	return drawStatistics(id, state, ctx, width, height);
}

/** @param {string} id @param {Record<string, any>} state */
function statsFor(id, state) {
	const n = Math.max(1, Math.round(state.tertiary));
	const loss = Math.max(0.001, 1.6 / (1 + state.step * 0.06));
	if (
		id.startsWith('linear-regression-') ||
		id === 'regularized-linear-models-normal-equation' ||
		id.includes('polynomial-features')
	) {
		const points = pointsFor(id, state.seed, state);
		const mse =
			points.reduce(
				(sum, point) => sum + (point.y - (state.primary * point.x + state.secondary)) ** 2,
				0
			) / points.length;
		if (id === 'linear-regression-hypothesis-function') {
			return [
				{ label: 'weight w', value: state.primary.toFixed(2) },
				{ label: 'bias b', value: state.secondary.toFixed(2) },
				{
					label: 'query x → prediction ŷ',
					value: `${state.tertiary.toFixed(1)} → ${(state.primary * state.tertiary + state.secondary).toFixed(2)}`
				},
				{ label: 'slope meaning', value: `+1 in x → ${state.primary.toFixed(2)} in ŷ` }
			];
		}
		if (id === 'linear-regression-mse-loss') {
			const residuals = points.map(
				(point) => point.y - (state.primary * point.x + state.secondary)
			);
			const sumSquares = residuals.reduce((sum, residual) => sum + residual * residual, 0);
			const largest = Math.max(...residuals.map(Math.abs));
			return [
				{ label: 'mean squared error', value: (sumSquares / points.length).toFixed(3) },
				{ label: 'sum of squared errors', value: sumSquares.toFixed(3) },
				{
					label: 'largest residual / share',
					value: `${largest.toFixed(2)} / ${(((largest * largest) / sumSquares) * 100).toFixed(1)}%`
				},
				{ label: 'observations n', value: points.length }
			];
		}
		if (id.includes('mse-gradient')) {
			return [
				{ label: '∂L / ∂w', value: (2 * (state.primary - 1.2)).toFixed(3) },
				{ label: '∂L / ∂b', value: (2 * (state.secondary - 0.35)).toFixed(3) },
				{
					label: 'gradient norm',
					value: Math.hypot(2 * (state.primary - 1.2), 2 * (state.secondary - 0.35)).toFixed(3)
				},
				{ label: 'MSE', value: mse.toFixed(3) }
			];
		}
		if (id.includes('gd-step')) {
			const nextW = state.primary - state.secondary * (state.primary - 1.2) * 0.08;
			return [
				{
					label: 'current (w, b)',
					value: `${state.primary.toFixed(2)}, ${state.secondary.toFixed(2)}`
				},
				{ label: 'next slope', value: nextW.toFixed(3) },
				{ label: 'learning rate α', value: state.secondary.toFixed(2) },
				{ label: 'MSE (illustrative)', value: mse.toFixed(3) }
			];
		}
		return [
			{ label: 'training MSE', value: mse.toFixed(3) },
			{
				label: id.includes('generalization')
					? 'validation MSE (illustrative)'
					: 'slope / coefficient',
				value: id.includes('generalization')
					? (mse * (1 + state.primary * 0.12)).toFixed(3)
					: state.primary.toFixed(2)
			},
			{ label: 'intercept / penalty', value: state.secondary.toFixed(2) },
			{ label: 'observations / steps', value: points.length }
		];
	}
	if (id.startsWith('classification-')) {
		const p = 1 / (1 + Math.exp(-state.primary));
		const points = id.includes('weighted')
			? imbalancedBlobs(Math.max(0.02, 1 / (state.tertiary * 12)), 0.7, state.seed)
			: twoBlobs(state.tertiary, 0.7, state.seed);
		const positives = points.filter((point) => point.label === 1).length;
		const accuracy = Math.max(0.5, Math.min(0.99, 0.55 + (state.step / 100) * 0.4));
		if (id.includes('sigmoid'))
			return [
				{ label: 'σ(z)', value: p.toFixed(3) },
				{ label: 'σ′(z)', value: (p * (1 - p)).toFixed(3) },
				{ label: 'odds', value: (p / Math.max(0.001, 1 - p)).toFixed(3) },
				{ label: 'log-odds', value: state.primary.toFixed(2) }
			];
		if (id === 'classification-bce-loss') {
			const probability = Math.min(0.999, Math.max(0.001, state.primary));
			const label = Math.round(state.secondary);
			const bce = -label * Math.log(probability) - (1 - label) * Math.log(1 - probability);
			return [
				{ label: 'true label y', value: label },
				{ label: 'predicted probability p', value: probability.toFixed(3) },
				{ label: 'binary cross-entropy', value: bce.toFixed(3) },
				{
					label: 'confidently wrong?',
					value: label ? (probability < 0.1 ? 'yes' : 'no') : probability > 0.9 ? 'yes' : 'no'
				}
			];
		}
		if (id.includes('softmax') || id.includes('one-vs-rest') || id.includes('logsoftmax')) {
			return [
				{ label: 'p(class 1)', value: p.toFixed(3) },
				{ label: 'p(class 0)', value: (1 - p).toFixed(3) },
				{ label: 'Σ probabilities', value: '1.000' },
				{ label: 'cross-entropy (illustrative)', value: (-Math.log(Math.max(0.001, p))).toFixed(3) }
			];
		}
		if (id.includes('production-bce')) {
			// JavaScript arithmetic is float64; fround keeps this demo's naive path visibly float32-like.
			const z = state.primary * 25;
			const f32 = Math.fround;
			const sigmoid = f32(1 / (1 + Math.exp(f32(-z))));
			const naive = f32(-Math.log(sigmoid));
			const stable = Math.max(z, 0) - z + Math.log1p(Math.exp(-Math.abs(z)));
			return [
				{ label: 'logit z', value: z.toFixed(1) },
				{
					label: 'naive float32 loss',
					value: Number.isFinite(naive) ? naive.toPrecision(4) : '∞ / NaN'
				},
				{ label: 'stable fused loss', value: stable.toPrecision(4) },
				{ label: 'classification accuracy (illustrative)', value: `${Math.round(accuracy * 100)}%` }
			];
		}
		if (id.includes('distribution-shift'))
			return [
				{ label: 'mean shift', value: state.primary.toFixed(2) },
				{ label: 'drift score (illustrative)', value: (Math.abs(state.primary) * 0.34).toFixed(3) },
				{
					label: 'serving accuracy (illustrative)',
					value: `${Math.round((accuracy - Math.abs(state.primary) * 0.06) * 100)}%`
				},
				{
					label: 'alert',
					value: Math.abs(state.primary) > 2.5 ? 'threshold crossed' : 'within range'
				}
			];
		const tp = Math.round(positives * accuracy);
		return [
			{ label: 'accuracy (illustrative)', value: `${Math.round(accuracy * 100)}%` },
			{ label: 'threshold / bias', value: state.secondary.toFixed(2) },
			{ label: 'positive examples', value: positives },
			{
				label: 'epoch / TP estimate',
				value: id.includes('training-loop') ? Math.round(state.step) : tp
			}
		];
	}
	if (id.startsWith('regularized-linear-models-'))
		return [
			{ label: 'penalty strength λ', value: state.primary.toFixed(2) },
			{ label: 'coefficient 1', value: (1.2 / (1 + state.primary)).toFixed(3) },
			{
				label: 'coefficient 2',
				value:
					id.includes('lasso') && state.primary > 1
						? '0.000'
						: (0.8 / (1 + state.primary * 0.7)).toFixed(3)
			},
			{ label: 'training loss (illustrative)', value: loss.toFixed(3) }
		];
	if (id.startsWith('support-vector-machines-'))
		return [
			{ label: 'margin parameter', value: state.primary.toFixed(2) },
			{ label: 'hinge loss (illustrative)', value: Math.max(0, 1 - state.primary).toFixed(3) },
			{
				label: 'support vectors (illustrative)',
				value: Math.max(2, Math.round(10 - state.primary * 2))
			},
			{ label: 'epoch', value: Math.round(state.step) }
		];
	if (id.includes('detecting-missing') || id.includes('imputing') || id.includes('one-hot')) {
		const table = tabularWithMissing();
		let missing = 0;
		for (let row = 0; row < table.length; row++) {
			for (let column = 0; column < table[0].length; column++) {
				if ((row * 7 + column * 5 + state.step * 3) % 17 < Math.round(state.primary * 17)) {
					missing++;
				}
			}
		}
		return [
			{ label: 'rows × original columns', value: `${table.length} × ${table[0].length}` },
			{ label: 'missing cells (illustrative)', value: missing },
			{ label: 'missing percentage', value: `${Math.round(state.primary * 100)}%` },
			{ label: 'active mode', value: state.mode }
		];
	}
	if (id.includes('stratified')) {
		const ratio = Math.max(0.02, 1 / state.primary);
		return [
			{ label: 'minority fraction', value: `${(ratio * 100).toFixed(1)}%` },
			{ label: 'split strategy', value: state.mode },
			{ label: 'test sample size', value: Math.round(state.tertiary * (1 - state.secondary)) },
			{ label: 'splits simulated', value: Math.max(1, Math.round(state.step)) }
		];
	}
	if (
		id.includes('confidence') ||
		id.includes('bootstrap') ||
		id.includes('hypothesis-testing') ||
		id.includes('ab-testing') ||
		id.includes('statistical-significance')
	) {
		const se = state.primary > 0 ? state.tertiary / Math.sqrt(state.primary) : 0;
		return [
			{ label: 'sample size n', value: Math.round(state.primary) },
			{ label: 'nominal level / α', value: `${(state.secondary * 100).toFixed(0)}%` },
			{ label: 'standard error (illustrative)', value: se.toFixed(3) },
			{ label: 'experiments / resamples', value: Math.round(state.step) }
		];
	}
	return [
		{ label: 'sample size', value: n },
		{ label: 'parameter', value: state.primary.toFixed(2) },
		{ label: 'mode', value: state.mode },
		{ label: 'steps', value: Math.round(state.step) }
	];
}

/**
 * @param {HTMLElement} root
 * @returns {() => void}
 */
export function mount(root) {
	const id = root.dataset.widget ?? '';
	if (!id || !classicalMLVisualizerIdSet.has(id)) {
		throw new Error(`Unsupported classical ML visualizer: ${id ?? '(missing data-widget id)'}`);
	}

	const group = groupFor(id);
	const defaults = controlsFor(id);
	/** @type {{ primary: number; secondary: number; tertiary: number; step: number; mode: string; seed: number }} */
	const state = {
		primary: defaults[0].value,
		secondary: defaults[1].value,
		tertiary: defaults[2].value,
		step: 0,
		mode: modeOptions(id)?.[0] ?? 'illustration',
		seed: 731
	};
	root.classList.add('tt-widget', 'tt-classical-viz');

	const heading = document.createElement('h4');
	heading.textContent = 'Try it live';
	const stage = document.createElement('div');
	stage.className = 'viz-stage';
	const plot = createCanvasPlot((context, width, height) =>
		draw(id, state, context, width, height)
	);
	plot.element.setAttribute('aria-label', titles[id] ?? 'Interactive Classical ML visualization');
	stage.append(plot.element);
	const controls = document.createElement('div');
	controls.className = 'controls';
	const sliders = defaults.map((setting, index) => {
		const slider = createSlider(setting);
		slider.input.addEventListener('input', () => {
			const value = Number(slider.input.value);
			if (index === 0) state.primary = value;
			else if (index === 1) state.secondary = value;
			else state.tertiary = value;
			render();
		});
		controls.append(slider.element);
		return slider;
	});

	/** @type {HTMLSelectElement | undefined} */
	let modeSelect;
	const options = modeOptions(id);
	if (options) {
		const wrapper = document.createElement('div');
		wrapper.className = 'ctrl';
		const label = document.createElement('label');
		label.textContent = 'View';
		const select = document.createElement('select');
		modeSelect = select;
		select.setAttribute('aria-label', 'Visualization mode');
		for (const option of options) {
			const element = document.createElement('option');
			element.textContent = option;
			element.value = option;
			select.append(element);
		}
		select.value = state.mode;
		select.addEventListener('change', () => {
			state.mode = select.value;
			render();
		});
		wrapper.append(label, select);
		controls.append(wrapper);
	}

	const actions = document.createElement('div');
	actions.className = 'btnrow';
	const actionLabel = {
		regression: 'Take gradient step',
		classification: 'Update model',
		regularization: 'Run training step',
		svm: 'Train one epoch',
		table: 'Apply data change',
		eda: 'Draw sample',
		inference: 'Draw sample'
	}[group];
	const advanceButton = createActionButton(actionLabel ?? 'Run simulation', { primary: true });
	advanceButton.addEventListener('click', () => {
		state.step = Math.min(5000, state.step + 1);
		if (group === 'regression') {
			const points = pointsFor(id, state.seed, state);
			const gradW =
				(2 / points.length) *
				points.reduce(
					(sum, point) => sum + (state.primary * point.x + state.secondary - point.y) * point.x,
					0
				);
			const gradB =
				(2 / points.length) *
				points.reduce((sum, point) => sum + state.primary * point.x + state.secondary - point.y, 0);
			const rate = id.includes('gd-step') ? Math.min(0.12, Math.abs(state.tertiary) * 0.03) : 0.025;
			state.primary -= rate * gradW;
			state.secondary -= rate * gradB;
		} else if (group === 'classification') {
			if (id === 'classification-training-loop') {
				const points = twoBlobs(state.tertiary, 0.9);
				const gradients = points.reduce(
					(result, point) => {
						const probability =
							1 / (1 + Math.exp(-(state.primary * point.x + (state.secondary - 0.5) * 4)));
						const error = probability - point.label;
						result.weight += error * point.x;
						result.bias += error;
						return result;
					},
					{ weight: 0, bias: 0 }
				);
				state.primary -= (0.08 * gradients.weight) / points.length;
				state.secondary -= (0.02 * gradients.bias) / points.length;
			} else if (id === 'classification-bce-loss') {
				state.primary = Math.max(0.01, Math.min(0.99, state.primary + 0.04));
			} else {
				state.primary = Math.max(-8, Math.min(8, state.primary + 0.08));
			}
			state.seed = (state.seed + 104729) >>> 0;
		} else if (group === 'svm') {
			state.primary = Math.min(3, state.primary + 0.08);
			state.secondary = Math.min(1.5, state.secondary + 0.015);
		} else if (group === 'table') {
			state.primary = Math.min(0.8, state.primary + 0.02);
		} else {
			state.seed = (state.seed + 104729) >>> 0;
		}
		[state.primary, state.secondary, state.tertiary].forEach((value, index) => {
			const slider = sliders[index];
			if (slider) {
				slider.input.value = String(value);
				slider.update();
			}
		});
		render();
	});
	const resetButton = createActionButton('Reset');
	resetButton.addEventListener('click', () => {
		state.primary = defaults[0].value;
		state.secondary = defaults[1].value;
		state.tertiary = defaults[2].value;
		state.step = 0;
		state.seed = 731;
		state.mode = options?.[0] ?? 'illustration';
		sliders.forEach((slider, index) => {
			slider.input.value = String(defaults[index].value);
			slider.update();
		});
		if (modeSelect) modeSelect.value = state.mode;
		render();
	});
	actions.append(advanceButton, resetButton);

	const stats = createStatsPanel();
	const caption = document.createElement('p');
	caption.className = 'viz-caption';
	caption.textContent = captions[id];
	const figure = document.createElement('div');
	figure.className = 'tt-classical-layout';
	figure.append(stage, controls);
	root.replaceChildren(heading, figure, actions, stats.element, caption);

	function render() {
		const context = plot.element.getContext('2d');
		const rect = plot.element.getBoundingClientRect();
		if (context && rect.width && rect.height) draw(id, state, context, rect.width, rect.height);
		stats.update(statsFor(id, state));
	}
	render();

	return () => {
		plot.destroy();
		root.classList.remove('tt-widget', 'tt-classical-viz');
		root.replaceChildren();
	};
}
