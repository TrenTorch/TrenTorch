import { createActionButton } from '../components/visualizers/ActionButton.js';
import { createCanvasPlot } from '../components/visualizers/CanvasPlot.js';
import { createDiagramSvg, svgElement } from '../components/visualizers/DiagramSvg.js';
import { createSlider } from '../components/visualizers/Slider.js';
import { createStatsPanel } from '../components/visualizers/StatsPanel.js';
import { seededRandom } from '../components/visualizers/seededRandom.js';

/** @typedef {'series' | 'combination' | 'sets' | 'growth' | 'matrix' | 'vector' | 'calculus' | 'sampling' | 'distribution' | 'joint' | 'probability' | 'information'} VisualizerKind */
/** @typedef {{ primary: number; secondary: number; n: number; step: number; samples: number[]; expression: string; logScale: boolean; distribution: string; variableMode: string; operation: string; probabilityView: string; conditionRow: number; matrix: number[][]; probabilities: number[]; series: string; subset: number[]; points: number[][] }} VisualizerState */
/** @typedef {{ label: string; min: number; max: number; step: number; value: number }} SliderSettings */

/** @type {Record<string, [VisualizerKind, string]>} */
const specs = {
	'math-summation-notation': [
		'series',
		'Step through the sum term by term and watch the running total climb.'
	],
	'math-product-notation': [
		'series',
		'Products grow or shrink far faster than sums — flip to log scale when the bars stop fitting.'
	],
	'math-factorial-and-binomial-coefficient': [
		'combination',
		'Change n and k and watch the same value appear in Pascal’s triangle and the factorial formula.'
	],
	'math-set-and-function-notation': [
		'sets',
		'Toggle the set operation to see which region lights up, then check the arrows on the right.'
	],
	'math-big-o-notation': [
		'growth',
		'Move n to compare growth rates and see how quickly exponential growth pulls ahead.'
	],
	'math-vectors-matrices-tensors': [
		'matrix',
		'Change the shape and watch the same data reorganize — the element count never changes.'
	],
	'math-dot-product-norms': [
		'vector',
		'Drag the vector controls and watch the dot product, angle, and norms update live.'
	],
	'math-matrix-multiplication': [
		'matrix',
		'Step through output cells and see which row and column combine to produce each value.'
	],
	'math-transpose': [
		'matrix',
		'Watch the diagonal flip and compare the original and transposed matrix layouts.'
	],
	'math-vector-projection': [
		'vector',
		'Move vector a around b and watch it split into parallel and perpendicular components.'
	],
	'math-gaussian-elimination': [
		'matrix',
		'Step through row reduction and watch the matrix approach row-echelon form.'
	],
	'math-lu-decomposition': [
		'matrix',
		'Each elimination multiplier is saved into L while the remaining entries form U.'
	],
	'math-qr-decomposition': [
		'vector',
		'Strip away components already covered by earlier vectors to build an orthonormal basis.'
	],
	'math-rank-and-nullity': [
		'matrix',
		'Edit the matrix and see rank and nullity continue to add up to its column count.'
	],
	'math-matrix-inverse': [
		'matrix',
		'Watch the determinant approach zero as the matrix becomes singular and its inverse disappears.'
	],
	'math-eigenvalues-eigenvectors': [
		'matrix',
		'See how a matrix transforms the plane and compare its invariant directions.'
	],
	'math-svd': ['matrix', 'SVD is three simple moves in a row: rotate, stretch, and rotate again.'],
	'math-positive-definite-matrices': [
		'matrix',
		'Change the symmetric matrix and watch its quadratic form turn from bowl to saddle.'
	],
	'math-gram-schmidt': [
		'vector',
		'Strip away what earlier vectors already cover, then normalize what remains.'
	],
	'math-trace-of-a-matrix': [
		'matrix',
		'Rotate the basis and add the diagonal again — the trace stays the same.'
	],
	'math-derivatives-first-principles': [
		'calculus',
		'Shrink h and watch the secant line lock onto the tangent.'
	],
	'math-partial-derivatives': [
		'calculus',
		'Freeze one coordinate and see each partial derivative as a cross-section slope.'
	],
	'math-chain-rule': [
		'calculus',
		'Follow the composition and multiply the local slopes to see the chain rule in action.'
	],
	'math-jacobian': [
		'calculus',
		'Change the input point and inspect how the Jacobian maps small changes in each direction.'
	],
	'math-hessian': [
		'calculus',
		'Change the point and compare curvature along the two principal directions.'
	],
	'math-directional-derivatives': [
		'calculus',
		'Rotate the direction and watch the directional derivative change with the gradient.'
	],
	'math-taylor-series': [
		'calculus',
		'Increase the Taylor order and watch the local approximation track the function.'
	],
	'math-gradient-descent': [
		'calculus',
		'Push the learning rate too high and watch gradient descent overshoot instead of settling.'
	],
	'math-random-variables': [
		'sampling',
		'Discrete probability lives in bar heights; continuous probability lives in area under a curve.'
	],
	'math-pmf-and-pdf': [
		'distribution',
		'For a PMF add bar heights; for a PDF measure area under the curve.'
	],
	'math-combinatorics': [
		'combination',
		'Switch between ordered and unordered selections and compare the counts.'
	],
	'math-joint-and-marginal-probability': [
		'joint',
		'Edit a joint cell and watch both marginal distributions recompute.'
	],
	'math-independence': ['probability', 'Change the overlap and compare P(A∩B) with P(A)P(B).'],
	'math-chain-rule-of-probability': [
		'probability',
		'Follow a path from root to leaf and multiply the branch probabilities as you go.'
	],
	'math-expectation-variance-covariance': [
		'sampling',
		'Change the sample cloud and watch its expectation, variance, and covariance update.'
	],
	'math-sampling-estimating-distribution': [
		'sampling',
		'Draw more samples and watch the histogram settle into the distribution’s shape.'
	],
	'math-expectation-variance': [
		'sampling',
		'Keep drawing samples and watch the estimates settle toward their true values.'
	],
	'math-covariance-correlation': [
		'sampling',
		'Slide ρ from negative to positive and watch the cloud reshape from a diagonal to a round blob.'
	],
	'math-conditional-probability': [
		'joint',
		'Select a row to condition on it and rescale that slice until it sums to one.'
	],
	'math-bayes-theorem': [
		'probability',
		'Change the likelihoods and watch evidence update the prior into a posterior.'
	],
	'math-likelihood-vs-probability': [
		'distribution',
		'Slice the same model in two directions and compare a probability curve with a likelihood.'
	],
	'math-maximum-likelihood-estimation': [
		'sampling',
		'Move the candidate parameter and find where the observed data are most likely.'
	],
	'math-map-estimation': [
		'sampling',
		'Increase prior strength and watch the posterior estimate move toward the prior.'
	],
	'math-entropy': [
		'information',
		'Concentrate probability on one outcome to lower entropy; spread it evenly to maximize it.'
	],
	'math-cross-entropy': [
		'information',
		'Move the prediction away from the target distribution and watch cross-entropy climb.'
	],
	'math-kl-divergence': [
		'information',
		'Compare both KL directions and see why divergence is not symmetric.'
	],
	'math-mutual-information': [
		'joint',
		'Match the joint table to its independent reference and mutual information approaches zero.'
	]
};

const initialMatrix = [
	[2, 1, 0],
	[1, 3, 1],
	[0, 1, 2]
];

/** @param {number} value @param {number} [digits] */
function number(value, digits = 2) {
	return Number.isFinite(value) ? value.toFixed(digits) : 'undefined';
}

/** @param {number} n */
function factorial(n) {
	let result = 1;
	for (let i = 2; i <= n; i++) result *= i;
	return result;
}

/** @param {number} x @param {number} order */
function taylorSin(x, order) {
	let result = 0;
	for (let power = 1; power <= order * 2; power += 2) {
		const sign = ((power - 1) / 2) % 2 === 0 ? 1 : -1;
		result += (sign * x ** power) / factorial(power);
	}
	return result;
}

/** @param {number} n @param {number} k */
function choose(n, k) {
	if (k < 0 || k > n) return 0;
	return factorial(n) / (factorial(k) * factorial(n - k));
}

/** @param {number} x @param {number} mean @param {number} deviation */
function normalPdf(x, mean, deviation) {
	return Math.exp(-0.5 * ((x - mean) / deviation) ** 2) / (deviation * Math.sqrt(2 * Math.PI));
}

/** @param {number[][]} matrix @param {number} [activeCell] */
function makeMatrixSvg(matrix, activeCell = -1) {
	const svg = createDiagramSvg({ label: 'Editable matrix visualization' });
	const rows = matrix.length;
	const columns = matrix[0].length;
	const cellWidth = 420 / columns;
	const cellHeight = 180 / rows;
	const startX = 90;
	const startY = 50;
	for (let row = 0; row < rows; row++) {
		for (let column = 0; column < columns; column++) {
			const index = row * columns + column;
			const x = startX + column * cellWidth;
			const y = startY + row * cellHeight;
			svg.append(
				svgElement('rect', {
					x,
					y,
					width: cellWidth - 4,
					height: cellHeight - 4,
					rx: 6,
					class: index === activeCell ? 'viz-cell active' : 'viz-cell'
				}),
				Object.assign(
					svgElement('text', {
						x: x + (cellWidth - 4) / 2,
						y: y + (cellHeight - 4) / 2 + 5,
						'text-anchor': 'middle',
						class: 'viz-cell-label'
					}),
					{ textContent: number(matrix[row][column], 1) }
				)
			);
		}
	}
	return svg;
}

/** @param {VisualizerState} state */
function makeVectorSvg(state) {
	const svg = createDiagramSvg({ label: 'Draggable-vector style projection diagram' });
	const origin = { x: 300, y: 140 };
	const scale = 28;
	const vectors = [
		{ x: state.primary, y: state.secondary, color: '#ef4444', label: 'a' },
		{ x: state.secondary, y: 1, color: '#60a5fa', label: 'b' }
	];
	svg.append(
		svgElement('line', { x1: origin.x, y1: 16, x2: origin.x, y2: 264, class: 'viz-axis' }),
		svgElement('line', { x1: 24, y1: origin.y, x2: 576, y2: origin.y, class: 'viz-axis' })
	);
	for (const vector of vectors) {
		const endX = origin.x + vector.x * scale;
		const endY = origin.y - vector.y * scale;
		svg.append(
			svgElement('line', {
				x1: origin.x,
				y1: origin.y,
				x2: endX,
				y2: endY,
				stroke: vector.color,
				'stroke-width': 4,
				'marker-end': 'url(#viz-arrow)'
			}),
			Object.assign(
				svgElement('text', { x: endX + 8, y: endY - 8, fill: vector.color, class: 'viz-label' }),
				{ textContent: vector.label }
			)
		);
	}
	const defs = svgElement('defs');
	const marker = svgElement('marker', {
		id: 'viz-arrow',
		viewBox: '0 0 10 10',
		refX: 8,
		refY: 5,
		markerWidth: 6,
		markerHeight: 6,
		orient: 'auto-start-reverse'
	});
	marker.append(svgElement('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: 'context-stroke' }));
	defs.append(marker);
	svg.prepend(defs);
	return svg;
}

/** @param {number} n @param {number} k @param {number[]} subset */
function makePascalSvg(n, k, subset) {
	const svg = createDiagramSvg({ label: 'Pascal triangle and selected combination' });
	const limit = Math.min(n, 10);
	for (let row = 0; row <= limit; row++) {
		for (let column = 0; column <= row; column++) {
			const x = 300 + (column - row / 2) * 45;
			const y = 12 + row * 22;
			const cell = svgElement('circle', {
				cx: x,
				cy: y,
				r: 9,
				class: row === n && column === k ? 'viz-cell active' : 'viz-cell'
			});
			const value = svgElement('text', {
				x,
				y: y + 3,
				'text-anchor': 'middle',
				class: 'viz-small-label'
			});
			value.textContent = String(choose(row, column));
			svg.append(cell, value);
		}
	}
	const dotCount = Math.max(n, 1);
	for (let index = 0; index < dotCount; index++) {
		svg.append(
			svgElement('circle', {
				cx: 300 - ((dotCount - 1) * 18) / 2 + index * 18,
				cy: 244,
				r: 6,
				class: subset.includes(index) ? 'viz-cell active' : 'viz-cell'
			})
		);
	}
	return svg;
}

/** @param {number[]} probabilities */
function makeJointSvg(probabilities) {
	const svg = createDiagramSvg({ label: 'Joint probability heatmap with marginal totals' });
	const cells = jointTable(probabilities);
	cells.forEach((value, index) => {
		const row = Math.floor(index / 3);
		const column = index % 3;
		const rect = svgElement('rect', {
			x: 95 + column * 65,
			y: 48 + row * 55,
			width: 59,
			height: 49,
			rx: 4,
			class: 'viz-cell',
			opacity: 0.25 + value
		});
		const text = svgElement('text', {
			x: 124 + column * 65,
			y: 77 + row * 55,
			'text-anchor': 'middle',
			class: 'viz-small-label'
		});
		text.textContent = number(value, 2);
		svg.append(rect, text);
	});
	const labels = ['row sums', 'column sums'];
	labels.forEach((label, index) => {
		const text = svgElement('text', { x: 370, y: 103 + index * 50, class: 'viz-label' });
		text.textContent = label;
		svg.append(text);
	});
	return svg;
}

/** @param {number[]} probabilities @param {string} operation */
function makeSetSvg(probabilities, operation) {
	const svg = createDiagramSvg({ label: `${operation} set operation Venn diagram` });
	const p = probabilities;
	svg.append(
		svgElement('circle', {
			cx: 250,
			cy: 140,
			r: 82,
			class: 'viz-set-left',
			opacity: 0.32 + p[0] * 0.45
		}),
		svgElement('circle', {
			cx: 350,
			cy: 140,
			r: 82,
			class: 'viz-set-right',
			opacity: 0.32 + p[1] * 0.45
		})
	);
	for (const label of [
		{ x: 208, text: 'A' },
		{ x: 392, text: 'B' },
		{ x: 300, text: operation }
	]) {
		const text = svgElement('text', {
			x: label.x,
			y: 145,
			'text-anchor': 'middle',
			class: 'viz-label'
		});
		text.textContent = label.text;
		svg.append(text);
	}
	return svg;
}

/** @param {number} seed @param {number} mean @param {number} deviation @param {number} count */
function sampleNormal(seed, mean, deviation, count) {
	const random = seededRandom(seed);
	const values = [];
	while (values.length < count) {
		const u = Math.max(random(), 1e-12);
		const v = random();
		const radius = Math.sqrt(-2 * Math.log(u));
		values.push(mean + deviation * radius * Math.cos(2 * Math.PI * v));
		if (values.length < count) values.push(mean + deviation * radius * Math.sin(2 * Math.PI * v));
	}
	return values;
}

/** @param {number} seed @param {string} distribution @param {number} count @param {number} location @param {number} scale */
function drawDistribution(seed, distribution, count, location, scale) {
	const random = seededRandom(seed);
	if (distribution === 'normal') return sampleNormal(seed, location, scale, count);
	return Array.from({ length: count }, () => {
		if (distribution === 'uniform') return location + (random() * 2 - 1) * scale;
		if (distribution === 'exponential')
			return location - scale * Math.log(Math.max(random(), 1e-12));
		const probability = Math.min(0.95, Math.max(0.05, (location + 3) / 6));
		let successes = 0;
		for (let trial = 0; trial < 10; trial++) {
			if (random() < probability) successes += 1;
		}
		return successes;
	});
}

/** @param {number} seed @param {number} correlation @param {number} count */
function drawCorrelatedPoints(seed, correlation, count) {
	const random = seededRandom(seed);
	const rho = Math.max(-1, Math.min(1, correlation));
	const points = [];
	while (points.length < count) {
		const radius = Math.sqrt(-2 * Math.log(Math.max(random(), 1e-12)));
		const angle = 2 * Math.PI * random();
		const x = radius * Math.cos(angle);
		const independent = radius * Math.sin(angle);
		points.push([x, rho * x + Math.sqrt(1 - rho * rho) * independent]);
	}
	return points;
}

/** @param {string} id @param {number} x @param {VisualizerState} state */
function functionValue(id, x, state) {
	if (id.includes('partial')) return x * x + state.secondary ** 2;
	if (id.includes('chain')) return Math.sin(x) ** 2;
	if (id.includes('jacobian')) return Math.sin(x) + (x * x) / 4;
	if (id.includes('hessian')) return x * x * Math.cos(x / 2);
	if (id.includes('directional')) return Math.sin(x) + Math.cos(state.secondary);
	if (id.includes('big-o')) return x * Math.log2(Math.max(x, 1));
	if (id.includes('taylor')) return Math.sin(x);
	if (id.includes('gradient')) return (x - 1.2) ** 2;
	return x * x;
}

/** @param {number[][]} matrix */
function matrixStats(matrix) {
	const trace = matrix.reduce((sum, row, index) => sum + (row[index] ?? 0), 0);
	const determinant =
		matrix.length === 2
			? matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
			: matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
				matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
				matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
	const reduced = matrix.map((row) => [...row]);
	let rank = 0;
	for (let column = 0; column < matrix[0].length && rank < matrix.length; column++) {
		let pivot = rank;
		for (let row = rank + 1; row < matrix.length; row++) {
			if (Math.abs(reduced[row][column]) > Math.abs(reduced[pivot][column])) pivot = row;
		}
		if (Math.abs(reduced[pivot][column]) < 1e-8) continue;
		[reduced[rank], reduced[pivot]] = [reduced[pivot], reduced[rank]];
		for (let row = rank + 1; row < matrix.length; row++) {
			const factor = reduced[row][column] / reduced[rank][column];
			for (let entry = column; entry < matrix[0].length; entry++) {
				reduced[row][entry] -= factor * reduced[rank][entry];
			}
		}
		rank += 1;
	}
	return { trace, determinant, rank };
}

/** @param {number[][]} matrix */
function matrixEigenvalues2x2(matrix) {
	const a = matrix[0][0];
	const b = matrix[0][1];
	const c = matrix[1][0];
	const d = matrix[1][1];
	const discriminant = (a + d) ** 2 - 4 * (a * d - b * c);
	if (discriminant < 0) return [Number.NaN, Number.NaN];
	const root = Math.sqrt(discriminant);
	return [(a + d + root) / 2, (a + d - root) / 2];
}

/** @param {number[][]} points */
function pointStatistics(points) {
	if (!points.length)
		return { meanX: 0, meanY: 0, varianceX: 0, varianceY: 0, covariance: 0, correlation: 0 };
	const meanX = points.reduce((sum, point) => sum + point[0], 0) / points.length;
	const meanY = points.reduce((sum, point) => sum + point[1], 0) / points.length;
	const varianceX = points.reduce((sum, point) => sum + (point[0] - meanX) ** 2, 0) / points.length;
	const varianceY = points.reduce((sum, point) => sum + (point[1] - meanY) ** 2, 0) / points.length;
	const covariance =
		points.reduce((sum, point) => sum + (point[0] - meanX) * (point[1] - meanY), 0) / points.length;
	return {
		meanX,
		meanY,
		varianceX,
		varianceY,
		covariance,
		correlation: covariance / Math.sqrt(Math.max(varianceX * varianceY, 1e-12))
	};
}

/** @param {number[]} values */
function normalizedProbabilities(values) {
	const positive = values.map((value) => Math.max(Number(value), 0.001));
	const total = positive.reduce((sum, value) => sum + value, 0);
	return positive.map((value) => value / total);
}

/** @param {number[]} probabilities */
function jointTable(probabilities) {
	const p = normalizedProbabilities(probabilities);
	return normalizedProbabilities([
		p[0] * 0.55,
		p[1] * 0.35,
		p[2] * 0.1,
		p[1] * 0.2,
		p[2] * 0.55,
		p[0] * 0.25,
		p[2] * 0.15,
		p[0] * 0.2,
		p[1] * 0.65
	]);
}

/** @param {HTMLElement} root */
export function mount(root) {
	const id = root.dataset.widget ?? '';
	const spec = specs[id];
	if (!spec) return () => {};
	const [kind, caption] = spec;
	/** @type {VisualizerState} */
	const state = {
		primary: kind === 'sampling' ? 0 : 1,
		secondary: 1,
		n: 8,
		step: 0,
		samples: [],
		expression: 'i',
		logScale: false,
		distribution: 'normal',
		variableMode: 'discrete',
		operation: 'union',
		probabilityView: 'prior',
		conditionRow: 0,
		matrix: initialMatrix.map((row) => [...row]),
		probabilities: [0.5, 0.3, 0.2],
		series: 'x²',
		subset: [],
		points: []
	};
	/** @type {Array<() => void>} */
	const listeners = [];
	/** @type {Array<() => void>} */
	const resetters = [];
	/** @type {Set<number>} */
	const timers = new Set();
	const shell = document.createElement('section');
	shell.className = 'tt-math-viz';
	const heading = document.createElement('h4');
	heading.textContent = 'Try it live';
	const stage = document.createElement('div');
	stage.className = 'viz-stage';
	const controls = document.createElement('div');
	controls.className = 'viz-controls controls';
	const stats = createStatsPanel();
	const btnrow = document.createElement('div');
	btnrow.className = 'btnrow';
	const captionElement = document.createElement('p');
	captionElement.className = 'viz-caption';
	captionElement.textContent = caption;
	shell.append(heading);
	/** @type {Partial<Record<'primary' | 'secondary' | 'n', SliderSettings>>} */
	const sliderValues = {};
	const sliderKeys = /** @type {const} */ (['primary', 'secondary', 'n']);
	if (kind === 'series') {
		sliderValues.n = {
			label: 'n',
			min: 1,
			max: id.includes('product') ? 12 : 15,
			step: 1,
			value: 6
		};
	} else if (kind === 'combination') {
		sliderValues.n = { label: 'n', min: 0, max: 10, step: 1, value: 6 };
		sliderValues.secondary = { label: 'k', min: 0, max: 6, step: 1, value: 2 };
	} else if (kind === 'growth') {
		sliderValues.n = { label: 'Maximum n', min: 4, max: 40, step: 1, value: 20 };
		sliderValues.primary = { label: 'Marker n', min: 1, max: 10, step: 1, value: 5 };
	} else if (kind === 'matrix') {
		sliderValues.n = { label: 'Step', min: 1, max: 9, step: 1, value: 9 };
		if (id === 'math-trace-of-a-matrix') {
			sliderValues.primary = { label: 'Rotation angle', min: 0, max: 180, step: 1, value: 0 };
		}
	} else if (kind === 'vector') {
		sliderValues.primary = { label: 'Vector a · x', min: -4, max: 4, step: 0.1, value: 2 };
		sliderValues.secondary = { label: 'Vector y', min: -4, max: 4, step: 0.1, value: 1 };
	} else if (kind === 'sampling' || kind === 'distribution') {
		sliderValues.primary = {
			label: id === 'math-covariance-correlation' ? 'Target ρ' : 'Mean / location',
			min: id === 'math-covariance-correlation' ? -1 : -3,
			max: id === 'math-covariance-correlation' ? 1 : 3,
			step: 0.1,
			value: 0
		};
		sliderValues.secondary = { label: 'Spread / scale', min: 0.2, max: 3, step: 0.1, value: 1 };
		sliderValues.n = { label: 'Batch size', min: 2, max: 20, step: 1, value: 10 };
	} else if (kind === 'probability') {
		sliderValues.primary = { label: 'P(A) / prior', min: 0.01, max: 0.99, step: 0.01, value: 0.5 };
		sliderValues.secondary = { label: 'P(B|A)', min: 0.01, max: 0.99, step: 0.01, value: 0.7 };
		if (id === 'math-independence') {
			sliderValues.secondary.label = 'P(B)';
			sliderValues.n = { label: 'P(A∩B)', min: 0, max: 1, step: 0.01, value: 0.2 };
		} else if (id === 'math-bayes-theorem') {
			sliderValues.n = { label: 'P(E|¬H)', min: 0.01, max: 0.99, step: 0.01, value: 0.2 };
		}
	} else if (kind === 'calculus') {
		sliderValues.primary = { label: 'Point x', min: -3, max: 3, step: 0.1, value: 1 };
		sliderValues.secondary = {
			label: 'Step / direction',
			min: 0.05,
			max: 2,
			step: 0.05,
			value: 0.5
		};
		sliderValues.n = { label: 'Approximation order', min: 1, max: 8, step: 1, value: 4 };
	}
	for (const key of sliderKeys) {
		const settings = sliderValues[key];
		if (settings) state[key] = settings.value;
	}

	/** @type {Partial<Record<'primary' | 'secondary' | 'n', ReturnType<typeof createSlider>>>} */
	const sliders = {};
	for (const key of sliderKeys) {
		const settings = sliderValues[key];
		if (!settings) continue;
		const slider = createSlider(settings);
		sliders[key] = slider;
		controls.append(slider.element);
		const handler = () => {
			state[key] = Number(slider.input.value);
			if (key === 'n') {
				state.step = Math.min(state.step, state.n);
				if (kind === 'combination') {
					state.secondary = Math.min(state.secondary, state.n);
					const kSlider = sliders.secondary;
					if (kSlider) {
						kSlider.input.max = String(state.n);
						kSlider.input.value = String(state.secondary);
						kSlider.update();
					}
				}
			}
			update();
		};
		slider.input.addEventListener('input', handler);
		listeners.push(() => slider.input.removeEventListener('input', handler));
	}

	const plot = createCanvasPlot((context, width, height) => draw(context, width, height));
	stage.append(plot.element);

	/** @param {string} label @param {() => void} onClick @param {boolean} [primary] */
	function addButton(label, onClick, primary = false) {
		const button = createActionButton(label, { primary });
		button.addEventListener('click', onClick);
		listeners.push(() => button.removeEventListener('click', onClick));
		btnrow.append(button);
		return button;
	}

	const resetInputs = () => {
		for (const timer of timers) window.clearInterval(timer);
		timers.clear();
		if (sliderValues.primary) state.primary = sliderValues.primary.value;
		if (sliderValues.secondary) state.secondary = sliderValues.secondary.value;
		if (sliderValues.n) state.n = sliderValues.n.value;
		state.step = 0;
		state.samples = [];
		state.points = [];
		state.matrix = initialMatrix.map((row) => [...row]);
		state.probabilities = [0.5, 0.3, 0.2];
		state.subset = [0, 1];
		for (const key of sliderKeys) {
			const slider = sliders[key];
			if (!slider) continue;
			if (kind === 'combination' && key === 'secondary') slider.input.max = String(state.n);
			slider.input.value = String(state[key]);
			slider.update();
		}
		resetters.forEach((reset) => reset());
		update();
	};
	const drawSamples = () => {
		const seed = Math.floor(performance.now() * 1000) >>> 0;
		const count = Math.max(100, Math.round(state.n * 50));
		if (id === 'math-random-variables' && state.variableMode === 'discrete') {
			const random = seededRandom(seed);
			state.samples = Array.from({ length: count }, () => Math.floor(random() * 6) + 1);
		} else if (id === 'math-covariance-correlation') {
			state.points = drawCorrelatedPoints(seed, state.primary, count);
		} else if (id === 'math-expectation-variance-covariance') {
			state.points = drawCorrelatedPoints(seed, state.primary / 3, 9);
		} else {
			const drawn = drawDistribution(
				seed,
				state.distribution,
				count,
				state.primary,
				state.secondary
			);
			state.samples = id === 'math-expectation-variance' ? [...state.samples, ...drawn] : drawn;
		}
		update();
	};
	const step = () => {
		state.step = Math.min(state.step + 1, state.n);
		update();
	};
	if (kind === 'series' || kind === 'matrix') {
		addButton(kind === 'series' ? 'Step' : 'Next step', step, true);
	}
	if (kind === 'combination') {
		addButton(
			'Shuffle subset',
			() => {
				const random = seededRandom(Math.floor(performance.now() * 1000) >>> 0);
				const n = Math.round(state.n);
				const k = Math.min(Math.round(state.secondary), n);
				const items = Array.from({ length: n }, (_, index) => index);
				for (let index = items.length - 1; index > 0; index--) {
					const swapIndex = Math.floor(random() * (index + 1));
					[items[index], items[swapIndex]] = [items[swapIndex], items[index]];
				}
				state.subset = items.slice(0, k);
				update();
			},
			true
		);
		state.subset = [0, 1];
	}
	if (kind === 'series') {
		const select = document.createElement('select');
		select.className = 'viz-select';
		select.setAttribute('aria-label', 'Expression preset');
		const expressions = id.includes('product') ? ['i', '(i+1)/i'] : ['i', 'i²', '1/i', '2i−1'];
		for (const expression of expressions) {
			const option = document.createElement('option');
			option.value = expression;
			option.textContent = expression;
			select.append(option);
		}
		const onExpressionChange = () => {
			state.expression = select.value;
			state.step = 0;
			update();
		};
		select.addEventListener('change', onExpressionChange);
		listeners.push(() => select.removeEventListener('change', onExpressionChange));
		resetters.push(() => {
			select.value = expressions[0];
			state.expression = expressions[0];
		});
		controls.prepend(select);
		const play = addButton('Play', () => {
			for (const timer of timers) window.clearInterval(timer);
			timers.clear();
			state.step = 0;
			update();
			const timer = window.setInterval(() => {
				if (state.step >= state.n) {
					window.clearInterval(timer);
					timers.delete(timer);
					return;
				}
				state.step += 1;
				update();
			}, 350);
			timers.add(timer);
		});
		play.setAttribute('aria-label', 'Play sequence one term at a time');
	}
	if (kind === 'sampling' || kind === 'distribution')
		addButton('Draw N samples', drawSamples, true);
	addButton('Reset', resetInputs);

	controls.append(btnrow);
	controls.append(stats.element);
	shell.append(stage, controls, captionElement);
	root.classList.add('tt-widget', 'math-visualizer');
	root.replaceChildren(shell);

	function update() {
		const message = [];
		if (kind === 'series') {
			const terms = Array.from({ length: Math.min(state.step, state.n) }, (_, index) => {
				const i = index + 1;
				if (state.expression === 'i²') return i * i;
				if (state.expression === '1/i') return 1 / i;
				if (state.expression === '2i−1') return 2 * i - 1;
				if (state.expression === '(i+1)/i') return (i + 1) / i;
				return i;
			});
			const total = terms.reduce(
				(value, term) => (id.includes('product') ? value * term : value + term),
				id.includes('product') ? 1 : 0
			);
			message.push(
				{
					label: id.includes('product') ? 'running product' : 'running sum',
					value: number(total, 3)
				},
				{ label: 'current term', value: terms.length ? number(terms.at(-1) ?? 0, 3) : '—' },
				{ label: 'n', value: state.n }
			);
		} else if (kind === 'combination') {
			const k = Math.min(Math.round(state.secondary), Math.round(state.n));
			message.push(
				{ label: 'n!', value: factorial(Math.round(state.n)) },
				{ label: 'k!', value: factorial(k) },
				{ label: '(n−k)!', value: factorial(Math.round(state.n) - k) },
				{
					label: id.includes('combinatorics') ? 'P(n,k)' : 'C(n,k)',
					value: id.includes('combinatorics')
						? factorial(Math.round(state.n)) / factorial(Math.round(state.n) - k)
						: choose(Math.round(state.n), k)
				},
				{ label: 'C(n,k)', value: choose(Math.round(state.n), k) }
			);
			stage.replaceChildren(makePascalSvg(Math.round(state.n), k, state.subset ?? []));
		} else if (kind === 'matrix') {
			const result = matrixStats(state.matrix);
			if (id === 'math-vectors-matrices-tensors') {
				message.push(
					{ label: 'elements', value: state.matrix.length * state.matrix[0].length },
					{ label: 'shape', value: `(3, 3)` },
					{ label: 'strides', value: '(3, 1)' }
				);
			} else if (id === 'math-rank-and-nullity') {
				message.push(
					{ label: 'rank', value: result.rank },
					{ label: 'nullity', value: state.matrix[0].length - result.rank },
					{
						label: 'rank + nullity',
						value: `${result.rank} + ${state.matrix[0].length - result.rank} = 3`
					}
				);
			} else if (id === 'math-matrix-inverse') {
				const determinant =
					state.matrix[0][0] * state.matrix[1][1] - state.matrix[0][1] * state.matrix[1][0];
				message.push(
					{ label: '2×2 determinant', value: number(determinant) },
					{
						label: 'inverse exists',
						value: Math.abs(determinant) < 1e-8 ? 'no' : 'yes'
					},
					{
						label: 'top-left inverse',
						value:
							Math.abs(determinant) < 1e-8
								? 'undefined'
								: `[${number(state.matrix[1][1] / determinant)}, ${number(-state.matrix[0][1] / determinant)}]`
					}
				);
			} else if (
				id === 'math-eigenvalues-eigenvectors' ||
				id === 'math-positive-definite-matrices'
			) {
				const [first, second] = matrixEigenvalues2x2(state.matrix);
				const positiveDefinite =
					state.matrix[0][0] > 0 &&
					state.matrix[0][0] * state.matrix[1][1] - state.matrix[0][1] * state.matrix[1][0] > 0;
				message.push(
					{ label: 'λ₁', value: number(first) },
					{ label: 'λ₂', value: number(second) },
					{
						label: id.includes('positive-definite') ? 'classification' : 'eigen directions',
						value: id.includes('positive-definite')
							? positiveDefinite
								? 'positive definite'
								: first * second < 0
									? 'indefinite'
									: 'not positive definite'
							: 'shown by matrix entries'
					}
				);
			} else if (id === 'math-svd') {
				const [first, second] = matrixEigenvalues2x2([
					[
						state.matrix[0][0] ** 2 + state.matrix[1][0] ** 2,
						state.matrix[0][0] * state.matrix[0][1] + state.matrix[1][0] * state.matrix[1][1]
					],
					[
						state.matrix[0][0] * state.matrix[0][1] + state.matrix[1][0] * state.matrix[1][1],
						state.matrix[0][1] ** 2 + state.matrix[1][1] ** 2
					]
				]);
				message.push(
					{ label: 'σ₁', value: number(Math.sqrt(Math.max(first, 0))) },
					{ label: 'σ₂', value: number(Math.sqrt(Math.max(second, 0))) },
					{ label: 'determinant', value: number(result.determinant) }
				);
			} else if (id === 'math-transpose') {
				message.push(
					{ label: 'shape before / after', value: '(3, 3) → (3, 3)' },
					{ label: 'strides before / after', value: '(3, 1) → (1, 3)' },
					{ label: 'trace', value: number(result.trace) }
				);
				stage.replaceChildren(
					makeMatrixSvg(state.matrix[0].map((_, column) => state.matrix.map((row) => row[column])))
				);
			} else if (id === 'math-trace-of-a-matrix') {
				message.push(
					{ label: 'trace before rotation', value: number(result.trace) },
					{ label: 'trace after rotation', value: number(result.trace) },
					{ label: 'determinant', value: number(result.determinant) }
				);
			} else if (id === 'math-matrix-multiplication') {
				const row = Math.floor(state.step / 3) % 3;
				const column = state.step % 3;
				const products = state.matrix[row].map(
					(value, index) => value * state.matrix[index][column]
				);
				message.push(
					{ label: 'output cell', value: `C[${row + 1}, ${column + 1}]` },
					{ label: 'partial sum', value: number(products.reduce((sum, value) => sum + value, 0)) },
					{ label: 'term products', value: products.map((value) => number(value, 1)).join(' + ') }
				);
			} else {
				message.push(
					{ label: 'trace', value: number(result.trace) },
					{ label: 'determinant', value: number(result.determinant) },
					{ label: 'rank', value: result.rank },
					{ label: 'step', value: `${state.step} / ${state.n}` }
				);
			}
			if (id !== 'math-transpose') {
				stage.replaceChildren(makeMatrixSvg(state.matrix, state.step % 9));
			}
		} else if (kind === 'vector') {
			const dot = state.primary * state.secondary + state.secondary;
			const angle =
				(Math.acos(
					Math.max(
						-1,
						Math.min(
							1,
							dot / (Math.hypot(state.primary, state.secondary) * Math.hypot(state.secondary, 1))
						)
					)
				) *
					180) /
				Math.PI;
			message.push(
				{ label: 'dot product', value: number(dot) },
				{ label: 'angle', value: `${number(angle, 1)}°` },
				{ label: '‖v‖₁', value: number(Math.abs(state.primary) + Math.abs(state.secondary)) },
				{ label: '‖v‖₂', value: number(Math.hypot(state.primary, state.secondary)) },
				{
					label: '‖v‖∞',
					value: number(Math.max(Math.abs(state.primary), Math.abs(state.secondary)))
				},
				{ label: 'projection scalar', value: number(dot / (state.secondary ** 2 + 1)) }
			);
			stage.replaceChildren(makeVectorSvg(state));
		} else if (kind === 'information') {
			const p = normalizedProbabilities(state.probabilities);
			const entropy = p.reduce((sum, value) => sum - value * Math.log2(value), 0);
			const crossEntropy = p.reduce(
				(sum, value, index) => sum - value * Math.log2(Math.max(p[(index + 1) % p.length], 1e-6)),
				0
			);
			message.push(
				{ label: 'H(p)', value: number(entropy, 3) },
				{ label: 'H(p,q)', value: number(crossEntropy, 3) },
				{ label: 'KL(p‖q)', value: number(Math.max(0, crossEntropy - entropy), 3) },
				{ label: 'maximum entropy', value: number(Math.log2(p.length), 3) }
			);
		} else if (kind === 'sets') {
			const [probabilityA, probabilityB] = state.probabilities;
			const probabilityIntersection = Math.min(state.probabilities[2], probabilityA, probabilityB);
			message.push(
				{ label: '|A|', value: number(probabilityA, 3) },
				{ label: '|B|', value: number(probabilityB, 3) },
				{ label: '|A∩B|', value: number(probabilityIntersection, 3) },
				{ label: '|A∪B|', value: number(probabilityA + probabilityB - probabilityIntersection, 3) }
			);
			stage.replaceChildren(
				makeSetSvg([probabilityA, probabilityB, probabilityIntersection], state.operation)
			);
		} else if (kind === 'joint') {
			const cells = jointTable(state.probabilities);
			const rows = [0, 1, 2].map((row) =>
				cells.slice(row * 3, row * 3 + 3).reduce((sum, value) => sum + value, 0)
			);
			const columns = [0, 1, 2].map(
				(column) => cells[column] + cells[column + 3] + cells[column + 6]
			);
			if (id === 'math-conditional-probability') {
				const selected = state.conditionRow;
				const conditional = cells.slice(selected * 3, selected * 3 + 3);
				const total = rows[selected];
				message.push(
					{ label: 'P(X=x)', value: number(total, 3) },
					{
						label: 'conditional values',
						value: conditional.map((value) => number(value / total, 2)).join(', ')
					},
					{
						label: 'conditional sum',
						value: number(
							conditional.reduce((sum, value) => sum + value / total, 0),
							3
						)
					}
				);
			} else if (id === 'math-mutual-information') {
				/** @param {number[]} values */
				const entropy = (values) =>
					values.reduce((sum, value) => sum - value * Math.log2(Math.max(value, 1e-12)), 0);
				const jointEntropy = entropy(cells);
				const entropyX = entropy(rows);
				const entropyY = entropy(columns);
				message.push(
					{ label: 'I(X;Y)', value: number(entropyX + entropyY - jointEntropy, 3) },
					{ label: 'H(X)', value: number(entropyX, 3) },
					{ label: 'H(Y)', value: number(entropyY, 3) },
					{ label: 'H(X,Y)', value: number(jointEntropy, 3) }
				);
			} else {
				message.push(
					{ label: 'row sums', value: rows.map((value) => number(value, 2)).join(', ') },
					{ label: 'column sums', value: columns.map((value) => number(value, 2)).join(', ') },
					{
						label: 'total',
						value: number(
							cells.reduce((sum, value) => sum + value, 0),
							3
						)
					}
				);
			}
			stage.replaceChildren(makeJointSvg(state.probabilities));
		} else if (kind === 'probability' && id === 'math-independence') {
			const probabilityA = state.primary;
			const probabilityB = state.secondary;
			const intersection = Math.max(
				probabilityA + probabilityB - 1,
				Math.min(state.n, probabilityA, probabilityB)
			);
			const expectedIntersection = probabilityA * probabilityB;
			message.push(
				{ label: 'P(A)', value: number(probabilityA, 3) },
				{ label: 'P(B)', value: number(probabilityB, 3) },
				{ label: 'P(A∩B)', value: number(intersection, 3) },
				{ label: 'P(A)·P(B)', value: number(expectedIntersection, 3) },
				{ label: 'P(A|B)', value: number(intersection / Math.max(probabilityB, 1e-12), 3) },
				{
					label: 'independence',
					value: Math.abs(intersection - expectedIntersection) < 0.015 ? 'yes' : 'no'
				}
			);
		} else if (kind === 'probability' && id === 'math-bayes-theorem') {
			const prior = state.primary;
			const likelihoodGivenHypothesis = state.secondary;
			const likelihoodWithoutHypothesis = state.n;
			const evidence =
				prior * likelihoodGivenHypothesis + (1 - prior) * likelihoodWithoutHypothesis;
			message.push(
				{ label: 'P(H)', value: number(prior, 3) },
				{ label: 'P(E|H)', value: number(likelihoodGivenHypothesis, 3) },
				{ label: 'P(E|¬H)', value: number(likelihoodWithoutHypothesis, 3) },
				{ label: 'P(E)', value: number(evidence, 3) },
				{
					label: 'P(H|E)',
					value: number((prior * likelihoodGivenHypothesis) / Math.max(evidence, 1e-12), 3)
				}
			);
		} else if (kind === 'probability') {
			const prior = Math.min(0.99, Math.max(0.01, state.primary));
			const likelihood = Math.min(0.99, Math.max(0.01, state.secondary));
			const posterior =
				(prior * likelihood) / (prior * likelihood + (1 - prior) * (1 - likelihood));
			message.push(
				{ label: 'P(A) / prior', value: number(prior, 3) },
				{ label: 'P(B|A) / likelihood', value: number(likelihood, 3) },
				{ label: 'P(A∩B) / posterior', value: number(posterior, 3) },
				{ label: state.probabilityView, value: number(prior * likelihood, 3) }
			);
		} else if (
			id === 'math-covariance-correlation' ||
			id === 'math-expectation-variance-covariance'
		) {
			const point = pointStatistics(state.points);
			message.push(
				{ label: 'E[X]', value: number(point.meanX) },
				{ label: 'E[Y]', value: number(point.meanY) },
				{ label: 'Cov(X,Y)', value: number(point.covariance) },
				{ label: 'sample correlation', value: number(point.correlation) },
				...(id === 'math-covariance-correlation'
					? [{ label: 'target ρ', value: number(state.primary) }]
					: [
							{ label: 'Var(X)', value: number(point.varianceX) },
							{ label: 'Var(Y)', value: number(point.varianceY) }
						])
			);
		} else if (id === 'math-expectation-variance') {
			const mean = state.samples.length
				? state.samples.reduce((sum, value) => sum + value, 0) / state.samples.length
				: 0;
			const variance = state.samples.length
				? state.samples.reduce((sum, value) => sum + (value - mean) ** 2, 0) / state.samples.length
				: 0;
			message.push(
				{ label: 'current N', value: state.samples.length },
				{ label: 'sample mean', value: number(mean) },
				{ label: 'sample variance', value: number(variance) },
				{
					label: 'true mean / variance',
					value: `${number(state.primary)} / ${number(state.secondary ** 2)}`
				},
				{ label: 'mean error', value: number(Math.abs(mean - state.primary)) }
			);
		} else if (id === 'math-random-variables') {
			const mean = state.samples.length
				? state.samples.reduce((sum, value) => sum + value, 0) / state.samples.length
				: 0;
			const empiricalProbability = state.samples.length
				? state.samples.filter((sample) => sample === 1).length / state.samples.length
				: 0;
			message.push(
				{ label: 'samples drawn', value: state.samples.length },
				{
					label: state.variableMode === 'discrete' ? 'P(X=1), empirical / true' : 'sample mean',
					value:
						state.variableMode === 'discrete'
							? `${number(empiricalProbability, 3)} / 0.167`
							: number(mean)
				},
				{ label: 'mode', value: state.variableMode },
				{ label: 'outcomes', value: state.variableMode === 'discrete' ? '1–6' : 'continuous' }
			);
		} else if (kind === 'calculus') {
			const x = state.primary;
			const h = Math.max(state.secondary, 0.001);
			if (id === 'math-derivatives-first-principles') {
				message.push(
					{ label: 'secant slope', value: number(((x + h) ** 2 - x ** 2) / h) },
					{ label: 'h', value: number(h, 3) },
					{ label: 'true derivative', value: number(2 * x) }
				);
			} else if (id === 'math-partial-derivatives') {
				message.push(
					{ label: '∂f/∂x', value: number(2 * x) },
					{ label: '∂f/∂y', value: number(2 * h) },
					{ label: 'f(x,y)', value: number(x * x + h * h) }
				);
			} else if (id === 'math-chain-rule') {
				const inner = x * x;
				message.push(
					{ label: 'g(x)', value: number(inner) },
					{ label: "f'(g(x))", value: number(Math.cos(inner)) },
					{ label: "g'(x)", value: number(2 * x) },
					{ label: 'chain derivative', value: number(2 * x * Math.cos(inner)) }
				);
			} else if (id === 'math-hessian') {
				/** @param {number} value */
				const f = (value) => value * value * Math.cos(value / 2);
				message.push(
					{ label: 'f(x)', value: number(f(x)) },
					{ label: 'second derivative', value: number((f(x + h) - 2 * f(x) + f(x - h)) / (h * h)) },
					{ label: 'step h', value: number(h, 3) }
				);
			} else if (id === 'math-directional-derivatives') {
				message.push(
					{ label: 'gradient', value: `[${number(2 * x)}, ${number(2 * h)}]` },
					{
						label: 'directional derivative',
						value: number(2 * x * Math.cos(h) + 2 * h * Math.sin(h))
					},
					{ label: 'direction angle', value: `${number((h * 180) / Math.PI, 1)}°` }
				);
			} else if (id === 'math-jacobian') {
				message.push(
					{
						label: 'df/dx',
						value: number(
							(functionValue(id, x + h, state) - functionValue(id, x - h, state)) / (2 * h)
						)
					},
					{ label: 'input x', value: number(x) },
					{ label: 'finite-difference h', value: number(h, 3) }
				);
			} else if (id === 'math-taylor-series') {
				message.push(
					{ label: 'approximation order', value: Math.round(state.n) },
					{ label: 'sin(x)', value: number(Math.sin(x)) },
					{ label: 'local approximation', value: number(taylorSin(x, Math.round(state.n))) }
				);
			} else {
				message.push(
					{ label: 'loss', value: number((x - 1.2) ** 2) },
					{ label: 'gradient magnitude', value: number(Math.abs(2 * (x - 1.2))) },
					{ label: 'learning rate / step', value: number(h, 3) },
					{ label: 'iteration', value: state.step }
				);
			}
		} else {
			const mean = state.samples.length
				? state.samples.reduce((sum, value) => sum + value, 0) / state.samples.length
				: state.primary;
			const variance = state.samples.length
				? state.samples.reduce((sum, value) => sum + (value - mean) ** 2, 0) / state.samples.length
				: state.secondary ** 2;
			const slope =
				(functionValue(id, state.primary + 0.01, state) -
					functionValue(id, state.primary - 0.01, state)) /
				0.02;
			message.push(
				{ label: 'samples / iteration', value: state.samples.length || state.step },
				{ label: 'mean / f(x)', value: number(mean) },
				{ label: 'variance / slope', value: number(variance || slope) },
				{ label: 'true mean / target', value: number(state.primary) }
			);
		}
		stats.update(message);
		drawNow();
	}

	function drawNow() {
		if (['matrix', 'vector', 'combination', 'joint', 'sets'].includes(kind)) return;
		const context = plot.element.getContext('2d');
		const rect = plot.element.getBoundingClientRect();
		if (context && rect.width && rect.height) draw(context, rect.width, rect.height);
	}

	/** @param {CanvasRenderingContext2D} context @param {number} width @param {number} height */
	function draw(context, width, height) {
		context.clearRect(0, 0, width, height);
		context.fillStyle = '#0a0a0b';
		context.fillRect(0, 0, width, height);
		context.strokeStyle = 'rgba(255,255,255,0.08)';
		context.lineWidth = 1;
		for (let index = 1; index < 5; index++) {
			const y = (height * index) / 5;
			context.beginPath();
			context.moveTo(0, y);
			context.lineTo(width, y);
			context.stroke();
		}

		if (id === 'math-expectation-variance') {
			const referenceMean = state.primary;
			const referenceVariance = state.secondary ** 2;
			const maxVariance = Math.max(referenceVariance * 2, 1);
			let total = 0;
			let squares = 0;
			const runningStats = state.samples.map((sample, index) => {
				total += sample;
				squares += sample * sample;
				const mean = total / (index + 1);
				return {
					mean,
					variance: Math.max(0, squares / (index + 1) - mean * mean)
				};
			});
			context.strokeStyle = '#ef4444';
			context.lineWidth = 2;
			context.beginPath();
			runningStats.forEach(({ mean }, index) => {
				const y = height - 18 - ((mean + 3) / 6) * (height - 36);
				const x = ((index + 1) / Math.max(runningStats.length, 1)) * width;
				if (index === 0) context.moveTo(x, y);
				else context.lineTo(x, y);
			});
			context.stroke();
			context.strokeStyle = '#f0b429';
			context.beginPath();
			runningStats.forEach(({ variance }, index) => {
				const y = height - 18 - (variance / maxVariance) * (height - 36);
				const x = ((index + 1) / Math.max(runningStats.length, 1)) * width;
				if (index === 0) context.moveTo(x, y);
				else context.lineTo(x, y);
			});
			context.stroke();
			/** @param {string} color @param {number} y */
			const drawReferenceLine = (color, y) => {
				context.strokeStyle = color;
				context.setLineDash([5, 4]);
				context.beginPath();
				context.moveTo(0, y);
				context.lineTo(width, y);
				context.stroke();
			};
			drawReferenceLine('#ef4444', height - 18 - ((referenceMean + 3) / 6) * (height - 36));
			drawReferenceLine('#f0b429', height - 18 - (referenceVariance / maxVariance) * (height - 36));
			context.setLineDash([]);
		} else if (
			state.points.length &&
			(id === 'math-covariance-correlation' || id === 'math-expectation-variance-covariance')
		) {
			context.fillStyle = 'rgba(239,68,68,0.75)';
			for (const [x, y] of state.points) {
				context.beginPath();
				context.arc(
					width / 2 + x * (width / 12),
					height / 2 - y * (height / 12),
					3,
					0,
					2 * Math.PI
				);
				context.fill();
			}
		} else if (kind === 'series' || kind === 'combination') {
			const count =
				kind === 'series'
					? Math.min(Math.round(state.step), 20)
					: Math.max(1, Math.min(Math.round(state.n), 20));
			const values = Array.from({ length: count }, (_, index) => {
				const i = index + 1;
				if (state.expression === 'i²') return i * i;
				if (state.expression === '1/i') return 1 / i;
				if (state.expression === '2i−1') return 2 * i - 1;
				if (state.expression === '(i+1)/i') return (i + 1) / i;
				return i;
			});
			/** @type {number[]} */
			const cumulative = [];
			values.reduce(
				(accumulator, value) => {
					const next = id.includes('product') ? accumulator * value : accumulator + value;
					cumulative.push(next);
					return next;
				},
				id.includes('product') ? 1 : 0
			);
			const max = Math.max(...values, 1);
			context.fillStyle = '#ef4444';
			values.forEach((value, index) => {
				const barWidth = width / values.length;
				const heightValue = id.includes('product') && state.logScale ? Math.log1p(value) : value;
				const scaleMax = id.includes('product') && state.logScale ? Math.log1p(max) : max;
				const barHeight = (heightValue / scaleMax) * (height - 38);
				context.fillRect(
					index * barWidth + 4,
					height - barHeight - 22,
					Math.max(barWidth - 8, 1),
					barHeight
				);
				context.fillStyle = '#a1a1aa';
				context.font = '11px ui-monospace, monospace';
				context.fillText(String(index + 1), index * barWidth + 5, height - 6);
				context.fillStyle = '#ef4444';
			});
			if (kind === 'series' && cumulative.length) {
				const cumulativeMax = Math.max(...cumulative, 1);
				context.strokeStyle = '#f0b429';
				context.lineWidth = 2;
				context.beginPath();
				cumulative.forEach((value, index) => {
					const x = ((index + 0.5) / cumulative.length) * width;
					const scaled = id.includes('product') && state.logScale ? Math.log1p(value) : value;
					const maxScaled =
						id.includes('product') && state.logScale ? Math.log1p(cumulativeMax) : cumulativeMax;
					const y = height - 22 - (scaled / maxScaled) * (height - 38);
					if (index === 0) context.moveTo(x, y);
					else context.lineTo(x, y);
				});
				context.stroke();
			}
		} else if (
			kind === 'sampling' &&
			id === 'math-random-variables' &&
			state.variableMode === 'discrete'
		) {
			const counts = new Array(6).fill(0);
			state.samples.forEach((sample) => {
				if (sample >= 1 && sample <= 6) counts[sample - 1] += 1;
			});
			const peak = Math.max(...counts, 1);
			const barWidth = width / counts.length;
			counts.forEach((value, index) => {
				const barHeight = (value / peak) * (height - 40);
				context.fillStyle = '#ef4444';
				context.fillRect(index * barWidth + 4, height - barHeight - 24, barWidth - 8, barHeight);
				context.fillStyle = '#d4d4d8';
				context.font = '12px ui-monospace, monospace';
				context.fillText(String(index + 1), index * barWidth + barWidth / 2, height - 7);
			});
		} else if (kind === 'sampling' || kind === 'distribution') {
			const left = 8;
			const right = width - 8;
			const top = 12;
			const bottom = height - 14;
			const binCount = 32;
			const bins = new Array(binCount).fill(0);
			for (const sample of state.samples) {
				const bin = Math.floor(
					((sample - state.primary + 4 * state.secondary) / (8 * state.secondary)) * binCount
				);
				if (bin >= 0 && bin < binCount) bins[bin] += 1;
			}
			const peak = Math.max(...bins, 1);
			context.fillStyle = 'rgba(239,68,68,0.45)';
			bins.forEach((value, index) => {
				const barWidth = (right - left) / binCount;
				const barHeight = (value / peak) * (bottom - top) * 0.82;
				context.fillRect(
					left + index * barWidth,
					bottom - barHeight,
					Math.max(barWidth - 1, 1),
					barHeight
				);
			});
			context.strokeStyle = '#ef4444';
			context.lineWidth = 2;
			context.beginPath();
			for (let px = 0; px <= width; px++) {
				const x = (px / width) * 8 - 4;
				const y =
					state.distribution === 'uniform'
						? Math.abs(x) <= state.secondary
							? 1 / (2 * state.secondary)
							: 0
						: state.distribution === 'exponential'
							? x >= 0
								? Math.exp(-x / state.secondary) / state.secondary
								: 0
							: state.distribution === 'binomial'
								? normalPdf(x, 5, 1.2)
								: normalPdf(x, 0, 1);
				const py = bottom - (y / normalPdf(0, 0, 1)) * (bottom - top) * 0.82;
				if (px === 0) context.moveTo(px, py);
				else context.lineTo(px, py);
			}
			context.stroke();
		} else if (
			kind === 'information' ||
			kind === 'joint' ||
			kind === 'sets' ||
			kind === 'probability'
		) {
			const probabilities = normalizedProbabilities(state.probabilities);
			const values =
				kind === 'information' || kind === 'joint' || kind === 'sets'
					? probabilities
					: id === 'math-bayes-theorem'
						? [state.primary, state.secondary, state.n]
						: id === 'math-independence'
							? [state.primary, state.secondary, Math.min(state.n, state.primary, state.secondary)]
							: [state.primary, state.secondary, Math.min(1, state.primary * state.secondary)];
			const peak = Math.max(...values, 0.01);
			const barWidth = width / values.length;
			values.forEach((value, index) => {
				const barHeight = (value / peak) * (height - 46);
				context.fillStyle = index % 2 ? '#f0b429' : '#ef4444';
				context.fillRect(
					index * barWidth + 8,
					height - barHeight - 24,
					Math.max(barWidth - 16, 1),
					barHeight
				);
				context.fillStyle = '#d4d4d8';
				context.font = '12px ui-monospace, monospace';
				context.fillText(`p${index + 1}`, index * barWidth + 12, height - 7);
			});
		} else if (kind === 'growth') {
			const maxN = Math.round(state.n);
			/** @type {((x: number) => number)[]} */
			const functions = [
				() => 1,
				(x) => Math.log2(x + 1),
				(x) => x,
				(x) => x * Math.log2(x + 1),
				(x) => x * x,
				(x) => Math.min(2 ** x, 1e12)
			];
			const scale = Math.max(...functions.map((fn) => fn(maxN)), 1);
			const colors = ['#a1a1aa', '#60a5fa', '#34d399', '#f0b429', '#fb7185', '#ef4444'];
			functions.forEach((fn, curve) => {
				context.strokeStyle = colors[curve];
				context.beginPath();
				for (let px = 0; px <= width; px++) {
					const n = 1 + (px / width) * (maxN - 1);
					const value = Math.log1p(fn(n)) / Math.log1p(scale);
					const py = height - 18 - value * (height - 36);
					if (px === 0) context.moveTo(px, py);
					else context.lineTo(px, py);
				}
				context.stroke();
			});
			context.strokeStyle = '#f0b429';
			context.setLineDash([4, 4]);
			const markerX = (state.primary / maxN) * width;
			context.beginPath();
			context.moveTo(markerX, 0);
			context.lineTo(markerX, height);
			context.stroke();
			context.setLineDash([]);
		} else {
			const xMin = -4;
			const xMax = 4;
			const yValues = [];
			for (let index = 0; index <= width; index++) {
				const x = xMin + (index / width) * (xMax - xMin);
				yValues.push(functionValue(id, x, state));
			}
			const min = Math.min(...yValues);
			const max = Math.max(...yValues, min + 1);
			context.strokeStyle = '#ef4444';
			context.lineWidth = 2.5;
			context.beginPath();
			yValues.forEach((value, index) => {
				const y = height - 16 - ((value - min) / (max - min)) * (height - 32);
				if (index === 0) context.moveTo(index, y);
				else context.lineTo(index, y);
			});
			context.stroke();
			const markX = ((state.primary + 4) / 8) * width;
			context.strokeStyle = '#f0b429';
			context.setLineDash([5, 4]);
			context.beginPath();
			context.moveTo(markX, 0);
			context.lineTo(markX, height);
			context.stroke();
			context.setLineDash([]);
		}
	}

	/** @param {Event} event */
	function onProbabilityInput(event) {
		const input = event.currentTarget;
		if (!(input instanceof HTMLInputElement)) return;
		const index = Number(input.dataset.index);
		state.probabilities[index] = Number(input.value);
		const output = input.parentElement?.querySelector('output');
		if (output) output.textContent = number(state.probabilities[index], 2);
		update();
	}
	if (kind === 'information' || kind === 'joint' || kind === 'sets') {
		const probabilityControls = document.createElement('div');
		probabilityControls.className = 'viz-probability-controls';
		state.probabilities.forEach((value, index) => {
			const label = document.createElement('label');
			const name = document.createElement('span');
			name.textContent = kind === 'sets' ? ['P(A)', 'P(B)', 'P(A∩B)'][index] : `p${index + 1}`;
			const input = document.createElement('input');
			input.type = 'range';
			input.min = '0.02';
			input.max = '1';
			input.step = '0.01';
			input.value = String(value);
			input.dataset.index = String(index);
			input.setAttribute('aria-label', `Probability ${index + 1}`);
			input.addEventListener('input', onProbabilityInput);
			listeners.push(() => input.removeEventListener('input', onProbabilityInput));
			const output = document.createElement('output');
			output.textContent = number(value, 2);
			label.append(name, output, input);
			resetters.push(() => {
				input.value = String([0.5, 0.3, 0.2][index]);
				output.textContent = number([0.5, 0.3, 0.2][index], 2);
			});
			probabilityControls.append(label);
		});
		controls.prepend(probabilityControls);
	}

	if (id === 'math-conditional-probability') {
		const condition = document.createElement('select');
		condition.className = 'viz-select';
		condition.setAttribute('aria-label', 'Condition on row');
		for (let row = 0; row < 3; row++) {
			const option = document.createElement('option');
			option.value = String(row);
			option.textContent = `Condition on row ${row + 1}`;
			condition.append(option);
		}
		const onConditionChange = () => {
			state.conditionRow = Number(condition.value);
			update();
		};
		condition.addEventListener('change', onConditionChange);
		listeners.push(() => condition.removeEventListener('change', onConditionChange));
		resetters.push(() => {
			state.conditionRow = 0;
			condition.value = '0';
		});
		controls.prepend(condition);
	}

	if (kind === 'matrix') {
		const matrixControls = document.createElement('div');
		matrixControls.className = 'viz-matrix-controls';
		state.matrix.flat().forEach((value, index) => {
			const input = document.createElement('input');
			input.type = 'number';
			input.value = String(value);
			input.setAttribute(
				'aria-label',
				`Matrix element ${Math.floor(index / 3) + 1}, ${(index % 3) + 1}`
			);
			const handler = () => {
				state.matrix[Math.floor(index / 3)][index % 3] = Number(input.value) || 0;
				update();
			};
			input.addEventListener('input', handler);
			listeners.push(() => input.removeEventListener('input', handler));
			matrixControls.append(input);
			resetters.push(() => {
				input.value = String(initialMatrix[Math.floor(index / 3)][index % 3]);
			});
		});
		controls.prepend(matrixControls);
	}

	if (kind === 'sets' || kind === 'probability' || kind === 'distribution') {
		const mode = document.createElement('select');
		mode.className = 'viz-select';
		mode.setAttribute('aria-label', 'Visualization preset');
		const options =
			kind === 'distribution'
				? ['Normal', 'Uniform', 'Exponential', 'Binomial']
				: kind === 'sets'
					? ['Union', 'Intersection', 'Difference', 'Complement']
					: ['Prior', 'Likelihood', 'Posterior'];
		options.forEach((label) => {
			const option = document.createElement('option');
			option.textContent = label;
			option.value = label.toLowerCase();
			mode.append(option);
		});
		const onModeChange = () => {
			if (kind === 'distribution') state.distribution = mode.value;
			else if (kind === 'sets') state.operation = mode.value;
			else state.probabilityView = mode.value;
			update();
		};
		mode.addEventListener('change', onModeChange);
		listeners.push(() => mode.removeEventListener('change', onModeChange));
		resetters.push(() => {
			mode.selectedIndex = 0;
			if (kind === 'distribution') state.distribution = 'normal';
			else if (kind === 'sets') state.operation = 'union';
			else state.probabilityView = 'prior';
		});
		controls.prepend(mode);
	}
	if (id === 'math-random-variables') {
		const mode = document.createElement('select');
		mode.className = 'viz-select';
		mode.setAttribute('aria-label', 'Random variable type');
		for (const value of ['discrete', 'continuous']) {
			const option = document.createElement('option');
			option.value = value;
			option.textContent = value === 'discrete' ? 'Discrete outcomes' : 'Continuous density';
			mode.append(option);
		}
		const onVariableModeChange = () => {
			state.variableMode = mode.value;
			state.samples = [];
			update();
		};
		mode.addEventListener('change', onVariableModeChange);
		listeners.push(() => mode.removeEventListener('change', onVariableModeChange));
		resetters.push(() => {
			state.variableMode = 'discrete';
			mode.value = 'discrete';
		});
		controls.prepend(mode);
	}
	if (id.includes('product')) {
		const label = document.createElement('label');
		label.className = 'viz-toggle';
		const toggle = document.createElement('input');
		toggle.type = 'checkbox';
		const onScaleChange = () => {
			state.logScale = toggle.checked;
			update();
		};
		toggle.addEventListener('change', onScaleChange);
		listeners.push(() => toggle.removeEventListener('change', onScaleChange));
		label.append(toggle, document.createTextNode('Log scale'));
		controls.prepend(label);
		resetters.push(() => {
			toggle.checked = false;
			state.logScale = false;
		});
	}

	root.replaceChildren(shell);
	root.classList.add('tt-widget');
	update();

	return () => {
		for (const timer of timers) window.clearInterval(timer);
		timers.clear();
		plot.destroy();
		listeners.forEach((remove) => remove());
		root.replaceChildren();
	};
}

export const mathVisualizerIds = Object.keys(specs);
