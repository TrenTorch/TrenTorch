// Widget for `math-gradient-descent`: runs gradient descent on a fixed
// 1D loss curve f(x) = x^2 + 2*sin(3x) (a bumpy bowl, so a too-large
// learning rate visibly overshoots), stepping one iteration at a time or
// auto-playing. Expects a `[data-widget="gradient-descent-playground"]`
// root containing `#gdcanvas`, `#lrSlider`, `#lrVal`, `#stepBtn`,
// `#playBtn`, `#resetBtn`, `#roPosition`, `#roLoss`, `#roGradient`,
// `#roIteration`.
import { observeCanvasResize, bindRange, fmt } from './widget-base.js';

const START_X = 2.2;

/** @param {number} x */
function loss(x) {
	return x * x + 2 * Math.sin(3 * x);
}
/** @param {number} x */
function gradient(x) {
	return 2 * x + 6 * Math.cos(3 * x);
}

/** @param {HTMLElement} root */
export function mount(root) {
	const canvas = /** @type {HTMLCanvasElement} */ (root.querySelector('#gdcanvas'));
	const lrSlider = /** @type {HTMLInputElement} */ (root.querySelector('#lrSlider'));
	const lrVal = /** @type {HTMLElement} */ (root.querySelector('#lrVal'));
	const stepBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#stepBtn'));
	const playBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#playBtn'));
	const resetBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#resetBtn'));
	const roPosition = /** @type {HTMLElement} */ (root.querySelector('#roPosition'));
	const roLoss = /** @type {HTMLElement} */ (root.querySelector('#roLoss'));
	const roGradient = /** @type {HTMLElement} */ (root.querySelector('#roGradient'));
	const roIteration = /** @type {HTMLElement} */ (root.querySelector('#roIteration'));

	const ctx = /** @type {CanvasRenderingContext2D} */ (canvas.getContext('2d'));
	const xMin = -3;
	const xMax = 3;
	const yMin = -3;
	const yMax = 10;

	let x = START_X;
	let iteration = 0;
	/** @type {number[]} */
	let trail = [x];
	let playing = false;
	/** @type {number | undefined} */
	let playTimer;

	/**
	 * @param {number} px
	 * @param {number} py
	 * @param {number} w
	 * @param {number} h
	 */
	function toScreen(px, py, w, h) {
		return [((px - xMin) / (xMax - xMin)) * w, h - ((py - yMin) / (yMax - yMin)) * h];
	}

	function draw() {
		const w = canvas.clientWidth;
		const h = canvas.clientHeight;
		ctx.clearRect(0, 0, w, h);

		ctx.strokeStyle = '#e4e4e7';
		ctx.lineWidth = 2;
		ctx.beginPath();
		for (let p = 0; p <= w; p++) {
			const px = xMin + (p / w) * (xMax - xMin);
			const [, py] = toScreen(px, loss(px), w, h);
			if (p === 0) ctx.moveTo(p, py);
			else ctx.lineTo(p, py);
		}
		ctx.stroke();

		ctx.strokeStyle = 'rgba(240,180,41,0.6)';
		ctx.lineWidth = 1.5;
		ctx.beginPath();
		trail.forEach((tx, i) => {
			const [sx, sy] = toScreen(tx, loss(tx), w, h);
			if (i === 0) ctx.moveTo(sx, sy);
			else ctx.lineTo(sx, sy);
		});
		ctx.stroke();

		const [cx, cy] = toScreen(x, loss(x), w, h);
		ctx.fillStyle = '#ef4444';
		ctx.beginPath();
		ctx.arc(cx, cy, 6, 0, Math.PI * 2);
		ctx.fill();
	}

	function updateReadouts() {
		lrVal.textContent = fmt(lrSlider.value, 2);
		roPosition.textContent = fmt(x, 4);
		roLoss.textContent = fmt(loss(x), 4);
		roGradient.textContent = fmt(gradient(x), 4);
		roIteration.textContent = String(iteration);
	}

	function step() {
		const lr = parseFloat(lrSlider.value);
		x = x - lr * gradient(x);
		trail.push(x);
		iteration += 1;
		updateReadouts();
		draw();
	}

	function stopPlaying() {
		playing = false;
		playBtn.textContent = 'Play';
		if (playTimer !== undefined) {
			window.clearInterval(playTimer);
			playTimer = undefined;
		}
	}

	function onStep() {
		stopPlaying();
		step();
	}

	function onPlayToggle() {
		if (playing) {
			stopPlaying();
			return;
		}
		playing = true;
		playBtn.textContent = 'Pause';
		playTimer = window.setInterval(step, 400);
	}

	function onReset() {
		stopPlaying();
		x = START_X;
		iteration = 0;
		trail = [x];
		updateReadouts();
		draw();
	}

	stepBtn.addEventListener('click', onStep);
	playBtn.addEventListener('click', onPlayToggle);
	resetBtn.addEventListener('click', onReset);
	const unbindLr = bindRange(lrSlider, () => updateReadouts());

	const disconnectResize = observeCanvasResize(canvas, draw);
	updateReadouts();

	return () => {
		stopPlaying();
		stepBtn.removeEventListener('click', onStep);
		playBtn.removeEventListener('click', onPlayToggle);
		resetBtn.removeEventListener('click', onReset);
		unbindLr();
		disconnectResize();
	};
}
