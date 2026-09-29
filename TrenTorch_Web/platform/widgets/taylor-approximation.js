// Widget for `math-taylor-series`: draws f(x) = sin(x) alongside its
// 1st-order (tangent line) and 2nd-order (parabola) Taylor
// approximations centered at an adjustable point `a`, so the learner can
// drag `a` and see both approximations stay accurate near it and
// diverge away from it. Expects a
// `[data-widget="taylor-approximation"]` root containing `#tacanvas`,
// `#aSlider`, `#aVal`, `#roA`, `#roError1`, `#roError2`.
import { observeCanvasResize, bindRange, fmt } from './widget-base.js';

/** @param {number} x */
function f(x) {
	return Math.sin(x);
}
/** @param {number} x */
function fPrime(x) {
	return Math.cos(x);
}
/** @param {number} x */
function fDoublePrime(x) {
	return -Math.sin(x);
}

/**
 * @param {number} x
 * @param {number} a
 */
function firstOrder(x, a) {
	return f(a) + fPrime(a) * (x - a);
}
/**
 * @param {number} x
 * @param {number} a
 */
function secondOrder(x, a) {
	return f(a) + fPrime(a) * (x - a) + (fDoublePrime(a) / 2) * (x - a) ** 2;
}

/** @param {HTMLElement} root */
export function mount(root) {
	const canvas = /** @type {HTMLCanvasElement} */ (root.querySelector('#tacanvas'));
	const aSlider = /** @type {HTMLInputElement} */ (root.querySelector('#aSlider'));
	const aVal = /** @type {HTMLElement} */ (root.querySelector('#aVal'));
	const roA = /** @type {HTMLElement} */ (root.querySelector('#roA'));
	const roError1 = /** @type {HTMLElement} */ (root.querySelector('#roError1'));
	const roError2 = /** @type {HTMLElement} */ (root.querySelector('#roError2'));

	const ctx = /** @type {CanvasRenderingContext2D} */ (canvas.getContext('2d'));
	const xMin = -6;
	const xMax = 6;
	const yMin = -2.5;
	const yMax = 2.5;

	/**
	 * @param {number} x
	 * @param {number} y
	 * @param {number} w
	 * @param {number} h
	 */
	function toScreen(x, y, w, h) {
		return [((x - xMin) / (xMax - xMin)) * w, h - ((y - yMin) / (yMax - yMin)) * h];
	}

	/**
	 * @param {(x: number) => number} fn
	 * @param {string} color
	 * @param {number} w
	 * @param {number} h
	 */
	function drawCurve(fn, color, w, h) {
		ctx.strokeStyle = color;
		ctx.lineWidth = 2;
		ctx.beginPath();
		for (let px = 0; px <= w; px++) {
			const x = xMin + (px / w) * (xMax - xMin);
			const y = fn(x);
			const [, py] = toScreen(x, y, w, h);
			if (px === 0) ctx.moveTo(px, py);
			else ctx.lineTo(px, py);
		}
		ctx.stroke();
	}

	function draw() {
		const w = canvas.clientWidth;
		const h = canvas.clientHeight;
		ctx.clearRect(0, 0, w, h);

		const a = parseFloat(aSlider.value);

		ctx.strokeStyle = 'rgba(255,255,255,0.06)';
		ctx.lineWidth = 1;
		const [, zeroY] = toScreen(0, 0, w, h);
		ctx.beginPath();
		ctx.moveTo(0, zeroY);
		ctx.lineTo(w, zeroY);
		ctx.stroke();

		drawCurve(f, '#e4e4e7', w, h);
		drawCurve((x) => secondOrder(x, a), '#f0b429', w, h);
		drawCurve((x) => firstOrder(x, a), '#ef4444', w, h);

		const [ax, ay] = toScreen(a, f(a), w, h);
		ctx.fillStyle = '#6bbf8a';
		ctx.beginPath();
		ctx.arc(ax, ay, 5, 0, Math.PI * 2);
		ctx.fill();
	}

	function updateReadouts() {
		const a = parseFloat(aSlider.value);
		aVal.textContent = fmt(a, 2);
		roA.textContent = fmt(a, 2);
		const testX = a + 2;
		roError1.textContent = fmt(Math.abs(f(testX) - firstOrder(testX, a)), 4);
		roError2.textContent = fmt(Math.abs(f(testX) - secondOrder(testX, a)), 4);
	}

	const unbindA = bindRange(aSlider, () => {
		updateReadouts();
		draw();
	});

	const disconnectResize = observeCanvasResize(canvas, draw);
	updateReadouts();

	return () => {
		unbindA();
		disconnectResize();
	};
}
