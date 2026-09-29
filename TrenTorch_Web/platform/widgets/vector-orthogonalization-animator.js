// Widget for `math-gram-schmidt`: steps through orthonormalizing a fixed
// set of 2D vectors, drawing the current basis so far, the vector being
// processed, its projection onto each earlier basis vector (dashed), and
// the resulting orthogonal component before normalization. Expects a
// `[data-widget="vector-orthogonalization-animator"]` root containing
// `#voacanvas`, `#stepBackBtn`, `#stepForwardBtn`, `#resetBtn`,
// `#stepLabel`, `#stepDescription`.
import { observeCanvasResize } from './widget-base.js';

// Two starting vectors, deliberately not orthogonal.
const INPUT_VECTORS = [
	[3, 1],
	[2, 2]
];

/**
 * @param {number[]} a
 * @param {number[]} b
 */
function dot(a, b) {
	return a[0] * b[0] + a[1] * b[1];
}
/** @param {number[]} a */
function norm(a) {
	return Math.sqrt(dot(a, a));
}
/**
 * @param {number[]} a
 * @param {number} s
 */
function scale(a, s) {
	return [a[0] * s, a[1] * s];
}
/**
 * @param {number[]} a
 * @param {number[]} b
 */
function sub(a, b) {
	return [a[0] - b[0], a[1] - b[1]];
}

/**
 * Builds one animation frame per vector: the projection subtracted (if
 * any earlier basis vector exists) and the resulting normalized basis
 * vector.
 * @returns {{basisSoFar: number[][], current: number[], projection: number[] | null, orthogonal: number[], description: string}[]}
 */
function computeFrames() {
	/** @type {number[][]} */
	const basis = [];
	/** @type {ReturnType<typeof computeFrames>} */
	const frames = [];

	INPUT_VECTORS.forEach((v, idx) => {
		let orthogonal = [...v];
		let projection = null;
		if (basis.length > 0) {
			const u = basis[basis.length - 1];
			const coeff = dot(v, u) / dot(u, u);
			projection = scale(u, coeff);
			orthogonal = sub(v, projection);
		}
		const unit = scale(orthogonal, 1 / norm(orthogonal));
		frames.push({
			basisSoFar: basis.map((b) => [...b]),
			current: v,
			projection,
			orthogonal: unit,
			description:
				idx === 0
					? `Vector 1 has no earlier basis vector to project against -- normalize it directly.`
					: `Subtract vector ${idx + 1}'s projection onto the previous basis vector (dashed), then normalize what's left.`
		});
		basis.push(unit);
	});

	frames.push({
		basisSoFar: basis.map((b) => [...b]),
		current: [0, 0],
		projection: null,
		orthogonal: [0, 0],
		description: `Done -- an orthonormal basis built one vector at a time.`
	});

	return frames;
}

/** @param {HTMLElement} root */
export function mount(root) {
	const canvas = /** @type {HTMLCanvasElement} */ (root.querySelector('#voacanvas'));
	const stepBackBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#stepBackBtn'));
	const stepForwardBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#stepForwardBtn'));
	const resetBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#resetBtn'));
	const stepLabel = /** @type {HTMLElement} */ (root.querySelector('#stepLabel'));
	const stepDescription = /** @type {HTMLElement} */ (root.querySelector('#stepDescription'));

	const ctx = /** @type {CanvasRenderingContext2D} */ (canvas.getContext('2d'));
	const frames = computeFrames();
	let current = 0;

	const scaleFactor = 40; // pixels per unit
	/**
	 * @param {number[]} p
	 * @param {number} w
	 * @param {number} h
	 */
	function toScreen(p, w, h) {
		return [w / 2 + p[0] * scaleFactor, h / 2 - p[1] * scaleFactor];
	}

	/**
	 * @param {number[]} from
	 * @param {number[]} to
	 * @param {string} color
	 * @param {boolean} dashed
	 * @param {number} w
	 * @param {number} h
	 */
	function drawArrow(from, to, color, dashed, w, h) {
		const [x0, y0] = toScreen(from, w, h);
		const [x1, y1] = toScreen(to, w, h);
		ctx.strokeStyle = color;
		ctx.fillStyle = color;
		ctx.lineWidth = 2;
		ctx.setLineDash(dashed ? [5, 4] : []);
		ctx.beginPath();
		ctx.moveTo(x0, y0);
		ctx.lineTo(x1, y1);
		ctx.stroke();
		ctx.setLineDash([]);

		const angle = Math.atan2(y1 - y0, x1 - x0);
		const headLen = 8;
		ctx.beginPath();
		ctx.moveTo(x1, y1);
		ctx.lineTo(
			x1 - headLen * Math.cos(angle - Math.PI / 6),
			y1 - headLen * Math.sin(angle - Math.PI / 6)
		);
		ctx.lineTo(
			x1 - headLen * Math.cos(angle + Math.PI / 6),
			y1 - headLen * Math.sin(angle + Math.PI / 6)
		);
		ctx.closePath();
		ctx.fill();
	}

	function draw() {
		const w = canvas.clientWidth;
		const h = canvas.clientHeight;
		ctx.clearRect(0, 0, w, h);

		ctx.strokeStyle = 'rgba(255,255,255,0.08)';
		ctx.lineWidth = 1;
		ctx.beginPath();
		ctx.moveTo(0, h / 2);
		ctx.lineTo(w, h / 2);
		ctx.moveTo(w / 2, 0);
		ctx.lineTo(w / 2, h);
		ctx.stroke();

		const frame = frames[current];
		frame.basisSoFar.forEach((b) => drawArrow([0, 0], b, '#6bbf8a', false, w, h));
		if (frame.projection) {
			drawArrow([0, 0], frame.projection, '#f0b429', true, w, h);
		}
		if (frame.current[0] !== 0 || frame.current[1] !== 0) {
			drawArrow([0, 0], frame.current, '#ef4444', false, w, h);
		}
	}

	function render() {
		draw();
		stepLabel.textContent = `${current} / ${frames.length - 1}`;
		stepDescription.textContent = frames[current].description;
		stepBackBtn.disabled = current === 0;
		stepForwardBtn.disabled = current === frames.length - 1;
	}

	function onBack() {
		if (current > 0) {
			current -= 1;
			render();
		}
	}
	function onForward() {
		if (current < frames.length - 1) {
			current += 1;
			render();
		}
	}
	function onReset() {
		current = 0;
		render();
	}

	stepBackBtn.addEventListener('click', onBack);
	stepForwardBtn.addEventListener('click', onForward);
	resetBtn.addEventListener('click', onReset);

	const disconnectResize = observeCanvasResize(canvas, draw);
	render();

	return () => {
		stepBackBtn.removeEventListener('click', onBack);
		stepForwardBtn.removeEventListener('click', onForward);
		resetBtn.removeEventListener('click', onReset);
		disconnectResize();
	};
}
